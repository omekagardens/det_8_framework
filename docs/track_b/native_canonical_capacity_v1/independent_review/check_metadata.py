"""Independent administrative seal/admission/reference checks; no scientific parser or arithmetic."""
from pathlib import Path
import os,hashlib,json,stat,re
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri231-native-six-root-witness-qboypkl8';R=B/'ri231-independent-six-root-review-fipt97mw';T=B/'ri230-root-lower-combinations-review-v9mxbmtc'
labels=[];seen={};bodies={}
def ck(value,label):
 labels.append(label)
 if not value:raise ValueError(label)
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
def eq(a,b,label):ck(canon(a)==canon(b),label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(path):
 p=Path(path);ck(p.is_absolute() and str(p)==os.path.normpath(str(p)),'absolute normalized '+str(p))
 for q in [p,*p.parents]:ck(not q.is_symlink(),'no symlink '+str(q))
 a=p.stat();ck(stat.S_ISREG(a.st_mode) and a.st_size<=67108864,'bounded regular '+str(p))
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  eq(state(os.fstat(fd)),state(a),'fd before '+str(p));chunks=[];n=0
  while n<=a.st_size:
   z=os.read(fd,min(65536,a.st_size+1-n))
   if not z:break
   chunks.append(z);n+=len(z)
  b=b''.join(chunks);ck(len(b)==a.st_size,'full bytes '+str(p));eq(state(os.fstat(fd)),state(a),'fd after '+str(p))
 finally:os.close(fd)
 eq(state(p.stat()),state(a),'path after '+str(p));row=dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),state=state(a),resolved_path=str(p.resolve()),symlink_chain=[]);ck(row['resolved_path']==str(p),'literal resolution '+str(p));seen[str(p)]=row;bodies[str(p)]=b;return row
def pin(row):
 p=row['path'];a=seen.get(p) or read(p)
 eq({k:a[k] for k in ('path','bytes','sha256')},{k:row[k] for k in ('path','bytes','sha256')},'exact opaque FilePin '+p);return a
