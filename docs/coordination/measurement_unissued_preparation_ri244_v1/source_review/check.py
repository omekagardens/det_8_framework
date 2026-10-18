"""Independent administrative source-byte review; never imports reviewed source."""
from pathlib import Path
import hashlib,json,os,stat,difflib
R=Path(__file__).resolve().parent
W=Path('/private/tmp/ri244-preparation-proposal-3udz0imk')
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
E=B/'ri154-white-execution-proposed-42_uvw15'
REPO=Path('/Volumes/AI_DATA/development/det_8_framework-ret')
seen={};checks=[]
def need(ok,label):
    if not ok:raise ValueError(label)
    checks.append(label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def opaque(p):
    p=Path(p)
    need(p.is_relative_to(W) or p.is_relative_to(B) or p.is_relative_to(REPO),'allowed source/admin domain '+str(p))
    need(not p.is_relative_to(E),'no current E inventory '+str(p))
    need(p.resolve(strict=True)==p and not p.is_symlink(),'literal opaque source '+str(p))
    before=p.lstat();need(stat.S_ISREG(before.st_mode) and before.st_size<=67108864,'bounded regular source '+str(p))
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        need(state(os.fstat(f.fileno()))==state(before),'descriptor opening '+str(p))
        body=f.read(67108865)
        need(state(os.fstat(f.fileno()))==state(before),'descriptor closing '+str(p))
    need(state(p.lstat())==state(before) and len(body)==before.st_size,'stable whole body '+str(p))
    row={'path':str(p),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
    if str(p) in seen:need(seen[str(p)]==row,'repeat exact body '+str(p))
    seen[str(p)]=row
    return body

def verify(row):
    body=opaque(row['path'])
    need(seen[row['path']]=={k:row[k] for k in ('path','bytes','sha256')},'declared identity '+row['path'])
    return body

def pairs(rows):
    out={}
    for k,v in rows:
        if k in out:raise ValueError('duplicate administrative key')
        out[k]=v
    return out

def obj(body):
    return json.loads(body,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def loadref(row):return obj(verify(row))
def same(a,b,label):
    need(json.dumps(a,sort_keys=True,allow_nan=False)==json.dumps(b,sort_keys=True,allow_nan=False),label)

handoff=loadref({'path':str(W/'HANDOFF.json'),'bytes':4462,'sha256':'31e3265d02d9323c0b3224800e70ccac16955c696e0f3f2c2e84af23857b0ba1'})
same(sorted(x.name for x in W.iterdir()),handoff['namespace'],'exact eleven-file namespace')
need(len(handoff['files'])==10 and len(handoff['namespace'])==11,'ten payload eleven namespace')
need(len({r['path'] for r in handoff['files']})==10,'unique payloads')
need(handoff['author']=='/root/archive_repro_review' and handoff['independent_acceptance'] is False,'author versus independent status')
for row in handoff['files']:verify(row)
refs=obj(opaque(W/'REFERENCES.json'));need(len(refs)==18,'eighteen direct references')
for row in refs.values():verify(row)
manifest=loadref(refs['source_manifest'])
need(len(manifest['modules'])==11 and len(manifest['dependencies'])==567,'twelve component and 567 dependency rows')
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:verify(row)
need(manifest['bootstrap_provenance'] in manifest['dependencies'],'bootstrap provenance membership')
need(manifest['bootstrap_binding']['path']==manifest['bootstrap_binding']['resolved_path'] and manifest['bootstrap_binding']['symlink_chain']==[],'declared direct binding only; not observed')
author=obj(opaque(W/'AUTHOR_CHECK.json'))
need(author['opaque_distinct_files']==605 and len(author['identities'])==605 and author['predicates']==1259,'exact author report cardinalities')
for row in author['identities']:verify(row)
need(author['proposal_imported_compiled_or_executed'] is False and author['vendor_or_E_observed'] is False and author['scientific_body_decoded'] is False,'author claim scope preserved')
helper={'path':str(B/'ri122-root-execution-review-6whn_vky/metadata.py'),'bytes':3144,'sha256':'d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'}
verify(helper)
recipe=loadref({'path':str(B/'ri245-root-hook-review-ichvs643/RI244_ROOT_RECIPE_ADJUDICATION.json'),'bytes':2528,'sha256':'1886e256b35a416ac008f789da8330a38c7383231af5ab60fda3be416860f616'})
need(recipe['status']=='ACCEPT_CONCRETE_PREPARATION_RECIPE_NOT_OPERATIONAL_ADMISSION','recipe scope')
oldadmission={'path':str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),'bytes':2114,'sha256':'ac86cac1f9973266d84b2a1ad1b9a34e9655d897153dc264d6b0805f437389cd'}
oldcard=loadref(oldadmission)
source=opaque(W/'prepare_unissued.py').decode();bootstrap=opaque(W/'PRE_MODE_BOOTSTRAP.proposal.txt').decode()
oldboot=verify(refs['bootstrap_template']).decode()
need(len(source.splitlines())==334 and len(bootstrap.splitlines())==18,'complete source line counts')
D=str(B/'ri244-current-normal-premode-2kfsmiea');env=dict(oldcard['environment'],TMPDIR=D+'/tmp')
changes=[('# One root-admitted administrative adapters action; unchanged RI141 child monitor.','# UNISSUED RI244 bootstrap proposal. Separate root admission/dispatch required.'),(repr(oldcard['environment']),repr(env)),('ri204_whole_unchanged_ri141_adapters_monitor','ri244_whole_unchanged_ri141_premode_monitor'),(str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),D+'/ADMIT_PRE_MODE.json'),(str(B/'ri204-root-adapters-f04k2tg9/monitor'),D+'/monitor'),("'ADAPTERS', 180, expected_environment)","'PRE_MODE', 180, expected_environment)")]
expected=oldboot
for a,b in changes:
    need(expected.count(a)==1,'unique bootstrap old literal '+a)
    expected=expected.replace(a,b)
    need(expected.count(b)==1,'unique bootstrap new literal '+b)
need(expected==bootstrap,'six-change whole bootstrap equality')
for a,b in reversed(changes):expected=expected.replace(b,a)
need(expected==oldboot,'exact complete reverse projection')
for name,old,new,oldname,newname in [('BOOTSTRAP_DIFF.patch',oldboot,bootstrap,refs['bootstrap_template']['path'],str(W/'PRE_MODE_BOOTSTRAP.proposal.txt')),('PREPARATION_DIFF.patch',verify(refs['preparation_predecessor']).decode(),source,refs['preparation_predecessor']['path'],str(W/'prepare_unissued.py')),('CUSTODY_DIFF.patch',verify(refs['observer_predecessor']).decode(),source,refs['observer_predecessor']['path'],str(W/'prepare_unissued.py'))]:
    need(opaque(W/name).decode()==''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile=oldname,tofile=newname)),'full diff '+name)
