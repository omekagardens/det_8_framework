"""Fresh administrative custody observation only; no subject import or startup."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,time,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=Path(__file__).resolve().parent;D=B/'ri236-current-e-normal-preparation-3geu_r1s';W=D/'worker_proposal';E=B/'ri154-white-execution-proposed-42_uvw15';OLD=B/'ri234-root-reconciliation-tzop5ais';Q=B/'ri237-root-cross-root-review-jkfg7vlx'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=hp.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
phase=sys.argv[1];assert phase in ('PRE','POST');count=0
seen={}
def eq(a,b):
 global count
 assert m.canonical(a)==m.canonical(b);count+=1
def pinload(p,pin=None):
 if pin:m.verify(p,pin)
 return m.load(p)
def fresh(row):
 v=m.identity(row['path']);eq({k:v[k] for k in row},row)
 if v['path'] in seen:eq(v,seen[v['path']])
 seen[v['path']]=v;return v
def state(p):
 t=p.lstat();return [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
def namespaces(rows):
 out=[]
 for x in rows:
  p=Path(x['path']);a=state(p);v=dict(path=str(p),kind=x['kind'],state=a)
  if x['kind']=='directory':assert stat.S_ISDIR(p.lstat().st_mode);v['entries']=sorted(y.name for y in p.iterdir())
  else:assert x['kind']=='symlink' and p.is_symlink();v['target']=os.readlink(p)
  eq(state(p),a);eq(v,x);out.append(v)
 return out
recipe=pinload(W/'CAPTURE_RECIPE.json',dict(bytes=12114,sha256='3f46d182e4adedf6b6e346ebd5e5dd6eae60cf42b4e77b073a957531e4c68195'))
handoff=pinload(W/'HANDOFF.json',dict(bytes=5801,sha256='43a6c5eddc662f3aa220cceb8e6c8467744e1e1e8731e240e7e5a4dc393cca1b'))
eq(sorted(p.name for p in W.iterdir()),sorted(handoff['exact_namespace']))
for row in handoff['files']:fresh(row)
dep=pinload(W/'DEPENDENCIES.json');source_rows=[fresh(row) for row in dep['unique']];assert len(source_rows)==986
assert pinload(Q/'RI236_ROOT_DESIGN_ADJUDICATION.json',dict(bytes=2656,sha256='9d669a14732daea258b6659d1861c19f41063ca26fc8089901ee28f020cb5d4f'))['status']=='ACCEPT_CONCRETE_UNISSUED_CAPTURE_DESIGN_FOR_FRESH_ROOT_PREPARATION'
old=pinload(OLD/'POST_SUPPLIER.json');host=pinload(R/('GENUINE_'+phase+'_HOST.json'));assert host['result']['exit_code']==0;obs=json.loads(host['result']['output']);eq(obs,host['observation']);assert obs['returncode']==0 and obs['stderr']=='';eq(obs['environment'],dict(PATH='/usr/bin:/bin',LC_ALL='C'));eq(obs['uname'],list(os.uname()))
supplier=dict(absent=[],environment=recipe['environment'],host=dict(argv=obs['command'],exit_code=obs['returncode'],stderr=obs['stderr'],stdout=obs['stdout'],uname=obs['uname']),namespace=namespaces(old['namespace']),observed_at_unix_ns=time.time_ns(),tools=[fresh(x) for x in old['tools']],vendor=[fresh(x) for x in old['vendor']])
for p in old['absent']:assert not os.path.lexists(p);supplier['absent'].append(p)
eq({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in old.items() if k not in ('environment','observed_at_unix_ns')})
assert len(supplier['vendor'])==1810 and sum(x['bytes'] for x in supplier['vendor'])==48024515 and len(supplier['tools'])==4 and len(supplier['namespace'])==195 and len(supplier['absent'])==2
binding=fresh(recipe['admission_field_recipe']['bootstrap_host_preflight']['selected_interpreter_binding_exact_historical'])
eq(binding,recipe['admission_field_recipe']['bootstrap_host_preflight']['selected_interpreter_binding_exact_historical'])
hostcard=dict(uname=list(os.uname()),system_version=m.ref('/System/Library/CoreServices/SystemVersion.plist'));eq(hostcard,recipe['admission_field_recipe']['host']['fresh_observation_equals_historical'])
ebase=pinload(B/'ri226-directory-custody-recovery-yvfg_p1b/E_BEFORE.json');etree=[]
for row in ebase:
 p=E/row['relative'];a=state(p);assert not p.is_symlink();v=dict(relative=row['relative'],kind=row['kind'],state=a)
 if row['kind']=='directory':assert p.is_dir();v['entries']=sorted(x.name for x in p.iterdir())
 else:assert row['kind']=='file';v['identity']=fresh(row['identity']);assert v['identity']['state'][3]==1
 eq(v,row);eq(state(p),a);etree.append(v)
assert len(etree)==58 and sum(x['kind']=='file' for x in etree)==49
frozen=pinload(B/'ri226-freeze-reconciliation-operation-yvfg_p1b/FROZEN.json');roles=frozen['source_states'];assert len(roles['copies'])==48
for pair in roles['copies']:
 a=fresh(pair['original']);c=fresh(pair['copy']);eq(m.pure(a),m.pure(c))
for key,rows in roles.items():
 if key!='copies':
  for row in rows:fresh(row)
assert sorted(len(x) for x in roles.values())==[30,48,124]
for p in [E/'tmp',E/'runs/normal',E/'runs/optimized']:eq(list(p.iterdir()),[])
for p in [E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:assert not os.path.lexists(p)
controls={}
for name in ['ADMIT_CAPTURE.json','CAPTURE_PREFLIGHT.json','ROOT_CAPTURE_SOURCE_ADOPTION.json']:
 p=D/name
 if phase=='PRE':assert not os.path.lexists(p)
 else:controls[name]=m.identity(p)
if phase=='PRE':assert not os.path.lexists(recipe['paths']['capture_output'])
else:
 issued=pinload(R/'ISSUED_CAPTURE_CONTROLS.json')
 for name,row in controls.items():eq(row,issued['controls'][name])
 pre=pinload(R/'PRE_SUPPLIER.json');eq({k:v for k,v in supplier.items() if k!='observed_at_unix_ns'},{k:v for k,v in pre.items() if k!='observed_at_unix_ns'});eq(etree,pinload(R/'PRE_E.json'));eq(source_rows,pinload(R/'PRE_SOURCES.json'))
for row in list(seen.values()):eq(m.identity(row['path']),row)
eq(namespaces(supplier['namespace']),supplier['namespace'])
for row in etree:
 p=E/row['relative'];eq(state(p),row['state'])
 if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'])
eq(m.snapshot(),pinload(R/'REPO_ENTRY.json'))
refs=dict(supplier=m.save(phase+'_SUPPLIER.json',supplier),E=m.save(phase+'_E.json',etree),sources=m.save(phase+'_SOURCES.json',source_rows),role_custody=m.save(phase+'_ROLE_CUSTODY.json',dict(source_states=roles,observed_identities=list(seen.values()))),host=m.ref(R/('GENUINE_'+phase+'_HOST.json')))
record=dict(schema='ri239-fresh-capture-custody-v1',status='PASS_FRESH_'+phase+'_CUSTODY',phase=phase,refs=refs,selected_interpreter_binding=binding,host=hostcard,environment=recipe['environment'],source_roles=recipe['source_roles'],counts=dict(comparisons=count,whole_identities=len(seen),sources=986,vendor=1810,vendor_bytes=48024515,tools=4,namespaces=195,absences=2,E_files=49,E_directories=9,copy_pairs=48,history=124,targets=30),controls=controls,observed_at_unix_ns=time.time_ns(),scientific_execution=False,E_unchanged=True,repository_unchanged=True,collector_started_by_this_script=False,helper=m.ref(hp),observer=m.ref(Path(__file__).resolve()),historical_supplier=m.ref(OLD/'POST_SUPPLIER.json'),historical_E=m.ref(B/'ri226-directory-custody-recovery-yvfg_p1b/E_BEFORE.json'))
print(json.dumps(dict(receipt=m.save(phase+'_CUSTODY.json',record),counts=record['counts'])))
