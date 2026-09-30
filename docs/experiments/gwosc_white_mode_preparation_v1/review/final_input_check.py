"""Final RI154 source/evidence identity and full original namespace check only."""
import hashlib,importlib.util,json,os,stat
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri154-independent-relocation-review-_2275plo';A=B/'ri154-white-mode-preparation-42_uvw15';S=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
p=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=p.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted metadata helper drift')
s=importlib.util.spec_from_file_location('trusted_metadata',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
v=json.loads((R/'METADATA_CHECK.json').read_bytes());old={r['path']:r for r in v['observed']}
for path,row in old.items():
 if m.identity(path)!=row:raise ValueError('final full identity drift '+path)
deps=json.loads((B/'ri141-white-bootstrap-source-h58ls076/DEPENDENCIES.source-only.json').read_bytes())
namespace=[]
for p in sorted(S.rglob('*')):
 st=p.lstat();row={'relative':str(p.relative_to(S))}
 if stat.S_ISLNK(st.st_mode):raise ValueError('unexpected original source link')
 if stat.S_ISDIR(st.st_mode):row['kind']='directory'
 elif stat.S_ISREG(st.st_mode):row.update(kind='file',**m.pure(old[str(p)]))
 else:raise ValueError('unexpected original special member')
 namespace.append(row)
if namespace!=deps['packet_namespace']:raise ValueError('full original source namespace mismatch')
E=B/'ri154-white-execution-proposed-42_uvw15'
if os.path.lexists(E):raise ValueError('prospective root no longer absent')
value={'schema':'ri154-independent-final-input-check-v1','status':'PASS','unchanged_full_identities':len(old),'original_namespace':namespace,'original_file_count':48,'original_directory_count':4,'prospective_root_absent':True,'scientific_execution':False,'installed_runtime_observation':False,'basis':m.ref(R/'METADATA_CHECK.json')}
m.save('FINAL_INPUT_CHECK.json',value)
print(json.dumps({'status':'PASS','unchanged':len(old),'original_namespace_entries':len(namespace),'prospective_root_absent':True},sort_keys=True))
