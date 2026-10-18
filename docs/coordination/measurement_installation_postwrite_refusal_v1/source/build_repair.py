"""RI222 literal source preparation only; no target loading or execution."""
from pathlib import Path
import hashlib,json,difflib,os,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence');OLD=B/'ri218-freeze-byte-repair-x62withm/worker_proposal';W=B/'ri222-freeze-cwd-repair-ypiy2jqw/worker_proposal';R=B/'ri221-root-installation-ru2v15ie'
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
def check(r):q={k:r[k] for k in ('path','bytes','sha256')};assert pin(q['path'])==q;return q
def save(n,v):
 b=canonical(v)
 with (W/n).open('xb') as f:assert f.write(b)==len(b)
def write(n,s):
 b=s.encode()
 with (W/n).open('xb') as f:assert f.write(b)==len(b)
a=pin(R/'RI222_REPAIR_ASSIGNMENT.json');assert a['bytes']==2264 and a['sha256']=='bae3531b2bc3e50f3685beca009610bf7356d36ba7e7ad0cfc3a10f2b5a162b8';assignment=load(a['path']);assert assignment['worker']==str(W)
for key in ('predecessor','supersession','review','genuine_failure','custody'):check(assignment[key])
hand=load(assignment['predecessor']['path']);assert sorted(p.name for p in OLD.iterdir())==sorted(hand['namespace']) and len(hand['files'])==14
for r in hand['files']:check(r)
superv=load(assignment['supersession']['path']);assert superv['status']=='REPAIR_REQUIRED_WRONG_CHILD_CWD_NO_RETRY'
custody=load(assignment['custody']['path']);assert custody['status']=='REFUSED_BEFORE_OUTPUT_OWNERSHIP_E_UNCHANGED' and custody['qualification_credit']==0
oldrepair=load(OLD/'REPAIR_PROVENANCE.json');assert len(oldrepair['files'])==43
root_names=['CALLER_FAILURE_REVIEW.json','FRESH_PREDISPATCH_CHECK.json','GENUINE_INSTALLATION_TOOL.json','GENUINE_POST_HOST_TOOL.json','POST_FAILURE_CUSTODY.json','REPO_ENTRY.json','RI218_OPERATIONAL_SUPERSESSION.json','RI222_REPAIR_ASSIGNMENT.json','ROOT_INSTALLATION_ADMISSION_DECISION.json','postfailure_failed.py','postfailure_v2.py']
failed_names=['ADMIT_INSTALL.json','DISPATCH.json','E_BEFORE.json','HOST_BEFORE.json','HOST_GENUINE_TOOL.json','INSTALLATION_PROPOSAL.json','INSTALL_BOOTSTRAP.py','INSTALL_PREFLIGHT.json','PREPARATION_CUSTODY.json','ROOT_SOURCE_REVIEW.json','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json']
monitor_names=['INSTALL.ATTEMPT.json','INSTALL.COMPLETION.json','INSTALL.stderr','INSTALL.stdout']
assert sorted(p.name for p in (OLD.parent/'monitor').iterdir())==sorted(monitor_names)
review=load(OLD.parent/'ROOT_SOURCE_REVIEW.json');prep=load(OLD.parent/'PREPARATION_CUSTODY.json')
extras=[check(review['independent_review']),check(review['root_metadata']),check(superv['concrete_review']),check(prep['preparation_source']),check(prep['original_genuine_host'])]
groups=dict(inherited43=oldrepair['files'],predecessor15=hand['files']+[assignment['predecessor']],failed_root12=[pin(OLD.parent/n) for n in failed_names],failed_monitor4=[pin(OLD.parent/'monitor'/n) for n in monitor_names],root_adjudication11=[pin(R/n) for n in root_names],support5=extras)
by={}
for rows in groups.values():
 for row in rows:
  r=check(row);assert r['path'] not in by or by[r['path']]==r;by[r['path']]=r
