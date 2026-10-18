"""Root independent RI226 metadata only: no subject imports or operational execution."""
from pathlib import Path
import importlib.util,hashlib,json,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri227-root-profile-review-chshj2qq';W=B/'ri226-directory-custody-recovery-yvfg_p1b/worker_proposal'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=h.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
m.verify(W/'HANDOFF.json',dict(bytes=9657,sha256='bead93928f1f1af37379f4d8add4c5e254b31633fa8d00acb274a2739d237fdc'));a=m.load(W/'HANDOFF.json')
assert sorted(x.name for x in W.iterdir())==sorted(a['namespace'])==sorted([Path(x['path']).name for x in a['files']]+['HANDOFF.json'])
for row in a['files']:m.verify(row['path'],row)
m.verify(W/'SOURCE_PINS.json',a['source_manifest']);manifest=m.load(W/'SOURCE_PINS.json');assert manifest['schema']=='ri226-proposal-source-pins-v1' and manifest['status']=='SOURCE_ONLY_NOT_ADMISSION'
assert [Path(x['path']).name for x in manifest['files']]==['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_reconciliation.py','reconcile_freeze.py']
for row in manifest['files']:m.verify(row['path'],row)
i=m.load(W/'INPUT_PINS.json');r=m.load(W/'REPAIR_PROVENANCE.json');assert len(i['files'])==806 and len(r['files'])==157
union={}
for row in i['files']+r['files']+manifest['files']:
 if row['path'] in union:assert m.pure(row)==m.pure(union[row['path']])
 union[row['path']]=row
assert len(union)==968
for row in union.values():m.verify(row['path'],row)
old=m.load(B/'ri222-freeze-cwd-repair-ypiy2jqw/SOURCES_BEFORE.json');assert len(old)==904 and {x['path'] for x in old}<=set(union)
for row in old:assert m.identity(row['path'])==row
post=m.load(B/'ri224-root-cwd-review-nyvru347/POST_FAILURE_CUSTODY.json');assert m.identity(post['installed_partial']['path'])==post['installed_partial']
for row in post['operation_files']+post['monitor_files']:m.verify(row['path'],row)
for p in [W.parent/'ROOT_SOURCE_REVIEW.json',W.parent/'ADMIT_RECONCILE.json',W.parent/'RECONCILE_BOOTSTRAP.py',W.parent/'RECONCILIATION_POSTCHECK.json',W.parent/'monitor',W.parent/'tmp',B/'ri226-freeze-reconciliation-operation-yvfg_p1b']:
 assert not os.path.lexists(p),str(p)
entry=m.load(R/'REPO_ENTRY.json');assert m.snapshot()==entry
result=dict(schema='ri227-root-ri226-source-metadata-check-v1',status='PASS_SOURCE_IDENTITY_AND_PRESERVATION_ONLY',sealed_namespace=19,sealed_payloads=18,source_manifest=m.ref(W/'SOURCE_PINS.json'),base_files=806,history_files=157,fixed_inputs=963,opaque_union_checked=968,prospective_bindings=971,old_source_states_unchanged=904,installed_partial_full_state_unchanged=True,old_operation_and_monitor_pins_unchanged=True,new_operational_authority_and_outputs_absent=True,repository_unchanged=True,subjects_imported_or_executed=False,scientific_body_decoded=False,qualification_credit=0)
print(json.dumps(dict(result=result,receipt=m.save('RI226_ROOT_SOURCE_METADATA.json',result))))
with (R/'source_metadata_check.py').open('xb') as f:f.write(Path(__file__).read_bytes())
