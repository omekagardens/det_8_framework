"""Root administrative source authentication and fresh layout; no target imports."""
import importlib.util, tempfile
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
B=m.B; S=B/'ri141-white-bootstrap-source-h58ls076'; R=B/'ri141-bootstrap-independent-review-k5bss5xp'; P=B/'ri143-root-feasibility-review-b9bt7rgh'
pins={}; namespaces=[]
def add(row):
 old=pins.setdefault(row['path'],m.pure(row)); assert old==m.pure(row)
def packet(root,expected):
 m.verify(root/'HANDOFF.json',expected); h=m.load(root/'HANDOFF.json')
 assert sorted(x.name for x in root.iterdir())==sorted(h['exact_namespace'])
 namespaces.append(dict(path=str(root),names=h['exact_namespace']))
 add(m.ref(root/'HANDOFF.json'))
 for row in h['files']:add(row)
packet(S,dict(bytes=9366,sha256='40effed085b2b79cd8933d675ec627e51c2910d95ea1f2e02ea75d2927c40f65'))
packet(R,dict(bytes=5103,sha256='fb2ccb6ea23abd009db852c56fa2ac6e33f1c0b54a5b1db9324722e05ca214fb'))
dep=m.load(S/'DEPENDENCIES.source-only.json')
for row in dep['opaque_files']:add(row)
for path,size,digest in [
 (B/'ri140-root-source-adjudication-8796wh9l/RI141_ROOT_ADJUDICATION.json',3799,'4e63c273bb537f0afff99cebf92d6d70d389fe0707f5a902d164abe979f8849c'),
 (P/'RI144_ROOT_ACTUAL_ADJUDICATION.json',3715,'37ec9c8cfafe8136a99ab6bddc435467c059c05e402b8923c66f49f8e51a2d48'),
 (P/'ROOT_ACTUAL_REVIEW_CORRECTION.json',1325,'faacac55ae6858ba9287857b1e15b508f8004565eec8fd5aac0d1e7c52e0177e'),
 (B/'ri144-independent-actual15-review-rt_iv488/HANDOFF.json',5688,'4e1cf194aa8e7f4b641ddf68037fb0c93b4e5b45123f2b4284a62d479cc77dd7')]:
 add(dict(path=str(path),bytes=size,sha256=digest))
rows=[m.verify(path,pin) for path,pin in sorted(pins.items())]
print(m.save('SOURCE_PRE.json',dict(schema='ri146-root-source-pre-v1',identities=rows,namespaces=namespaces,scientific_body_decode=False,subject_execution=False)))
selected=m.identity(dep['selected_bootstrap_binding']['path']);assert selected==dep['selected_bootstrap_binding']
operation=Path(tempfile.mkdtemp(prefix='ri146-genuine-current-capture-',dir=B));(operation/'environment/tmp').mkdir(parents=True)
environment=dict(m.load(P/'OPERATION_LAYOUT.json')['environment']);environment['TMPDIR']=str(operation/'environment/tmp')
print(m.save('OPERATION_LAYOUT.json',dict(operation=str(operation),environment=environment,selected_interpreter_binding=selected,purpose='One genuine RI141 current capture after fresh source/supplier checks; no operational card yet')))
collector=(P/'observe_bootstrap.py').read_bytes()
assert m.pin(collector)==dict(bytes=4602,sha256='515fd37793cf77e8a7fa18711dae4d1b049d199d9df9bb2ba5003b1e14df43cf')
with (m.D/'observe_bootstrap.py').open('xb') as f:f.write(collector.replace(b'ri144-root-direct-vendor-bootstrap-observation-v1',b'ri146-root-direct-vendor-bootstrap-observation-v1'))
print(dict(operation=str(operation),source_files=len(rows),selected=selected))
