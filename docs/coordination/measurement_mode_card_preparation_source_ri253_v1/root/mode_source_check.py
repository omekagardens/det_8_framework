"""Root source and administrative identities only; never evaluates the proposal."""
from pathlib import Path
import hashlib,importlib.util,difflib,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri253-root-sigma-review-oij6zgup'
Q=Path('/private/tmp/ri249-mode-card-preparation-proposal-y170alnf')
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(sp);exec(compile(raw,str(hp),'exec'),m.__dict__);m.D=R
seen={}
def check(r):
 v=m.verify(r['path'],r)
 if v['path'] in seen:assert v==seen[v['path']]
 seen[v['path']]=v
 return v
hand={'path':str(Q/'HANDOFF.json'),'bytes':8850,'sha256':'ccf34c9baf147994366595cf73be92534733a9b7e3c3810d72c3f227f3a2ab3c'}
check(hand);h=m.load(hand['path']);assert sorted(p.name for p in Q.iterdir())==h['namespace'] and len(h['files'])==16
for r in h['files']:check(r)
author=m.load(Q/'AUTHOR_CHECK.json');assert len(author['identities'])==626
for r in author['identities']:check(r)
refs=m.load(Q/'REFERENCES.json');assert len(refs)==27
for r in refs.values():check(r)
check(h['direct_preparation_predecessor']);old=Path(h['direct_preparation_predecessor']['path']).read_text();new=(Q/'prepare_unissued.py').read_text()
changes=m.load(Q/'SOURCE_CHANGES.json')['changes'];v=old
for c in changes:
 assert v.count(c['before'])==c['occurrences']
 v=v.replace(c['before'],c['after'])
assert v==new
for c in reversed(changes):
 assert v.count(c['after'])==c['occurrences']
 v=v.replace(c['after'],c['before'])
assert v==old
assert ''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=h['direct_preparation_predecessor']['path'],tofile=str(Q/'prepare_unissued.py')))==(Q/'SOURCE_DIFF.patch').read_text()
assert old[old.index('    def input_tail():'):old.index("    completion={'schema'")]==new[new.index('    def input_tail():'):new.index("    completion={'schema'")]
request=m.load(Q/'MODE_CARD_REQUEST.proposal.json');prior=m.load(refs['request']['path'])
assert request==dict(freeze=prior['freeze'],mode='normal',pre=h['actual_pre_result'],normal_acceptance=None)
assert m.canonical(request)==(Q/'MODE_CARD_REQUEST.proposal.json').read_bytes()
recipe=m.load(Q/'ROOT_RECIPES.json');assert not recipe['operational_authorization'] and recipe['outer_alarm_seconds']==960
assert recipe['operation_bounds']==dict(file_bytes=67108864,maximum_sample_gap_seconds=0.1,ps_timeout_seconds=0.05,rss_kib=524288,target_poll_seconds=0.025,wall_seconds=180)
assert recipe['operation_environment']['TMPDIR']==h['prospective_D']+'/tmp'
assert all(not os.path.lexists(h[k]) for k in ('prospective_D','prospective_O'))
for r in list(seen.values()):assert m.identity(r['path'])==r
result=dict(schema='ri253-root-mode-card-preparation-source-check-v1',status='PASS_SOURCE_COMPARISON_ONLY',handoff=hand,whole_identities=len(seen),identities=list(seen.values()),proposal_files=17,author_declared_opaque_files=626,direct_references=27,complete_forward_and_inverse_source=True,complete_source_diff=True,six_tail_block_unchanged=True,request4_bound=True,prospective_D_O_absent=True,manual_reads=['a2ba53','29503a','3e5a0d','dbdfda','58e7db'],proposal_executed=False,scientific_body_decoded=False,fresh_vendor_or_E_inventory=False,operational_authorization=False)
print(m.save('MODE_CARD_ROOT_SOURCE_CHECK.json',result))
