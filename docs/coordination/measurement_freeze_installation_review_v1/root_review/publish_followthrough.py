"""Archive reviewed decisions and current bounded assignments only."""
from pathlib import Path
import hashlib,importlib.util
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri214-root-installation-review-xlkw6cbw';old=B/'ri211-root-global-W-review-xh6eetn1';W=B/'ri209-freeze-installation-b3bokxbe/worker_proposal'
p=B/'ri207-root-four-maxima-review-rrel_hre/publication_helpers.py';b=p.read_bytes()
assert len(b)==3490 and hashlib.sha256(b).hexdigest()=='8b04758d4e19988f67d0d96e86c93a8eb5405704f5b2a3e3d0b401f33afa4277'
with (D/'publication_helpers.py').open('xb') as f:f.write(b)
s=importlib.util.spec_from_file_location('pub',D/'publication_helpers.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);m=h.m
m.save('ACTUAL_ROOT_CHECKS_AND_DISPATCH.json',dict(schema='ri214-root-receipts-v1',corrected_record_construction=dict(initial_chunk='474612',session_id=71277,terminal_chunk='1f6d8a',exit_code=0),failed_record_construction=dict(initial_chunk='97d0c0',session_id=42671,terminal_chunk='6cc5a8',exit_code=1,diagnostic=m.ref(D/'ROOT_ADMIN_DIAGNOSTIC.json')),repair_dispatch=dict(tool='collaboration.followup_task',target='/root/ri116_complete_caller_review',outcome='Delivered successfully; active worker',assignment=m.ref(D/'RI213_REPAIR_ASSIGNMENT.json')),QR_dispatch=dict(tool='mcp__codex_app__send_message_to_thread',threadId='01a074c4-4b09-76a3-8cb2-0caf116f6b9c',outcome='Tool returned matching threadId and isError=false',admission=m.ref(D/'RI212_LITERAL_COMPLEMENT_ADMISSION.json')),operational_admission=False,subject_execution=False))
for source,name in [(Path('/private/tmp/ri214_checkpoint.md'),'CURRENT_FOLLOWTHROUGH.md'),(Path(__file__),'publish_followthrough.py')]:
 with (D/name).open('xb') as f:f.write(source.read_bytes())
names=['RI209_NONAUTHOR_REVIEW.json','RI209_ROOT_SOURCE_DECISION.json','MEASUREMENT_BOUNDARY.json','RI213_REPAIR_ASSIGNMENT.json','RI212_LITERAL_COMPLEMENT_ADMISSION.json','ROOT_ADMIN_DIAGNOSTIC.json','ACTUAL_ROOT_CHECKS_AND_DISPATCH.json','record_followthrough.failed-6cc5a8.py','record_followthrough.py','publish_followthrough.py']
origins=[(D/name,'root_review/'+name) for name in names]
origins.extend([(old/'RI212_LITERAL_SEED_RELATION_ADMISSION.json','native_sources/RI212_LITERAL_SEED_RELATION_ADMISSION.json'),(old/'VERIFIED_REMOTE_CHECKPOINT.json','prior_checkpoint/VERIFIED_REMOTE_CHECKPOINT.json'),(B/'ri122-root-execution-review-6whn_vky/metadata.py','root_review/metadata.py')])
rows=[m.ref(p) for p,_ in origins]+[m.ref(D/'publication_helpers.py'),m.ref(D/'CURRENT_FOLLOWTHROUGH.md'),m.ref(old/'RI212_NATIVE_ASSIGNMENT.json')]
rows.extend(m.ref(p) for p in W.iterdir())
rows.append(m.ref(B/'ri206-root-freeze-5e_n5lj_/FREEZE_CANDIDATE_ACCEPTANCE.json'))
for name in [D/'RI212_LITERAL_COMPLEMENT_ADMISSION.json',old/'RI212_LITERAL_SEED_RELATION_ADMISSION.json']:
 a=m.load(name);rows.append(a['reference'])
 if 'original' in a:rows.append(a['original'])
unique={}
for r in rows:
 if r['path'] in unique:assert m.pure(r)==m.pure(unique[r['path']])
 unique[r['path']]=r
bundle='docs/coordination/measurement_freeze_installation_review_v1'
readme='''# Freeze installation source review and active follow-through

RI209 requires a source repair before operational admission. Independent and root review identified two clock-failure paths that bypass required failure evidence. RI213 is assigned a narrow repair; RI209 remains sealed and no installation has run. Archived records preserve exact findings, attribution, diagnostics and the source-only assignment. The external RI209 proposal is referenced by pin, not accepted or published here as operational code.

RI212 continues the two original individual-margin question after accepted global M6 and strict weighted W. Two additional original analytic texts are admitted literally for manual seed/complement reasoning, without scientific-body or execution authority. Worker proposals remain unaccepted pending independent review. The previous verified remote checkpoint is retained.

PUBLICATION_MANIFEST pins the exact archive. DEPENDENCY_MAP separates archived records, committed equivalents and external source evidence. This is not a complete transitive/runtime archive. Archived administrative scripts describe original provenance; relocated execution is not authorized. All executable qualification remains separate and RET remains paused.
'''
check=h.archive(bundle,origins,list(unique.values()),readme,True)
fronts=['REVIEW_IMPLEMENTATION_PLAN.md','docs/coordination/REVIEW_PROGRESS.md','docs/coordination/QR_HANDOFF.md','docs/coordination/PUBLICATION_BACKLOG.md']
block=(D/'CURRENT_FOLLOWTHROUGH.md').read_text()
for name in fronts:
 p=m.REPO/name;t=p.read_text();a='**Current checkpoint — global maximum bound and strict weighted sign accepted.**'
 assert t.count(a)==1;t=t.replace(a,'**Prior checkpoint — global maximum bound and strict weighted sign accepted.**',1)
 first,rest=t.split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
files=fronts+[p.relative_to(m.REPO).as_posix() for p in sorted((m.REPO/bundle).rglob('*')) if p.is_file()]
dm=m.load(m.REPO/bundle/'DEPENDENCY_MAP.json')
m.save('PUBLICATION_SCOPE_FINAL.json',dict(schema='ri214-publication-scope-v1',parent=h.entry['head'],bundles=[bundle],checks=[check],files=sorted(files),copies=[dict(path=bundle+'/'+r['path'],original=r['original']) for r in dm['copies']],scientific_execution=False,excluded='All unrelated work, sealed RI209 source, active RI212/RI213, protected scientific bodies and paused RET.'))
for src,dst in [('check_final_checkpoint.py','check_final_checkpoint.py'),('check_dependencies.py','check_dependencies.py')]:
 with (D/dst).open('x') as f:f.write((old/src).read_text().replace('ri211-','ri214-'))
print(check)
