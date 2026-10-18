"""Independent RI218 administrative identities and source-text review support.
No subject, author checker, metadata helper, vendor or fixture is imported/run.
Only explicitly selected administrative records are decoded as JSON.
"""
from pathlib import Path
import json,hashlib,os,stat,difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=Path(__file__).resolve().parent
W=B/'ri218-freeze-byte-repair-x62withm/worker_proposal'
OLD=B/'ri213-freeze-clock-repair-2xc_b29x/worker_proposal'
R=B/'ri217-root-native-witness-1yj1_b61'
checks=0;observed={};predicates=[]
def demand(ok,where):
 global checks
 checks+=1
 if not ok:raise ValueError(where)
def canonical(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def same(a,b,label):demand(canonical(a)==canonical(b),label)
def state(z):return [z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
def pure(r):return {k:r[k] for k in ('path','bytes','sha256')}
def identity(p):
 p=Path(p);a=p.lstat();demand(p.is_absolute() and p.resolve()==p and stat.S_ISREG(a.st_mode),'literal regular '+str(p));h=hashlib.sha256();n=0
 with p.open('rb') as f:
  same(state(os.fstat(f.fileno())),state(a),'opened identity '+str(p))
  while True:
   chunk=f.read(1048576)
   if not chunk:break
   h.update(chunk);n+=len(chunk)
  same(state(os.fstat(f.fileno())),state(a),'descriptor identity '+str(p))
 same(state(p.lstat()),state(a),'closed selection '+str(p));demand(n==a.st_size,'full size '+str(p))
 v=dict(path=str(p),resolved_path=str(p),symlink_chain=[],bytes=n,sha256=h.hexdigest(),state=state(a));observed[str(p)]=v;return v

def verify(r):
 v=identity(r['path']);same(pure(v),pure(r),'pin '+r['path']);return v

def load(p):
 # Administrative record only; caller explicitly selects each path.
 def pairs(rows):
  out={}
  for k,v in rows:demand(k not in out,'duplicate administrative key');out[k]=v
  return out
 def bad(value):raise ValueError('nonfinite administrative record')
 return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=bad)

def seal(path,sha,size):
 row=dict(path=str(path),bytes=size,sha256=sha);verify(row);h=load(path);root=path.parent
 same(sorted(x.name for x in root.iterdir()),sorted(h['namespace']),'exact sealed namespace')
 same(sorted(Path(x['path']).name for x in h['files']),sorted(set(h['namespace'])-{'HANDOFF.json'}),'exact sealed payload domain')
 for r in h['files']:demand(Path(r['path']).parent==root,'payload parent');verify(r)
 return h

handoff=seal(W/'HANDOFF.json','bd62168cf3cb2fe468f7488a140ad98f9dc433c21b3ad17d642ba29623acbeb1',8207)
prior=seal(OLD/'HANDOFF.json','f8e4ab402fe4621352c7fe1f9b3d3bfeb6d5bc1194afcc7fb98cf34f8eb2f512',7600)
manifest=load(W/'SOURCE_PINS.json');verify(dict(path=str(W/'SOURCE_PINS.json'),bytes=1368,sha256='de91cbd42647e012c7f900dbff1355691986f6e6a8b1622c2ff9216c1f7dd443'))
same(sorted(manifest),['files','schema','status'],'manifest fields');same([Path(x['path']).name for x in manifest['files']],['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py'],'ordered five source payloads')
for r in manifest['files']:demand(Path(r['path']).parent==W,'manifest parent');verify(r)
inputs=load(W/'INPUT_PINS.json');repair=load(W/'REPAIR_PROVENANCE.json');oldrepair=load(OLD/'REPAIR_PROVENANCE.json')
demand((W/'INPUT_PINS.json').read_bytes()==(OLD/'INPUT_PINS.json').read_bytes(),'unchanged full input manifest bytes')
same([len(inputs['files']),inputs['prior_current_source_count'],inputs['prior_role_count'],len(inputs['prior_role_rows'])],[806,764,810,810],'retained base and every role')
by={}
for r in inputs['files']+repair['files']:
 z=pure(r)
 if z['path'] in by:same(z,by[z['path']],'consistent overlapping dependency')
 by[z['path']]=z
same([len(repair['files']),len(oldrepair['files']),len(by)],[43,19,849],'dependency exact cardinalities')
for r in by.values():verify(r)
provenance={r['path']:pure(r) for r in repair['files']}
for r in oldrepair['files']+prior['files']+[pure(observed[str(OLD/'HANDOFF.json')])]:same(provenance[r['path']],pure(r),'preserved predecessor provenance')
assignment=load(R/'RI218_BYTE_REPAIR_ASSIGNMENT.json');sup=load(R/'RI213_SOURCE_ACCEPTANCE_SUPERSESSION.json');failure=load(R/'PREPARATION_FAILURE_PARTIALS.json');oldreview=load(sup['prior_acceptance']['path'])
extras=[repair['assignment'],repair['source_acceptance_supersession'],repair['actual_preparation_failure'],failure['original_source'],failure['original_host'],failure['genuine_host'],sup['prior_acceptance'],oldreview['independent_review'],oldreview['root_metadata']]
expected={r['path']:pure(r) for r in oldrepair['files']+prior['files']+[pure(observed[str(OLD/'HANDOFF.json')])]+extras}
same(provenance,expected,'complete 19+15+9 exact provenance union')
same(len({r['path'] for r in extras}),9,'nine exact added roles')
same(sup['status'],'RI213_REQUIRES_BYTE_COMPARISON_REPAIR_NO_OPERATIONAL_ADMISSION','operative predecessor supersession')
future=set(by)
for r in manifest['files']+[pure(observed[str(W/'SOURCE_PINS.json')])]:demand(r['path'] not in future,'new source path');future.add(r['path'])
# Two distinct future root objects, not fabricated FilePins or current admissions.
for name in ('ROOT_SOURCE_REVIEW.json','INSTALL_BOOTSTRAP.py'):
 path=str(W.parent/name);demand(path not in future,'future root distinct path');future.add(path)
same(len(future),857,'prospective full source domain')
new_src={n:(W/n).read_text() for n in ('install_freeze.py','check_installation.py')}
old_src={n:(OLD/n).read_text() for n in new_src}
changes=[("same(Path(path).read_bytes(),data,'written exact bytes')","need(Path(path).read_bytes()==data,'written exact bytes')"),("same(DEST.read_bytes(),candidate,'exact accepted byte copy')","need(DEST.read_bytes()==candidate,'exact accepted byte copy')")]
for name,current in new_src.items():
 old=old_src[name];projection=current
 for new,previous in [('ri218-freeze-byte-repair-x62withm','ri213-freeze-clock-repair-2xc_b29x'),('ri218-freeze-install-operation-x62withm','ri213-freeze-install-operation-2xc_b29x')]:projection=projection.replace(new,previous)
 a=[x for x in old.splitlines() if x.startswith('REPAIR=')];c=[x for x in projection.splitlines() if x.startswith('REPAIR=')];demand(len(a)==len(c)==1,'one provenance constant');projection=projection.replace(c[0],a[0])
 if name=='install_freeze.py':
  for oldtext,newtext in changes:demand(current.count(newtext)==1 and oldtext not in current,'unique direct byte repair');projection=projection.replace(newtext,oldtext)
 demand(projection==old,'entire inverse source delta '+name)
 demand(len(current.splitlines())==len(old.splitlines()),'line count retained '+name)
 source_constant=[x for x in current.splitlines() if x.startswith('REPAIR=')][0]
 same(source_constant,'REPAIR='+repr(pure(observed[str(W/'REPAIR_PROVENANCE.json')])),'whole exact repair constant')
inst=new_src['install_freeze.py'];oldinst=old_src['install_freeze.py']
for start,end in [(147,171),(195,218),(219,237)]:same(inst.splitlines()[start-1:end],oldinst.splitlines()[start-1:end],'unchanged clock/tail lines '+str((start,end)))
same(inst.splitlines()[24],oldinst.splitlines()[24],'JSON comparator retained')
same(new_src['check_installation.py'].splitlines()[23],old_src['check_installation.py'].splitlines()[23],'postchecker JSON retained')
diff=''.join(''.join(difflib.unified_diff((OLD/name).read_text().splitlines(True),(W/name).read_text().splitlines(True),fromfile=str(OLD/name),tofile=str(W/name))) for name in ('install_freeze.py','check_installation.py','PROTOCOL.md'))
demand(diff==(W/'SOURCE_DIFF.patch').read_text(),'entire published three-file diff reproduced')
# Current exact prior partials and all absences, not subjects or runtime probes.
same(sorted(x.name for x in OLD.parent.iterdir()),failure['reservation_namespace'],'old partial namespace')
same(identity(failure['genuine_host']['path']),failure['genuine_host'],'entire retained host selection')
for row in failure['empty_control_directories']:
 p=Path(row['path']);same(state(p.lstat()),row['state'],'partial directory state');same(sorted(x.name for x in p.iterdir()),row['entries'],'partial directory members')
saved=Path(failure['genuine_host']['path']).read_bytes();original=load(failure['original_host']['path']);demand(saved==canonical(original),'saved host entire canonical original')
for name in failure['absent']:demand(not os.path.lexists(name),'old missing operational path')
for name in ('tmp','monitor','INSTALL_BOOTSTRAP.py','ADMIT_INSTALL.json','DISPATCH.json','INSTALL_PREFLIGHT.json','INSTALLATION_PROPOSAL.json'):demand(not os.path.lexists(W.parent/name),'new operational path absent '+name)
demand(not os.path.lexists(assignment['future_operation']),'new output absent')
# E is a copy/source metadata tree. Read opaque bytes only; saved JSON is metadata.
E=B/'ri154-white-execution-proposed-42_uvw15';saved_tree=load(inputs['roles']['historical_E']['path']);current=[]
for row in saved_tree:
 p=E/row['relative'];a=p.lstat();same(state(a),row['state'],'E exact seven state '+row['relative']);r=dict(relative=row['relative'],state=state(a),kind=row['kind'])
 if row['kind']=='directory':demand(stat.S_ISDIR(a.st_mode),'E directory');r['entries']=sorted(x.name for x in p.iterdir())
 else:demand(row['kind']=='file','only files or dirs');r['identity']=identity(p)
 current.append(r)
same(current,saved_tree,'entire E saved/current tree')
same([sum(x['kind']=='file' for x in current),sum(x['kind']=='directory' for x in current)],[48,9],'complete E counts')
same(sorted(str(p.relative_to(E)) for p in E.rglob('*')),sorted(x['relative'] for x in saved_tree if x['relative']!='.'),'no unlisted E descendants')
# Admin attribution only. Not qualification and not independently authenticated tool origin.
receipts=load(W/'ACTUAL_ADMIN_RECEIPTS.json');author_result=load(W/'ADMIN_CHECK.json')
same(author_result['checks'],5332,'author declared predicates');same([(r['chunk_id'],r['exit_code']) for r in receipts['receipts'] if r['kind'] in ('administrative_source_build','administrative_opaque_and_literal_check')],[('710180',0),('87f168',0)],'author saved receipt attribution')
same(author_result['qualification_credit'],0,'no author qualification credit')
result=dict(schema='ri218-independent-administrative-check-v1',status='PASS_SOURCE_TEXT_OPAQUE_PINS_AND_PRESERVED_STATE_ONLY',predicates=checks,observed_identities=sorted(observed.values(),key=lambda r:r['path']),distinct_observed=len(observed),declared_dependency_union=849,prospective_source_domain=857,actual_runtime_inventory_created=False,source_execution=False,scientific_body_decoded=False,qualification_credit=0,subject_handoff=pure(observed[str(W/'HANDOFF.json')]),source_manifest=pure(observed[str(W/'SOURCE_PINS.json')]),repairs=changes,entire_inverse_source_projection=True,complete_published_diff=True,old_partials_unchanged=True,E_files=48,E_directories=9,failures=[])
output=D/'CHECK_RESULT.json';body=canonical(result)
with output.open('xb') as f:
 demand(f.write(body)==len(body),'complete independent result write');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(path=str(output),bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),predicates=result['predicates'],distinct_observed=result['distinct_observed'],status=result['status'])))
