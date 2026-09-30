"""Root opaque/admin preflight for unchanged separately admitted caller guards."""
import importlib.util
import tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
prior=m.B/'ri150-root-optimized-profile-0ydjxad3'
m.verify(prior/'PROFILES_ACCEPTANCE.json',dict(bytes=2194,sha256='4bf521e8e8cceafce449b0e8620c515df53a2cb2b2d1c0ff612cbb4934c91716'))
m.verify(prior/'RI150_ROOT_ACTUAL_ADJUDICATION.json',dict(bytes=5626,sha256='4920cd7296e1e3c537e9d83f90dc3ff5711ec0952709549f85d9f4631b2bc495'))
pins={}
def add(r):
 old=pins.setdefault(r['path'],m.pure(r));assert old==m.pure(r)
for r in m.load(prior/'SOURCE_POST.json')['identities']:
 assert m.identity(r['path'])==r
 add(r)
for n in ['PROFILES_ACCEPTANCE.json','RI150_ROOT_ACTUAL_ADJUDICATION.json','GENUINE_OUTER.json','GENUINE_TOOL_COMPLETE.json','GENUINE_TOOL_CALL_DETAILS.json','MEASUREMENT_NEXT_ACTION.json','ROOT_PROFILE_CHECK.json','ROOT_CHECK_TOOL.json','ROOT_REVIEW_READ.json','OPERATION_FINAL_IDENTITIES.json','PROFILE_SOURCE_ADJUDICATION.json','SOURCE_PRE.json','SOURCE_POST.json','BOOTSTRAP_PRE.json','BOOTSTRAP_POST.json','BOOTSTRAP_PRE_TOOL.json','BOOTSTRAP_POST_TOOL.json']:
 add(m.ref(prior/n))
href=m.load(prior/'PROFILES_ACCEPTANCE.json')['independent_review'];m.verify(href['path'],href);add(href);h=m.load(href['path']);R=Path(href['path']).parent
assert sorted(p.name for p in R.iterdir())==sorted(h['exact_namespace'])
for r in h['files']:add(r)
for r in m.load(prior/'OPERATION_FINAL_IDENTITIES.json')['identities']:
 assert m.identity(r['path'])==r
 add(r)
rows=[m.verify(p,r) for p,r in sorted(pins.items())]
print(m.save('SOURCE_PRE.json',dict(schema='ri152-root-source-baseline-and-profiles-pre-v1',identities=rows,scientific_body_decode=False,subject_execution=False)))
old=m.load(prior/'OPERATION_LAYOUT.json');selected=m.identity(old['selected_interpreter_binding']['path']);assert selected==old['selected_interpreter_binding']
envroot=Path(old['environment_root']);assert not list((envroot/'tmp').iterdir())
op=Path(tempfile.mkdtemp(prefix='ri152-genuine-caller-guards-',dir=m.B))
print(m.save('OPERATION_LAYOUT.json',dict(operation=str(op),environment_root=str(envroot),environment=old['environment'],selected_interpreter_binding=selected,purpose='One separately admitted unchanged RI141 guards phase with original RI130 nonscientific65 harness; no operational card yet')))
with (m.D/'observe_bootstrap.py').open('xb') as f:f.write((prior/'observe_bootstrap.py').read_bytes().replace(b'ri150-root-direct-vendor-bootstrap-observation-v1',b'ri152-root-direct-vendor-bootstrap-observation-v1'))
print(m.save('REPO_ENTRY.json',m.snapshot()))
print(dict(operation=str(op),source_and_predecessor_files=len(rows),selected=selected))
