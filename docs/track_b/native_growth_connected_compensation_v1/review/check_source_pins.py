"""Opaque RI127 source/premise identities; no scientific decoding or execution."""
import hashlib
import json
from pathlib import Path
E=Path('/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5')
O=Path('/Volumes/AI_DATA/development/det-review-evidence/ri127-independent-proof-review-F2Esp0RB')
def pin(p):
    data=Path(p).read_bytes()
    return {'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
refs=[('assigned handoff',{'path':str(E/'HANDOFF.json'),'bytes':7625,'sha256':'af806b93b3306c7e68fe8584250b709faaea4012f9bd28a2ac8f1fd05446bc80'})]
# Only these three source-provenance inventories are decoded as JSON.
for name in ('HANDOFF.json','SOURCES.json','LOCAL_POSITIVITY_SOURCE_IDENTITIES.json'):
    obj=json.loads((E/name).read_text())
    def visit(value,loc):
        if isinstance(value,dict):
            if all(k in value for k in ('path','bytes','sha256')):
                refs.append((loc,{k:value[k] for k in ('path','bytes','sha256')}))
            for k,v in value.items(): visit(v,loc+'.'+k)
        elif isinstance(value,list):
            for n,v in enumerate(value): visit(v,loc+'['+str(n)+']')
    visit(obj,name)
checks=[]
for role,expected in refs:
    observed=pin(expected['path'])
    checks.append({'role':role,'expected':expected,'observed':observed,'matches':expected==observed})
report={
 'schema':'ri127-independent-opaque-source-pin-check-v1',
 'status':'PASS_OPAQUE_SOURCE_IDENTITIES' if all(c['matches'] for c in checks) else 'FAIL_OPAQUE_SOURCE_IDENTITIES',
 'scope':'Opaque byte-length/SHA-256 checks only. No scientific rational decoding, target/helper activity, mathematical calculation or input acquisition.',
 'declared_reference_occurrences':len(checks),
 'distinct_declared_paths':len({c['expected']['path'] for c in checks}),
 'checks':checks,
 'additional_complete_text_read':pin('/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_four_vertex_cap_check_v1/RESULT_REVIEW.md'),
 'all_match':all(c['matches'] for c in checks),
 'scientific_execution':False,
 'scientific_numerical_decoding':False,
 'repository_or_git_mutation':False
}
with (O/'SOURCE_PIN_CHECK.json').open('x') as f:
    f.write(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':report['status'],'occurrences':len(checks),'distinct_paths':report['distinct_declared_paths'],'report':pin(O/'SOURCE_PIN_CHECK.json')}))
if not report['all_match']: raise SystemExit(1)