def load(path):
 p=str(path);ck(p.endswith('.json') and not p.endswith('/CERTIFICATE.json'),'explicit administrative load '+p)
 if p not in seen:read(p)
 def pairs(rows):
  d={}
  for k,v in rows:
   if k in d:raise ValueError('duplicate administrative key')
   d[k]=v
  return d
 return json.loads(bodies[p],object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def simple(path):return {k:seen[str(path)][k] for k in ('path','bytes','sha256')}
pin(dict(path=str(D/'HANDOFF.json'),bytes=21131,sha256='baff3300c296e43de7f0253cbafe4c7fbf192a9b05a209d5a33ab9cb52949033'));h=load(D/'HANDOFF.json')
eq(sorted(p.name for p in D.iterdir()),h['namespace'],'whole six-file namespace');eq(len(h['payloads']),5,'five payloads');eq(sorted(Path(v['path']).name for v in h['payloads']),[n for n in h['namespace'] if n!='HANDOFF.json'],'payload exact coverage')
for row in h['payloads']:pin(row)
s=load(D/'SOURCE_REFERENCES.json');a=load(D/'AUTHOR_VERIFICATION.json')
for key in ['assignment','accepted_predecessor','predecessor_handoff','predecessor_references','accepted_four_root_witness']:pin(s[key])
for row in s['direct_sources']:pin(row['identity'])
eq(len(s['direct_sources']),32,'direct32');eq(sum(r['identity']['bytes'] for r in s['direct_sources']),796922,'direct byte count');eq(len({r['identity']['path'] for r in s['direct_sources']}),32,'direct distinct');eq([r['identity']['path'] for r in s['direct_sources']],sorted(r['identity']['path'] for r in s['direct_sources']),'direct order')
prior=load(s['predecessor_handoff']['path']);ps=load(s['predecessor_references']['path']);pm=load(s['inherited_manifest_by_reference']['identity']['path']);assignment=load(s['assignment']['path']);decision=load(s['accepted_predecessor']['path'])
eq(sorted(p.name for p in Path(s['predecessor_handoff']['path']).parent.iterdir()),prior['namespace'],'predecessor complete namespace')
for row in prior['payloads']:pin(row)
eq(decision['status'],'ACCEPT_CONDITIONAL_LOWER_COMBINATION_ROUTING_AND_BOUNDS','predecessor acceptance');eq(decision['packet'],s['predecessor_handoff'],'exact accepted predecessor');eq(assignment['reservation'],str(D),'author exclusive reservation');eq(assignment['new_scientific_execution_authority'],False,'no execution authority');eq(assignment['qualification_credit'],0,'no numerical credit');eq(s['scope'],h['scope'],'whole handoff scope');eq(a['scope'],s['scope'],'whole author scope');eq(a['manual_checks'],h['proof_steps'],'whole declared proof audit list')
by={r['identity']['path']:r for r in pm['protected_files']};eq(len(by),423,'inherited423 by reference');boundary={k:v for k,v in pm.items() if k not in ['schema','status','protected_files','scope']};eq(len(boundary),15,'fifteen boundary objects');eq(s['inherited_manifest_by_reference']['boundary_objects'],boundary,'whole original boundary values');eq(s['inherited_manifest_by_reference'],ps['inherited_manifest_by_reference'],'whole inherited manifest boundary unchanged')
for key in ['inherited_original_six_admissions','inherited_additional_admissions','inherited_RI189_analytic_admission','inherited_shared_affine_admission','inherited_RI223_literal_admissions','inherited_RI225_disconnected_admission','predecessor_literal_exception_boundary','inherited_RI216_native_premises_by_reference','predecessor_lower_law_metadata_boundary','executable_obligations']:
 eq(s[key],ps[key],'whole inherited field '+key)
eq(s['inherited_RI228_construction_admissions'],ps['additional_literal_admissions'],'whole renewed RI228 construction records')
extra=T/'RI231_REVIEWER_SIX_ROOT_LITERAL_ADMISSION.json';pin(dict(path=str(extra),bytes=4858,sha256='c49b52dcb224d0f7a82d381212a7067ab81f2ba778495b0acb604bbf0c4564bd'));ra=load(extra);original=s['separate_current_literal_exception'];pin(original['authority']);oa=load(original['authority']['path']);eq(ra['actor'],'/root/archive_repro_review','exact independent actor');eq(ra['reservation'],str(R),'exact independent reservation');eq(ra['subject'],simple(D/'HANDOFF.json'),'exact independent subject');eq(ra['status'],'ADMIT_EXACT_SIX_ROOT_LITERAL_INDEPENDENT_REVIEW_ONLY','literal-only independent permission');eq(ra['original_admission'],original['authority'],'original admission retained');eq(ra['identity'],oa['identity'],'same complete admitted body identity');eq(ra['keys'],oa['keys'],'same admitted six keys');eq(ra['prohibitions'],oa['prohibitions'],'all original prohibitions');eq(ra['inherited_body_row_not_reclassified'],by[original['body']['path']],'whole historical opaque body boundary');eq(original['inherited_body_row_not_reclassified'],ra['inherited_body_row_not_reclassified'],'same author opaque declaration')
for k in ['admitted_program_execution','source_inventory_expansion','typed_reference_expansion']:eq(ra[k],False,'no added authority '+k)
eq(ra['qualification_credit'],0,'no literal read execution credit');eq(ra['RET_paused'],True,'RET paused');pin(original['body']);lit=load(R/'LITERAL_IDENTITY.json');eq(lit['before'],lit['after'],'literal before/after whole states');eq({k:lit['before'][k] for k in ['path','bytes','sha256']},original['body'],'literal exact body');eq(lit['admission'],simple(extra),'literal exact separate permission')
for k in ['scientific_JSON_parsed','automatic_scientific_arithmetic']:eq(lit[k],False,'literal scope '+k)
eq([r['identity'] for r in s['direct_sources'] if r['access']=='exact-literal-scientific-exception'],[original['body']],'one scientific literal exception only')
eq(h['executable_obligations'],s['executable_obligations'],'all executable obligations unchanged');eq(s['executable_obligations']['new_credit'],0,'no new qualification')
for name in ['CANONICAL_CAPACITY.md','SIX_ROOT_WITNESS.md','HANDOFF.md']:
 text=bodies[str(D/name)].decode();ck(not re.search(r'^(<{7}|={7}|>{7})( |$)',text,re.M),'no conflict '+name)
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):ck(target in h['namespace'],'closed local link '+target)
replay=load(R/'AUTHOR_REPLAY.json');eq(replay['returncode'],0,'reviewed author metadata replay exit0');rv=json.loads(replay['stdout']);eq([rv['current_namespace'],rv['direct_sources'],rv['whole_identity_fresh_rechecks'],rv['explicit_selected_reference_checks']],[6,32,38,45],'exact author final-stage metadata coverage');eq(rv['scientific_body_JSON_parsed'],False,'author replay body opaque');eq(rv['automated_proof_arithmetic'],False,'author replay not mathematical proof')
# Check each already observed subject/dependency still has identical full current state.
for p,row in list(seen.items()):eq(state(Path(p).stat()),row['state'],'final unchanged full state '+p)
eq(sorted(p.name for p in D.iterdir()),h['namespace'],'final source namespace unchanged')
out=dict(schema='ri231-independent-administrative-review-v1',status='PASS_BOUNDED_IDENTITY_ADMISSION_AND_REFERENCE_REPLAY_NOT_MATHEMATICAL_ACCEPTANCE',checks=len(labels),labels=labels,whole_file_identities=[seen[p] for p in sorted(seen)],direct_sources=32,inherited423_freshly_rehashed=False,inherited15_boundaries_exact=True,reviewer_literal_exception=simple(extra),scientific_JSON_parsed=False,automated_proof_arithmetic=False,subjects_executed=False,qualification_credit=0,RET_paused=True)
data=(json.dumps(out,sort_keys=True,indent=2)+'\n').encode();p=R/'CHECK_RESULT.json'
with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(report=dict(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()),checks=len(labels),whole_files=len(seen))))
