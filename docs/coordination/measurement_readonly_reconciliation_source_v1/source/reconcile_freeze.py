"""UNEXECUTED RI226 proposal: one root-admitted READ-ONLY reconciliation, no E write.
Root authenticates this source, metadata helper, bootstrap and admission before
startup. JSON statuses are not authority. Run only under the retained RI141
owned-child monitor; no monitor, launcher or scientific source is implemented here.
"""
import argparse,hashlib,importlib.util,json,os,stat,sys,time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri226-directory-custody-recovery-yvfg_p1b';W=D/'worker_proposal'
E=B/'ri154-white-execution-proposed-42_uvw15';DEST=E/'AUTHORIZED_FREEZE.json'
OUT=B/'ri226-freeze-reconciliation-operation-yvfg_p1b'
OLD_OUT=B/'ri222-freeze-install-operation-ypiy2jqw'
CAP=67108864;TREE_CAP=25000;TREE_BYTES=536870912
LIMITS=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=CAP)
ENV=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
REPAIR={'path': '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/worker_proposal/REPAIR_PROVENANCE.json', 'bytes': 82537, 'sha256': 'ad7253f46b76dc4c5e72fa32ac0beabbe834606133dd4a46b26a516606dd41f3'}
VENDOR='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
INPUT={'path':str(W/'INPUT_PINS.json'),'bytes':677925,'sha256':'ba05f97194b141f4546ea3b0323d97f0ef5461d4cd33c0523174ac291bb98a84'}
CANDIDATE={'path':str(B/'ri156-operation-ri206-freeze-5e_n5lj_/RESULT.json'),'bytes':26214,'sha256':'9e0c0e4953c7213a76fea291d5f799984422de8628f039eac4e0d7b3c5758b14'}
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('RI209: metadata helper pin')
s=importlib.util.spec_from_file_location('ri209_root_metadata',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def need(ok,msg):
 if not ok:raise ValueError('RI209: '+msg)
def same(a,b,msg):need(m.canonical(a)==m.canonical(b),msg)
def keys(v,n,msg):need(type(v) is dict and set(v)==set(n.split()),msg)
def st(v):return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]
def literal(p):
 p=Path(p);need(p.is_absolute() and p.resolve()==p,'literal nonsymlink path');return p
def read(ref):
 keys(ref,'path bytes sha256','FilePin');p=literal(ref['path']);a=m.identity(p);same(m.pure(a),m.pure(ref),'metadata pin')
 need(0<ref['bytes']<=CAP,'metadata cap');data=p.read_bytes();same(m.pin(data),m.pure(ref),'read bytes');same(m.identity(p),a,'read selection');return data

def parse(data):
 def pairs(rows):
  v={}
  for k,x in rows:need(k not in v,'duplicate metadata key');v[k]=x
  return v
 def bad(x):raise ValueError('RI209: nonfinite metadata')
 v=json.loads(data.decode('ascii'),object_pairs_hook=pairs,parse_constant=bad);same(data.decode('ascii'),m.canonical(v).decode('ascii'),'canonical JSON');return v

