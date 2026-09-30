"""Reviewer opaque file/source-text check only; no subject code evaluation."""
from pathlib import Path
import hashlib,json,re,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
S=B/'ri132-native-caller-qualification-source-0ZmB3R5I'
R=B/'ri132-native-qualification-independent-review-ye271mv3'
A=B/'ri129-native-sign-caller-source-8TksBLo0'
V=B/'ri129-native-caller-independent-review-Z0SqaY10'
checks=[]
def need(ok,label):
 checks.append({'check':label,'passed':bool(ok)})
 if not ok:raise ValueError(label)
def pin(path):
 p=Path(path);need(stat.S_ISREG(p.lstat().st_mode),'regular nonsymlink '+str(p));raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def bound(row):
 actual=pin(row['path']);need(actual==row,'exact opaque identity '+row['path']);return actual
hpin=bound({'path':str(S/'HANDOFF.json'),'bytes':9135,'sha256':'5841f7d783b549b4e8e5a978e1ed3ebceb169412ffc8573ed04ebe52a6d9d53e'})
h=json.loads((S/'HANDOFF.json').read_bytes());sealed=[bound(row) for row in h['files']];need(len(sealed)==10,'10 handoff-bound files plus self11')
need({p.name for p in S.iterdir()}=={Path(x['path']).name for x in sealed}|{'HANDOFF.json'},'exact11 sealed namespace')
ids=json.loads((S/'SOURCE_IDENTITIES.json').read_bytes());prior=[bound(row) for row in ids['files']];need(len(prior)==40==len({p['path'] for p in prior}),'40 unique predecessor pins')
for root,count in [(A,13),(V,9)]:
 expected={Path(row['path']).name for row in prior if Path(row['path']).parent==root};actual={p.name for p in root.iterdir()};need(len(expected)==count and expected==actual,'exact predecessor namespace '+str(root))
for key in ('accepted_predecessor','accepted_source_handoff','accepted_independent_review_handoff'):bound(h[key])
def declarations(path,key):
 text=Path(path).read_text();block=text.split(key+' = (\n',1)[1].split('\n)',1)[0];lines=block.splitlines();out=[]
 for line in lines:
  m=re.fullmatch(r"\s*\('([^']*)', '([^']*)', (None|'[^']*'), '([^']*)'\),",line)
  need(m is not None,'literal declaration format '+str(path)+':'+line)
  name,fun,code,condition=m.groups();out.append({'name':name,'function':fun,'code':None if code=='None' else code[1:-1],'condition':condition})
 return block,out
native_direct=['history-zero-byte-log-valid','missing-root-source-card','missing-independent-review','changed-scientific-copy','runtime-file-changed','changed-runtime-bytes','changed-runtime-links','changed-historical-file','changed-source-dependency','transient-current-admission-body','transient-saved-witness-body','wrong-completed-output-reference','supplemental-reference-outside-closure','freeze-input-order','premature-normal','premature-optimized']
audit_direct=['binding-null-identity','binding-zero-size','binding-zero-digest','binding-arbitrary-path','history-zero-log-valid','missing-explicit-auth','metadata-unclosed-reference','runtime-file-changed']
coverage=[]
for which,filename,count,direct in [('native','supervise.py',52,native_direct),('audit','launch_audit.py',69,audit_direct)]:
 old,od=declarations(A/filename,'CONTROL_DECLARATIONS');new,nd=declarations(S/(which+'_controls.py'),'DECLARATIONS');need(old==new,'complete literal declaration block equality '+which);need(len(nd)==count,'declaration count '+which)
 text=(S/(which+'_controls.py')).read_text()
 if which=='native':
  retained_block=text.split('_RETAINED = {',1)[1].split('\n}',1)[0];retained=re.findall(r"^    '([^']+)':",retained_block,re.M)
  blocked_block=text.split('_BLOCKED = {',1)[1].split('\n}',1)[0];blocked=re.findall(r"^    '([^']+)':",blocked_block,re.M)
  whole=['missing-prerequisite-before-attempt']
 else:
  retained_block=text.split('_RETAINED_NAMES = frozenset((',1)[1].split('))',1)[0];retained=re.findall(r"'([^']+)'",retained_block)
  whole=['missing-binding'];blocked=[row['name'] for row in nd if row['name'] not in direct+retained+whole]
 names=[row['name'] for row in nd];need(set(names)==set(direct+retained+whole+blocked) and len(direct+retained+whole+blocked)==count,'complete disjoint classification '+which)
 expected=(16,10,1,25) if which=='native' else (8,12,1,48);need(tuple(map(len,(direct,retained,whole,blocked)))==expected,'classification counts '+which)
 for row in nd:
  classification='direct' if row['name'] in direct else 'retained' if row['name'] in retained else 'whole_entry_specification' if row['name'] in whole else 'blocked'
  coverage.append({'caller':which,'declaration':row,'classification':classification,'executed':False})
 need(re.findall(r"_case\('([^']+)'",text)==next(x['case_ids'] for x in ids['literal_text_checks'] if x['caller']==which),'exact ordered case source labels '+which)
