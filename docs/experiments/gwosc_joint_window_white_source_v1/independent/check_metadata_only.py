"""Opaque pins and source-text comparisons only; no target loading or parsing."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import stat

D=Path(__file__).resolve().parent
B=D.parent
S=B/'ri125-white-source-completion-bg27qfdn'
P=B/'ri125-joint-window-application-source-fsra3wcw'
R=B/'ri125-independent-source-review-mlsKzUKA'
records=[]
def pin(p):
 before=p.lstat();assert stat.S_ISREG(before.st_mode)
 h=hashlib.sha256();count=0
 with p.open('rb') as f:
  while True:
   block=f.read(65536)
   if not block:break
   h.update(block);count+=len(block)
 after=p.lstat()
 assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
 return {'path':str(p),'bytes':count,'sha256':h.hexdigest()}
def check(row):
 found=pin(Path(row['path']));assert all(found[k]==row[k] for k in ('bytes','sha256')),row
 records.append(found)
 return found
for folder in (S,P,R):
 handoff=json.loads((folder/'HANDOFF.json').read_bytes())
 records.append(pin(folder/'HANDOFF.json'))
 for row in handoff['files']:check(row)
for folder in (S,P):
 for row in json.loads((folder/'PREDECESSOR_PINS.json').read_bytes())['records']:check(row)
assert (S/'white_kernel.py').read_bytes()==(P/'white_kernel.py').read_bytes()
# Recreate only a textual unified diff of the eight declared source documents.
# No compiler, AST, evaluator, import, or scientific parser is involved.
names=['white_path.py','white_controls.py','CONTRACT.md','CASES.md','KERNEL_REFUSALS.md','FABRICATED_INTERFACES.md','WHITE_REFUSALS.md','PREPARATION_RECORD.md']
parts=[]
for name in names:
 old=(P/name).read_text().splitlines(keepends=True) if (P/name).exists() else []
 new=(S/name).read_text().splitlines(keepends=True)
 parts.extend(difflib.unified_diff(old,new,fromfile='sealed-predecessor/'+name,tofile='white-successor/'+name))
assert ''.join(parts).encode()==(S/'SOURCE_DIFF.patch').read_bytes()
# Source literals only: reproduce historical gate identifiers without executing
# refusal_actions or any other predecessor or successor function.
historical=Path('/Volumes/AI_DATA/development/det_8_framework-ret/docs/experiments/gwosc_noise_operator_covariance_v1/check.py').read_text()
section=historical.split('def refusal_actions(admitted):',1)[1].split('def fixture_inventory',1)[0]
refusal=[]
for line in section.splitlines():
 m=re.match(r"    case\('([^']+)'",line)
 if m:refusal.append(m.group(1))
 if "for kind in ('coefficient', 'stage_order', 'padding'):" in line:
  refusal.extend('changed_manifest_'+k for k in ('coefficient','stage_order','padding'))
assert len(refusal)==64
fixtures=['fir','cancellation','singleton','offdiagonal_small','offdiagonal_large','failed_gate','midpoint','rank_ambiguity','singular','output_law']
expected=['fixture:'+x for x in fixtures]+['refusal:'+x for x in refusal]+['integration:'+x for x in ('reconstruction','gram','mathematical','accuracy','cross')]+['probe:'+x for x in ('zero','constant','0','1','27','805','1384','2741','2767','2768')]+['integration:law','integration:final_custody','completion:custody']
successor=(S/'white_path.py').read_text()
tuple_text=successor.split('RI73_GATES = (',1)[1].split('\n)',1)[0]
literal=re.findall(r"'([^']+)'",tuple_text)
assert literal==expected and len(literal)==92
control=(S/'white_controls.py').read_text()
ids=re.findall(r"    case\('(W[KCG][0-9]+)'",control)
assert ids==['WK38']+['WC%02d'%i for i in range(1,47)]
assert len(ids)+len(literal)+3==142
# Consult historical custody METAdata only; actual report/capture opaque-hashed above.
reconciliation=json.loads((B/'ri73-execution/root-20260924/FINAL_RECONCILIATION.json').read_bytes())
review=json.loads((B/'ri73-execution/independent-review-20260924T213526Z-1385e996/FINAL_INDEPENDENT_REVIEW.json').read_bytes())
freeze=json.loads((B/'ri73-execution/root-20260924/AUDIT_INPUT_FREEZE.json').read_bytes())
assert reconciliation['report']==review['report'] and reconciliation['snapshot']==review['snapshot']
freeze_pin=pin(B/'ri73-execution/root-20260924/AUDIT_INPUT_FREEZE.json')
assert {k:freeze_pin[k] for k in ('bytes','sha256')}==reconciliation['audit_input_freeze']==review['audit_input_freeze']
# Every hardcoded six input digest/size pair must occur in the authenticated pins.
fixed_text=successor.split('FIXED = {',1)[1].split('\n}',1)[0]
fixed=[]
for role,count,sha in re.findall(r"'([^']+)': \{'bytes': ([0-9]+), 'sha256': '([0-9a-f]{64})'\}",fixed_text):
 assert any(r['bytes']==int(count) and r['sha256']==sha for r in records)
 fixed.append({'role':role,'bytes':int(count),'sha256':sha})
assert len(fixed)==6
out={'schema':'ri125-white-independent-source-metadata-check-v1','status':'SEALED_PINS_AND_COMPLETE_SOURCE_DIFF_AND_LITERAL_INVENTORIES_MATCH','source_handoff':pin(S/'HANDOFF.json'),'verified_role_records':records,'verified_distinct_paths':len({r['path'] for r in records}),'complete_diff_documents':names,'unchanged_kernel':pin(S/'white_kernel.py'),'historical_gate_ids':literal,'literal_WK_WC_ids':ids,'declared_primary_controls':142,'declared_kernel_controls':38,'declared_cases':32,'six_fixed_historical_inputs':fixed,'actual_capture_result_decoded':False,'target_import_compile_AST_probe_or_execution':False,'fixture_generation_or_execution':False,'scientific_arithmetic_performed':False,'source_review_only':True,'full_runtime_or_transitive_custody_reaudit':False}
(D/'SOURCE_PIN_AND_TEXT_CHECK.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':out['status'],'verified_role_records':len(records),'verified_distinct_paths':out['verified_distinct_paths'],'diff_documents':len(names),'historical_gates':len(literal),'declared_primary_controls':142}))