def load(ref):return parse(read(ref))
def error(exc):return dict(type=type(exc).__name__,message=str(exc)[:2048],secondary=getattr(exc,'ri209_secondary',[]))
def write(path,data):
 need(Path(path).parent==OUT,'only fresh external output writes');need(type(data) is bytes and len(data)<=CAP,'bounded output');fd=None;first=None;secondary=[]
 try:
  fd=os.open(literal(path),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  done=0
  while done<len(data):
   n=os.write(fd,data[done:done+65536]);need(type(n) is int and 0<n<=min(65536,len(data)-done),'write progress');done+=n
  os.fsync(fd)
 except BaseException as exc:first=exc
 finally:
  if fd is not None:
   try:os.close(fd)
   except BaseException as exc:
    if first is None:first=exc
    else:secondary.append(error(exc))
 if first is not None:
  first.ri209_secondary=secondary;raise first
 need(Path(path).read_bytes()==data,'written exact bytes');return m.ref(path)
def save(path,v):return write(path,m.canonical(v))

def tree():
 rows=[];total=0
 def visit(p,depth):
  nonlocal total
  a=p.lstat();need(depth<=16 and len(rows)<TREE_CAP,'tree bound');r=dict(relative=str(p.relative_to(E)),state=st(a))
  if stat.S_ISLNK(a.st_mode):r.update(kind='symlink',target=os.readlink(p))
  elif stat.S_ISDIR(a.st_mode):r.update(kind='directory',entries=sorted(x.name for x in p.iterdir()))
  else:
   need(stat.S_ISREG(a.st_mode) and a.st_size<=CAP,'regular bounded tree member');ident=m.identity(p);need(ident['symlink_chain']==[] and ident['resolved_path']==str(p),'tree no links');total+=ident['bytes'];need(total<=TREE_BYTES,'tree aggregate');r.update(kind='file',identity=ident)
  rows.append(r)
  if r['kind']=='directory':
   for name in r['entries']:visit(p/name,depth+1)
   same(sorted(x.name for x in p.iterdir()),r['entries'],'directory membership drift')
  same(st(p.lstat()),st(a),'tree selection drift')
 visit(literal(E),0);return sorted(rows,key=lambda r:r['relative'])

def source_states(g):
 def observed(path,pin):
  v=m.identity(path);need(v['resolved_path']==path and v['symlink_chain']==[],'source literal selection');same(m.pure(v),m.pure(pin),'source full pin');return {k:v[k] for k in ('path','bytes','sha256','state')}
 return dict(copies=[dict(relative=r['relative'],original=observed(r['source']['path'],r['source']),copy=observed(r['destination'],r['source'])) for r in g['copied_files']],history=[observed(r['path'],r) for r in g['history_originals']],target_originals=[observed(r['original'],r['pin']) for r in g['sources']])

def frozen(g,rows,selection):
 by={r['relative']:r for r in rows};names={r['relative'] for r in g['copied_files']}|{'.','science','science/primary','science/qualifier','science/validator','tmp','runs','runs/normal','runs/optimized','AUTHORIZED_FREEZE.json'}
 need(set(by)==names,'full frozen domain')
 simple=[]
 for r in rows:
  if r['kind']=='directory':simple.append(dict(relative=r['relative'],kind='directory'))
  else:
   need(r['kind']=='file','no frozen links');simple.append(dict(relative=r['relative'],kind='file',**m.pure(r['identity'])))
 f=by['AUTHORIZED_FREEZE.json']['identity'];same(m.pure(f),m.pure(CANDIDATE),'installed candidate');need(f['state'][3]==1,'single-link installed freeze')
 for r in g['copied_files']:same(m.pure(by[r['relative']]['identity']),m.pure(r['source']),'frozen complete copied pin')
 for name in ('tmp','runs/normal','runs/optimized'):same(by[name]['entries'],[],'empty controlled directory')
 return dict(schema='ri156-complete-copy-card-observation-v1',root=str(E),stage='frozen',source_states=selection,cards={'AUTHORIZED_FREEZE.json':{k:f[k] for k in ('path','bytes','sha256','state')}},tree=simple,tmp_empty=True,scientific_body_decoded=False,source_acceptance_created=False)

def retained_failure(repair):
 # All operands are closed, exact-pinned ADMINISTRATIVE saved records. No
 # scientific body is decoded. Genuine tool origin remains root's premise.
 refs=repair['roles'];old_before=load(refs['original_before']);old_obs=load(refs['original_observations']);c=load(refs['original_complete']);post=load(refs['postflight']);sup=load(refs['supersession'])
 keys(old_before,'E source_states source_observations bindings','original before')
 keys(old_obs,'E_after binding_actual installation_write sources_actual supplier_actual','original partial observations')
 keys(c,'schema status admission candidate destination first_error independent_tails produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed scientific_execution mode_admission_issued ret_paused','original refused receipt')
 expected_error=dict(type='ValueError',message='RI209: root device inode mode links',secondary=[])
 same([c['schema'],c['status'],c['candidate'],c['destination'],c['first_error'],c['complete_not_self_hashed'],c['scientific_execution'],c['mode_admission_issued'],c['ret_paused']],['ri213-installation-completion-v1','REFUSED_RETAIN_ALL_PARTIALS',CANDIDATE,str(DEST),expected_error,True,False,False,True],'preserved actual original refusal')
 same(sup['status'],'OPERATIONAL_READINESS_SUPERSEDED_AFTER_ACTUAL_POSTWRITE_REFUSAL','old readiness superseded')
 same(post['status'],'REFUSAL_AND_RETAINED_PARTIALS_CONFIRMED_NOT_INSTALLATION_ACCEPTANCE','postflight narrow scope')
 same(post['first_error'],expected_error,'postflight original error');same(post['failed_tails'],['E_and_frozen','final_E'],'two exact failed tails');same(post['passed_tail_count'],6,'six original successful tails')
 same(old_obs['installation_write'],dict(error=None,cleanup_errors=[]),'original write and closes completed')
 names=['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json']
 same(sorted(p.name for p in OLD_OUT.iterdir()),names,'retained original four-file namespace')
 for n in names:
  r=m.identity(OLD_OUT/n);need(r['symlink_chain']==[] and r['resolved_path']==str(OLD_OUT/n) and stat.S_ISREG(r['state'][2]) and r['state'][3]==1 and r['bytes']<=CAP,'original regular single-link output')
 pins={n:m.ref(OLD_OUT/n) for n in names if n!='COMPLETE.json'};same(c['produced_outputs'],pins,'original three produced files');same(post['operation_files'],[m.ref(OLD_OUT/n) for n in names],'entire pinned original operation')
 same(c['admission'],{k:old_before['bindings']['admission'][k] for k in ('path','bytes','sha256')},'original admission pin')
 at=load(refs['original_attempt']);same(at,dict(schema='ri209-exclusive-install-attempt-v1',admission=c['admission'],candidate=CANDIDATE,destination=str(DEST),no_retry=True,scientific_execution=False),'original complete attempt')
 old_sources=load(refs['original_sources']);same(len(old_sources),904,'original source count');same(old_before['source_observations'],old_sources,'original complete source baseline');same(old_obs['sources_actual'],old_sources,'original full source tail');same(old_obs['binding_actual'],old_before['bindings'],'original full binding tail')
 t=c['independent_tails'];keys(t,'source_inputs root_bindings supplier E_and_frozen save_observations ordinary_outputs final_E output_namespace','all eight original tails')
 values=dict(source_inputs=old_sources,root_bindings=old_before['bindings'],supplier=old_obs['supplier_actual'],save_observations=pins['OBSERVATIONS.json'],ordinary_outputs=pins,output_namespace=[m.identity(OLD_OUT/n) for n in sorted(pins)])
 for name in ('E_and_frozen','final_E'):same(t[name],dict(value=None,error=expected_error),'exact failed original tail '+name)
 for name,value in values.items():same(t[name],dict(value=value,error=None),'whole successful original tail '+name)
 for r in old_sources:same(m.identity(r['path']),r,'retained original source selection')
 for r in old_before['bindings'].values():same(m.identity(r['path']),r,'retained original binding selection')
 timing=c['timing'];keys(timing,'initial final elapsed','original timing')
 for row in timing.values():keys(row,'value error','original clock record');need(row['error'] is None and type(row['value']) in (int,float) and float('-inf')<row['value']<float('inf'),'original finite successful clocks')
 same(timing['elapsed']['value'],c['elapsed_seconds_before_complete_write'],'original elapsed binding');same(timing['final']['value']-timing['initial']['value'],timing['elapsed']['value'],'original elapsed arithmetic');need(0<=timing['elapsed']['value']<=180,'original inner bound')
 old={r['relative']:r for r in old_before['E']};after=old_obs['E_after'];new={r['relative']:r for r in after}
 need(len(old)==57 and len(new)==58 and len(old_before['E'])==57 and len(after)==58 and set(new)==set(old)|{'AUTHORIZED_FREEZE.json'},'exact original sole addition')
 same(old['.'],post['root_before'],'pinned original root');same({k:new['.'][k] for k in ('state','entries')},post['root_after'],'pinned retained root')
 same(new['.']['kind'],'directory','root kind');same(new['.']['state'][:3],old['.']['state'][:3],'root device inode mode retained');same([old['.']['state'][3],new['.']['state'][3]],[23,24],'exact recorded host-specific link transition')
 same(new['.']['entries'],sorted(old['.']['entries']+['AUTHORIZED_FREEZE.json']),'only exact root member addition')
 for name,row in old.items():
  if name!='.':same(new[name],row,'all prior member states unchanged '+name)
 for row in after:
  if row['kind']=='file':need(stat.S_ISREG(row['identity']['state'][2]) and row['identity']['state'][3]==1 and row['identity']['symlink_chain']==[],'all retained files regular single-link')
 same(new['AUTHORIZED_FREEZE.json']['identity'],post['installed_partial'],'whole retained freeze selection');same(m.pure(post['installed_partial']),m.pure(CANDIDATE),'retained candidate exact pin')
 need(sum(r['kind']=='file' for r in after)==49 and sum(r['kind']=='directory' for r in after)==9,'retained exact file/directory counts')
 # There is no general nlink law: the pinned AFTER state is now immutable.
 return dict(E=after,source_states=old_before['source_states'],original_complete=refs['original_complete'],postflight=refs['postflight'],original_status=c['status'])


def main():
 p=argparse.ArgumentParser();p.add_argument('--admission',required=True);args=p.parse_args()
 need(args.admission==str(D/'ADMIT_RECONCILE.json'),'literal root admission');a_ref=m.ref(args.admission);a=load(a_ref)
 keys(a,'schema status source_manifest source_review preflight output environment limits genuine_outer_required','closed admission')
 same([a['schema'],a['status'],a['output'],a['environment'],a['limits'],a['genuine_outer_required']],['ri226-root-read-only-reconciliation-admission-v1','AUTHORIZE_ONE_READ_ONLY_RECONCILIATION',str(OUT),ENV,LIMITS,True],'admission exact scope')
 same(dict(os.environ),ENV,'cleared exact environment');same(sys.executable,VENDOR,'direct selected bootstrap');need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==0,'bootstrap flags')
 need(Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W,'fixed operation paths')
 manifest=load(a['source_manifest']);keys(manifest,'schema status files','source manifest');same([manifest['schema'],manifest['status']],['ri226-proposal-source-pins-v1','SOURCE_ONLY_NOT_ADMISSION'],'source pin scope')
 need([Path(r['path']).name for r in manifest['files']]==['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_reconciliation.py','reconcile_freeze.py'],'complete source payloads')
 for r in manifest['files']:need(Path(r['path']).parent==W,'fixed source reservation');read(r)
 review=load(a['source_review']);same(review['source_manifest'],a['source_manifest'],'root source review binding');same(review['status'],'ACCEPT_RI226_READ_ONLY_RECONCILIATION_SOURCE_ONLY','source accepted separately')
 inputs=load(INPUT);repair=load(REPAIR);retained=retained_failure(repair);same(review['retained_failure'],retained['original_complete'],'root acknowledges actual failure');same(review['retained_postflight'],retained['postflight'],'root acknowledges retained custody');g=load(inputs['roles']['graph']);accepted=load(inputs['roles']['candidate_acceptance']);candidate=read(CANDIDATE)
 same(inputs['roles']['result'],CANDIDATE,'accepted candidate role');same(accepted['result'],CANDIDATE,'accepted candidate');same(accepted['status'],'ACCEPT_COMPLETE_ADMINISTRATIVE_FREEZE_CANDIDATE','root accepted result');need(accepted['candidate_is_complete_canonical_result'] is True and accepted['freeze_installed'] is False,'candidate acceptance scope')
 same(sorted(load(inputs['roles']['historical_E']),key=lambda r:r['relative']),load(repair['roles']['original_before'])['E'],'complete original accepted E baseline');same(g['prospective_root'],str(E),'fixed graph root');need(len(g['copied_files'])==48 and len(g['history_originals'])==124 and len(g['sources'])==30,'graph counts')
 pre=load(a['preflight']);keys(pre,'schema status sources supplier E_before host_tool_receipts monitor_bootstrap source_manifest environment scientific_execution','preflight fields');same([pre['schema'],pre['status'],pre['source_manifest'],pre['environment'],pre['scientific_execution']],['ri226-root-reconciliation-preflight-v1','FRESH_EXACT_READ_ONLY_RECONCILIATION_PREFLIGHT',a['source_manifest'],ENV,False],'preflight scope');read(pre['host_tool_receipts']);need(pre['monitor_bootstrap']['path']==str(D/'RECONCILE_BOOTSTRAP.py'),'fixed whole monitor bootstrap');read(pre['monitor_bootstrap'])
 source_expected=load(pre['sources']);expected={r['path']:r for r in inputs['files']+repair['files']+manifest['files']+[a['source_manifest'],a['source_review'],pre['monitor_bootstrap']]}
 need(type(source_expected) is list and [r['path'] for r in source_expected]==sorted(expected),'complete sorted preflight source domain')
 for r in source_expected:same(m.pure(r),m.pure(expected[r['path']]),'preflight source input pin');same(m.identity(r['path']),r,'fresh whole source preflight')
 supplier=load(pre['supplier']);historical=load(inputs['roles']['historical_supplier']);same({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in historical.items() if k not in ('environment','observed_at_unix_ns')},'unchanged entire supplier scope');same(supplier['environment'],ENV,'supplier environment')
 host=load(pre['host_tool_receipts']);keys(host,'schema command environment returncode stdout stderr uname genuine_tool','actual host receipt');same([host['schema'],host['command'],host['environment'],host['returncode'],host['stdout'],host['stderr'],host['uname']],['ri209-root-host-command-record-v1',supplier['host']['argv'],{'PATH':'/usr/bin:/bin','LC_ALL':'C'},0,supplier['host']['stdout'],'',supplier['host']['uname']],'complete root actual host observation');read(host['genuine_tool'])
 def suppliers():
  result=dict(files=[m.identity(r['path']) for r in supplier['vendor']+supplier['tools']],namespace=[],absent=[],uname=list(os.uname()))
  observations['supplier_actual']=result
  for r in supplier['namespace']:
   path=Path(r['path']);v=dict(path=str(path),kind=r['kind'],state=st(path.lstat()))
   if r['kind']=='directory':v['entries']=sorted(x.name for x in path.iterdir())
   else:v['target']=os.readlink(path)
   result['namespace'].append(v)
  result['absent']=[dict(path=n,absent=not os.path.lexists(n)) for n in supplier['absent']]
  same(result['files'],supplier['vendor']+supplier['tools'],'whole supplier identities');same(result['namespace'],supplier['namespace'],'complete supplier namespace');need(all(r['absent'] for r in result['absent']),'supplier absences');same(result['uname'],supplier['host']['uname'],'current uname');return result
 observations={};suppliers()
 before=tree();same(before,load(pre['E_before']),'fresh whole E before');same(before,retained['E'],'entire retained postwrite E unchanged');need(len(before)==58,'complete58 retained E');selection=source_states(g);same(selection,retained['source_states'],'whole original48/124/30 retained');same(m.pure(m.identity(DEST)),m.pure(CANDIDATE),'existing candidate pin');need(DEST.read_bytes()==candidate,'complete existing candidate byte equality')
 for x in (OUT,):need(not os.path.lexists(x),'fresh external one-attempt output')
 same(m.ref(args.admission),a_ref,'admission before ownership')
 binding_refs=dict(admission=a_ref,preflight=a['preflight'],source_manifest=a['source_manifest'],source_review=a['source_review'],sources=pre['sources'],supplier=pre['supplier'],E_before=pre['E_before'],host_tool_receipts=pre['host_tool_receipts'],monitor_bootstrap=pre['monitor_bootstrap'])
 binding_before={name:m.identity(row['path']) for name,row in binding_refs.items()}
 for name,row in binding_refs.items():same(m.pure(binding_before[name]),m.pure(row),'bound input before ownership '+name)
 # Successful mkdir owns the attempt. Every subsequent fallible step is caught;
 # an existing output is a refusal and never resumed or removed.
 # RI213: all safe receipt/error state and closures exist before ownership.
 start=None;finish=None;elapsed=None;first=None;tails={};produced={};install=m.identity(DEST)
 timing={name:dict(value=None,error=None) for name in ('initial','final','elapsed')}
 def remember(exc):
  nonlocal first
  e=error(exc)
  if first is None:first=e
  return e
 def attempt(name,fn):
  try:tails[name]=dict(value=fn(),error=None)
  except BaseException as exc:tails[name]=dict(value=None,error=remember(exc))
 def output(name,value):
  data=m.canonical(value);pin=dict(path=str(OUT/name),**m.pin(data));produced[name]=pin;save(OUT/name,value);return pin
 OUT.mkdir(mode=0o700)
 try:
  # The first fallible post-mkdir operation is protected. Invalid readings are
  # represented by an error and null value, never serialized as NaN/Infinity.
  try:
   reading=time.monotonic()
   need(type(reading) in (int,float) and float('-inf')<reading<float('inf'),'initial clock must be finite numeric')
   start=reading;timing['initial']['value']=start
  except BaseException as exc:
   timing['initial']['error']=remember(exc);raise
  same(m.ref(args.admission),a_ref,'admission after ownership')
  output('ATTEMPT.json',dict(schema='ri226-exclusive-read-only-reconciliation-attempt-v1',admission=a_ref,candidate=CANDIDATE,destination=str(DEST),original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True,no_retry=True,scientific_execution=False))
  output('BEFORE.json',dict(E=before,source_states=selection,source_observations=source_expected,bindings=binding_before))
  # No E mutation exists. Byte readback does not decode the candidate.
  same(m.identity(DEST),install,'existing freeze complete selection');need(DEST.read_bytes()==candidate,'exact retained candidate bytes');same(m.identity(DEST),install,'existing freeze selection after read')
  observations['read_only_reconciliation']=dict(original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True)
 except BaseException as exc:remember(exc)
 finally:
  def sources_tail():
   values=[];observations['sources_actual']=values
   for r in source_expected:values.append(m.identity(r['path']))
   same(values,source_expected,'all source/input selection unchanged');observations['retained_failure_after']=retained_failure(repair);same(observations['retained_failure_after'],retained,'whole original failure custody retained');return values
  def binding_tail():
   values={name:m.identity(row['path']) for name,row in binding_refs.items()};observations['binding_actual']=values
   same(values,binding_before,'whole control/input selection retained');return values
  def E_tail():
   after=tree();observations['E_after']=after;same(after,before,'whole read-only E unchanged');current=source_states(g);observations['source_states_after']=current;same(current,selection,'all48/124/30 complete selections');v=frozen(g,after,current)
   if install is not None:same(v['cards']['AUTHORIZED_FREEZE.json'],{k:install[k] for k in ('path','bytes','sha256','state')},'freeze selection retained')
   observations['frozen']=v;return output('FROZEN.json',v)
  attempt('source_inputs',sources_tail);attempt('root_bindings',binding_tail);attempt('supplier',suppliers);attempt('E_and_frozen',E_tail)
  attempt('save_observations',lambda:output('OBSERVATIONS.json',observations))
  def outputs_tail():
   vals={name:m.ref(OUT/name) for name in produced};same(vals,produced,'all captured ordinary output pins');return vals
  attempt('ordinary_outputs',outputs_tail)
  def final_E():
   rows=tree();same(rows,before,'whole final read-only E unchanged');need('E_after' in observations,'prior complete E observation');same(rows,observations['E_after'],'final E selection/namespace');return rows
  attempt('final_E',final_E)
  def namespace():
   names=sorted(p.name for p in OUT.iterdir());same(names,sorted(produced),'whole final pre-receipt namespace');return [m.identity(OUT/name) for name in names]
  attempt('output_namespace',namespace)
  # All eight ordinary tails above were attempted before final timing. A
  # clock/subtraction failure cannot bypass the refused COMPLETE attempt or
  # replace an earlier installation/tail failure.
  try:
   reading=time.monotonic()
   need(type(reading) in (int,float) and float('-inf')<reading<float('inf'),'final clock must be finite numeric')
   finish=reading;timing['final']['value']=finish
  except BaseException as exc:timing['final']['error']=remember(exc)
  try:
   need(start is not None and finish is not None,'elapsed unavailable: initial or final clock invalid or missing')
   duration=finish-start
   need(type(duration) in (int,float) and 0<=duration<float('inf'),'elapsed interval must be finite and nonnegative')
   elapsed=duration;timing['elapsed']['value']=elapsed
  except BaseException as exc:timing['elapsed']['error']=remember(exc)
  if elapsed is not None and elapsed>180:attempt('soft_deadline',lambda:need(False,'reconciliation soft wall exceeded'))
  completion=dict(schema='ri226-read-only-reconciliation-completion-v1',status='RECONCILED_PENDING_INDEPENDENT_ROOT_REVIEW' if first is None else 'REFUSED_RETAIN_ALL_PARTIALS',admission=a_ref,candidate=CANDIDATE,destination=str(DEST),original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True,first_error=first,independent_tails=tails,produced_outputs=produced,elapsed_seconds_before_complete_write=elapsed,timing=timing,complete_not_self_hashed=True,scientific_execution=False,mode_admission_issued=False,ret_paused=True)
  # If this final exclusive write fails, genuine outer/partials are the failure
  # evidence. Never replace an incomplete receipt or claim successful return.
  save(OUT/'COMPLETE.json',completion)
 return 0 if first is None else 1
if __name__=='__main__':raise SystemExit(main())
