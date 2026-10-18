"""RI128 administrative metadata only; never loads scientific JSON or Python code."""
import hashlib
import json
from pathlib import Path
import re

E=Path('/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv')
O=Path('/Volumes/AI_DATA/development/det-review-evidence/ri128-independent-proof-source-review-Q4vXBzjt')
expected_handoff={'path':str(E/'HANDOFF.json'),'bytes':9587,'sha256':'afa9831b15250ef48ff8b6277e253afcb72b78914b79fdad5f5a4274d6ee7c25'}

def identity(path):
 p=Path(path); st1=p.stat(); h=hashlib.sha256(); total=0
 with p.open('rb') as f:
  while True:
   b=f.read(1024*1024)
   if not b:break
   total+=len(b);h.update(b)
 st2=p.stat()
 signature=lambda st:(st.st_dev,st.st_ino,st.st_mode,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
 return {'path':str(p),'bytes':total,'sha256':h.hexdigest()},signature(st1)==signature(st2)

records=[]
def check(ref, role):
 actual,stable=identity(ref['path'])
 ok=all(actual[k]==ref[k] for k in ('bytes','sha256')) and stable
 records.append({'role':role,'expected':{k:ref[k] for k in ('path','bytes','sha256')},'actual':actual,'metadata_stable':stable,'matches':ok})
 return ok

check(expected_handoff,'RI128 author handoff')
h=json.loads((E/'HANDOFF.json').read_text())
for ref in h['artifacts']:check(ref,'RI128 artifact:'+ref['file'])
s=json.loads((E/'SOURCES.json').read_text())
for ref in s['sources']:check(ref,ref['role'])
previous=next(x for x in s['sources'] if x['role']=='Immutable RI127 author packet')
p=json.loads(Path(previous['path']).read_text())
for ref in p['artifacts']:check(ref,'RI127 retained artifact:'+ref['file'])

texts={name:(E/name).read_text() for name in ('check.py','audit_saved.py')}
producer_actual,_=identity(E/'check.py')
fixed="PRODUCER_PIN = (%d, '%s')"%(producer_actual['bytes'],producer_actual['sha256'])
textual={
 'producer_pin_literal_matches':fixed in texts['audit_saved.py'],
 'complete_source_line_counts':{k:len(v.splitlines()) for k,v in texts.items()},
 'imports':{k:[{'line':i,'text':line} for i,line in enumerate(v.splitlines(),1) if re.match(r'^\s*(from |import )',line)] for k,v in texts.items()},
 'assert_guard_lines':{k:[i for i,line in enumerate(v.splitlines(),1) if re.match(r'^\s*assert\b',line)] for k,v in texts.items()},
 'dynamic_source_loading_lines':{k:[{'line':i,'text':line} for i,line in enumerate(v.splitlines(),1) if re.search(r'__import__|importlib|runpy|\bexec\s*\(|\beval\s*\(',line)] for k,v in texts.items()},
}
role_to_source={
 'ri88':'Existing scientific held object','ri88_root':'Explicit accepted seed result',
 'ri122_root':'Accepted complete RI122 pattern/sign evidence',
 'ri124_root':'Accepted RI124 full conditional H30 system',
 'ri127_root':'RI127 accepted root decision'}
pin_checks=[]
for role,label in role_to_source.items():
 ref=next(x for x in s['sources'] if x['role']==label)
 for name,quote in [('check.py','"'),('audit_saved.py',"'")]:
  literal=quote+role+quote+': ('+str(ref['bytes'])+', '+quote+ref['sha256']+quote+')'
  pin_checks.append({'source':name,'role':role,'literal_pin_matches':literal in texts[name]})

passed=all(r['matches'] for r in records) and textual['producer_pin_literal_matches'] and all(x['literal_pin_matches'] for x in pin_checks)
result={'schema':'ri128-independent-source-metadata-check-v1','status':'PASS_OPAQUE_METADATA_ONLY' if passed else 'FAIL',
 'reference_occurrences':len(records),'unique_paths':len({r['actual']['path'] for r in records}),
 'records':records,'source_text_metadata':textual,'five_input_pin_text_checks':pin_checks,
 'method':'Opaque whole-file hashing and pre/post stat metadata; three administrative handoff/source manifests decoded; Python sources inspected only as text. No target import, compile, AST, probe, fixture or numerical scientific decoding/evaluation.',
 'scientific_decode':False,'target_execution':False,'execution_authorized':False}
with (O/'SOURCE_METADATA_CHECK.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({k:result[k] for k in ('status','reference_occurrences','unique_paths')},sort_keys=True))
print(json.dumps({'textual':textual,'input_pin_matches':all(x['literal_pin_matches'] for x in pin_checks)},sort_keys=True))
