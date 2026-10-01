from pathlib import Path
import importlib.util,hashlib,tempfile,json
p=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');raw=p.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(tempfile.mkdtemp(prefix='ri247-root-hook-branch-review-',dir=m.B));R=m.D
entry=m.snapshot();assert entry['head']=='8a218efec0f7e951fe5ffb0281b86bd4b6e17bc0' and entry['branch']=='ret' and entry['upstream']=='origin/ret' and entry['index']=='';print(m.save('REPO_ENTRY.json',entry))
for src,name in [('/private/tmp/ri246-genuine-author-tools.json','RI246_GENUINE_AUTHOR_TOOLS.json'),(str(m.B/'ri245-root-hook-review-ichvs643/publication_helpers_v3.py'),'publication_helpers_v3.py')]:
 b=Path(src).read_bytes()
 if name.endswith('.py'):assert len(b)==4112 and hashlib.sha256(b).hexdigest()=='847d2cab4284131059f0b5ca7d9d623e12f48feb54fc6a448f981f3dae9a1be3'
 with (R/name).open('xb') as f:f.write(b)
 assert (R/name).read_bytes()==b;print(m.ref(R/name))
Q=m.B/'ri246-native-hook-literals-0_fkiagp';m.verify(Q/'HANDOFF.json',dict(bytes=12317,sha256='a1d7be65df8cf3ef7ecbe11ff129591ca0b85d87708dd530b5274936887e6bca'))
h=m.load(Q/'HANDOFF.json');seen={}
def check(row):
 v=m.verify(row['path'],row);assert v['path']==v['resolved_path'] and not v['symlink_chain']
 if row['path'] in seen:assert seen[row['path']]==v
 seen[row['path']]=v;return v
check(m.ref(Q/'HANDOFF.json'));assert sorted(p.name for p in Q.iterdir())==h['namespace']
for row in h['files']:check(row)
s=m.load(Q/'SOURCE_REFERENCES.json');a=m.load(Q/'AUTHOR_VERIFICATION.json')
for row in a['payloads']:check(row)
assert s['current_scope']==a['current_scope']==h['current_scope'] and s['diagnostics']==a['diagnostics']==h['diagnostics']
assert s['current_literal_exception']==a['current_literal_exception']
for row in s['direct_sources']:check(row['identity'])
for key in ('assignment','accepted_predecessor','independent_predecessor_review','root_predecessor_review','predecessor_handoff','predecessor_references'):check(s[key])
prior=m.load(s['predecessor_references']['path']);ph=m.load(s['predecessor_handoff']['path'])
assert s['preserved_boundaries']==prior['preserved_boundaries'] and s['preserved_boundary_keys']==prior['preserved_boundary_keys'] and len(s['preserved_boundary_keys'])==15
assert len(prior['direct_sources'])==81 and all(x['identity'] in [v['identity'] for v in s['direct_sources']] for x in prior['direct_sources'])
for row in ph['files']:check(row)
assert sorted(p.name for p in Path(s['predecessor_handoff']['path']).parent.iterdir())==ph['namespace']
exception=s['current_literal_exception'];check(exception['authority']);admission=m.load(exception['authority']['path']);assert admission['status']=='ISSUED_BOUNDED_LITERAL_SOURCE_ADMISSION'
assert exception['body']==admission['source']==h['original_source'];check(exception['body'])
assert exception['body']['path'] not in [v['identity']['path'] for v in s['direct_sources']]
assert exception['custody_before']==exception['custody_after'] and exception['scientific_JSON_decoded'] is False and exception['other_coefficient_resolution'] is False
assert len(s['direct_sources'])==91 and sum(x['identity']['bytes'] for x in s['direct_sources'])==1879633 and len(seen)==98
assert s['diagnostics']['failed_shell_commands']==2 and s['diagnostics']['predecessor_diagnostics']==prior['diagnostics']
assert h['actual_d7_excluded'] is True and h['canonical_Cb_resolved'] is False and h['qualification_credit']==0
assert h['actual_full_normalized_witness'] is False and h['actual_signed_inconsistency'] is False and h['successor_assigned'] is False
for v in list(seen.values()):assert m.identity(v['path'])==v
tools=m.load(R/'RI246_GENUINE_AUTHOR_TOOLS.json');assert [x['exitCode'] for x in tools]==[0,1,1,0,0]
assert tools[0]['output']['truncated'] is False and tools[-1]['output']['truncated'] is True
print(m.save('RI246_ROOT_METADATA_CHECK.json',dict(schema='ri247-root-ri246-metadata-review-v1',status='PASS_METADATA_ONLY',direct_sources=91,direct_bytes=1879633,separate_original_scientific_body=exception['body'],whole_identities=98,preserved_predecessor_direct_sources=81,preserved_boundaries=15,identities=list(seen.values()),scientific_JSON_decoded=False,automatic_scientific_arithmetic=False,author_checker_replayed=False,genuine_author_receipts=m.ref(R/'RI246_GENUINE_AUTHOR_TOOLS.json'),root_full_proof_read={'chunk_id':'49abc5','exit_code':0},root_author_diagnostics_read={'clipped':'e90efc','complete_recovery':'8c018b'},original_author_final={'id':tools[-1]['id'],'status':tools[-1]['status'],'exit_code':tools[-1]['exitCode'],'API_truncated':True,'original_chars':tools[-1]['output']['originalChars']},root_literal_verification=m.ref(m.B/'ri245-root-hook-review-ichvs643/RI246_ROOT_LITERAL_PRELIMINARY.json'))))
print('ROOT_RESERVATION',R)
