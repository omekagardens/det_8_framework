from pathlib import Path
import hashlib,importlib.util,json
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri234-root-reconciliation-tzop5ais';Q=B/'ri233-native-same-root-contrast-sa2lhrgp'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7';s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
checked={}
def verify(row):checked[row['path']]=m.verify(row['path'],row)
verify(dict(path=str(Q/'HANDOFF.json'),bytes=18397,sha256='bcd0a7c893b4e1ebec2f79ac9c92047a88972de0e6800a2a299176c1ef8a7cf6'));packet=m.load(Q/'HANDOFF.json');assert sorted(x.name for x in Q.iterdir())==sorted(['HANDOFF.json']+[Path(r['path']).name for r in packet['payloads']])
for row in packet['payloads']:verify(row)
refs=m.load(Q/'SOURCE_REFERENCES.json');assert len(refs['direct_sources'])==33
for row in refs['direct_sources']:verify(row['identity'])
verify(refs['predecessor_references']);old=m.load(refs['predecessor_references']['path'])
keys=['inherited_manifest_by_reference','inherited_original_six_admissions','inherited_additional_admissions','inherited_RI189_analytic_admission','inherited_shared_affine_admission','inherited_RI223_literal_admissions','inherited_RI225_disconnected_admission','inherited_RI228_construction_admissions','accepted_four_root_witness','predecessor_literal_exception_boundary','inherited_RI216_native_premises_by_reference','predecessor_lower_law_metadata_boundary','historical_diagnostics_preserved','executable_obligations']
for k in keys:assert m.canonical(refs[k])==m.canonical(old[k])
for row in checked.values():assert m.canonical(m.identity(row['path']))==m.canonical(row)
result=m.save('RI233_ROOT_METADATA.json',dict(schema='ri233-root-source-custody-v1',status='PASS_SOURCE_SEAL_AND_DIRECT_IDENTITIES_NOT_PROOF_ACCEPTANCE',identities=list(checked.values()),whole_identities=len(checked),source_namespace=6,direct_sources=33,direct_bytes=sum(r['identity']['bytes'] for r in refs['direct_sources']),unchanged_boundary_fields=keys,complete_proof_reads=['0ca7dd exit0 OFFSET_ELIMINATION complete','e72dfa exit0 ROOT_TRANSPORT complete'],inherited_423_manifest_replayed=False,scientific_body_decoded=False,automatic_proof_arithmetic=False,subject_execution=False,checker=m.ref(Path(__file__).resolve())))
print(json.dumps(dict(record=result,identities=len(checked),direct_bytes=sum(r['identity']['bytes'] for r in refs['direct_sources']))))
