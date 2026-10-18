"""Final administrative opaque replay; seals only the independent RI190 review."""
import hashlib,json,os,stat
from pathlib import Path
D=Path(__file__).parent
names=sorted(['ADMIN_CHECK.json','IDENTITIES.json','INDEPENDENT_REVIEW.md','VERDICT.json','TOOL_OUTCOMES.json','build_admin_checker.py','check_normal_saved.py','profile_checks_fragment.txt','seal_review.py'])
if sorted(p.name for p in D.iterdir())!=names:raise ValueError('unexpected review namespace')
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def ref(p):
 before=p.lstat()
 if not stat.S_ISREG(before.st_mode):raise ValueError('nonregular identity')
 h=hashlib.sha256();n=0
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  if state(before)!=state(os.fstat(f.fileno())):raise ValueError('open drift')
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  if state(before)!=state(os.fstat(f.fileno())):raise ValueError('descriptor drift')
 if state(before)!=state(p.lstat()) or n!=before.st_size:raise ValueError('final drift')
 return {'path':str(p),'bytes':n,'sha256':h.hexdigest()}
def save(name,v):
 with (D/name).open('xb') as f:f.write((json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
rows=json.loads((D/'IDENTITIES.json').read_bytes())['identities'];total=0
for r in rows:
 p=Path(r['path']);q=Path(r['resolved_path'])
 if p.resolve(strict=True)!=q or state(q.lstat())!=r['state']:raise ValueError('identity changed '+str(p))
 for link in r['symlink_chain']:
  if os.readlink(link['path'])!=link['target']:raise ValueError('link changed')
 fresh=ref(q)
 if any(fresh[k]!=r[k] for k in ('bytes','sha256')):raise ValueError('bytes changed '+str(p))
 total+=fresh['bytes']
save('FINAL_CHECK.json',{'schema':'ri190-independent-final-rehash-v1','status':'PASS','identities_rehashed':len(rows),'opaque_bytes_rehashed_including_named_aliases':total,'subject_execution':False,'scientific_body_decode':False,'review_payloads_before_seal':[ref(D/n) for n in names]})
names=sorted(names+['FINAL_CHECK.json'])
h={'schema':'ri190-independent-normal-profile-handoff-v1','status':'SEALED_ACCEPT_CURRENT_E_NORMAL_PROFILE_EVIDENCE','root':str(D),'reviewer':'/root/archive_repro_review','exclusive_namespace':sorted(names+['HANDOFF.json']),'files':[ref(D/n) for n in names],'review':ref(D/'INDEPENDENT_REVIEW.md'),'verdict':ref(D/'VERDICT.json'),'independent_administrative_terminal':{'chunk_id':'d3bdb9','exit_code':0},'actual_root_terminal':{'chunk_id':'9aba56','exit_code':0},'own_administrative_failures':[],'compact_publication_subset':[n for n in names+['HANDOFF.json'] if n!='IDENTITIES.json'],'external_only_identity_inventory':ref(D/'IDENTITIES.json'),'blocking_findings':[],'scope':'Actual normal-profile independent evidence acceptance only. Prior WHITE/bootstrap authorship and inherited source approval disclosed. No subject invocation, scientific decode, operational card or optimized profile by this reviewer. Root alone adjudicates and publishes.','ret_paused':True}
save('HANDOFF.json',h)
print(json.dumps({'handoff':ref(D/'HANDOFF.json'),'final_check':ref(D/'FINAL_CHECK.json'),'files':len(h['exclusive_namespace']),'payloads':len(names),'identities_rehashed':len(rows)},sort_keys=True))