roles=loadref(refs['old_roles']);frozen=loadref(refs['copy_observation']);etree=loadref(refs['old_E']);supplier=loadref(refs['old_supplier'])
need(len(roles['observed_identities'])==2811,'historical all-role observed count')
same(roles['source_states'],frozen['source_states'],'complete historic frozen role map')
same({k:len(v) for k,v in roles['source_states'].items()},{'copies':48,'history':124,'target_originals':30},'retained role multiplicities')
need(len(etree)==58 and sum(x['kind']=='file' for x in etree)==49 and sum(x['kind']=='directory' for x in etree)==9,'historical E49/9; no current observation')
need(len(supplier['vendor'])==1810 and sum(x['bytes'] for x in supplier['vendor'])==48024515 and len(supplier['tools'])==4 and len(supplier['namespace'])==195 and len(supplier['absent'])==2,'saved whole supplier cardinalities; not current observation')
request=loadref(refs['request']);runtime=loadref(refs['runtime']);accepted=loadref(refs['input_review'])
need(len(request)==5 and len(runtime)==13,'request5 runtime13')
same(accepted['request'],refs['request'],'accepted request body');same(accepted['runtime'],refs['runtime'],'accepted runtime body')
same(runtime['freeze'],{k:request['freeze'][k] for k in ('bytes','sha256')},'opaque freeze two versus three fields')
same(request['actual_runtime'],refs['runtime'],'actual runtime binding')
same(runtime['copy_observation'],refs['copy_observation'],'whole accepted copy observation')
need(runtime['environment']['TMPDIR']==str(E/'tmp') and env['TMPDIR']==D+'/tmp','distinct runtime/admin TMPDIR')
same({k:v for k,v in runtime['environment'].items() if k!='TMPDIR'},{k:v for k,v in env.items() if k!='TMPDIR'},'identical other environment fields')
need(source.index("same(sorted(p.name for p in D.iterdir()),[]")<source.index("(D/'tmp').mkdir"),'complete preeffect checks before ownership')
need(source.index('first=None;artifacts={}')<source.index("(D/'tmp').mkdir"),'failure state before ownership')
need("(D/'tmp').mkdir(mode=0o700)  # Failure here is genuine preownership refusal.\n    try:\n        (D/'monitor').mkdir" in source,'remaining effects guarded after ownership')
for name in ['inputs','supplier','E','authority_absences','outputs','namespace']:need("('"+name+"'," in source,'six independently attempted tail '+name)
for prohibited in ["emit('ADMIT_PRE_MODE.json'","emit('DISPATCH.json'","O.mkdir","os.chdir(","subprocess.run(","subprocess.Popen(","m.git(","m.snapshot(","read(request['freeze'])","unlink("]:
    need(prohibited not in source,'no operational/scientific effect '+prohibited)
need(source.count('exec(compile(')==1,'single future captured administrative helper load')
need("cwd=out, env=env, start_new_session=True" in verify(refs['monitor']).decode(),'inherited child cwd contract')
need("Path('"+D+"/monitor'), 'PRE_MODE', 180, expected_environment)" in bootstrap,'exact child output/cwd and wall bound')
need("'UNISSUED_NOT_OPERATIONAL_AUTHORITY'" in source and "'operational_authorization':False" in source,'wrapper has no authority')
same(sorted(x.name for x in W.iterdir()),handoff['namespace'],'final exact sealed namespace')
for row in handoff['files']:verify(row)
result={'schema':'ri244-independent-administrative-source-check-v1','status':'PASS_SOURCE_IDENTITY_CORRESPONDENCE_ONLY','predicates':len(checks),'distinct_opaque_files':len(seen),'identities':list(seen.values()),'checks':checks,'subject_or_proposal_import_compile_ast_execute':False,'current_supplier_or_E_observation':False,'scientific_body_decode':False,'exact_bootstrap_substitutions':6,'whole_exact_diff_files':3,'historical_roles':{'copies':48,'history':124,'target_originals':30,'observed_identities':2811},'current_runtime_or_operation_acceptance':False}
body=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
with (R/'CHECK.json').open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
assert (R/'CHECK.json').read_bytes()==body
print(json.dumps({'predicates':len(checks),'distinct_opaque_files':len(seen),'output':{'path':str(R/'CHECK.json'),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()},'postwrite_readback':True}))
