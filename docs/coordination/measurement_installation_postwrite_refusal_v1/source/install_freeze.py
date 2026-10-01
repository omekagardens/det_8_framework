"""UNEXECUTED RI209 proposal: one root-admitted byte installation, no subject load.
Root authenticates this source, metadata helper, bootstrap and admission before
startup. JSON statuses are not authority. Run only under the retained RI141
owned-child monitor; no monitor, launcher or scientific source is implemented here.
"""
import argparse,hashlib,importlib.util,json,os,stat,sys,time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri222-freeze-cwd-repair-ypiy2jqw';W=D/'worker_proposal'
E=B/'ri154-white-execution-proposed-42_uvw15';DEST=E/'AUTHORIZED_FREEZE.json'
OUT=B/'ri222-freeze-install-operation-ypiy2jqw'
CAP=67108864;TREE_CAP=25000;TREE_BYTES=536870912
LIMITS=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=CAP)
ENV=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
REPAIR={'path': '/Volumes/AI_DATA/development/det-review-evidence/ri222-freeze-cwd-repair-ypiy2jqw/worker_proposal/REPAIR_PROVENANCE.json', 'bytes': 48176, 'sha256': '77f52137ab3a4799253ca79bb0f3380a551ac623346052e1eebe6735b4182fd6'}
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
 need(type(data) is bytes and len(data)<=CAP,'bounded output');fd=None;first=None;secondary=[]
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

def difference(before,after):
 old={r['relative']:r for r in before};new={r['relative']:r for r in after}
 need(set(new)==set(old)|{'AUTHORIZED_FREEZE.json'},'one added file only')
 for name,r in old.items():
  if name=='.':
   z=new[name];same(z['kind'],'directory','root remains directory');same(z['state'][:4],r['state'][:4],'root device inode mode links');same(z['entries'],sorted(r['entries']+['AUTHORIZED_FREEZE.json']),'root adds exact freeze')
  else:same(new[name],r,'unchanged prior member '+name)
 same(m.pure(new['AUTHORIZED_FREEZE.json']['identity']),m.pure(CANDIDATE),'candidate installed pin')


