"""Independent administrative custody; mathematical review is manual."""
from pathlib import Path
import hashlib, importlib.util, json
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri255-root-compensation-review-m__fsupr'
Q=B/'ri254-native-compensation-cover-dxjpomko'
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
 if z['path'] in seen:assert seen[z['path']]==z
 seen[z['path']]=z
 return z
hand=dict(path=str(Q/'HANDOFF.json'),bytes=19285,sha256='5d56bac5238e9d8f1fa82fc912bc2ec1be66811ebb7af6f420504a898be88693')
check(hand);h=m.load(hand['path'])
assert sorted(p.name for p in Q.iterdir())==h['namespace']
for r in h['files']:check(r)
s=m.load(Q/'SOURCE_REFERENCES.json');a=m.load(Q/'AUTHOR_VERIFICATION.json')
assert len(s['direct_sources'])==133 and len({r['identity']['path'] for r in s['direct_sources']})==133
assert sum(r['identity']['bytes'] for r in s['direct_sources'])==2719249
for r in s['direct_sources']:
 assert r['access'] in ('accepted-analytic-text','administrative-reference','opaque-historical-support')
 check(r['identity'])
assert len(seen)==139
prior=m.load(s['predecessor_references']['path'])
assert len(prior['direct_sources'])==123
for r in prior['direct_sources']:assert any(r['identity']==x['identity'] for x in s['direct_sources'])
assert len(s['preserved_boundary_keys'])==15 and s['preserved_boundary_keys']==prior['preserved_boundary_keys']
for k in s['preserved_boundary_keys']:assert s['preserved_boundaries'][k]==prior['preserved_boundaries'][k]
assert s['preserved_boundaries']['inherited_manifest_by_reference']['selected_paths']==423
closed=s['closed_original_literal_exceptions_by_reference']
assert closed['closed'] and closed['all_older_exceptions_remain_closed'] and not closed['new_body_read_or_hash'] and not s['current_literal_reads']
assert h['diagnostics']==s['diagnostics']==a['diagnostics']
for k in ('canonical_Cb_resolved','actual_kappa_gap_resolved','actual_cover_minimum_evaluated','actual_full_normalized_witness','actual_signed_inconsistency'):assert h[k] is False
assert h['complete_original_recovery_retained'] and h['accepted_full_system_iff_retained'] and h['inherited_zero_hook_branch_retained']
ass=m.load(s['assignment']['path']);dec=m.load(s['accepted_predecessor']['path'])
assert ass['reservation']==str(Q) and not ass['new_literal_authority']
assert dec['status']=='ACCEPT_COMPLETE_SIGMA_EXCHANGE_CRITERION_AND_STRICT_TIGHT_MEAN_OBSTRUCTION'
g=m.load(R/'RI254_GENUINE_FINAL.json')['receipt']
assert g['status']=='completed' and g['exitCode']==0 and g['output']['truncated'] is False
actual=json.loads(g['output']['text'])
assert actual['whole_identities']==139 and actual['direct_sources']==133 and actual['preserved_boundaries']==15
for r in actual['current_identities']:check(r)
for r in list(seen.values()):assert m.identity(r['path'])==r
out=m.save('RI254_ROOT_METADATA_CHECK.json',dict(status='PASS_ADMINISTRATIVE_CUSTODY_ONLY',handoff=hand,whole_identities=139,identities=list(seen.values()),direct_sources=133,direct_bytes=2719249,predecessor_sources=123,preserved_boundaries=15,manifest_sources_by_reference=423,genuine_final=m.ref(R/'RI254_GENUINE_FINAL.json'),manual_complete_proof_reads=['777db8 recovered without aggregate clipping','cbecae','883a70 with missing interval recovered by65040b','bab4fe'],original_literal_authority_closed=True,original_scientific_body_access=False,scientific_execution=False,mathematical_engine=False))
print(out)
