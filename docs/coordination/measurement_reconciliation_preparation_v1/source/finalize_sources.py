"""Administrative text/manifest finalization; no proposal imports or execution."""
from pathlib import Path
import hashlib,json,difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=B/'ri229-reconciliation-preparation-t93t1607/worker_proposal';P=B/'ri224-root-cwd-review-nyvru347/prepare_installation.py'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def canon(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def put(n,b,exclusive=False):
 with (W/n).open('xb' if exclusive else 'wb') as f:f.write(b)
 assert (W/n).read_bytes()==b
s=(W/'prepare_reconciliation.py').read_text();old=P.read_text();put('PREPARATION_DIFF.patch',''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile=str(P),tofile=str(W/'prepare_reconciliation.py'))).encode())
b= json.loads((W/'BUILD_METADATA.json').read_bytes());b['writer']=pin(W/'prepare_reconciliation.py');b['draft_refinements']=pin(W/'DRAFT_REFINEMENTS.json');put('BUILD_METADATA.json',canon(b))
put('SOURCE_PINS.json',canon(dict(schema='ri229-preparation-source-pins-v1',status='SOURCE_ONLY_NOT_ADMISSION',files=[pin(W/n) for n in ['BOOTSTRAP_DIFF.patch','DEPENDENCIES.json','PROTOCOL.md','RECONCILE_BOOTSTRAP.source-only.py','prepare_reconciliation.py']])),True)
print(json.dumps(dict(writer=pin(W/'prepare_reconciliation.py'),bootstrap=pin(W/'RECONCILE_BOOTSTRAP.source-only.py'),manifest=pin(W/'SOURCE_PINS.json'))))
