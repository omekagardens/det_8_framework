"""Administrative text/pin preparation only; never imports or executes proposals."""
from pathlib import Path
import hashlib,json,difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
OLD=B/'ri209-freeze-installation-b3bokxbe/worker_proposal'
W=B/'ri213-freeze-clock-repair-2xc_b29x/worker_proposal'
R=B/'ri214-root-installation-review-xlkw6cbw'
def pin(p):
 p=Path(p);a=p.lstat();b=p.read_bytes();z=p.lstat();assert (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(Path(p).read_bytes())
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def save(n,v):
 with (W/n).open('xb') as f:f.write(canonical(v))
def write(n,v):
 with (W/n).open('x') as f:f.write(v)
assignment=pin(R/'RI213_REPAIR_ASSIGNMENT.json');assert assignment['bytes']==2782 and assignment['sha256']=='4ff18523d648b5b8a6a116db2cf7cd34a5e7ddb9da6e7fd5458af3f842891d9c'
handoff=load(OLD/'HANDOFF.json');assert pin(OLD/'HANDOFF.json')['sha256']=='b507c85ff8d4fbe37093854376c71de5de293dfeea3308c6236a1de48e2260df'
assert set(p.name for p in OLD.iterdir())==set(handoff['namespace'])
for r in handoff['files']:assert pin(r['path'])==r
root=load(R/'RI209_ROOT_SOURCE_DECISION.json');assert pin(R/'RI209_ROOT_SOURCE_DECISION.json')['sha256']=='fcc0dca49359fc883477f7a07885bbb881e4f73da74847babc77f0b68e4b6d85';assert root['status']=='REVISE_SOURCE_ONLY_WITHOUT_EXECUTION'
assert pin(root['independent_review']['path'])==root['independent_review']
refs=[pin(p) for p in sorted(OLD.iterdir())]+[pin(R/'RI213_REPAIR_ASSIGNMENT.json'),pin(R/'RI209_ROOT_SOURCE_DECISION.json'),pin(R/'RI209_NONAUTHOR_REVIEW.json'),root['boundary']]
assert len(refs)==19
for r in refs:assert pin(r['path'])==r
save('REPAIR_PROVENANCE.json',dict(schema='ri213-exact-clock-repair-provenance-v1',status='SOURCE_ONLY_NOT_ADMISSION',assignment=assignment,predecessor_handoff=pin(OLD/'HANDOFF.json'),root_decision=pin(R/'RI209_ROOT_SOURCE_DECISION.json'),independent_review=root['independent_review'],files=sorted(refs,key=lambda r:r['path']),base_input_pins=806,preserved_prior_roles=810,base_input_manifest=pin(OLD/'INPUT_PINS.json'),scope='Only clock handling, explicit timing receipt/checker schema, fresh source/output path provenance and corresponding source dependency declarations change.'))
repair_pin=pin(W/'REPAIR_PROVENANCE.json')
with (W/'INPUT_PINS.json').open('xb') as f:f.write((OLD/'INPUT_PINS.json').read_bytes())
texts={}
for n in ('install_freeze.py','check_installation.py'):
 s=(OLD/n).read_text().replace('ri209-freeze-installation-b3bokxbe','ri213-freeze-clock-repair-2xc_b29x').replace('ri209-freeze-install-operation-b3bokxbe','ri213-freeze-install-operation-2xc_b29x')
 # Old RI209-family admission/source/postcheck schemas remain compatible; the
 # changed completion shape is distinctly versioned RI213 below.
 marker="VENDOR='/Applications/" if n=='install_freeze.py' else "VENDOR='/Applications/"
 pos=s.index(marker)
 s=s[:pos]+'REPAIR='+repr(repair_pin)+'\n'+s[pos:]
 s=s.replace("['INPUT_PINS.json','PROTOCOL.md','check_installation.py','install_freeze.py']","['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py']")
 s=s.replace("inputs=load(INPUT);g=", "inputs=load(INPUT);repair=load(REPAIR);g=")
 s=s.replace("inputs['files']+manifest['files']", "inputs['files']+repair['files']+manifest['files']")
 texts[n]=s
s=texts['install_freeze.py']
old=" OUT.mkdir(mode=0o700);start=time.monotonic();first=None;tails={};produced={};install=None"
new=""" # RI213: all safe receipt/error state and closures exist before ownership.
 start=None;finish=None;elapsed=None;first=None;tails={};produced={};install=None
 timing={name:dict(value=None,error=None) for name in ('initial','final','elapsed')}"""
assert s.count(old)==1;s=s.replace(old,new)
old=" try:\n  same(m.ref(args.admission),a_ref,'admission after ownership')"
new=""" OUT.mkdir(mode=0o700)
 try:
  # The first fallible post-mkdir operation is protected. Invalid readings are
  # represented by an error and null value, never serialized as NaN/Infinity.
  try:
   reading=time.monotonic()
   need(type(reading) in (int,float) and float('-inf')<reading<float('inf'),'initial clock must be finite numeric')
   start=reading;timing['initial']['value']=start
  except BaseException as exc:
   timing['initial']['error']=remember(exc);raise
  same(m.ref(args.admission),a_ref,'admission after ownership')"""
assert s.count(old)==1;s=s.replace(old,new)
old="  elapsed=time.monotonic()-start\n  if elapsed>180:attempt('soft_deadline',lambda:need(False,'installation soft wall exceeded'))"
new="""  # All eight ordinary tails above were attempted before final timing. A
  # clock/subtraction failure cannot bypass the refused COMPLETE attempt or
  # replace an earlier installation/tail failure.
  try:
   reading=time.monotonic()
   need(type(reading) in (int,float) and float('-inf')<reading<float('inf'),'final clock must be finite numeric')
   finish=reading;timing['final']['value']=finish
  except BaseException as exc:timing['final']['error']=remember(exc)
  try:
   need(start is not None and finish is not None,'elapsed unavailable: initial or final clock invalid or missing')
   duration=finish-start
   need(type(duration) in (int,float) and 0<=duration<float('inf'),'elapsed interval must be finite and nonnegative')
   elapsed=duration;timing['elapsed']['value']=elapsed
  except BaseException as exc:timing['elapsed']['error']=remember(exc)
  if elapsed is not None and elapsed>180:attempt('soft_deadline',lambda:need(False,'installation soft wall exceeded'))"""
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("schema='ri209-installation-completion-v1'", "schema='ri213-installation-completion-v1'")
s=s.replace("elapsed_seconds_before_complete_write=elapsed,complete_not_self_hashed=True", "elapsed_seconds_before_complete_write=elapsed,timing=timing,complete_not_self_hashed=True")
texts['install_freeze.py']=s
s=texts['check_installation.py']
s=s.replace('produced_outputs elapsed_seconds_before_complete_write complete_not_self_hashed','produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed')
s=s.replace("'ri209-installation-completion-v1'", "'ri213-installation-completion-v1'")
needle=" names=['ATTEMPT.json','BEFORE.json','FROZEN.json','OBSERVATIONS.json']"
addition=""" timing=c['timing'];fields(timing,'initial final elapsed')
 for name,row in timing.items():
  fields(row,'value error');eq(row['error'],None,'successful '+name+' timing has no error');check(type(row['value']) in (int,float) and float('-inf')<row['value']<float('inf'),'finite numeric '+name+' timing')
 eq(timing['elapsed']['value'],c['elapsed_seconds_before_complete_write'],'entire elapsed binding')
 eq(timing['final']['value']-timing['initial']['value'],timing['elapsed']['value'],'recorded clock arithmetic');check(timing['elapsed']['value']>=0,'nonnegative elapsed')
"""
assert s.count(needle)==1;s=s.replace(needle,addition+needle)
texts['check_installation.py']=s
for n,s in texts.items():write(n,s)
# The previous protocol is carried in full, with explicit fresh path/shape edits
# and the repair appendix. No silent deletion of inherited prerequisites.
p=(OLD/'PROTOCOL.md').read_text().replace('# RI209 — exact accepted freeze installation proposal','# RI213 — narrow clock-path repair of RI209').replace('ri209-freeze-installation-b3bokxbe','ri213-freeze-clock-repair-2xc_b29x').replace('ri209-freeze-install-operation-b3bokxbe','ri213-freeze-install-operation-2xc_b29x')
p=p.replace('ordered four complete FilePins `INPUT_PINS.json`, `PROTOCOL.md`, `check_installation.py`, `install_freeze.py`','ordered five complete FilePins `INPUT_PINS.json`, `PROTOCOL.md`, `REPAIR_PROVENANCE.json`, `check_installation.py`, `install_freeze.py`')
p=p.replace('all 806 input declarations, four source payloads, source manifest','all unchanged 806 input declarations plus the 19 exact repair-provenance pins, five source payloads, source manifest')
p=p.replace('produced_outputs,elapsed_seconds_before_complete_write,complete_not_self_hashed','produced_outputs,elapsed_seconds_before_complete_write,timing,complete_not_self_hashed')
p+='''

## RI213 exact repair and source-version provenance

The root RI209 decision and complete nonauthor review required two clock fixes. The sealed original15-file RI209 packet, its original806-input manifest, all810 prior roles, both author/reviewer diagnostic histories and the accepted RI206 candidate remain unchanged. REPAIR_PROVENANCE.json adds only those15 original packet files and the four exact selecting assignment/decision/review/boundary records. The unchanged806 base declarations are not relabeled as a new or wider runtime inventory. Future source preflight includes the union of those original declarations,19 repair records, five current payloads, current source manifest/root review and actual monitor bootstrap. The full source card still uses RI209-family admission/source schemas; its exact new manifest distinguishes this version. No previous source acceptance transfers to the repaired bytes.

D, W, O, administrative TMPDIR and source references move to the explicit RI213 reservation/operation shown above. E, the candidate, scientific mode directories, all authority/measurement history, direct vendor binding, inherited monitor and all limits stay fixed. Both the old RI209 operation and new RI213 operation remain uncreated by this author. This is source relocation for the repair, not permission to replace an old attempt.

Safe state (`start`, `finish`, `elapsed`, first error, tails, produced pins, installed identity and the complete timing record), plus the error/tail/output closures, now exists **before** the exclusive O mkdir. The first fallible post-mkdir operation is an initial clock call inside the protected body. If it raises or returns an invalid type/NaN/infinity, its error is retained, no valid start or elapsed is invented, and no candidate write begins. The finally block still attempts the eight original named tails; failed E/frozen checks and incomplete ordinary outputs are rejection evidence, not success. A refused COMPLETE is attempted even if ATTEMPT could not be emitted.

After all eight tails, the final clock call and elapsed calculation have separate protected handling. Earlier first errors remain first. A valid final reading is retained even when the initial one is absent. Missing initial/final readings, a subtraction exception, overflow/nonfinite difference or negative difference leave elapsed null and a separate elapsed error; they never produce a made-up zero or successful interval. Finite successful clock values and their nonnegative difference remain subject to the original180-second soft bound. An actual bound exceedance retains the existing additional soft_deadline tail; no bound is widened.

The completion schema is now distinctly `ri213-installation-completion-v1` with the original13 fields plus `timing` (14 total). Timing has exactly `initial,final,elapsed`; each is `{value,error}`. Values are finite numeric or null; errors use the unchanged type/message/secondary shape. On success all three errors are null, elapsed equals final minus initial exactly, and the top-level elapsed field equals timing.elapsed.value. On failure the top-level elapsed is null if unavailable/invalid; otherwise its actual valid duration remains visible even if installation failed. The postchecker requires the new closed schema and independently checks every successful timing field and the arithmetic before accepting its remaining unchanged complete reconstruction. It continues to reject refused outcomes; it is not a failure-to-success normalizer.

The exact clock-domain refusal messages are `RI209: initial clock must be finite numeric`, `RI209: final clock must be finite numeric`, `RI209: elapsed unavailable: initial or final clock invalid or missing`, and `RI209: elapsed interval must be finite and nonnegative`. An exception thrown by the real clock retains its original exception type/message instead. The first existing installation or tail error is preserved if a later clock error occurs. No invalid raw object/NaN/infinity is embedded in canonical JSON.

Manual branch correspondence, **not executed controls**: (1) two valid readings leave original installation/tail/namespace semantics plus explicit timing; (2) initial throw/invalid reading reaches all eight tails and refused COMPLETE with initial+elapsed errors; (3) final throw/invalid reading after healthy work reaches refused COMPLETE with final+elapsed errors; (4) earlier write/tail failure plus final clock failure preserves the earlier first error and both timing errors; (5) finite clocks with negative/overflowed interval retain both clock values, null elapsed and its own error; (6) both clock calls fail, both original clock errors and the missing-elapsed error remain; (7) final COMPLETE serialization/write failure still requires genuine external failure and all retained partial files. No new qualification campaign, fixtures, fault injection or proposed source execution occurred.
'''
write('PROTOCOL.md',p)
diff=''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md'))
write('SOURCE_DIFF.patch',diff)
save('BUILD_METADATA.json',dict(schema='ri213-administrative-repair-build-v1',assignment=assignment,predecessor_namespace=15,predecessor_payloads_verified=14,unchanged_base_input_manifest=pin(W/'INPUT_PINS.json'),repair_provenance=repair_pin,new_source_lines={n:len(s.splitlines()) for n,s in texts.items()},proposal_import_compile_AST_probe_execute=False,scientific_body_decode=False,runtime_observation=False,E_modified=False,admission_created=False))
print(json.dumps(dict(status='SOURCE_TEXT_REPAIR_CREATED_NOT_EXECUTED',repair_provenance=repair_pin,source_lines={n:len(s.splitlines()) for n,s in texts.items()},build=pin(W/'BUILD_METADATA.json'))))
