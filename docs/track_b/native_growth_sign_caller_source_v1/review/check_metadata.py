"""Reviewer-owned opaque identities and source text only; never load target code."""
import collections, difflib, hashlib, json, os, pathlib, re, stat
R=pathlib.Path('/Volumes/AI_DATA/development/det-review-evidence/ri129-native-caller-independent-review-Z0SqaY10')
S=pathlib.Path('/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0')
A=pathlib.Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx')
errors=[]
def need(ok,label):
 if not ok: errors.append(label)
def sig(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(name):
 p=pathlib.Path(name); before=p.stat(); h=hashlib.sha256(); n=0
 with p.open('rb') as f:
  opened=os.fstat(f.fileno())
  while True:
   b=f.read(1048576)
   if not b: break
   n+=len(b); h.update(b)
  end=os.fstat(f.fileno())
 after=p.stat(); need(sig(before)==sig(opened)==sig(end)==sig(after),'unstable:'+str(p)); need(n==after.st_size,'size:'+str(p))
 links=[]; current=pathlib.Path(p.anchor)
 for bit in p.parts[1:]:
  current=current/bit
  if current.is_symlink(): links.append(str(current))
 return {'path':str(p),'resolved_path':str(p.resolve(strict=True)),'bytes':n,'sha256':h.hexdigest(),'symlinks':links}
def short(i): return {k:i[k] for k in ['path','bytes','sha256']}
def load(p): return json.loads(pathlib.Path(p).read_bytes())
def refs(v,where='$'):
 if type(v) is dict:
  if {'path','bytes','sha256'} <= set(v) and type(v['path']) is str and type(v['bytes']) is int and type(v['sha256']) is str:
   yield where,short(v)
  for k,x in v.items(): yield from refs(x,where+'.'+k)
 elif type(v) is list:
  for k,x in enumerate(v): yield from refs(x,where+'.'+str(k))
handoff=load(S/'HANDOFF.json'); hi=identity(S/'HANDOFF.json'); need((hi['bytes'],hi['sha256'])==(10184,'b3839ba2f81e791321e2549107ce5f1b84ffdbbcc635396ab4e72002386feac0'),'handoffpin')
packet=[hi]
for item in handoff['files']:
 actual=identity(item['path']); need(short(actual)==short(item),'packet:'+item['name']); packet.append(actual)
need(sorted(p.name for p in S.iterdir())==sorted(pathlib.Path(p['path']).name for p in packet),'source-only-namespace')
dep=load(S/'SOURCE_DEPENDENCIES.json'); hist=load(A/'HISTORY_RECONCILIATION.json'); runtime=load(A/'RUNTIME_CLOSURE.json')
need(set(dep)=={'schema','status','protected_files','scope'},'depkeys'); need(len(dep['protected_files'])==299,'depcount')
depchecks=[]; previous=''
for j,x in enumerate(dep['protected_files'],1):
 need(set(x)=={'role','path','identity','classification','access_policy','reference_provenance'},'depfields:'+str(j))
 need(x['role']=='dep_'+str(j).zfill(4) and previous<x['path'],'deporder:'+str(j)); previous=x['path']
 need(pathlib.Path(x['path']).is_absolute() and os.path.normpath(x['path'])==x['path'],'deppath:'+str(j))
 actual=identity(x['path']); need(actual==x['identity'],'depidentity:'+x['role']); need(not actual['symlinks'] and actual['resolved_path']==actual['path'],'depalias:'+x['role'])
 need(type(x['reference_provenance']) is list and all(type(v) is str for v in x['reference_provenance']),'provenance:'+x['role'])
 depchecks.append({'role':x['role'],'identity':actual,'matches':actual==x['identity']})
oldmanifests=[identity(A/n) for n in ['HISTORY_RECONCILIATION.json','RUNTIME_CLOSURE.json']]
need([(x['bytes'],x['sha256']) for x in oldmanifests]==[(2170307,'b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c'),(2862854,'35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920')],'oldmanifests')
known={}
for x in hist['protected_files']+runtime['files']+dep['protected_files']:
 p=x['path']; i=x['identity']; need(p not in known or known[p]==short(i),'crossmanifest:'+p);known[p]=short(i)
for i in packet+oldmanifests: known[i['path']]=short(i)
metadata_ref_checks=[]; mismatches=[]; unknown=[]
for x in dep['protected_files']:
 if x['classification']!='existing-administrative-source-custody-metadata': continue
 # Explicit administrative allowlist from reviewed manifest; scientific artifacts opaque.
 for field,ref in refs(load(x['path'])):
  expected=known.get(ref['path'])
  if expected is None: unknown.append({'source':x['path'],'field':field,'reference':ref})
  elif expected!=ref: mismatches.append({'source':x['path'],'field':field,'reference':ref,'current':expected})
  metadata_ref_checks.append({'source':x['path'],'field':field,'in_closed_map':expected is not None,'current_identity_matches':expected==ref})
patch_checks=[]
for name,patch in [('supervise.py','SUPERVISE_SOURCE_DELTA.patch'),('launch_audit.py','AUDIT_CALLER_SOURCE_DELTA.patch')]:
 before=(A/name).read_text().splitlines(keepends=True); after=(S/name).read_text().splitlines(keepends=True)
 expected=''.join(difflib.unified_diff(before,after,fromfile=str(A/name),tofile=str(S/name)))
 saved=(S/patch).read_text()
 matches=expected.splitlines(keepends=True)[2:]==saved.splitlines(keepends=True)[2:]
 need(matches,'diff:'+name);patch_checks.append({'file':name,'original':identity(A/name),'current':identity(S/name),'complete_diff_body_identical':matches})
def textblock(text,start,end): return text[text.index(start):text.index(end)]
checks=[]
for name,start,end in [('supervise.py','def runtime_prepare():','def dependency_prepare():'),('supervise.py','def resolve_links(path):','def expected_pairs(mode):'),('supervise.py','class Attempt:','def run(mode):')]:
 old=(A/name).read_text();new=(S/name).read_text()
 # runtime block ends before an RI129-only function: use next old function for old span.
 oldend='def preparation_ready():' if end=='def dependency_prepare():' else end
 try:
  before=textblock(old,start,oldend).strip(); after=textblock(new,start,end).strip()
  matches=before==after;checks.append({'file':name,'start':start,'end':end,'identical':matches});need(matches,'retained:'+start)
 except ValueError:
  checks.append({'file':name,'start':start,'end':end,'not_checked_marker_absent':True})
for name,start in [('supervise.py','def run(mode):'),('launch_audit.py','class Attempt:')]:
 old=(A/name).read_text();new=(S/name).read_text();a=old[old.index(start):];b=new[new.index(start):].replace('    pre_attempt_prerequisites(mode)\n','',1);same=a==b
 checks.append({'file':name,'start':start,'end':'EOF','identical_after_removing_only_new_preflight_call':same});need(same,'retainedtail:'+name)
result={'schema':'ri129-independent-source-metadata-check-v1','scope':'Opaque identities, closed administrative metadata and literal text only; no target or fixture activity and no current runtime file scan.', 'packet':packet,'dependencies':depchecks,'historical_manifests':oldmanifests,'history_role_count':len(hist['protected_files']),'runtime_file_roles':len(runtime['files']),'runtime_directory_records':len(runtime['directories']),'runtime_absence_records':len(runtime['absences']),'source_deltas':patch_checks,'retained_text':checks,'administrative_reference_checks':metadata_ref_checks,'reference_identity_mismatches':mismatches,'references_outside_closed_map':unknown,'errors':errors,'target_activity':False,'scientific_json_decode':False,'new_runtime_inventory':False,'repository_git_edits':False}
with (R/'METADATA_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'errors':errors,'packet':len(packet),'dep':len(depchecks),'adminrefs':len(metadata_ref_checks),'mismatches':mismatches,'outside_closed_map':unknown,'retained_text':checks},indent=2))
