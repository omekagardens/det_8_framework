"""Source-text and manifest finalization only; no target import or execution."""
from pathlib import Path
import json,hashlib,difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=B/'ri226-directory-custody-recovery-yvfg_p1b/worker_proposal';OW=B/'ri222-freeze-cwd-repair-ypiy2jqw/worker_proposal'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def canon(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def put(n,b,exclusive=False):
 with (W/n).open('xb' if exclusive else 'wb') as f:f.write(b)
 assert (W/n).read_bytes()==b
for old,new,out in [('install_freeze.py','reconcile_freeze.py','RECONCILER_DIFF.patch'),('check_installation.py','check_reconciliation.py','CHECKER_DIFF.patch')]:
 a=(OW/old).read_text();b=(W/new).read_text();put(out,''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=str(OW/old),tofile=str(W/new))).encode())
build=json.loads((W/'BUILD_METADATA.json').read_bytes());build['new_reconciler']=pin(W/'reconcile_freeze.py');build['new_checker']=pin(W/'check_reconciliation.py');build['draft_revisions']=['Added complete old historical E comparison to both programs after text review.','Added entire retained-failure postcheck in the source_inputs tail and its saved observation.'];put('BUILD_METADATA.json',canon(build))
put('SOURCE_PINS.json',canon(dict(schema='ri226-proposal-source-pins-v1',status='SOURCE_ONLY_NOT_ADMISSION',files=[pin(W/n) for n in ['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_reconciliation.py','reconcile_freeze.py']])),True)
print(json.dumps(dict(manifest=pin(W/'SOURCE_PINS.json'),reconciler=pin(W/'reconcile_freeze.py'),checker=pin(W/'check_reconciliation.py'))))
