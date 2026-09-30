"""Administrative opaque identity and closed namespace check only."""
from pathlib import Path
import hashlib,json
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=Path(__file__).resolve().parent
P=B/'ri158-white-custody-repair-68cdvzn6';V=B/'ri158-independent-repair-review-nxij3eju';R=B/'ri158-root-fixture-review-tupyksou'
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(row):
 actual=pin(Path(row['path']));assert actual==row,(row,actual);return actual
known=[(R/'MEASUREMENT_REPAIR_ASSIGNMENT.json',3860,'1cb89c7279761a3b892d9d8c440d97db3e0b5f5aecb4b43792b2bac19eff64e8'),(R/'RI158_ROOT_ADJUDICATION.json',2058,'d4b636f90564a7eba586de4bbb5f8bbb82f50a63d02c51c1b91f37471c57f7a9'),(P/'HANDOFF.json',12934,'69638eb05897dc2e72c4a29f84d27593dff5e83b98e102c1efccc67f9ded4fa2'),(V/'HANDOFF.json',5894,'02f3ef205a747dfdc096f849c1ff64a58984b10a4c3eb635e292b284a1314619')]
records=[require({'path':str(p),'bytes':n,'sha256':h}) for p,n,h in known]
packets=[]
for directory in (P,V):
 h=json.loads((directory/'HANDOFF.json').read_bytes());payload=h['payloads'];rows=list(payload.values()) if type(payload) is dict else payload
 checked=[require(row) for row in rows]
 assert sorted(p.name for p in directory.iterdir())==sorted(h['namespace'])
 assert sorted(Path(x['path']).name for x in rows)==sorted(n for n in h['namespace'] if n!='HANDOFF.json')
 packets.append({'root':str(directory),'namespace':h['namespace'],'verified_payloads':checked})
result={'known_pins':records,'packets':packets,'subject_execution':False,'runtime_observation':False}
(D/'PREDECESSOR_AUTHENTICATION.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({'authenticated_known':len(records),'packets':[(x['root'],len(x['verified_payloads'])) for x in packets],'source_execution':False}))
