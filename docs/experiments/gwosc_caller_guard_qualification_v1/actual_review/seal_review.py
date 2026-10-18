"""Reviewer-owned metadata sealing only; no subject imports or execution."""
import hashlib,json,pathlib,stat
R=pathlib.Path('/Volumes/AI_DATA/development/det-review-evidence/ri152-independent-actual65-review-ssaGIKOi')
def pin(p):
 p=pathlib.Path(p); b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(name):return json.loads((R/name).read_text())
def save(name,v):
 with (R/name).open('x') as f: f.write(json.dumps(v,sort_keys=True,indent=2)+'\n')
s=load('SAVED_CHECK.json'); failed=load('FAILED_CHECK_01.json')
assert s['status']=='PASS' and len(s['checks'])==87358 and all(c['passed'] is True for c in s['checks'])
assert len(s['read_inputs'])==1820
assert len({x['path'] for x in s['read_inputs']})==1820
save('READ_INPUT_IDENTITIES.json',{'schema':'ri152-independent-read-input-identities-v1','scope':'Complete actual administrative read-input closure from the successful independent saved-evidence check; includes source, fixture and evidence bytes only, not fresh installed runtime observations.','source':pin(R/'SAVED_CHECK.json'),'files':s['read_inputs']})
save('FAILURE_DIAGNOSTIC.json',{'schema':'ri152-preserved-reviewer-failure-v1','failed_check':pin(R/'FAILED_CHECK_01.json'),'original_checker':pin(R/'review_saved.before-worker-custody-fields-fix.py'),'error':failed['error'],'completed_predicates':len(failed['checks']),'failing_predicates':[x for x in failed['checks'] if x['passed'] is not True],'read_input_count':len(failed['read_inputs']),'repair':'Reviewer expected custody omitted full32_qualified:false and actual_data_admitted:false. Actual source/output were correct. Only reviewer expected object changed; original script/log/full failure retained; no target retry.','commands':pin(R/'ACTUAL_REVIEWER_COMMANDS.json')})
gp=pathlib.Path(s['summary']['guard_report']['path']); g=json.loads(gp.read_text())
save('SOURCE_ORACLE_COVERAGE.json',{'schema':'ri152-complete-source-oracle-coverage-v1','guard_report':pin(gp),'ordered_ids':g['control_order'],'declared_outcomes':65,'group_counts':{'failure_receipt':12,'capture':4,'monitor':10,'runtime':7,'static':8,'acceptance':9,'mode':6,'relation':9},'failure_case_reconstructions':s['failure_case_reconstructions'],'full_oracle_implementation':pin(R/'review_saved.py'),'narrative':pin(R/'INDEPENDENT_ACTUAL_REVIEW.md'),'scope_limit':'Complete saved objects and finite counters/trees are reconstructed. Several exact refusal messages and metadata mutations exist only in executed harness memory; their scope is source-mediated genuine execution evidence, not an independently saved exception trace. Inert fabricated scientific labels have zero scientific qualification credit.','saved_full_outcomes':g['controls'],'full_saved_predicates':pin(R/'SAVED_CHECK.json')})
unchanged=[]
for ref in s['read_inputs']:
 p=pathlib.Path(ref['path'])
 assert '/env/' not in str(p),'fresh installed runtime read forbidden'
 assert str(p).startswith('/Volumes/AI_DATA/development/det-review-evidence/') or str(p).startswith('/Volumes/AI_DATA/development/det_8_framework-ret/')
 assert stat.S_ISREG(p.lstat().st_mode),str(p)
 actual=pin(p)
 assert actual==ref, {'expected':ref,'actual':actual}
 unchanged.append(actual)
save('FINAL_INPUT_CUSTODY.json',{'schema':'ri152-independent-final-input-custody-v1','status':'PASS','checked_regular_files':len(unchanged),'read_input_manifest':pin(R/'READ_INPUT_IDENTITIES.json'),'all_exact_pin_matches':True,'scope':'Fresh opaque bytes rehash of the 1820 previously read source/evidence/fixture regular files only. No installed runtime or vendor recapture; no target execution.','changed':[]})
print(json.dumps({'status':'PASS','checked_inputs':len(unchanged),'new_outputs':[pin(R/n) for n in ['READ_INPUT_IDENTITIES.json','FAILURE_DIAGNOSTIC.json','SOURCE_ORACLE_COVERAGE.json','FINAL_INPUT_CUSTODY.json']]},sort_keys=True))