def main():
 p=argparse.ArgumentParser();p.add_argument('--admission',required=True);args=p.parse_args()
 need(args.admission==str(D/'ADMIT_INSTALL.json'),'literal root admission');a_ref=m.ref(args.admission);a=load(a_ref)
 keys(a,'schema status source_manifest source_review preflight output environment limits genuine_outer_required','closed admission')
 same([a['schema'],a['status'],a['output'],a['environment'],a['limits'],a['genuine_outer_required']],['ri209-root-freeze-installation-admission-v1','AUTHORIZE_ONE_EXACT_FREEZE_INSTALLATION',str(OUT),ENV,LIMITS,True],'admission exact scope')
 same(dict(os.environ),ENV,'cleared exact environment');same(sys.executable,VENDOR,'direct selected bootstrap');need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==0,'bootstrap flags')
 need(Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W,'fixed operation paths')
 manifest=load(a['source_manifest']);keys(manifest,'schema status files','source manifest');same([manifest['schema'],manifest['status']],['ri209-proposal-source-pins-v1','SOURCE_ONLY_NOT_ADMISSION'],'source pin scope')
 need([Path(r['path']).name for r in manifest['files']]==['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py'],'complete source payloads')
 for r in manifest['files']:need(Path(r['path']).parent==W,'fixed source reservation');read(r)
 review=load(a['source_review']);same(review['source_manifest'],a['source_manifest'],'root source review binding');same(review['status'],'ACCEPT_RI209_INSTALLATION_SOURCE_ONLY','source accepted separately')
 inputs=load(INPUT);repair=load(REPAIR);g=load(inputs['roles']['graph']);accepted=load(inputs['roles']['candidate_acceptance']);candidate=read(CANDIDATE)
 same(inputs['roles']['result'],CANDIDATE,'accepted candidate role');same(accepted['result'],CANDIDATE,'accepted candidate');same(accepted['status'],'ACCEPT_COMPLETE_ADMINISTRATIVE_FREEZE_CANDIDATE','root accepted result');need(accepted['candidate_is_complete_canonical_result'] is True and accepted['freeze_installed'] is False,'candidate acceptance scope')
 same(g['prospective_root'],str(E),'fixed graph root');need(len(g['copied_files'])==48 and len(g['history_originals'])==124 and len(g['sources'])==30,'graph counts')
 pre=load(a['preflight']);keys(pre,'schema status sources supplier E_before host_tool_receipts monitor_bootstrap source_manifest environment scientific_execution','preflight fields');same([pre['schema'],pre['status'],pre['source_manifest'],pre['environment'],pre['scientific_execution']],['ri209-root-installation-preflight-v1','FRESH_EXACT_INSTALLATION_PREFLIGHT',a['source_manifest'],ENV,False],'preflight scope');read(pre['host_tool_receipts']);need(pre['monitor_bootstrap']['path']==str(D/'INSTALL_BOOTSTRAP.py'),'fixed whole monitor bootstrap');read(pre['monitor_bootstrap'])
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
 before=tree();same(before,load(pre['E_before']),'fresh whole E before');same(before,sorted(load(inputs['roles']['historical_E']),key=lambda r:r['relative']),'unchanged accepted E baseline');need(len(before)==57 and not os.path.lexists(DEST),'absent destination and complete57 E');selection=source_states(g)
 for x in (OUT,):need(not os.path.lexists(x),'fresh external one-attempt output')
 same(m.ref(args.admission),a_ref,'admission before ownership')
 binding_refs=dict(admission=a_ref,preflight=a['preflight'],source_manifest=a['source_manifest'],source_review=a['source_review'],sources=pre['sources'],supplier=pre['supplier'],E_before=pre['E_before'],host_tool_receipts=pre['host_tool_receipts'],monitor_bootstrap=pre['monitor_bootstrap'])
 binding_before={name:m.identity(row['path']) for name,row in binding_refs.items()}
 for name,row in binding_refs.items():same(m.pure(binding_before[name]),m.pure(row),'bound input before ownership '+name)
 # Successful mkdir owns the attempt. Every subsequent fallible step is caught;
 # an existing output is a refusal and never resumed or removed.
 # RI213: all safe receipt/error state and closures exist before ownership.
 start=None;finish=None;elapsed=None;first=None;tails={};produced={};install=None
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
  output('ATTEMPT.json',dict(schema='ri209-exclusive-install-attempt-v1',admission=a_ref,candidate=CANDIDATE,destination=str(DEST),no_retry=True,scientific_execution=False))
  output('BEFORE.json',dict(E=before,source_states=selection,source_observations=source_expected,bindings=binding_before))
  # E root is pinned through an opened directory descriptor during the sole write.
  fd=None;rootfd=None;write_error=None;cleanup=[]
  try:
   rootfd=os.open(E,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);same(st(os.fstat(rootfd)),before[0]['state'],'opened root selection')
   fd=os.open('AUTHORIZED_FREEZE.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=rootfd)
   n=0
   while n<len(candidate):
    k=os.write(fd,candidate[n:n+65536]);need(type(k) is int and 0<k<=len(candidate)-n,'candidate write progress');n+=k
   os.fsync(fd);same(os.fstat(fd).st_size,len(candidate),'descriptor complete length')
  except BaseException as exc:write_error=remember(exc)
  finally:
   if fd is not None:
    try:os.close(fd)
    except BaseException as exc:cleanup.append(remember(exc))
   if rootfd is not None:
    try:os.close(rootfd)
    except BaseException as exc:cleanup.append(remember(exc))
  observations['installation_write']=dict(error=write_error,cleanup_errors=cleanup)
  if write_error is not None or cleanup:raise ValueError('RI209: installation write/close failed')
  install=m.identity(DEST);need(install['state'][3]==1,'new freeze single link');same(m.pure(install),m.pure(CANDIDATE),'independent installed reread');need(DEST.read_bytes()==candidate,'exact accepted byte copy')
 except BaseException as exc:remember(exc)
 finally:
  def sources_tail():
   values=[];observations['sources_actual']=values
   for r in source_expected:values.append(m.identity(r['path']))
   same(values,source_expected,'all source/input selection unchanged');return values
  def binding_tail():
   values={name:m.identity(row['path']) for name,row in binding_refs.items()};observations['binding_actual']=values
   same(values,binding_before,'whole control/input selection retained');return values
  def E_tail():
   after=tree();observations['E_after']=after;difference(before,after);current=source_states(g);observations['source_states_after']=current;same(current,selection,'all48/124/30 complete selections');v=frozen(g,after,current)
   if install is not None:same(v['cards']['AUTHORIZED_FREEZE.json'],{k:install[k] for k in ('path','bytes','sha256','state')},'freeze selection retained')
   observations['frozen']=v;return output('FROZEN.json',v)
  attempt('source_inputs',sources_tail);attempt('root_bindings',binding_tail);attempt('supplier',suppliers);attempt('E_and_frozen',E_tail)
  attempt('save_observations',lambda:output('OBSERVATIONS.json',observations))
  def outputs_tail():
   vals={name:m.ref(OUT/name) for name in produced};same(vals,produced,'all captured ordinary output pins');return vals
  attempt('ordinary_outputs',outputs_tail)
  def final_E():
   rows=tree();difference(before,rows);need('E_after' in observations,'prior complete E observation');same(rows,observations['E_after'],'final E selection/namespace');return rows
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
  if elapsed is not None and elapsed>180:attempt('soft_deadline',lambda:need(False,'installation soft wall exceeded'))
  completion=dict(schema='ri213-installation-completion-v1',status='INSTALLED_PENDING_INDEPENDENT_ROOT_REVIEW' if first is None else 'REFUSED_RETAIN_ALL_PARTIALS',admission=a_ref,candidate=CANDIDATE,destination=str(DEST),first_error=first,independent_tails=tails,produced_outputs=produced,elapsed_seconds_before_complete_write=elapsed,timing=timing,complete_not_self_hashed=True,scientific_execution=False,mode_admission_issued=False,ret_paused=True)
  # If this final exclusive write fails, genuine outer/partials are the failure
  # evidence. Never replace an incomplete receipt or claim successful return.
  save(OUT/'COMPLETE.json',completion)
 return 0 if first is None else 1
if __name__=='__main__':raise SystemExit(main())
