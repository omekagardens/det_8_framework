"""Independent RI199 identity/administrative review, no scientific body decode."""
import hashlib,importlib.util,json,re
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri200-root-sidecars-ofv27lvp';Q=B/'ri199-native-maximum-bound-buxv337k'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
fresh={}
def check(r):
 row=m.verify(r['path'],r);assert row['resolved_path']==r['path'] and row['symlink_chain']==[];old=fresh.get(r['path']);assert old is None or old==row;fresh[r['path']]=row;return row
h=dict(path=str(Q/'HANDOFF.json'),bytes=5411,sha256='6ec9d77cccc140d397c02cc79dde4e5a0572adcb6125075f27aef259f33250ff');check(h);H=m.load(h['path'])
for row in H['payloads']:check(row)
assert sorted(p.name for p in Q.iterdir())==H['namespace']==sorted(['HANDOFF.json']+[Path(x['path']).name for x in H['payloads']])
S=m.load(Q/'SOURCE_REFERENCES.json');A=m.load(Q/'AUTHOR_VERIFICATION.json')
rows=S['direct_sources'];assert len(rows)==26 and len({r['identity']['path'] for r in rows})==26 and sum(r['identity']['bytes'] for r in rows)==1030155
for r in rows:assert r['access'] in ('accepted-analytic-text','administrative-reference','opaque-historical-support');check(r['identity'])
by={r['identity']['path']:r['identity'] for r in rows};refs=[]
for r in [S['assignment'],S['accepted_predecessor'],S['accepted_manual_packet'],S['inherited_manifest_by_reference']['identity'],S['inherited_manifest_by_reference']['acceptance']]:refs.append(r)
for group in S['current_complete_literal_read_groups']:refs.extend(group['sources'])
old=m.load(S['accepted_manual_packet']['path']);P=Path(S['accepted_manual_packet']['path']).parent
assert len(list(P.iterdir()))==8 and sorted(p.name for p in P.iterdir())==sorted(old['namespace'])==sorted(S['predecessor_namespace'])
refs.extend(old['payloads']);refs.extend([H['assignment'],H['accepted_predecessor']])
assert len(refs)==31
for r in refs:assert r==by[r['path']];check(r)
inherited=m.load(S['inherited_manifest_by_reference']['identity']['path']);assert len(inherited['protected_files'])==423
boundaries={k:v for k,v in inherited.items() if k not in ('schema','status','protected_files','scope')}
assert len(boundaries)==15 and boundaries==S['inherited_manifest_by_reference']['boundary_objects']
assert S['inherited_manifest_by_reference']['fresh423_file_or_transitive_typed_reference_recheck_claimed'] is False
assert H['executable_obligations']==A['executable_obligations']==S['executable_obligations']
assert H['manual_analysis_only'] is True and all(H[k] is False for k in ('global_M6_upper_bound_proved','concrete_parent_above_target_proved','actual_W_decided','both_individual_margins_or_H30_proved','new_scientific_body_read','automated_proof_arithmetic_or_subject_execution','qualification_credit','repository_or_Git_written')) and H['ret_paused'] is True
for name in ('MAXIMUM_BOUND.md','HANDOFF.md'):
 text=(Q/name).read_text();assert not re.search(r'[ \t]+$',text,re.M)
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):assert target in H['namespace']
assert len(fresh)==31
for r in fresh.values():assert m.identity(r['path'])==r
print(m.save('RI199_ROOT_METADATA_CHECK.json',dict(schema='ri200-independent-ri199-administrative-check-v1',status='PASS_METADATA_NOT_PROOF_EXECUTION',handoff=h,direct_sources=26,direct_bytes=1030155,current_payloads=5,selected_references=31,predecessor_namespace=8,current_namespace=5,inherited_boundary_objects=15,inherited423_manifest_by_reference=True,fresh423_replay=False,fresh_identities=list(fresh.values()),scientific_body_decoded=False,automatic_proof_arithmetic=False,subject_execution=False)))
