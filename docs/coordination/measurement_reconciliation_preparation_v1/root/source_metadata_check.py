from pathlib import Path
import importlib.util,hashlib,json,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=Path('/private/tmp/ri230_root_path.txt').read_text();R=Path(R);W=B/'ri229-reconciliation-preparation-t93t1607/worker_proposal';D=B/'ri226-directory-custody-recovery-yvfg_p1b'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=h.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
m.verify(W/'HANDOFF.json',dict(bytes=9292,sha256='7efdb57c59ce7a5f2834bbdb335ff4b2c0afe4e3849e15970fc3aa2c20c321e0'))
hand=m.load(W/'HANDOFF.json');assert sorted(x.name for x in W.iterdir())==hand['namespace'];assert len(hand['files'])==17
rows=m.load(W/'DEPENDENCIES.json')['files']+hand['files']+[m.ref(W/'HANDOFF.json')];known={}
for row in rows:
 if row['path'] in known:assert m.pure(row)==m.pure(known[row['path']])
 known[row['path']]=row
for row in known.values():m.verify(row['path'],row)
repair=m.load(D/'worker_proposal/REPAIR_PROVENANCE.json');old=m.load(repair['roles']['original_before']['path'])
assert len(old['source_observations'])==904
for row in old['source_observations']+list(old['bindings'].values()):assert m.identity(row['path'])==row
post=m.load(B/'ri224-root-cwd-review-nyvru347/POST_FAILURE_CUSTODY.json');assert m.identity(post['installed_partial']['path'])==post['installed_partial']
for row in post['operation_files']+post['monitor_files']:m.verify(row['path'],row)
for name in ['tmp','monitor','ADMIT_RECONCILE.json','DISPATCH.json','RECONCILE_BOOTSTRAP.py','RECONCILE_PREFLIGHT.json']:assert not os.path.lexists(D/name)
assert not os.path.lexists(B/'ri226-freeze-reconciliation-operation-yvfg_p1b')
assert m.snapshot()==m.load(R/'REPO_ENTRY.json')
result=dict(schema='ri230-root-preparation-source-metadata-v1',status='PASS_PINNED_SOURCE_AND_RETAINED_CUSTODY',whole_opaque_paths=len(known),sealed_namespace=18,sealed_payloads=17,dependencies=992,original_source_states_unchanged=904,original_binding_states_unchanged=len(old['bindings']),installed_partial_unchanged=True,old_operation_monitor_unchanged=True,preparation_or_recovery_outputs_absent=True,repository_unchanged=True,subject_or_scientific_execution=False,current_supplier_or_E_inventory_created=False)
with (R/'source_metadata_check.py').open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps(dict(result=result,record=m.save('RI229_ROOT_SOURCE_METADATA.json',result))))
