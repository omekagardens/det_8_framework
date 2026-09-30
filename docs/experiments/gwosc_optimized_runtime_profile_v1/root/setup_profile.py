"""Root administrative preparation for one optimized observation; no subject load."""
import importlib.util,tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
normal=m.B/'ri148-root-normal-profile-qfvdi_75';base=m.B/'ri146-root-current-capture-9bfi4u8s'
m.verify(normal/'NORMAL_ACCEPTANCE.json',dict(bytes=1662,sha256='516e64fbf2f432d3f65872dc2ceb7ebd3a21f88303139f5598946494d9ec68af'))
m.verify(normal/'RI148_ROOT_ACTUAL_ADJUDICATION.json',dict(bytes=4967,sha256='8f76c91ef005b305f796dcfd42dd491d3147a903d087f6914eb9fc8367e96074'))
m.verify(base/'BASELINE_ACCEPTANCE.json',dict(bytes=1659,sha256='4e82e7e3aae50e45fdbae3aada5a2ab55422c690a843edbb4fb6673e6607f2c8'))
pins={}
def add(r):
 old=pins.setdefault(r['path'],m.pure(r));assert old==m.pure(r)
for r in m.load(normal/'SOURCE_PRE.json')['identities']:add(r)
for n in ['NORMAL_ACCEPTANCE.json','RI148_ROOT_ACTUAL_ADJUDICATION.json','GENUINE_OUTER.json','GENUINE_TOOL_COMPLETE.json','MEASUREMENT_NEXT_ACTION.json','ROOT_PROFILE_CHECK.json','ROOT_CHECK_TOOL.json','ROOT_REVIEW_READ.json','OPERATION_FINAL_IDENTITIES.json']:
 add(m.ref(normal/n))
href=m.load(normal/'NORMAL_ACCEPTANCE.json')['independent_review'];m.verify(href['path'],href);add(href);h=m.load(href['path']);R=Path(href['path']).parent
assert sorted(p.name for p in R.iterdir())==sorted(h['exact_namespace'])
for r in h['files']:add(r)
for r in m.load(normal/'OPERATION_FINAL_IDENTITIES.json')['identities']:add(r)
rows=[m.verify(p,r) for p,r in sorted(pins.items())]
print(m.save('SOURCE_PRE.json',dict(schema='ri150-root-source-baseline-and-normal-pre-v1',identities=rows,scientific_body_decode=False,subject_execution=False)))
old=m.load(normal/'OPERATION_LAYOUT.json');selected=m.identity(old['selected_interpreter_binding']['path']);assert selected==old['selected_interpreter_binding']
envroot=Path(old['environment_root']);assert not list((envroot/'tmp').iterdir())
op=Path(tempfile.mkdtemp(prefix='ri150-genuine-optimized-profile-',dir=m.B))
print(m.save('OPERATION_LAYOUT.json',dict(operation=str(op),environment_root=str(envroot),environment=old['environment'],selected_interpreter_binding=selected,purpose='One separately admitted optimized runtime profile; accepted normal/baseline, same environment; no operational card yet')))
with (m.D/'observe_bootstrap.py').open('xb') as f:f.write((normal/'observe_bootstrap.py').read_bytes().replace(b'ri148-root-direct-vendor-bootstrap-observation-v1',b'ri150-root-direct-vendor-bootstrap-observation-v1'))
print(m.save('REPO_ENTRY.json',m.snapshot()))
print(dict(operation=str(op),source_and_predecessor_files=len(rows),selected=selected))
