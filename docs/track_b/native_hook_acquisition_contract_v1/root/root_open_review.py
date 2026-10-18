import hashlib, importlib.util, tempfile
from pathlib import Path
p=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
raw=p.read_bytes(); assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('metadata',p); m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
m.D=Path(tempfile.mkdtemp(prefix='ri245-root-hook-review-',dir=m.B))
entry=m.snapshot();assert entry['head']=='c4545e056d84d3880342a2df7c30cb1836cb3624' and entry['branch']=='ret' and entry['upstream']=='origin/ret' and entry['index']==''
print(m.save('REPO_ENTRY.json',entry))
for src,name,expected in [
('/private/tmp/ri243-independent-review-2d1848.txt','RI243_INDEPENDENT_REVIEW.txt',dict(bytes=11666,sha256='c44d55f63107d1498aaa90914b2e21538b9585eaecbbd70325c7494716215b08')),
('/private/tmp/ri243-genuine-final-tool.json','RI243_GENUINE_FINAL_TOOL.json',None),
('/Volumes/AI_DATA/development/det-review-evidence/ri242-root-canonical-review-vmbd1niz/publication_helpers_v3.py','publication_helpers_v3.py',dict(bytes=4112,sha256='847d2cab4284131059f0b5ca7d9d623e12f48feb54fc6a448f981f3dae9a1be3'))]:
 r=m.ref(src)
 if expected:assert m.pure(r)==expected
 body=Path(src).read_bytes();assert m.pin(body)==m.pure(r)
 with (m.D/name).open('xb') as f:f.write(body)
 assert (m.D/name).read_bytes()==body;print(m.ref(m.D/name))
q=m.B/'ri243-native-hook-acquisition-_9p7ia0h'
hp=dict(bytes=9847,sha256='0bc0006c3536556b57e0629ede95dbfb0cc93acd3376079abb2f6c147ac137ea')
m.verify(q/'HANDOFF.json',hp); h=m.load(q/'HANDOFF.json')
seen={}
def check(r):
 v=m.verify(r['path'],r);assert v['symlink_chain']==[] and v['path']==v['resolved_path']
 if r['path'] in seen:assert seen[r['path']]==v
 seen[r['path']]=v
check(m.ref(q/'HANDOFF.json'))
assert sorted(x.name for x in q.iterdir())==h['namespace']
for r in h['files']:check(r)
s=m.load(q/'SOURCE_REFERENCES.json');a=m.load(q/'AUTHOR_VERIFICATION.json')
assert s['current_scope']==a['current_scope']==h['current_scope']
assert s['diagnostics']==a['diagnostics']==h['diagnostics']
for r in a['payloads']:check(r)
for row in s['direct_sources']:
 assert not row['identity']['path'].endswith(('/CERTIFICATE.json','/check.py'))
 check(row['identity'])
for k in ('assignment','accepted_predecessor','independent_predecessor_review','root_predecessor_review','predecessor_handoff','predecessor_references'):check(s[k])
prior=m.load(s['predecessor_references']['path']);ph=m.load(s['predecessor_handoff']['path'])
assert s['preserved_boundary_keys']==prior['preserved_boundary_keys'] and len(s['preserved_boundary_keys'])==15
assert s['preserved_boundaries']==prior['preserved_boundaries']
assert all(row['identity'] in [x['identity'] for x in s['direct_sources']] for row in prior['direct_sources'])
assert len(prior['direct_sources'])==71
for r in ph['files']:check(r)
assert sorted(x.name for x in Path(s['predecessor_handoff']['path']).parent.iterdir())==sorted(['HANDOFF.json']+[Path(x['path']).name for x in ph['files']])
assert len(s['direct_sources'])==81 and sum(x['identity']['bytes'] for x in s['direct_sources'])==1672090 and len(seen)==87
assert s['proposed_acquisition']==h['proposed_acquisition']
assert s['proposed_acquisition']['source_identity_from_administrative_provenance']==s['preserved_boundaries']['historical_RI231_literal_exception']['body']
for v in list(seen.values()):assert m.identity(v['path'])==v
tool=m.load(m.D/'RI243_GENUINE_FINAL_TOOL.json');assert tool['exitCode']==0 and tool['status']=='completed'
result=dict(schema='ri245-root-ri243-metadata-review-v1',status='PASS_METADATA_ONLY',direct_sources=81,direct_bytes=1672090,whole_identities=len(seen),preserved_predecessor_direct_sources=71,preserved_boundaries=15,identities=list(seen.values()),original_certificate_body_access=False,scientific_arithmetic=False,author_checker_replayed=False,author_final_tool=dict(id=tool['id'],exitCode=tool['exitCode'],status=tool['status'],output=tool['output']),manual_proof_reads=['d9d726','99f02f','99c844'],reviewer_report=m.ref(m.D/'RI243_INDEPENDENT_REVIEW.txt'))
print(m.save('RI243_ROOT_METADATA_REVIEW.json',result));print('ROOT_RESERVATION',m.D)
