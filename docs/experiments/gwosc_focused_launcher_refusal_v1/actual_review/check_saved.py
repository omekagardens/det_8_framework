"""Independent saved refusal/administrative custody review. No subject execution."""
from pathlib import Path
from hashlib import sha256
import json, os, stat, shlex
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri137-root-launch-adjudication-ie1m0jc_';Q=B/'ri137-focused-control-launcher-source-nykv2tsg';O=B/'ri137-focused25-run-musr4qw9';R=B/'ri137-actual-refusal-independent-review-5hya_8t5'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pairs(rows):
 d={}
 for k,v in rows:need(k not in d,'duplicate admin key');d[k]=v
 return d
def read(p):return json.loads(p.read_text(),object_pairs_hook=pairs)
def pin(p):
 p=Path(p);need(p.is_absolute() and p.resolve(strict=True)==p and not p.is_symlink(),'literal metadata source path')
 before=p.stat();need(stat.S_ISREG(before.st_mode),'regular metadata source')
 h=sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 after=p.stat();state=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 need(state(before)==state(after) and n==before.st_size,'metadata read drift')
 return {'path':str(p),'bytes':n,'sha256':h.hexdigest()},state(after)
def verify(row):
 actual,state=pin(row['path']);need(actual=={k:row[k] for k in actual},'identity drift '+row['path'])
 if 'state' in row:need(state==row['state'] and row['resolved_path']==row['path'] and row['symlink_chain']==[],'source state drift '+row['path'])
 return actual
d=read(D/'ROOT_DISPATCH.json');t=read(D/'GENUINE_TOOL_INITIAL.json');c=read(O/'cards/launcher.json');control=read(O/'cards/controls.json');review=read(D/'RI137_ACTUAL_REFUSAL_REVIEW.json')
need(pin(D/'RI137_ACTUAL_REFUSAL_REVIEW.json')[0]['bytes']==3228 and pin(D/'RI137_ACTUAL_REFUSAL_REVIEW.json')[0]['sha256']=='8227aefa2338205826d713e00ef6b0737922b8f833822bc800f5305b5a2af022','assigned root review pin')
need(d['invocation']==t['invocation'],'genuine/admitted invocation')
terminal=t['result'];need(type(terminal['exit_code']) is int and terminal['exit_code']==1 and terminal['chunk_id']=='feff2a' and 'session_id' not in terminal,'real terminal failure')
need(terminal['output'].endswith('ValueError: actual complete environment\n'),'exact first error')
need('line 289, in prepare_launch' in terminal['output'],'actual failure line')
parts=shlex.split(d['invocation']['cmd']);need(parts[:3]==['exec','/usr/bin/env','-i'],'outer env prefix')
i=parts.index('/usr/bin/perl');environment=dict(x.split('=',1) for x in parts[3:i]);need(environment==c['environment'],'actual literal env assignments')
need(parts[i:i+3]==['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;'],'literal deadline expression')
need(parts[i+3:]==c['launcher_command'],'actual launcher argv')
need(d['invocation']['workdir']==str(O) and d['invocation']['login'] is False,'literal cwd/login')
need(c['launcher_command']==['/usr/bin/python3','-I','-B',str(Q/'launch_controls.source-only.py'),'--admission',str(O/'cards/launcher.json')],'fixed command')
need(c['child_command']==['/usr/bin/python3','-I','-B',str(B/'ri135-white-preparation-repair-source-lski1ize/fault_controls.source-only.py'),'--admission',str(O/'cards/controls.json'),'--output',str(O/'output/controls')],'planned not executed child')
need(control['output']==str(O/'output/controls') and len(control['controls'])==25,'control future scope')
cards=[verify(x) for x in d['cards']];copies=[]
for x in d['copies']:
 a=verify(x['original']);b=verify(x['operational']);need(Path(a['path']).read_bytes()==Path(b['path']).read_bytes(),'copy full bytes');copies.append({'original':a,'operational':b})
need(sorted(p.name for p in O.iterdir())==['cards','environment'],'operation top namespace')
need(not os.path.lexists(O/'output'),'no owned output')
need(sorted(p.name for p in (O/'cards').iterdir())==sorted(Path(x['path']).name for x in cards),'card namespace')
need(sorted(p.name for p in (O/'environment').iterdir())==['tmp'] and list((O/'environment/tmp').iterdir())==[],'empty retained environment')
namespace=[]
for p in sorted(O.rglob('*')):
 need(not p.is_symlink(),'operation unexpected symlink')
 namespace.append({'relative':str(p.relative_to(O)),'kind':'directory' if p.is_dir() else 'file',**({} if p.is_dir() else {'identity':pin(p)[0]})})
need(len(namespace)==8,'exact operation entries')
source=read(D/'ROOT_PRE_ADMISSION_SOURCE_CHECK.json');need(len(source['observations'])==289,'source observation count')
source_checks=[verify(x) for x in source['observations']]
need(len(set(x['path'] for x in source_checks))==289,'source distinct')
h=read(Q/'HANDOFF.json');need(sorted(p.name for p in Q.iterdir())==h['closed_namespace'],'source namespace')
v=Path(source['review']['path']);vh=read(v);need(sorted(p.name for p in v.parent.iterdir())==sorted(['HANDOFF.json']+[Path(x['path']).name for x in vh['files']]),'review namespace')
prebytes=(D/'BOOTSTRAP_PRE.json').read_bytes();postbytes=(D/'BOOTSTRAP_POST.json').read_bytes();need(prebytes==postbytes,'full bootstrap saved bytes')
pre=read(D/'BOOTSTRAP_PRE.json');post=read(D/'BOOTSTRAP_POST.json');need(pre==post,'full bootstrap decoded equality')
rows=pre['framework_namespace'];need(len(rows)==2004 and [x['path'] for x in rows]==sorted(set(x['path'] for x in rows)),'saved framework namespace')
fileindex={x['path']:x['identity'] for x in rows if x['kind']=='file'}
need(sum(x['bytes'] for x in fileindex.values())==48024515==pre['framework_file_bytes'],'saved file totals')
modules=pre['bootstrap_descriptor']['modules'];modulechecks=[]
for m in modules:
 if 'identity' not in m:continue
 identity=m['identity'];p=identity['path']
 if p==pre['collector']['path']:need(all(identity[k]==pre['collector'][k] for k in ('path','bytes','sha256')),'collector module pin');basis='collector'
 else:need(p in fileindex and identity==fileindex[p],'saved module identity outside framework '+p);basis='framework'
 modulechecks.append({'name':m['name'],'path':p,'basis':basis})