# Verify six claimed audit function text slices without importing/parsing Python.
def function_text(path,name):
 text=Path(path).read_text();start=text.index('def '+name+'(');end=text.find('\ndef ',start+1);return text[start:end if end>=0 else len(text)].rstrip()
retained=[]
for name in ('runtime_prepare','runtime_file_prerequisites','metadata','validate_freeze','monitor','terminate_owned'):
 old=function_text(B/'ri122-native-caller-source-jgehvvxx/launch_audit.py',name);new=function_text(A/'launch_audit.py',name);need(old==new,'retained whole audit function '+name);raw=new.encode();retained.append({'function':name,'bytes_without_trailing_whitespace':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
# Fixed administrative manifest role counts only; never decode referenced scientific bodies.
manifest_counts=[]
for name,path,key,count in [('runtime',B/'ri122-native-caller-source-jgehvvxx/RUNTIME_CLOSURE.json','files',2988),('history',B/'ri122-native-caller-source-jgehvvxx/HISTORY_RECONCILIATION.json','protected_files',699),('dependencies',A/'SOURCE_DEPENDENCIES.json','protected_files',299)]:
 m=json.loads(path.read_bytes());need(len(m[key])==count,'entry verifier fixed administrative count '+name);manifest_counts.append({'name':name,'pin':pin(path),'entries':count})
lines={p.name:len(p.read_bytes().splitlines()) for p in S.glob('*.py')};need(lines=={'audit_controls.py':428,'native_controls.py':416,'entry_evidence.py':416,'qualify_callers.py':270},'complete1530 source lines')
result={'schema':'ri132-independent-opaque-source-review-v1','status':'PASS_OPAQUE_IDENTITIES_AND_LITERAL_TEXT','source_handoff':hpin,'sealed_artifacts':sealed,'predecessors':prior,'namespace_counts':{'RI132':11,'RI129_source':13,'RI129_review':9},'declaration_coverage':coverage,'retained_audit_functions':retained,'administrative_manifest_counts':manifest_counts,'source_line_counts':lines,'prerequisite_dependent_cases_manual_review':{'native':['N05-runtime-file-identity','N06-runtime-link-identity','N07-historical-identity','N08-source-dependency-identity','N12-freeze-role-order'],'audit':['audit-no-argument-argv','audit-target-path-argument','audit-target-symlink-argument','audit-target-oversize-argument']},'checks':checks,'target_import_compile_ast_probe_execute':False,'scientific_body_decode':False,'all_transitive_runtime_files_currently_observed':False,'qualification':False}
(R/'OPAQUE_SOURCE_REVIEW.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'predicates':len(checks),'artifact':pin(R/'OPAQUE_SOURCE_REVIEW.json')},indent=2))
