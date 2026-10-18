"""Administrative text check. Parses unified patch text, never Python grammar/code."""
from pathlib import Path
import json,re,hashlib,collections
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri129-native-caller-independent-review-Z0SqaY10');S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0');A=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx')
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def apply_text(old,patch):
 lines=patch.splitlines(keepends=True); out=[];oi=0;i=2; hunks=0
 while i<len(lines):
  m=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n',lines[i]);
  if not m: raise ValueError('bad hunk header '+str(i))
  a,n,b,k=int(m[1]),int(m[2] or 1),int(m[3]),int(m[4] or 1);pos=a-1 if n else a
  if pos<oi:raise ValueError('overlap')
  out.extend(old[oi:pos]);oi=pos;i+=1;seenold=seennew=0
  while i<len(lines) and not lines[i].startswith('@@ '):
   line=lines[i];tag=line[0];text=line[1:]
   if tag in ' -':
    if old[oi]!=text:raise ValueError('old hunk mismatch')
    oi+=1;seenold+=1
   if tag in ' +':out.append(text);seennew+=1
   if tag not in ' +-':raise ValueError('unknown patch line')
   i+=1
  if (seenold,seennew)!=(n,k):raise ValueError('hunk counts')
  if len(out)!=b-1+k:raise ValueError('new line index')
  hunks+=1
 out.extend(old[oi:]);return ''.join(out),hunks
checks=[]
for name,patchname in [('supervise.py','SUPERVISE_SOURCE_DELTA.patch'),('launch_audit.py','AUDIT_CALLER_SOURCE_DELTA.patch')]:
 rebuilt,n=apply_text((A/name).read_text().splitlines(keepends=True),(S/patchname).read_text())
 checks.append({'name':name,'patch':pin(S/patchname),'hunks':n,'old_source':pin(A/name),'new_source':pin(S/name),'exact_reconstructed_new_source':rebuilt==(S/name).read_text()})
def span(t,a,b):return t[t.index(a):t.index(b)]
retained=[]
for name,a,oldend,newend in [('supervise.py','def runtime_prepare():','def preparation_ready():','def preparation_ready():'),('supervise.py','def resolve_links(path):','def runtime_canonical_path(value):','def runtime_canonical_path(value):'),('supervise.py','class Attempt:','def run(mode):','def pre_attempt_prerequisites(mode):')]:
 x=span((A/name).read_text(),a,oldend);y=span((S/name).read_text(),a,newend)
 retained.append({'name':name,'start':a,'old_end':oldend,'new_end':newend,'identical':x==y,'bytes':len(y.encode()),'sha256':hashlib.sha256(y.encode()).hexdigest()})
for name,a in [('supervise.py','def run(mode):'),('launch_audit.py','class Attempt:')]:
 x=(A/name).read_text();x=x[x.index(a):];y=(S/name).read_text();y=y[y.index(a):];needline='    pre_attempt_prerequisites(mode)\n';count=y.count(needline); y=y.replace(needline,'',1)
 retained.append({'name':name,'start':a,'end':'EOF','removed_exact_preflight_calls':count,'identical_except_that_call':x==y})
old=json.loads((R/'METADATA_REVIEW.json').read_bytes()); totals=collections.Counter(row['source'] for row in old['administrative_reference_checks'])
result={'schema':'ri129-independent-corrected-text-and-metadata-summary-v1','status':'PASS' if all(x['exact_reconstructed_new_source'] for x in checks) and all(x.get('identical',x.get('identical_except_that_call')) for x in retained) else 'FAIL','original_diagnostic':pin(R/'METADATA_REVIEW.json'),'correction_reason':'Initial regenerated diff comparison depended on hunk selection; exact patch-text application replaces it. Initial native runtime slice ended before its start; corrected same preparation_ready boundary. Initial Attempt slice included new preflight function; corrected boundary. Missing expected_pairs marker replaced by actual runtime_canonical_path marker. No target sources were changed or evaluated.','patches':checks,'retained':retained,'all_299_dependency_identities_match':all(x['matches'] for x in old['dependencies']),'all_13_packet_identity_errors': [e for e in old['errors'] if not e.startswith(('diff:','retained:'))],'administrative_metadata_files':len(totals),'typed_reference_occurrences':len(old['administrative_reference_checks']),'reference_sources':dict(totals),'reference_identity_mismatches':old['reference_identity_mismatches'],'references_outside_closed_map':old['references_outside_closed_map'],'current_runtime_inventory_created':False,'target_activity':False,'scientific_json_decode':False}
with (R/'CORRECTED_METADATA_SUMMARY.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['status','patches','retained','all_299_dependency_identities_match','all_13_packet_identity_errors','administrative_metadata_files','typed_reference_occurrences','reference_identity_mismatches','references_outside_closed_map']},indent=2))
