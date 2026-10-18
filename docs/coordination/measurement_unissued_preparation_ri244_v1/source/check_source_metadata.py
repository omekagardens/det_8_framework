"""Author-only bounded literal/opaque checks. Never loads the proposed subjects."""
from pathlib import Path
import hashlib
import json
import difflib
import os

W=Path(__file__).resolve().parent
checks=0
pins={}
def need(ok,label):
    global checks
    if not ok:raise ValueError(label)
    checks+=1

def identity(path):
    p=Path(path);before=p.stat();body=p.read_bytes();after=p.stat()
    need((before.st_dev,before.st_ino,before.st_mode,before.st_nlink,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==
         (after.st_dev,after.st_ino,after.st_mode,after.st_nlink,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'opaque stable '+str(p))
    row={'path':str(p),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
    if str(p) in pins:need(pins[str(p)]==row,'duplicate pin')
    pins[str(p)]=row
    return row

def check_ref(row):
    got=identity(row['path']);need({k:got[k] for k in ('path','bytes','sha256')}=={k:row[k] for k in ('path','bytes','sha256')},'declared body pin')

refs=json.loads((W/'REFERENCES.json').read_bytes())
need(len(refs)==18,'complete direct references')
for row in refs.values():check_ref(row)
manifest=json.loads(Path(refs['source_manifest']['path']).read_bytes())
need(len(manifest['modules'])==11 and len(manifest['dependencies'])==567,'source cardinalities')
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:check_ref(row)
source=(W/'prepare_unissued.py').read_text()
bootstrap=(W/'PRE_MODE_BOOTSTRAP.proposal.txt').read_text()
oldboot=Path(refs['bootstrap_template']['path']).read_text()
D='/Volumes/AI_DATA/development/det-review-evidence/ri244-current-normal-premode-2kfsmiea'
B='/Volumes/AI_DATA/development/det-review-evidence'
a=json.loads(Path(B+'/ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json').read_bytes())
check_ref({'path':B+'/ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json','bytes':2114,'sha256':'ac86cac1f9973266d84b2a1ad1b9a34e9655d897153dc264d6b0805f437389cd'})
env=dict(a['environment'],TMPDIR=D+'/tmp')
replacements=[('# One root-admitted administrative adapters action; unchanged RI141 child monitor.','# UNISSUED RI244 bootstrap proposal. Separate root admission/dispatch required.'),
 (repr(a['environment']),repr(env)),('ri204_whole_unchanged_ri141_adapters_monitor','ri244_whole_unchanged_ri141_premode_monitor'),
 (B+'/ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json',D+'/ADMIT_PRE_MODE.json'),
 (B+'/ri204-root-adapters-f04k2tg9/monitor',D+'/monitor'),("'ADAPTERS', 180, expected_environment)","'PRE_MODE', 180, expected_environment)")]
expected=oldboot
for before,after in replacements:
    need(expected.count(before)==1,'unique literal substitution '+before)
    expected=expected.replace(before,after)
need(bootstrap==expected,'entire expected bootstrap literal source')
reverse=bootstrap
for before,after in reversed(replacements):reverse=reverse.replace(after,before)
need(reverse==oldboot,'entire bootstrap reverse projection')
for name,old,new,oldname,newname in [
 ('BOOTSTRAP_DIFF.patch',oldboot,bootstrap,refs['bootstrap_template']['path'],str(W/'PRE_MODE_BOOTSTRAP.proposal.txt')),
 ('PREPARATION_DIFF.patch',Path(refs['preparation_predecessor']['path']).read_text(),source,refs['preparation_predecessor']['path'],str(W/'prepare_unissued.py')),
 ('CUSTODY_DIFF.patch',Path(refs['observer_predecessor']['path']).read_text(),source,refs['observer_predecessor']['path'],str(W/'prepare_unissued.py'))]:
    need((W/name).read_text()==''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile=oldname,tofile=newname)),'whole exact diff '+name)
for literal in ["decision_raw=initial_body(a.root_decision,a.root_decision_sha256)",
 "same(descriptor_state(f),before,'initial opened descriptor')", "same(descriptor_state(f),before,'initial final descriptor')",
 "exec(compile(helper,str(hp),'exec'),m.__dict__)", "old_E=read(refs['old_E'])", "len(oldroles['observed_identities'])==2811",
 "need((sys.flags.isolated,sys.flags.dont_write_bytecode,sys.flags.optimize)==(1,1,0)",
 "same(frozen['source_states'],oldroles['source_states']", "['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json']",
 "body=value if raw else canonical(value)", "need((D/name).read_bytes()==body", "snapshot=list(seen.values())",
 "'UNISSUED_NOT_OPERATIONAL_AUTHORITY'", "'REFUSED_RETAIN_ALL_PARTIALS'", "'operational_authorization':False",
 "if first is None:first=error", "len(manifest['dependencies'])==567", "[1810,48024515,4,195,2]",
 "'whole supplier post equality'", "'entire sealed bootstrap text'", "'root_decision':decision_ref"]:
    need(literal in source,'literal guard '+literal)
need(source.index("need(len(helper)==3144")<source.index("exec(compile(helper"),'helper auth before load')
need(source.index('first=None;artifacts={}')<source.index("(D/'tmp').mkdir"),'safe state before ownership')
need("(D/'tmp').mkdir(mode=0o700)  # Failure here is genuine preownership refusal.\n    try:\n        (D/'monitor').mkdir" in source,'protected owned body')
for label in ['inputs','supplier','E','authority_absences','outputs','namespace']:
    need("('"+label+"'," in source,'independent tail '+label)
for forbidden in ["emit('ADMIT_PRE_MODE.json'", "emit('DISPATCH.json'", "subprocess.run(", "subprocess.Popen(", "m.git(", "m.snapshot(", "read(request['freeze'])", "O.mkdir", "os.chdir(", "unlink("]:
    need(forbidden not in source,'no unrequested action '+forbidden)
need(source.count('exec(compile(')==1,'only captured administrative helper evaluation in future writer')
for name in ['prepare_unissued.py','REFERENCES.json','PRE_MODE_BOOTSTRAP.proposal.txt','PROTOCOL.md','BOOTSTRAP_DIFF.patch','PREPARATION_DIFF.patch','CUSTODY_DIFF.patch','check_source_metadata.py']:
    identity(W/name)
result={'schema':'ri244-author-literal-source-check-v1','status':'AUTHOR_SOURCE_METADATA_CHECK_PASSED_NOT_QUALIFICATION',
        'predicates':checks,'opaque_distinct_files':len(pins),'identities':list(pins.values()),
        'proposal_imported_compiled_or_executed':False,'vendor_or_E_observed':False,'scientific_body_decoded':False,
        'six_bootstrap_substitutions_reverse_exact':True,'whole_three_diffs_exact':True,'independent_acceptance':False}
body=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode('ascii')
with (W/'AUTHOR_CHECK.json').open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
need((W/'AUTHOR_CHECK.json').read_bytes()==body,'author report exact raw readback')
print(json.dumps({'saved_predicates':result['predicates'],'postwrite_readback':True,'opaque_distinct_files':len(pins),
                 'report':{'path':str(W/'AUTHOR_CHECK.json'),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}}))
