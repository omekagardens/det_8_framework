"""Issue only the exact relocated-source decision and prospective adapter inputs."""
import hashlib, importlib.util
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri202-root-two-maxima-review-kw07pwnj'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py'
assert hashlib.sha256(h.read_bytes()).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
observed={}
def verify(path,size,digest):
    p=B/path; r=dict(path=str(p),bytes=size,sha256=digest)
    observed[str(p)]=m.verify(p,r)
    return r
graph=verify('ri154-white-mode-preparation-42_uvw15/BINDING_GRAPH.source-only.json',86813,'7be820c27d7a7b5f5b1661a49e5119b7922a1c49f4f24fa2d4567d1f2e5942bf')
independent=verify('ri154-independent-relocation-review-_2275plo/INDEPENDENT_SOURCE_REVIEW.md',17896,'919f2db4f03167e5414a583e3bf7fb01f5c3c335fdefbfb37a7452a536d62bb1')
handoff=verify('ri130-white-qualification-caller-source-Q4Aq7hZg/HANDOFF.json',26684,'1e478b0db8fcda22daedc77bce20c59a1f142b09d61e64d2f4a29a813f1152e8')
original=verify('ri130-root-caller-adjudication-ijhv5s6r/RI130_ROOT_ADJUDICATION.json',2189,'3a9f030a18fdd4ef3cac3bb0204354a6250b2a0ae489e42fbf1be41c5d7fee79')
relocation=verify('ri154-root-relocation-review-3sgyua6i/RI154_ROOT_ADJUDICATION.json',3466,'de2544eff6b904258a8ec0dd106dd86e84debefa1f00b3759d648559a009e1eb')
guard=verify('ri196-root-pair-applicability-review-wurq10uo/GUARD_PATH_APPLICABILITY.json',4414,'222d2822fcf4256d7cd7d9abbec6976dca2221f306c675b35a25f752e0039773')
runtime=verify('ri196-root-pair-applicability-review-wurq10uo/RUNTIME_APPLICABILITY.json',18791,'828ba7dc2b73837d0ecbb47c45f520588d5be9bba0c29911546247a25a8d4a9e')
profiles=verify('ri170-current-e-root-records-proposed-gikj2giy/PROFILES_ACCEPTANCE.json',2208,'d498ccd200b054e8759a37c1cdf0d6014c3e49982e3e944697682266ecf30798')
result=verify('ri156-operation-ri200-sidecars-ofv27lvp/RESULT.json',1274,'6f2df4b476ef336755737fddd771e829441efbfec63facd03d68f91b66198b31')
sidecar_acceptance=verify('ri200-root-sidecars-ofv27lvp/SIDECARS_ADJUDICATION.json',1620,'734d9d46fb84e1f5045fb7e7d0efb37c42dbf1bd539b805786b6c8d72c065bff')
source_acceptance=verify('ri160-root-fixture-adjudication-0rmgmo7y/RI160_ROOT_ADJUDICATION.json',2582,'667e157b07b210952b819f9b9e4907abb4eb3dddb1c7bdcce4d3d6d04ad873b4')
qualification=verify('ri172-root-review-fkjv3v0z/RI162_CONSUMER_QUALIFICATION.json',4041,'0e27e1393c949a24a244ef2e2367ed8c72a10df1d3e3a6057cee8a4d20c9e0d7')
g=m.load(graph['path']); sidecars=m.load(result['path']); ra=m.load(runtime['path'])
assert g['evidence']['ri130_handoff']==handoff and g['evidence']['caller_source_acceptance']==original
assert len(g['helpers'])==11 and len(g['sources'])==30 and len(g['copied_files'])==48
assert ra['helpers']==g['helpers'] and ra['sources']==g['sources'] and ra['root']==g['prospective_root'] and ra['profiles_acceptance']==profiles
assert set(sidecars)=={'runtime_inventory','selection','optional_namespaces','observed_dyld_routes','host_scope'}
for r in sidecars.values(): observed[r['path']]=m.verify(r['path'],r)
for row in g['copied_files']:
    for path in (row['source']['path'],row['destination']): observed[path]=m.verify(path,row['source'])
for row in g['sources']:
    for path in (row['original'],row['copy']): observed[path]=m.verify(path,row['pin'])
for row in g['helpers']: observed[row['path']]=m.verify(row['path'],row['pin'])
root=Path(g['prospective_root']); namespace=[dict(path='.',kind='directory')]
for p in sorted(root.rglob('*')):
    assert not p.is_symlink()
    namespace.append(dict(path=str(p.relative_to(root)),kind='directory' if p.is_dir() else 'file'))
assert sum(x['kind']=='file' for x in namespace)==48
assert sum(x['kind']=='directory' for x in namespace)==9
assert {x['path'] for x in namespace if x['kind']=='file'}=={x['relative'] for x in g['copied_files']}
limits=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=0.025,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05)
decision=dict(schema='ri156-root-relocated-source-decision-v1',status='ACCEPT_EXACT_RELOCATED_WHITE_SOURCE',graph=graph,helpers=g['helpers'],sources=g['sources'],limits=limits,independent_review=independent,target_executed=False)
assert m.pin(m.canonical(decision))==dict(bytes=18097,sha256='d5784bc3971cd29824be4461756135d985bd720233ce940605ab87ac6b70d469')
for path,prior in observed.items(): assert m.identity(path)==prior
decision_ref=m.save('RELOCATED_SOURCE_DECISION.json',decision)
request=dict(root_decisions=dict(source_review=decision_ref,independent_source_review=independent,packet_handoff=handoff,guard_path_review=guard,runtime_applicability=runtime),profiles_acceptance=profiles,sidecars=sidecars)
request_ref=m.save('ADAPTERS_REQUEST.json',request)
print(m.save('MEASUREMENT_INPUT_RECONCILIATION.json',dict(schema='ri202-measurement-input-reconciliation-v1',status='PASS_INPUT_BINDINGS_ONLY',decision=decision_ref,request=request_ref,original_source_acceptance=original,relocation_acceptance=relocation,adapter_source_acceptance=source_acceptance,actual106_qualification=qualification,sidecar_result=result,sidecar_acceptance=sidecar_acceptance,whole_identities=list(observed.values()),namespace=namespace,files=48,directories=9,scientific_body_decode=False,adapter_executed=False,fresh_operational_vendor_host_custody=False)))
print(decision_ref); print(request_ref)
