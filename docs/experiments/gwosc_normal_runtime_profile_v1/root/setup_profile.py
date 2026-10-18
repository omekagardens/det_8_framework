"""Root administrative preparation; no subject source is imported."""
import importlib.util, tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
prior=m.B/'ri146-root-current-capture-9bfi4u8s'
m.verify(prior/'BASELINE_ACCEPTANCE.json',dict(bytes=1659,sha256='4e82e7e3aae50e45fdbae3aada5a2ab55422c690a843edbb4fb6673e6607f2c8'))
m.verify(prior/'RI146_ROOT_ACTUAL_ADJUDICATION.json',dict(bytes=4412,sha256='5357b3ce425db7c3b2ad34a3b7644158656f461c4d3bf9e190c6cfbf28611d84'))
base=m.load(prior/'BASELINE_ACCEPTANCE.json');pins={}
def add(row):
 old=pins.setdefault(row['path'],m.pure(row));assert old==m.pure(row)
for row in m.load(prior/'SOURCE_PRE.json')['identities']:add(row)
for name in ['BASELINE_ACCEPTANCE.json','RI146_ROOT_ACTUAL_ADJUDICATION.json','GENUINE_OUTER.json','GENUINE_TOOL_COMPLETE.json','GENUINE_TOOL_ARGUMENTS.json','MEASUREMENT_NEXT_ACTION.json']:
 add(m.ref(prior/name))
review=Path(base['independent_review']['path']);m.verify(review,base['independent_review']);h=m.load(review)
assert sorted(p.name for p in review.parent.iterdir())==sorted(h['exact_current_namespace'])
add(base['independent_review'])
for row in h['files']:add(row)
for row in m.load(prior/'OPERATION_FINAL_IDENTITIES.json')['identities']:add(row)
rows=[m.verify(p,r) for p,r in sorted(pins.items())]
print(m.save('SOURCE_PRE.json',dict(schema='ri148-root-source-and-baseline-pre-v1',identities=rows,scientific_body_decode=False,subject_execution=False)))
old=m.load(prior/'OPERATION_LAYOUT.json');selected=m.identity(old['selected_interpreter_binding']['path']);assert selected==old['selected_interpreter_binding']
envroot=Path(base['environment_root']);assert not list((envroot/'tmp').iterdir())
op=Path(tempfile.mkdtemp(prefix='ri148-genuine-normal-profile-',dir=m.B))
print(m.save('OPERATION_LAYOUT.json',dict(operation=str(op),environment_root=str(envroot),environment=old['environment'],selected_interpreter_binding=selected,purpose='One separately admitted normal runtime profile; same accepted environment; no operational card yet')))
collector=(prior/'observe_bootstrap.py').read_bytes()
with (m.D/'observe_bootstrap.py').open('xb') as f:f.write(collector.replace(b'ri146-root-direct-vendor-bootstrap-observation-v1',b'ri148-root-direct-vendor-bootstrap-observation-v1'))
print(dict(operation=str(op),source_and_baseline_files=len(rows),selected=selected))
