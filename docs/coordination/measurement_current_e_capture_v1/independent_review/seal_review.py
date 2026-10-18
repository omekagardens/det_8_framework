"""Administrative final identity replay and immutable review seal only."""
import hashlib,json,os,stat
from pathlib import Path
D=Path(__file__).resolve().parent
expected=sorted(['ADMIN_CHECK.json','ADMIN_FAILURE.json','IDENTITIES.json','INDEPENDENT_REVIEW.md','TOOL_OUTCOMES.json','VERDICT.json','check_saved_capture.py','check_saved_capture_v2.py','seal_review.py'])
if sorted(p.name for p in D.iterdir())!=expected:raise ValueError('unsealed namespace differs')
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def ref(p):
 s=p.lstat()
 if not stat.S_ISREG(s.st_mode):raise ValueError('nonregular seal artifact')
 h=hashlib.sha256();n=0
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  if state(s)!=state(os.fstat(f.fileno())):raise ValueError('seal open drift')
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);n+=len(b)
  if state(s)!=state(os.fstat(f.fileno())):raise ValueError('seal descriptor drift')
 if state(s)!=state(p.lstat()) or n!=s.st_size:raise ValueError('seal final drift')
 return {'path':str(p),'bytes':n,'sha256':h.hexdigest()}
def save(name,v):
 with (D/name).open('xb') as f:f.write((json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
rows=json.loads((D/'IDENTITIES.json').read_bytes())['identities']; total=0
for row in rows:
 p=Path(row['path']);resolved=Path(row['resolved_path'])
 if p.resolve(strict=True)!=resolved:raise ValueError('final resolution drift '+str(p))
 for link in row['symlink_chain']:
  if os.readlink(link['path'])!=link['target']:raise ValueError('final link drift')
 if state(resolved.lstat())!=row['state']:raise ValueError('final recorded state drift '+str(p))
 r=ref(resolved)
 if any(r[k]!=row[k] for k in ('bytes','sha256')):raise ValueError('final opaque bytes drift '+str(p))
 total+=r['bytes']
result={'schema':'ri186-independent-final-review-check-v1','status':'PASS','opaque_identities_rehashed':len(rows),'opaque_bytes_rehashed_including_named_aliases':total,'subject_or_vendor_execution':False,'scientific_body_decode':False,'original_namespace_before_seal':expected,'original_review_payload_pins':[ref(D/n) for n in expected]}
save('FINAL_CHECK.json',result)
payloads=sorted(expected+['FINAL_CHECK.json'])
handoff={'schema':'ri186-independent-capture-review-handoff-v1','status':'SEALED_ACCEPT_CURRENT_E_METADATA_BASELINE_EVIDENCE','root':str(D),'reviewer':'/root/archive_repro_review','exclusive_namespace':sorted(payloads+['HANDOFF.json']),'files':[ref(D/n) for n in payloads],'primary_verdict':ref(D/'VERDICT.json'),'primary_review':ref(D/'INDEPENDENT_REVIEW.md'),'successful_admin_terminal':{'chunk_id':'7c9995','exit_code':0},'preserved_failed_admin_terminal':{'chunk_id':'cd6614','exit_code':1},'fresh_final_check':ref(D/'FINAL_CHECK.json'),'compact_publication_subset':[n for n in payloads+['HANDOFF.json'] if n!='IDENTITIES.json'],'external_only_diagnostics':[ref(D/'IDENTITIES.json')],'scope':'Independent actual saved administrative outcome and opaque custody replay; inherited earlier authored source premises disclosed. No new source approval, card, baseline admission, profile or science execution. Root alone adjudicates and publishes.','blocking_findings':[],'ret_paused':True}
save('HANDOFF.json',handoff)
print(json.dumps({'handoff':ref(D/'HANDOFF.json'),'final_check':ref(D/'FINAL_CHECK.json'),'files':len(handoff['exclusive_namespace']),'payloads':len(payloads),'identities_rehashed':len(rows)},sort_keys=True))
