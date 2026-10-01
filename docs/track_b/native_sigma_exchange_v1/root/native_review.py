"""Independent administrative custody; mathematical review is manual."""
from pathlib import Path
import hashlib, importlib.util
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri253-root-sigma-review-oij6zgup'
Q=B/'ri252-native-sigma-exchange-dz_u_bc2'
p=B/'ri122-root-execution-review-6whn_vky/metadata.py'
raw=p.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(sp)
exec(compile(raw,str(p),'exec'),m.__dict__);m.D=R
seen={}
def check(r):
 assert not r['path'].endswith(('/CERTIFICATE.json','/check.py'))
 z=m.verify(r['path'],r)
 assert z['resolved_path']==z['path'] and not z['symlink_chain']
 if z['path'] in seen: assert seen[z['path']]==z
 seen[z['path']]=z
 return z
hand=dict(path=str(Q/'HANDOFF.json'),bytes=18040,sha256='df2a49e18c75ad3746fd6a7c2d941cf8910232b83eca2bc5b082eeafbcd719d7')
check(hand);h=m.load(hand['path'])
assert sorted(p.name for p in Q.iterdir())==h['namespace']
for r in h['files']:check(r)
s=m.load(Q/'SOURCE_REFERENCES.json');a=m.load(Q/'AUTHOR_VERIFICATION.json')
assert len(s['direct_sources'])==123 and len({r['identity']['path'] for r in s['direct_sources']})==123
assert sum(r['identity']['bytes'] for r in s['direct_sources'])==2517253
for r in s['direct_sources']:
 assert r['access'] in ('accepted-analytic-text','administrative-reference','opaque-historical-support')
 check(r['identity'])
assert len(seen)==129
prior=m.load(s['predecessor_references']['path'])
assert len(prior['direct_sources'])==113
for r in prior['direct_sources']:assert any(r['identity']==x['identity'] for x in s['direct_sources'])
assert len(s['preserved_boundary_keys'])==15 and s['preserved_boundary_keys']==prior['preserved_boundary_keys']
for k in s['preserved_boundary_keys']:assert s['preserved_boundaries'][k]==prior['preserved_boundaries'][k]
assert s['preserved_boundaries']['inherited_manifest_by_reference']['selected_paths']==423
assert s['closed_RI250_literal_exception_by_reference']['closed'] and not s['current_literal_reads']
assert h['diagnostics']==s['diagnostics']==a['diagnostics']
for k in ('canonical_Cb_resolved','actual_kappa_gap_resolved','constant_s_proved','actual_full_normalized_witness','actual_signed_inconsistency'):assert h[k] is False
assert h['complete_original_recovery_retained'] and h['accepted_full_system_iff_retained'] and h['inherited_zero_hook_branch_retained']
g=m.load(R/'RI252_GENUINE_FINAL.json')['receipt']
assert g['status']=='completed' and g['exitCode']==0 and g['output']['truncated'] is False
import json
actual=json.loads(g['output']['text'])
assert actual['whole_identities']==129 and actual['direct_sources']==123 and actual['preserved_boundaries']==15
for r in actual['current_identities']:check(r)
for r in list(seen.values()):assert m.identity(r['path'])==r
out=m.save('RI252_ROOT_METADATA_CHECK.json',dict(status='PASS_ADMINISTRATIVE_CUSTODY_ONLY',handoff=hand,whole_identities=129,identities=list(seen.values()),direct_sources=123,direct_bytes=2517253,predecessor_sources=113,preserved_boundaries=15,manifest_sources_by_reference=423,genuine_final=m.ref(R/'RI252_GENUINE_FINAL.json'),manual_complete_proof_reads=['ddbdc2','fbf81d','c21227','e6ea67'],original_literal_authority_closed=True,original_scientific_body_access=False,scientific_execution=False,mathematical_engine=False))
print(out)
