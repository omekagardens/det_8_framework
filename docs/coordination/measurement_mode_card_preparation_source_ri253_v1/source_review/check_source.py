"""Independent administrative source/metadata check only; never evaluates proposed source."""
from pathlib import Path
import json,hashlib,os,stat,difflib,shlex
Q=Path(__file__).resolve().parent
W=Path('/private/tmp/ri249-mode-card-preparation-proposal-y170alnf')
P=Path('/private/tmp/ri244-preparation-proposal-3udz0imk')
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri249-normal-mode-card-preparation-y170alnf';O=B/'ri156-operation-ri249-mode-card-y170alnf';E=B/'ri154-white-execution-proposed-42_uvw15'
V='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
count=0;seen={};jsonpaths=[]
def need(v,label):
 global count
 if not v:raise ValueError(label)
 count+=1
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def same(a,b,label):need(canonical(a)==canonical(b),label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);a=p.lstat();need(stat.S_ISREG(a.st_mode) and p.resolve()==p and 0<=a.st_size<=67108864,'literal bounded opaque reference')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  same(state(os.fstat(f.fileno())),state(a),'opened identity');b=f.read(67108865);same(state(os.fstat(f.fileno())),state(a),'end descriptor')
 same(state(p.lstat()),state(a),'end path');need(len(b)==a.st_size,'complete bytes')
 r={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 if str(p) in seen:same(r,seen[str(p)],'repeated source/reference bytes')
 seen[str(p)]=r;return r
def verify(r):same(pin(r['path']),{k:r[k] for k in ('path','bytes','sha256')},'declared opaque pin')
def load(p):
 p=Path(p);need(not p.is_relative_to(E),'no E decode');pin(p)
 def pairs(rows):
  d={}
  for k,v in rows:need(k not in d,'unique admin field');d[k]=v
  return d
 v=json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)));jsonpaths.append(str(p));return v
h=load(W/'HANDOFF.json');same(pin(W/'HANDOFF.json'),{'path':str(W/'HANDOFF.json'),'bytes':8850,'sha256':'ccf34c9baf147994366595cf73be92534733a9b7e3c3810d72c3f227f3a2ab3c'},'sealed subject')
same(sorted(p.name for p in W.iterdir()),h['namespace'],'exact17 namespace');need(len(h['files'])==16 and len(h['namespace'])==17,'17/16 complete seal')
for r in h['files']:verify(r)
sp=load(W/'SOURCE_PINS.json');need(len(sp['files'])==12,'12 direct source pins')
for r in sp['files']:verify(r);need(r in h['files'],'source pin within sealed payload')
refs=load(W/'REFERENCES.json');oldrefs=load(P/'REFERENCES.json');need(len(refs)==27 and len(oldrefs)==18,'27/18 reference domains')
for k,r in oldrefs.items():same(refs[k],r,'old role unchanged '+k)
for r in refs.values():verify(r)
m=load(refs['source_manifest']['path']);need(len(m['modules'])==11 and len(m['dependencies'])==567 and len({r['path'] for r in m['dependencies']})==567,'full source closure domains')
for r in [m['adapter'],*m['modules'].values(),*m['dependencies']]:verify(r)
need(m['bootstrap_provenance'] in m['dependencies'],'bootstrap provenance retained')
source=(W/'prepare_unissued.py').read_text();old=(P/'prepare_unissued.py').read_text();boot=(W/'MODE_CARD_BOOTSTRAP.proposal.txt').read_text();oldboot=(P/'PRE_MODE_BOOTSTRAP.proposal.txt').read_text();changes=load(W/'SOURCE_CHANGES.json')
same(changes['predecessor'],refs['direct_preparation_predecessor'],'exact old source ref')
s=old
for c in changes['changes']:
 need(s.count(c['before'])==c['occurrences'],'source before occurrences');s=s.replace(c['before'],c['after'])
need(s==source,'full forward projection')
for c in reversed(changes['changes']):
 need(s.count(c['after'])==c['occurrences'],'source after occurrences');s=s.replace(c['after'],c['before'])
