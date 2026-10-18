"""Root opaque byte/provenance reconciliation; no scientific bodies decoded."""
import hashlib,importlib.util
from pathlib import Path
hp=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(__file__).resolve().parent
s=m.B/'ri172-full-layer-implication-6n1jflgq';p=m.B/'ri168-terminal-row-coupling-f50p8xyj'
hpin=dict(bytes=6736,sha256='552d173833a735c2778c02a3c561e0a9c4c204cb214f4f5db3e3e8910479079d')
ids=[m.verify(s/'HANDOFF.json',hpin)];h=m.load(s/'HANDOFF.json')
print('HANDOFF keys',list(h))
rows=h.get('payloads',h.get('files'));assert isinstance(rows,list)
assert sorted(x.name for x in s.iterdir())==sorted(['HANDOFF.json']+[Path(r['path']).name for r in rows])
for row in rows:ids.append(m.verify(row['path'],row))
d=m.load(s/'SOURCE_DEPENDENCIES.json');old=m.load(p/'SOURCE_DEPENDENCIES.json')
records=d['protected_files'];assert len(records)==276 and len(old['protected_files'])==264
by_path={r['path']:r for r in records};assert len(by_path)==276
for r in old['protected_files']:
 assert {k:v for k,v in r.items() if k!='role'}=={k:v for k,v in by_path[r['path']].items() if k!='role'}
for row in records:ids.append(m.verify(row['path'],row['identity']))
ph=m.load(p/'HANDOFF.json');pr=ph.get('payloads',ph.get('files'))
assert sorted(x.name for x in p.iterdir())==sorted(['HANDOFF.json']+[Path(r['path']).name for r in pr])
assert all(r['path'] in by_path and m.pure(r)==m.pure(by_path[r['path']]['identity']) for r in pr)
assert len(ids)==284 and len({r['path'] for r in ids})==284
print(m.save('RI172_ROOT_METADATA_CHECK.json',dict(schema='ri172-root-opaque-byte-reconciliation-v1',status='PASS',current_packet_files=8,historical_paths=276,historical_bytes=sum(r['identity']['bytes'] for r in records),unchanged_inherited_rows=264,identities=ids,exact_predecessor_namespace=8,scientific_body_decode=False,subject_execution=False,scope='Whole identities and exact inherited rows; author2741 historical/123 current reference traversal is attributed to author, not replayed by this check. Explicit opaque historical-phase boundary preserved. Read-window stability only.')))