assert len(by)==90
save('REPAIR_PROVENANCE.json',dict(schema='ri222-exact-cwd-repair-provenance-v1',status='SOURCE_ONLY_NOT_ADMISSION',assignment=a,predecessor_handoff=assignment['predecessor'],prior_repair_provenance=pin(OLD/'REPAIR_PROVENANCE.json'),source_acceptance_supersession=assignment['supersession'],actual_installation_failure=assignment['genuine_failure'],root_failure_review=assignment['review'],complete_post_failure_custody=assignment['custody'],groups=groups,files=sorted(by.values(),key=lambda r:r['path']),base_input_pins=806,preserved_prior_roles=810,base_input_manifest=pin(OLD/'INPUT_PINS.json'),repair_rows=90,scope='One cwd predicate matches unchanged monitor cwd=out; only fresh D/W/O and repair pin otherwise change. All bytes, clocks, JSON, limits, tails and checker outer cwd retained.',actual_predecessor_installer_refused=True,actual_new_installer_execution=False,qualification_credit=0))
rp=pin(W/'REPAIR_PROVENANCE.json')
with (W/'INPUT_PINS.json').open('xb') as f:b=(OLD/'INPUT_PINS.json').read_bytes();assert f.write(b)==len(b)
change=("Path.cwd()==D and literal(OUT)==OUT and literal(W)==W","Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W")
for name in ('install_freeze.py','check_installation.py'):
 old=(OLD/name).read_text();s=old.replace('ri218-freeze-byte-repair-x62withm','ri222-freeze-cwd-repair-ypiy2jqw').replace('ri218-freeze-install-operation-x62withm','ri222-freeze-install-operation-ypiy2jqw');line=[x for x in s.splitlines() if x.startswith('REPAIR=')];assert len(line)==1;s=s.replace(line[0],'REPAIR='+repr(rp))
 if name=='install_freeze.py':assert s.count(change[0])==1;s=s.replace(*change)
 write(name,s);projected=s.replace(change[1],change[0]) if name=='install_freeze.py' else s
 projected=projected.replace('REPAIR='+repr(rp),[x for x in old.splitlines() if x.startswith('REPAIR=')][0]).replace('ri222-freeze-cwd-repair-ypiy2jqw','ri218-freeze-byte-repair-x62withm').replace('ri222-freeze-install-operation-ypiy2jqw','ri218-freeze-install-operation-x62withm');assert projected==old
