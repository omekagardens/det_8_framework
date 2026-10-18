"""Root reconciliation of sealed source/review identities and literal coverage only."""
import importlib.util,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('metadata','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri132-native-caller-qualification-source-0ZmB3R5I';R=m.B/'ri132-native-qualification-independent-review-ye271mv3';A=m.B/'ri129-native-sign-caller-source-8TksBLo0';V=m.B/'ri129-native-caller-independent-review-Z0SqaY10'
m.verify(S/'HANDOFF.json',dict(bytes=9135,sha256='5841f7d783b549b4e8e5a978e1ed3ebceb169412ffc8573ed04ebe52a6d9d53e'))
m.verify(R/'HANDOFF.json',dict(bytes=2150,sha256='575d63c2218d51aea7d489cb86fd49dd970229e17c181c7cdef55174a406932f'))
h=m.load(S/'HANDOFF.json');rh=m.load(R/'HANDOFF.json');sealed=[]
for root,hand,count in [(S,h,11),(R,rh,6)]:
 rows=hand['files'];assert len(rows)==count-1
 for row in rows:sealed.append(m.verify(row['path'],row))
 assert {str(x) for x in root.iterdir()}=={x['path'] for x in rows}|{str(root/'HANDOFF.json')}
ids=m.load(S/'SOURCE_IDENTITIES.json');assert len(ids['files'])==len({r['path'] for r in ids['files']})==40
prior=[m.verify(x['path'],x) for x in ids['files']]
for root,count in [(A,13),(V,9)]:
 expected={x['path'] for x in prior if Path(x['path']).parent==root};assert len(expected)==count and {str(x) for x in root.iterdir()}==expected
for key in ('accepted_predecessor','accepted_source_handoff','accepted_independent_review_handoff'):m.verify(h[key]['path'],h[key])
review=m.load(R/'INDEPENDENT_SOURCE_REVIEW.json');meta=m.load(R/'OPAQUE_SOURCE_REVIEW.json')
assert review['status']==rh['verdict']=='PASS_BOUNDED_UNEXECUTED_QUALIFICATION_SOURCE_ONLY';assert review['blocking_findings']==[] and review['executed_cases']==0 and review['complete_changed_caller_qualification'] is False
assert review['authored_RI132_or_RI129_components'] is False and len(meta['checks'])==378 and all(x['passed'] is True for x in meta['checks'])
def decl(path,key):
 text=path.read_text();block=text.split(key+' = (\n',1)[1].split('\n)',1)[0];rows=[]
 for line in block.splitlines():
  match=re.fullmatch(r"\s*\('([^']*)', '([^']*)', (None|'[^']*'), '([^']*)'\),",line);assert match
  name,function,code,condition=match.groups();rows.append(dict(name=name,function=function,code=None if code=='None' else code[1:-1],condition=condition))
 return block,rows
coverage=[]
for which,filename,total,counts in [('native','supervise.py',52,dict(direct=16,retained=10,whole_entry_specification=1,blocked=25)),('audit','launch_audit.py',69,dict(direct=8,retained=12,whole_entry_specification=1,blocked=48))]:
 old,original=decl(A/filename,'CONTROL_DECLARATIONS');new,rows=decl(S/(which+'_controls.py'),'DECLARATIONS');assert old==new and rows==original and len(rows)==total
 records=[x for x in meta['declaration_coverage'] if x['caller']==which];assert [x['declaration'] for x in records]==rows
 assert {key:sum(x['classification']==key for x in records) for key in counts}==counts and all(x['executed'] is False for x in records)
 # Text catalogue count/order; no evaluation of source or coverage builder.
 cases=re.findall(r"_case\('([^']+)'",(S/(which+'_controls.py')).read_text());assert cases==next(x['case_ids'] for x in ids['literal_text_checks'] if x['caller']==which)
 assert len(cases)==(17 if which=='native' else 16)
 coverage.append(dict(caller=which,declaration_count=total,case_ids=cases,partition=counts,literal_block=m.pin(new.encode())))
def fn(path,name):
 t=path.read_text();start=t.index('def '+name+'(');end=t.find('\ndef ',start+1);return t[start:end if end!=-1 else len(t)].rstrip()
spans=[]
for name in ('runtime_prepare','runtime_file_prerequisites','metadata','validate_freeze','monitor','terminate_owned'):
 old=fn(m.B/'ri122-native-caller-source-jgehvvxx/launch_audit.py',name);new=fn(A/'launch_audit.py',name);assert old==new;spans.append(dict(name=name,**m.pin(new.encode())))
counts=[]
for path,key,count in [(m.B/'ri122-native-caller-source-jgehvvxx/RUNTIME_CLOSURE.json','files',2988),(m.B/'ri122-native-caller-source-jgehvvxx/HISTORY_RECONCILIATION.json','protected_files',699),(A/'SOURCE_DEPENDENCIES.json','protected_files',299)]:
 obj=m.load(path);assert len(obj[key])==count;counts.append(dict(reference=m.ref(path),key=key,count=count))
lines={p.name:len(p.read_bytes().splitlines()) for p in S.glob('*.py')};assert lines==review['complete_source_read'] and sum(lines.values())==1530
for x in prior+sealed:assert m.identity(x['path'])==x
print(m.save('ROOT_REVIEW_RECONCILIATION.json',dict(schema='ri132-root-source-review-reconciliation-v1',status='PASS_SOURCE_IDENTITIES_AND_LITERAL_COVERAGE',source_handoff=m.ref(S/'HANDOFF.json'),independent_review_handoff=m.ref(R/'HANDOFF.json'),sealed_payload_identities=sealed,predecessor_identities=prior,exact_namespaces=dict(RI132=11,review=6,RI129=13,RI129_review=9),coverage=coverage,retained_audit_spans=spans,manifest_counts=counts,source_line_counts=lines,reviewer_predicates=378,current_transitive_runtime_observation=False,target_activity=False,scientific_body_decode=False,qualification=False)))
