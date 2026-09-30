"""Reviewer-owned opaque/source-manifest checks only. Never load target code."""
from pathlib import Path
import hashlib
import json
import os
import stat
S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri133-white-runtime-preparation-source-lrck33ys')
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri133-runtime-preparation-independent-review-ipnnpdq6')
checks=[]
def check(name, result):
    checks.append({'check':name,'passed':bool(result)})
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def obj(p):return json.loads(Path(p).read_bytes())
def checkpin(row):
    got=pin(row['path']);check('opaque '+row['path'],got=={k:row[k] for k in ('path','bytes','sha256')});return got
h=obj(S/'HANDOFF.json');d=obj(S/'DEPENDENCIES.source-only.json');m=obj(S/'SOURCE_METADATA_CHECK.json')
check('handoff authorized identity',pin(S/'HANDOFF.json')=={'path':str(S/'HANDOFF.json'),'bytes':5719,'sha256':'480188c24c2b4a0062e7a1b882d8a11eb1f7786c987224d23d22ece22927be59'})
packet=[checkpin(row) for row in h['artifacts']]+[pin(S/'HANDOFF.json')]
check('source packet exact 10 regular files',sorted(x.name for x in S.iterdir())==sorted([x['relative'] for x in h['artifacts']]+['HANDOFF.json']) and all(x.is_file() and not x.is_symlink() for x in S.iterdir()))
dependency_observations=[checkpin(row) for row in d['opaque_files']]
check('228 distinct opaque dependencies',len(dependency_observations)==228 and len({x['path'] for x in dependency_observations})==228)
check('15474401 opaque bytes',sum(x['bytes'] for x in dependency_observations)==15474401)
check('all author dependency check rows reconciled',m['dependency_checks']==[{**x,'matches':True} for x in dependency_observations])
for role in ('historical_optional_namespaces','historical_runtime','packet_handoff','root_adjudication'):
 check('declared role in complete dependencies '+role,d[role] in d['opaque_files'])
P=Path(d['packet_root']); ph=obj(P/'HANDOFF.json'); pairs=obj(P/'TARGET_CLOSURE.source-only.json')['sources']; history=obj(P/'HISTORY_CLOSURE.source-only.json')
check('48 predecessor files and 47 handoff artifacts',len(ph['artifacts'])==47)
for row in ph['artifacts']:
 check('predecessor artifact coverage '+row['relative'],{k:row[k] for k in ('path','bytes','sha256')} in d['opaque_files'])
check('124 history roles',len(history)==124)
for i,row in enumerate(history):check('history closure role '+str(i),row in d['opaque_files'])
check('30 original/copy pairs',len(pairs)==30)
pair_observations=[]
for row in pairs:
 original=pin(row['original']);copy=pin(P/row['relative']);p=row['pin']
 check('original/copy equality '+row['relative'],{k:original[k] for k in p}==p=={k:copy[k] for k in p} and original in d['opaque_files'] and copy in d['opaque_files'])
 pair_observations.append({'original':original,'copy':copy})
namespace=[]
for base,dirs,files in os.walk(P,followlinks=False):
 for name in sorted(dirs+files):
  p=Path(base)/name;r={'relative':str(p.relative_to(P))};st=p.lstat()
  if stat.S_ISLNK(st.st_mode):r.update(kind='symlink',target=os.readlink(p))
  elif stat.S_ISDIR(st.st_mode):r.update(kind='directory')
  elif stat.S_ISREG(st.st_mode):r.update(kind='file',**{k:v for k,v in pin(p).items() if k!='path'})
  else:r.update(kind='unsupported')
  namespace.append(r)
namespace.sort(key=lambda x:x['relative'])
check('entire predecessor 52 entry namespace',namespace==d['packet_namespace'] and len(namespace)==52)
correspondence=obj(S/'SOURCE_CORRESPONDENCE.json')
for block in correspondence['exact_text_blocks']:
 old=Path(block['old']['path']).read_text();new=Path(block['new']['path']).read_text();marker=block['new']['marker']
 if block['name']=='runtime domain constants':
  oldpart=old[old.index(marker):old.index('\n\ndef ',old.index(marker))]
  newpart=new[new.index(marker):new.index('\n\ndef ',new.index(marker))]
  check('runtime literal domain 1866 bytes',oldpart==newpart and len(oldpart.encode())==1866)
 else:
  oldpart=old[old.index(marker):old.index('\n',old.index("])\n",old.index(marker)))];newpart=new[new.index(marker):new.index('\n',new.index("])\n",new.index(marker)))]
  check('entire 65 ID literal expression',oldpart==newpart)
 check('correspondence original named line '+block['name'],old.splitlines()[block['old']['line']-1].startswith(marker))
 check('correspondence new named line '+block['name'],new.splitlines()[block['new']['line']-1].startswith(marker))
for row in m['source_files']:
 b=Path(row['path']).read_bytes();text=b.decode();headers=[{'line':i,'text':line} for i,line in enumerate(text.splitlines(),1) if line.startswith('def ')]
 check('source line count '+row['path'],len(text.splitlines())==row['lines'])
 check('all plain text function headers '+row['path'],headers==row['plain_text_function_headers'])
 check('source pin '+row['path'],pin(row['path'])=={k:row[k] for k in ('path','bytes','sha256')})
check('total source lines 1044',sum(x['lines'] for x in m['source_files'])==1044)
check('observer complete byte correspondence',(P/'profile_observe.source-only.py').read_bytes()==Path('/Volumes/AI_DATA/development/det-review-evidence/ri121-root-runtime-qualification-jsf0o3_x/runtime_profile_probe.py').read_bytes())
# Inventory JSONs are historical opaque files above; their scientific bodies are not parsed.
report={'schema':'ri133-independent-opaque-review-v1','method':'Reviewer-owned metadata/hash and administrative manifest JSON only; no target imports, compilation, AST, probe or execution; no scientific body decode or current installed runtime inventory.', 'reviewer_script':pin(__file__),'source_packet':packet,'dependency_observations':dependency_observations,'pair_observations':pair_observations,'predecessor_namespace':namespace,'checks':checks,'passed':all(x['passed'] for x in checks),'target_execution':False,'scientific_body_decode':False,'current_runtime_inventory':False,'repository_or_git_mutation':False}
out=R/'OPAQUE_METADATA_REVIEW.json'
with out.open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'output':pin(out),'checks':len(checks),'passed':report['passed'],'failures':[x for x in checks if not x['passed']]}))