p=(OLD/'PROTOCOL.md').read_text().replace('# RI218 — narrow byte-comparison repair of RI213','# RI222 — exact monitored-child cwd repair of RI218').replace('ri218-freeze-byte-repair-x62withm','ri222-freeze-cwd-repair-ypiy2jqw').replace('ri218-freeze-install-operation-x62withm','ri222-freeze-install-operation-ypiy2jqw')
p=p.replace('the RI204/206/209/213 proposals and the failed RI217 administrative preparation draft.','the RI204/206/209/213/218 proposals and the RI217/219 administrative preparation drafts.')
p=p.replace('changing only two byte comparisons in the installer plus exact paths and repair provenance; the accepted clock-handling changes and corresponding receipt checks are retained:','changing only the installer cwd predicate plus exact paths and repair provenance; the byte comparisons, clock handling and corresponding receipt checks are retained:')
p=p.replace('compares this repair against the exact immutable RI213 source/protocol.','compares this repair against the exact immutable RI218 source/protocol.')
p=p.replace('plus the 43 exact repair-provenance pins','plus the 90 exact repair-provenance pins')
p=p.replace('The tool call has cwd D, login=false,','The outer tool and bootstrap have cwd D. The unchanged monitor starts the installer with `Popen(cwd=out)`, where out is the literal `D/monitor`; the installer must require `Path.cwd()==literal(D/\'monitor\')`. These are distinct working directories, and changing the outer cwd does not override the monitor\'s child cwd. The tool call has cwd D, login=false,')
p=p.replace('## RI218 exact byte repair and current provenance','## Retained RI218 byte repair and historical provenance\n\nThe following section records the predecessor byte repair and its43-row history. Current RI222 paths and90-row provenance are defined above and below; RI218 operative acceptance is superseded by the actual cwd refusal.')
p+='''

## RI222 exact cwd repair and current provenance

The actual RI218 installer invocation685f23 exited1 before ownership. Its unchanged RI141 monitor started the child with `cwd=out`, and the actual bootstrap passed its literal `D218/monitor` output directory. The installer instead required `Path.cwd()==D218`, so its guard refused before source-preflight traversal, ATTEMPT, external O creation or any E write. The saved701-byte stderr, entire monitor attempt/completion/streams, real outer failure, root and nonauthor diagnosis, whole post-failure custody and root's separately corrected metadata audit are retained. The root audit's first10f0e2/session87577→352a4e exit1 was a namespace-list ordering diagnostic; corrected a3a21c/session31556→bdd104 exit0 is administrative evidence, not a second installation. There is no installer retry or success credit.

RI222 changes exactly one functional predicate: `Path.cwd()==D and literal(OUT)==OUT and literal(W)==W` becomes `Path.cwd()==literal(D/'monitor') and literal(OUT)==OUT and literal(W)==W`. This still requires one exact working directory and now explicitly validates its literal nonsymlink path. OUT/W validation, the guard's preownership position and its refusal message are unchanged. The program does not call chdir or accept arbitrary cwd. Every operative path remains absolute except the deliberate fixed destination basename opened relative to the authenticated E directory descriptor.

The correct interface is outer tool cwd D → full captured RI141 monitor → `child_run(command,D/monitor,'INSTALL',180,ENV)` → unchanged `Popen(command,cwd=out,...)` → installer cwd `D/monitor`. The postchecker continues to require outer dispatch/tool cwd D, exact whole command and bootstrap pin, the complete unchanged monitor source, four saved monitor files and all original limits. It need not mislabel the child's cwd as the outer cwd. No new monitor, subprocess wrapper, launch redirection, recorded receipt field or schema is introduced.

The administrative source-contract check binds the entire exact unchanged monitor and the retained actual bootstrap, checks the real `Popen(cwd=out)` statement and literal bootstrap call, derives the same call at the fresh D222 paths as source text only, and checks the corrected exact installer predicate plus the unchanged checker outer-cwd assertion. This establishes static interface agreement. It is not an observed current cwd, a launched bootstrap, a fixture, or a substitute for the later root review of the newly generated concrete bootstrap.

All source paths now use D=`/Volumes/AI_DATA/development/det-review-evidence/ri222-freeze-cwd-repair-ypiy2jqw`, W=D/worker_proposal and O=`/Volumes/AI_DATA/development/det-review-evidence/ri222-freeze-install-operation-ypiy2jqw`. Prior D218 operational records/monitor and D213 failed preparation remain untouched. Fresh preparation, host observations, explicit source review, concrete bootstrap review and separate admission belong to root. No operational object is created in this packet.

The base INPUT_PINS.json remains byte-identical with806 declarations and810 historical role rows. Current REPAIR_PROVENANCE has90 distinct files: all43 prior repair rows, all15 predecessor packet files,12 failed D218 root artifacts, four failed monitor files,11 root failure/custody/adjudication/diagnostic artifacts and five explicit supporting review/preparation/host records. The exact groups are saved, not implied by generic recursive trust. This gives896 distinct base-plus-repair paths. The future closed source observation adds five current payloads, the current source manifest, a new actual root source review and actual bootstrap for904 distinct paths. These are prospective counts, not runtime or operational admission.

Complete literal inverse projection restores the entire RI218 installer by undoing only this predicate, the D/W/O path names and exact REPAIR constant. The whole postchecker restores by reversing only paths/provenance. Direct byte equality, JSON comparator, complete clock and eight-tail blocks, fourteen-field RI213 completion, complete source/copy/card/output reconstruction and every threshold remain unchanged. Old source-only pass records remain historical; root's operative supersession is explicit. The author acknowledges the missed monitor/installer cwd mismatch, also missed in root/nonauthor interface review. No prior or new numerical/scientific qualification is claimed.
'''
write('PROTOCOL.md',p)
write('SOURCE_DIFF.patch',''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md')))
save('SOURCE_PINS.json',dict(schema='ri209-proposal-source-pins-v1',status='SOURCE_ONLY_NOT_ADMISSION',files=[pin(W/n) for n in ('INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py')]))
save('BUILD_METADATA.json',dict(schema='ri222-source-cwd-repair-build-v1',assignment=a,predecessor=assignment['predecessor'],source_supersession=assignment['supersession'],repair_provenance=rp,repair_rows=90,provenance_group_counts={k:len(v) for k,v in groups.items()},base_input=pin(W/'INPUT_PINS.json'),functional_change=change,whole_source_inverse_projection=True,postchecker_only_paths_and_provenance=True,source_execution=False,qualification_credit=0))
print(json.dumps(dict(status='SOURCE_REPAIR_CREATED_NOT_EXECUTED',source_manifest=pin(W/'SOURCE_PINS.json'),repair_provenance=rp,source_lines={n:len((W/n).read_text().splitlines()) for n in ('install_freeze.py','check_installation.py')})))