need(s==old,'full inverse projection')
for name,a,b,pa,pb in [('SOURCE_DIFF.patch',old,source,str(P/'prepare_unissued.py'),str(W/'prepare_unissued.py')),('BOOTSTRAP_DIFF.patch',oldboot,boot,str(P/'PRE_MODE_BOOTSTRAP.proposal.txt'),str(W/'MODE_CARD_BOOTSTRAP.proposal.txt'))]:
 expected=''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=pa,tofile=pb));need(expected==(W/name).read_text(),'whole exact diff '+name)
start='    def input_tail():';end="    completion={'schema':"
need(source[source.index(start):source.index(end)]==old[old.index(start):old.index(end)],'full six-tail block unchanged')
for start,end in [('def canonical(value):','def main():'),('    oldroles=read(',"    def absent_authority():")]:
 need(source[source.index(start):source.index(end)]==old[old.index(start):old.index(end)],'whole unchanged helper/supplier/E section')
base=Path(refs['bootstrap_template']['path']).read_text();ad=load(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json');env=dict(ad['environment'],TMPDIR=str(D/'tmp'))
pairs=[('# One root-admitted administrative adapters action; unchanged RI141 child monitor.','# UNISSUED RI249 mode-card bootstrap proposal. Separate root admission/dispatch required.'),(repr(ad['environment']),repr(env)),('ri204_whole_unchanged_ri141_adapters_monitor','ri249_whole_unchanged_ri141_mode_card_monitor'),(str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),str(D/'ADMIT_MODE_CARD.json')),(str(B/'ri204-root-adapters-f04k2tg9/monitor'),str(D/'monitor')),("'ADAPTERS', 180, expected_environment)","'MODE_CARD', 180, expected_environment)")]
t=base
for a,b in pairs:need(t.count(a)==1,'unique bootstrap substitution');t=t.replace(a,b)
need(t==boot,'whole monitor/bootstrap bytes');
for a,b in reversed(pairs):need(t.count(b)==1,'unique bootstrap inverse');t=t.replace(b,a)
need(t==base,'full bootstrap inverse')
req=load(W/'MODE_CARD_REQUEST.proposal.json');oldreq=load(refs['request']['path']);runtime=load(refs['runtime']['path']);pre=load(refs['pre_result']['path']);decision=load(refs['pre_mode_acceptance']['path'])
same(req,{'freeze':oldreq['freeze'],'mode':'normal','pre':refs['pre_result'],'normal_acceptance':None},'entire request4');need(len(req)==4,'four fields');need(canonical(req)==(W/'MODE_CARD_REQUEST.proposal.json').read_bytes(),'canonical request bytes')
same({k:pin(W/'MODE_CARD_REQUEST.proposal.json')[k] for k in ('bytes','sha256')},{'bytes':530,'sha256':'0ff48797216ca57b070e63ff2e3081add9421e77947c9864d9599155a4eae091'},'body identity')
same(pre,{'schema':'ri130-root-pre-mode-runtime-custody-v1','mode':'normal','freeze':runtime['freeze'],'runtime_acceptance':runtime['runtime_acceptance'],'selection_unchanged':True,'optional_namespaces_unchanged':True,'host_identity_unchanged':True,'observed_dyld_routes':runtime['observed_dyld_routes'],'metadata_record':refs['runtime']},'whole accepted pre9')
same([decision['status'],decision['result'],decision['root_custody'],decision['root_check'],decision['scientific_execution'],decision['mode_card_created'],decision['qualification_credit']],['ACCEPT_ONE_NORMAL_PRE_MODE_METADATA_OPERATION_ONLY',refs['pre_result'],refs['pre_mode_postflight'],refs['pre_mode_root_check'],False,False,0],'root actual metadata scope and bindings')
post=load(refs['pre_mode_postflight']['path']);rootcheck=load(refs['pre_mode_root_check']['path']);need(len(post['input_identities'])==2883 and len({r['path'] for r in post['input_identities']})==2883,'full saved2883 prior domain')
for r in post['input_identities']:need(set(r)=={'path','resolved_path','symlink_chain','state','bytes','sha256'} and len(r['state'])==7,'full saved shape, not current observation')
need(len(rootcheck['output_identities'])==3 and len(rootcheck['monitor_identities'])==4,'prior3/4 references')
for r in rootcheck['output_identities']+rootcheck['monitor_identities']:verify(r)
recipe=load(W/'ROOT_RECIPES.json');tools=load(recipe['actual_command_predecessor']['path']);verify(recipe['actual_command_predecessor'])
vec=['/usr/bin/env','-i']+[k+'='+env[k] for k in sorted(env)]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',V,'-I','-B',str(D/'MODE_CARD_BOOTSTRAP.proposal.py')]
same(shlex.split(recipe['operation_arguments_if_separately_admitted']['cmd']),vec,'literal exact outer argument vector without quoting drift');need(recipe['operation_arguments_if_separately_admitted']['cmd']==shlex.join(vec),'canonical actual command spelling')
expected=tools['operation']['arguments']['cmd'].replace(str(B/'ri244-current-normal-premode-2kfsmiea'),str(D)).replace('PRE_MODE_BOOTSTRAP.proposal.py','MODE_CARD_BOOTSTRAP.proposal.py')
same(recipe['operation_arguments_if_separately_admitted'],{'cmd':expected,'workdir':str(D),'login':False,'yield_time_ms':1000,'max_output_tokens':2000},'whole genuine predecessor command adaptation')
same(recipe['operation_environment'],env,'whole10 environment');same(recipe['operation_child_cwd'],str(D/'monitor'),'childcwd');need(recipe['operational_authorization'] is False and recipe['prepared_request_filepin'] is None,'no live authority or fake future ref')
same(recipe['operation_bounds'],{'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':.025,'maximum_sample_gap_seconds':.1,'ps_timeout_seconds':.05,'file_bytes':67108864},'unchanged six bounds');need(recipe['outer_alarm_seconds']==960,'outer960')
for k in ('preparation_source','bootstrap_source','request_source'):verify(recipe[k])
author=load(W/'AUTHOR_CHECK.json');need(author['saved_predicates']==24742 and len(author['identities'])==author['opaque_distinct_files']==626,'complete saved author report count')
for r in author['identities']:verify(r)
need(source.index("for row in previous['input_identities']:fresh(row)")<source.index('snapshot=list(seen.values())')<source.index("(D/'tmp').mkdir"),'before-effect complete snapshot')
need("(D/'tmp').mkdir(mode=0o700)  # Failure here is genuine preownership refusal.\n    try:\n        (D/'monitor').mkdir" in source,'immediate inherited protection')
need(source.index("request_ref=emit('MODE_CARD_REQUEST.json'")>source.index("        (D/'monitor').mkdir"),'request write under owned protection')
need("'qualification':refs['qualification'],'request':request_ref" in source and "'input_acceptance':refs['pre_mode_acceptance']" in source,'new exact request/predecessor bindings')
for x in ["emit('ADMIT_MODE_CARD.json'","emit('DISPATCH.json'","subprocess.run(","subprocess.Popen(","O.mkdir","read(request['freeze'])","os.chdir(","unlink("]:
 need(x not in source,'no forbidden writer effect '+x)