need(len(pre['bindings'])==9 and len(pre['absences'])==2,'saved bootstrap binding/absence count')
need(pre['bootstrap_descriptor']['isolated']==1 and pre['bootstrap_descriptor']['dont_write_bytecode']==1 and pre['bootstrap_descriptor']['optimize']==0,'saved bootstrap flags')
verify(pre['collector']);verify(pre['metadata_helper'])
diag=read(D/'BOOTSTRAP_ENV_DIAGNOSTIC.json');direct=read(D/'DIRECT_VENDOR_ENV_DIAGNOSTIC.json')
for x,chunk in ((diag,'1ac11a'),(direct,'a34537')):need(x['result']['exit_code']==0 and x['result']['chunk_id']==chunk and 'session_id' not in x['result'],'genuine diagnostic terminal')
actual=json.loads(diag['result']['output']);expected=c['environment'];need(all(actual[k]==v for k,v in expected.items()),'diagnostic intended fields changed')
extras={k:v for k,v in actual.items() if k not in expected};need(set(extras)=={'CPATH','LIBRARY_PATH','MANPATH','SDKROOT'},'exact diagnostic additions')
need(json.loads(direct['result']['output'])==expected,'direct diagnostic exact10')
for x in (diag,direct):
 argv=shlex.split(x['invocation']['cmd']);need(argv[:3]==parts[:3],'diagnostic outer prefix')
 j=next(j for j,z in enumerate(argv[3:],3) if '=' not in z)
 need(dict(y.split('=',1) for y in argv[3:j])==expected,'diagnostic exact declared environment')
 need(argv[j+1:]==['-I','-B','-c','import json,os; print(json.dumps(dict(os.environ),sort_keys=True))'],'benign diagnostic body')
 need(x['invocation']['workdir']==str(O) and x['invocation']['login'] is False,'diagnostic literal context')
vendor=next(x for x in pre['bindings'] if x['path']=='/Applications/Xcode.app/Contents/Developer/usr/bin/python3')
need(vendor['resolved_path'] in shlex.split(direct['invocation']['cmd']),'direct entry previously observed')
source_text=(Q/'launch_controls.source-only.py').read_text().splitlines()
need("same(dict(os.environ), env, 'actual complete environment')" in source_text[288],'unchanged exact guard')
need('module_bytes = captured' in source_text[298] and 'out.mkdir' in source_text[334] and 'P.child_run' in source_text[341],'later load ownership monitor order')
inputs=[pin(D/name)[0] for name in ('RI137_ACTUAL_REFUSAL_REVIEW.json','ROOT_DISPATCH.json','GENUINE_TOOL_INITIAL.json','BOOTSTRAP_ENV_DIAGNOSTIC.json','DIRECT_VENDOR_ENV_DIAGNOSTIC.json','BOOTSTRAP_PRE.json','BOOTSTRAP_POST.json','ROOT_PRE_ADMISSION_SOURCE_CHECK.json','ROOT_DEPENDENCY_CHECK.json','BOOTSTRAP_HOST_PREFLIGHT.json','RI137_ROOT_ADJUDICATION.json','DEADLINE_PROBE_INITIAL.json','ROOT_SOURCE_REVIEW.md','admit_focused.py','observe_bootstrap.py','review_refusal.py')]
result={'schema':'ri137-independent-saved-refusal-check-v1','status':'CONFIRMED_FAILED_PREOWNERSHIP_ATTEMPT_ZERO_CONTROLS','inputs':inputs,'actual_genuine_tool':terminal,'invocation_matches_admission':True,'literal_environment_assignments':environment,'literal_launcher_command':parts[i+3:],'cards':cards,'copies':copies,'operation_namespace':namespace,'owned_output_absent':True,'controls_executed':0,'monitor_called':False,'module_load_reached':False,'source_checks':source_checks,'unchanged_source_observations':289,'bootstrap_saved_complete_byte_equality':True,'saved_bootstrap_metadata':{'entries':2004,'files':len(fileindex),'file_bytes':48024515,'bindings':9,'absences':2,'modules':len(modules),'module_identity_checks':modulechecks},'bootstrap_runtime_currently_reinventoried':False,'diagnostic_extras':extras,'direct_diagnostic_equals_exact_environment':True,'direct_diagnostic_is_not_control_retry':True,'historical_outer_origin_premise':'Actual chunks and invocations supplied by coordinator genuine tool history; saved JSON shape alone cannot establish origin.','scientific_body_decode':False,'subject_reexecution':False}
p=R/'SAVED_REFUSAL_CHECK.json'
with p.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'output':pin(p)[0],'unchanged_source_observations':289,'saved_framework_entries':2004,'saved_module_identity_checks':len(modulechecks),'operation_entries':8}))
