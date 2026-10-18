"""RI218 administrative literal text/pin builder; no subject loading/execution."""
from pathlib import Path
import hashlib,json,difflib,os,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
OLD=B/'ri213-freeze-clock-repair-2xc_b29x/worker_proposal'
W=B/'ri218-freeze-byte-repair-x62withm/worker_proposal'
R=B/'ri217-root-native-witness-1yj1_b61'
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def state(a):return [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
def pin(p):
 p=Path(p);a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();h=hashlib.sha256();n=0
 with p.open('rb') as f:
  assert state(os.fstat(f.fileno()))==state(a)
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  assert state(os.fstat(f.fileno()))==state(a)
 assert state(p.lstat())==state(a) and n==a.st_size
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def load(p):return json.loads(Path(p).read_bytes())
def check(r):assert pin(r['path'])=={k:r[k] for k in ('path','bytes','sha256')};return {k:r[k] for k in ('path','bytes','sha256')}
def save(n,v):
 b=canonical(v)
 with (W/n).open('xb') as f:assert f.write(b)==len(b)
def write(n,s):
 b=s.encode()
 with (W/n).open('xb') as f:assert f.write(b)==len(b)
a=pin(R/'RI218_BYTE_REPAIR_ASSIGNMENT.json');assert a['bytes']==2827 and a['sha256']=='a72b9d4e51a2b184e4e03270e504ed89be82555271be17b4f26199532c70cf4a'
assignment=load(a['path']);assert assignment['worker_reservation']==str(W)
handoff_ref=check(assignment['predecessor']);handoff=load(handoff_ref['path'])
assert sorted(p.name for p in OLD.iterdir())==sorted(handoff['namespace']) and len(handoff['files'])==14
for row in handoff['files']:check(row)
super_ref=check(assignment['source_supersession']);supersession=load(super_ref['path'])
assert supersession['status']=='RI213_REQUIRES_BYTE_COMPARISON_REPAIR_NO_OPERATIONAL_ADMISSION'
failure_ref=check(supersession['actual_related_failure']);failure=load(failure_ref['path'])
assert failure['actual_tool']==dict(chunk_id='cb9b00',exit_code=1) and failure['subject_execution'] is False
old_provenance=load(OLD/'REPAIR_PROVENANCE.json');assert len(old_provenance['files'])==19
prior_review_ref=check(supersession['prior_acceptance']);prior_review=load(prior_review_ref['path'])
refs=old_provenance['files']+handoff['files']+[handoff_ref,a,super_ref,failure_ref,check(failure['original_source']),check(failure['original_host']),check(failure['genuine_host']),prior_review_ref,check(prior_review['independent_review']),check(prior_review['root_metadata'])]
by={}
for r in refs:
 r=check(r);prior=by.get(r['path']);assert prior is None or prior==r;by[r['path']]=r
assert len(by)==43
save('REPAIR_PROVENANCE.json',dict(schema='ri218-exact-byte-repair-provenance-v1',status='SOURCE_ONLY_NOT_ADMISSION',assignment=a,predecessor_handoff=handoff_ref,prior_repair_provenance=pin(OLD/'REPAIR_PROVENANCE.json'),prior_source_acceptance=prior_review_ref,source_acceptance_supersession=super_ref,actual_preparation_failure=failure_ref,files=sorted(by.values(),key=lambda r:r['path']),base_input_pins=806,preserved_prior_roles=810,base_input_manifest=pin(OLD/'INPUT_PINS.json'),preserved_prior_repair_rows=19,predecessor_packet_files=15,new_history_rows=9,scope='Only two byte-valued comparisons use direct equality; exact D/W/O and repair-provenance identities move. RI213 clocks, JSON comparison and all other custody/monitor/resource semantics stay unchanged.',actual_preparation_failed=True,actual_installer_execution=False,qualification_credit=0))
new_repair=pin(W/'REPAIR_PROVENANCE.json')
with (W/'INPUT_PINS.json').open('xb') as f:b=(OLD/'INPUT_PINS.json').read_bytes();assert f.write(b)==len(b)
changes=[("same(Path(path).read_bytes(),data,'written exact bytes')","need(Path(path).read_bytes()==data,'written exact bytes')"),("same(DEST.read_bytes(),candidate,'exact accepted byte copy')","need(DEST.read_bytes()==candidate,'exact accepted byte copy')")]
for name in ('install_freeze.py','check_installation.py'):
 old=(OLD/name).read_text();s=old.replace('ri213-freeze-clock-repair-2xc_b29x','ri218-freeze-byte-repair-x62withm').replace('ri213-freeze-install-operation-2xc_b29x','ri218-freeze-install-operation-x62withm')
 repair_line=[line for line in s.splitlines() if line.startswith('REPAIR=')];assert len(repair_line)==1
 s=s.replace(repair_line[0],'REPAIR='+repr(new_repair))
 if name=='install_freeze.py':
  for before,after in changes:assert s.count(before)==1;s=s.replace(before,after)
 write(name,s)
 projected=s
 if name=='install_freeze.py':
  for before,after in changes:assert projected.count(after)==1;projected=projected.replace(after,before)
 projected=projected.replace('REPAIR='+repr(new_repair),[line for line in old.splitlines() if line.startswith('REPAIR=')][0])
 projected=projected.replace('ri218-freeze-byte-repair-x62withm','ri213-freeze-clock-repair-2xc_b29x').replace('ri218-freeze-install-operation-x62withm','ri213-freeze-install-operation-2xc_b29x')
 assert projected==old
p=(OLD/'PROTOCOL.md').read_text()
p=p.replace('# RI213 — narrow clock-path repair of RI209','# RI218 — narrow byte-comparison repair of RI213')
p=p.replace('ri213-freeze-clock-repair-2xc_b29x','ri218-freeze-byte-repair-x62withm').replace('ri213-freeze-install-operation-2xc_b29x','ri218-freeze-install-operation-x62withm')
p=p.replace('The author previously wrote RI156/158/160 and the RI204/206/209 proposals.','The author previously wrote RI156/158/160 and the RI204/206/209/213 proposals and the failed RI217 administrative preparation draft.')
p=p.replace('This repair carries two administrative programs, changing only the clock handling, corresponding receipt checks and declared repair provenance:','This repair carries two administrative programs, changing only two byte comparisons in the installer plus exact paths and repair provenance; the accepted clock-handling changes and corresponding receipt checks are retained:')
p=p.replace('`SOURCE_DIFF.patch` compares this repair against the exact immutable RI209 source/protocol. RI209\'s original additions-only diff remains pinned in REPAIR_PROVENANCE; no predecessor file is patched.','`SOURCE_DIFF.patch` compares this repair against the exact immutable RI213 source/protocol. All RI209 and RI213 source, review and administrative diagnostic history remains pinned in REPAIR_PROVENANCE; no predecessor file is patched.')
p=p.replace('plus the 19 exact repair-provenance pins','plus the 43 exact repair-provenance pins')
p=p.replace('## RI213 exact repair and source-version provenance','## Retained RI213 clock semantics and historical provenance\n\nThe following section records the prior RI213 change. Its 19-row source-version description is historical; the current RI218 paths and 43-row explicit union are specified above and in the RI218 section below. No prior acceptance authorizes these new bytes.')
p+='''

## RI218 exact byte repair and current provenance

The actual root preparation attempt cb9b00 exited1 before admission or installation. Its `emit` routine successfully wrote a complete canonical HOST_GENUINE_TOOL.json and then passed the raw readback bytes to a JSON-canonicalizing comparator. The TypeError and exact retained source/host/partial/control-directory records remain pinned; neither that failed preparation nor any installer was retried by this author. The original root preparation and partials are not modified or resumed. A later, separately reviewed root preparation must correct its own raw-byte readback using direct equality and preserve its original failure evidence.

The corresponding RI213 installer source had the same type mismatch at two distinct byte comparisons. The first was the generic output write's independent reread: JSON serialization of raw bytes would fail after the exclusive write/fsync/close, beginning with ATTEMPT and also affecting COMPLETE. The second was the independent installed-candidate byte comparison. These are source-path findings, not observed installer executions. RI213's operative source acceptance is explicitly superseded by the pinned root record; its old approval remains historical evidence. Both root and nonauthor review had missed this error. The author accepts responsibility for the defective comparisons and claims no execution or qualification credit for diagnosing them.

RI218 replaces exactly `same(Path(path).read_bytes(),data,'written exact bytes')` with `need(Path(path).read_bytes()==data,'written exact bytes')`, and exactly `same(DEST.read_bytes(),candidate,'exact accepted byte copy')` with `need(DEST.read_bytes()==candidate,'exact accepted byte copy')`. Both operands are bytes from a bounded byte producer and complete readback. Direct equality compares every byte; it does not decode, coerce, truncate or weaken the existing pin, length, identity, single-link, exclusive-write, fsync, close, namespace or eight-tail requirements. The JSON comparator is completely unchanged and remains type-sensitive through canonical JSON. No broad polymorphic comparator or new encoding rule is introduced.

D is now `/Volumes/AI_DATA/development/det-review-evidence/ri218-freeze-byte-repair-x62withm`, W is its `worker_proposal`, and O is `/Volumes/AI_DATA/development/det-review-evidence/ri218-freeze-install-operation-x62withm`. The new root must freshly review and bind this exact manifest before preparing any admission. No old operational directory or partial file may be reused. The E tree, exact accepted candidate, supplier identity, complete ten-field environment apart from D/tmp, RI141 monitor and every bound are unchanged. Neither D/tmp, D/monitor, bootstrap, admission nor O is created in this source packet.

INPUT_PINS.json stays byte-identical to the original806 declarations, including all810 historical role rows. The explicit43-row repair union retains all19 RI213 provenance rows, all15 sealed RI213 packet files, and nine additional exact records: RI218 assignment, RI213 supersession, actual preparation failure, preserved failed root preparation source, original actual host transcript, complete partial canonical host transcript, prior RI213 source acceptance, its independent review and its root metadata check. Directory states and absent-path observations in the failure record remain historical observations; they are not falsely presented as newly executed qualification.

The future closed source observation is the sorted union of806 base declarations,43 repair declarations, five current payloads, current source manifest, new actual source review and actual monitor bootstrap. At these distinct literal paths that is857 files. All previous source, history and selected-copy roles remain present. The source manifest and admission schemas retain their RI209-family compatibility strings; `ri213-installation-completion-v1`, its14 fields and exact timing checks are unchanged. Reversing the two comparison substitutions, the D/W/O path changes and the complete REPAIR constant yields the entire original installer byte for byte. Reversing only paths and REPAIR yields the entire original postchecker. There are no other executable edits.

Only administrative source/pin/diff checks are performed for this packet. Neither byte-comparison branch is executed as a fixture, and no subject is imported, compiled, parsed as an AST or probed. Fresh nonauthor/root source review precedes fresh concrete root preparation; actual supplier/host/custody checks and real monitored installation remain separate. All normal-before-optimized, independent saved arithmetic, RI131/full32 and conventional public-data prerequisites remain unchanged.
'''
write('PROTOCOL.md',p)
write('SOURCE_DIFF.patch',''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md')))
save('SOURCE_PINS.json',dict(schema='ri209-proposal-source-pins-v1',status='SOURCE_ONLY_NOT_ADMISSION',files=[pin(W/n) for n in ('INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py')]))
save('BUILD_METADATA.json',dict(schema='ri218-byte-repair-build-v1',assignment=a,predecessor_handoff=handoff_ref,source_supersession=super_ref,repair_provenance=new_repair,prior_provenance_rows=19,preserved_RI213_packet=15,added_history_rows=9,repair_rows=43,base_input=pin(W/'INPUT_PINS.json'),exact_changed_byte_comparisons=changes,whole_source_reverse_projection=True,checker_changes_only_paths_and_provenance=True,clock_completion_schema_unchanged='ri213-installation-completion-v1',source_execution=False,qualification_credit=0))
print(json.dumps(dict(status='SOURCE_REPAIR_CREATED_NOT_EXECUTED',source_manifest=pin(W/'SOURCE_PINS.json'),repair_provenance=new_repair,repair_rows=43,source_lines={n:len((W/n).read_text().splitlines()) for n in ('install_freeze.py','check_installation.py')})))