need(source.count('exec(compile(')==1,'sole future captured admin helper')
for r in list(seen.values()):verify(r)
report={'schema':'ri249-independent-mode-card-source-check-v1','status':'PASS_SOURCE_METADATA_ONLY_NOT_OPERATIONAL_ACCEPTANCE','predicates':count,'distinct_opaque_files':len(seen),'packet_files':17,'sealed_payloads':16,'source_reference_roles':27,'unchanged_reference_roles':18,'declared_dependencies':567,'saved_previous_custody_rows':2883,'prior_current_rows_reobserved':False,'source_changes':len(changes['changes']),'source_inverse':True,'whole_two_diffs':True,'full_six_tail_equality':True,'bootstrap_six_changes_inverse':True,'request_fields':4,'future_preparation_files':9,'future_empty_directories':2,'future_inner_card_fields':12,'future_external_candidate_fields':10,'writer_lines':len(source.splitlines()),'bootstrap_lines':len(boot.splitlines()),'exact_reference_identities':list(seen.values()),'administrative_JSON_paths':sorted(set(jsonpaths)),'proposed_source_execution_import_compile_AST':False,'current_supplier_or_E_inventory':False,'genuine_origin_and_fresh_host_external':True}
raw=canonical(report)
with (Q/'CHECK.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert (Q/'CHECK.json').read_bytes()==raw
print(json.dumps({'report':{'path':str(Q/'CHECK.json'),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'predicates':count,'opaque_files':len(seen),'source_lines':len(source.splitlines()),'bootstrap_lines':len(boot.splitlines())}))
