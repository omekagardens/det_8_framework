"""Independent root opaque metadata/text reconciliation. No target execution."""
import importlib.util,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('metadata','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri130-white-qualification-caller-source-Q4Aq7hZg';R=m.B/'ri130-caller-independent-review-GpeTxmLW'
hp={'bytes':26684,'sha256':'1e478b0db8fcda22daedc77bce20c59a1f142b09d61e64d2f4a29a813f1152e8'}
rp={'bytes':2597,'sha256':'4092f5be60516217cebcf9c7a906184895635908977d5501d061d2cc16e36df4'}
m.verify(S/'HANDOFF.json',hp);m.verify(R/'HANDOFF.json',rp)
h=m.load(S/'HANDOFF.json');rh=m.load(R/'HANDOFF.json');sealed=[]
assert len(h['artifacts'])==h['artifact_count']==47 and len(rh['artifacts'])==6
for base,handoff in [(S,h),(R,rh)]:
    for row in handoff['artifacts']:sealed.append(m.verify(row['path'],row))
    declared={str(Path(x['path']).relative_to(base)) for x in handoff['artifacts']}|{'HANDOFF.json'}
    assert {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}==declared
assert rh['source_handoff']==m.ref(S/'HANDOFF.json') and rh['blocking_findings']==[] and rh['verdict']=='PASS_UNEXECUTED_SOURCE_ONLY'
t=m.load(S/'TARGET_CLOSURE.source-only.json');hist=m.load(S/'HISTORY_CLOSURE.source-only.json')
assert t['actual_scientific_inputs']==[] and len(t['sources'])==30
counts={n:sum(x['relative'].startswith('science/'+n+'/') for x in t['sources']) for n in ('primary','validator','qualifier')}
assert counts==t['packet_counts']==dict(primary=13,validator=8,qualifier=9)
pairs=[]
for x in t['sources']:
    a=m.verify(x['original'],x['pin']);b=m.verify(S/x['relative'],x['pin'])
    assert Path(x['original']).read_bytes()==(S/x['relative']).read_bytes()
    pairs.append(dict(original=a,copy=b))
assert len(hist)==len({x['path'] for x in hist})==124
history=[m.verify(x['path'],x) for x in hist]
assert sum(x['bytes'] for x in history)==10625600 and sum(x['bytes']==0 for x in history)==2
for key in ('white_root','integrated_root'):m.verify(t[key]['path'],t[key])
# Administrative root decision, no historical numerical bodies parsed.
integration=m.load(t['integrated_root']['path'])
assert integration['status']=='ACCEPT_BOUNDED_UNEXECUTED_WHITE_VALIDATOR_AND_QUALIFIER_INTEGRATION' and integration['source_execution'] is False and integration['qualification_accepted'] is False
support=[]
for original,name in [(m.B/'ri121-synthetic-caller-repair-7ys8vsc3/control.py','control.py'),(m.B/'ri121-synthetic-caller-repair-7ys8vsc3/runtime_support.py','runtime_support.py'),(m.B/'ri121-root-runtime-qualification-jsf0o3_x/runtime_profile_probe.py','profile_observe.source-only.py')]:
    assert original.read_bytes()==(S/name).read_bytes();support.append(dict(original=m.ref(original),copy=m.ref(S/name)))
old=(m.B/'ri121-synthetic-caller-repair-7ys8vsc3/launch.py').read_bytes();new=(S/'monitor.py').read_bytes()
a=old[old.index(b'def monitor_text('):old.index(b'def admit_command(')].rstrip()+b'\n';b=new[new.index(b'def monitor_text('):new.index(b'def supervise(')].rstrip()+b'\n';assert a==b
oldloop=b''.join(old.splitlines(keepends=True)[335:377]);newloop=b''.join(new.splitlines(keepends=True)[44:86])
assert all(not x.strip() or x.startswith(b'        ') for x in oldloop.splitlines(keepends=True))
assert b''.join(x[8:] if x.strip() else x for x in oldloop.splitlines(keepends=True))==newloop
corr=m.load(S/'BLOCK_CORRESPONDENCE.source-only.json');assert m.pin(oldloop)['sha256']==corr['retained_loop_sha256_before_indentation'] and m.pin(newloop)['sha256']==corr['current_loop_sha256']
oldguard=(m.B/'ri121-synthetic-caller-repair-7ys8vsc3/guard_controls.source-only.py').read_bytes();newguard=(S/'guard_controls.source-only.py').read_bytes()
a=oldguard[oldguard.index(b'def runtime_case('):oldguard.index(b'def main(')].rstrip()+b'\n';b=newguard[newguard.index(b'def runtime_case('):newguard.index(b'def static_case(')].rstrip()+b'\n';assert a==b
# Independently recover literal names with text patterns only, not AST/eval/import.
groups={}
for kind in ('FAILURE','CAPTURE','MONITOR','RUNTIME','STATIC','ACCEPTANCE','MODE','RELATION'):
    line=next(x for x in newguard.decode().splitlines() if x.startswith(kind+'_KINDS='));groups[kind.lower()]=re.findall(r"'([a-z_]+)'",line)
ids=[s+'_'+x for s in ('parent','worker') for x in groups['failure']]+[g+'_'+x for g in ('capture','monitor','runtime','static','acceptance','mode','relation') for x in groups[g]]
assert len(ids)==len(set(ids))==65
contract=(S/'caller_contract.py').read_text();decl=contract[contract.index('GUARD_IDS ='):contract.index('def need(')]
for words in groups.values():
    for word in words:assert "'"+word+"'" in decl
review=m.load(R/'INDEPENDENT_SOURCE_REVIEW.json');meta=m.load(R/'OPAQUE_METADATA_REVIEW.json')
assert ids==meta['prospective_guard_ids'] and len(meta['checks'])==654 and all(x['passed'] is True for x in meta['checks'])
assert review['status']==rh['verdict'] and review['executed_caller_controls']==0 and review['blocking_findings']==[]
assert review['opaque_original_copy_pairs']==30 and review['opaque_history_pins']==124 and review['prospective_caller_controls']==65
coverage=[]
for name,decl in h['source_declaration_locations_not_syntax_validation'].items():
    lines=(S/name).read_text().splitlines();found=[dict(line=i,name=re.match(r'def ([A-Za-z_][A-Za-z0-9_]*)',v).group(1)) for i,v in enumerate(lines,1) if re.match(r'def ([A-Za-z_][A-Za-z0-9_]*)',v)]
    assert len(lines)==decl['lines'] and found==decl['declarations'];coverage.append(dict(name=name,lines=len(lines)))
assert sum(x['lines'] for x in coverage)==1802 and len(coverage)==9
absent=['AUTHORIZED_FREEZE.json','ADMIT_NORMAL.json','ADMIT_OPTIMIZED.json','runs','controls','RUNTIME_INVENTORY.json']
assert all(not (S/x).exists() and not (S/x).is_symlink() for x in absent)
# Repeat full originals/copies/review/source identity checks at finish.
for row in sealed+history+[r[k] for r in pairs for k in ('original','copy')]:assert m.identity(row['path'])==row
print(m.save('ROOT_REVIEW_RECONCILIATION.json',dict(schema='ri130-root-source-reconciliation-v1',status='PASS_SOURCE_AND_REVIEW_IDENTITIES',source_handoff=m.ref(S/'HANDOFF.json'),review_handoff=m.ref(R/'HANDOFF.json'),sealed_artifacts=sealed,target_pairs=pairs,historical_identities=history,support=support,retained_monitor_loop=m.pin(newloop),retained_runtime_case=m.pin(b),source_declarations=coverage,prospective_guard_ids=ids,reviewer_metadata_predicates=654,source_only_absences=absent,scientific_body_decode=False,target_import_compile_ast_probe=False,qualification=False,execution_admitted=False)))
