"""Administrative RI218 source-text/opaque-pin comparison only. No subject imports,
compilation, AST parsing, runtime observation, fixture or byte-branch execution."""
from pathlib import Path
import hashlib,json,difflib,os,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=Path('/Volumes/AI_DATA/development/det-review-evidence/ri218-freeze-byte-repair-x62withm/worker_proposal')
OLD=B/'ri213-freeze-clock-repair-2xc_b29x/worker_proposal'
R=B/'ri217-root-native-witness-1yj1_b61'
checks=0
def need(v,msg):
 global checks
 checks+=1
 if not v:raise ValueError(msg)
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(p):return json.loads(Path(p).read_bytes())
def state(a):return [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
def pin(path):
 p=Path(path);before=p.lstat();need(stat.S_ISREG(before.st_mode) and not p.is_symlink(),'regular opaque object');h=hashlib.sha256();n=0
 with p.open('rb') as f:
  need(state(os.fstat(f.fileno()))==state(before),'opened opaque selection')
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk);n+=len(chunk)
  need(state(os.fstat(f.fileno()))==state(before),'closed opaque selection')
 need(state(p.lstat())==state(before) and n==before.st_size,'unchanged whole opaque read')
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def verify(row):
 r={k:row[k] for k in ('path','bytes','sha256')};need(pin(r['path'])==r,'complete declared pin '+r['path']);return r
assignment=load(R/'RI218_BYTE_REPAIR_ASSIGNMENT.json');supersession=load(assignment['source_supersession']['path']);failure=load(supersession['actual_related_failure']['path'])
need(pin(R/'RI218_BYTE_REPAIR_ASSIGNMENT.json')['sha256']=='a72b9d4e51a2b184e4e03270e504ed89be82555271be17b4f26199532c70cf4a','literal assignment')
verify(assignment['predecessor']);verify(assignment['source_supersession']);verify(supersession['actual_related_failure'])
manifest=load(W/'SOURCE_PINS.json');need(set(manifest)=={'schema','status','files'},'closed manifest');need(manifest['schema']=='ri209-proposal-source-pins-v1' and manifest['status']=='SOURCE_ONLY_NOT_ADMISSION','manifest scope')
need([Path(r['path']).name for r in manifest['files']]==['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py'],'five ordered payloads')
for row in manifest['files']:need(Path(row['path']).parent==W,'fixed current source path');verify(row)
old_hand=load(OLD/'HANDOFF.json');need(sorted(x.name for x in OLD.iterdir())==sorted(old_hand['namespace']),'preserved entire old15 namespace')
for row in old_hand['files']:verify(row)
inputs=load(W/'INPUT_PINS.json');repair=load(W/'REPAIR_PROVENANCE.json');old_repair=load(OLD/'REPAIR_PROVENANCE.json')
need((W/'INPUT_PINS.json').read_bytes()==(OLD/'INPUT_PINS.json').read_bytes(),'complete original base bytes unchanged')
need(len(inputs['files'])==806 and inputs['prior_role_count']==810,'original806 and810 roles')
need(len(repair['files'])==43 and len(old_repair['files'])==19,'provenance43 preserves19')
old_map={r['path']:r for r in old_repair['files']};new_map={r['path']:r for r in repair['files']}
for p,r in old_map.items():need(new_map[p]==r,'old repair row retained')
for r in old_hand['files']+[assignment['predecessor']]:need(new_map[r['path']]==r,'all old15 packet pins retained')
base={r['path']:r for r in inputs['files']};expected={}
for row in inputs['files']+repair['files']:
 r={k:row[k] for k in ('path','bytes','sha256')};need(r['path'] not in expected or expected[r['path']]==r,'nonconflicting union');expected[r['path']]=r
need(len(expected)==849,'complete distinct849 opaque declarations')
for p in sorted(expected):verify(expected[p])
for r in [repair['assignment'],repair['source_acceptance_supersession'],repair['actual_preparation_failure']]:need(expected[r['path']]==r,'new selecting exact role')
review=load(supersession['prior_acceptance']['path'])
extra=[repair['assignment'],assignment['source_supersession'],supersession['actual_related_failure'],failure['original_source'],failure['original_host'],failure['genuine_host'],supersession['prior_acceptance'],review['independent_review'],review['root_metadata']]
need(len({r['path'] for r in extra})==9,'exact nine new history rows')
for r in extra:need(new_map[r['path']]=={k:r[k] for k in ('path','bytes','sha256')},'explicit new history pin')
# Preserve old partials as historical failure evidence, never resume them.
need(pin(failure['genuine_host']['path'])=={k:failure['genuine_host'][k] for k in ('path','bytes','sha256')},'partial canonical host pin retained')
need(state(Path(failure['genuine_host']['path']).lstat())==failure['genuine_host']['state'],'old partial host state retained')
for row in failure['empty_control_directories']:
 p=Path(row['path']);need(state(p.lstat())==row['state'] and sorted(x.name for x in p.iterdir())==row['entries'],'old empty control directory retained')
need(sorted(x.name for x in OLD.parent.iterdir())==failure['reservation_namespace'],'old failure namespace unchanged')
rep=repr(pin(W/'REPAIR_PROVENANCE.json'));replacement_pairs=[("same(Path(path).read_bytes(),data,'written exact bytes')","need(Path(path).read_bytes()==data,'written exact bytes')"),("same(DEST.read_bytes(),candidate,'exact accepted byte copy')","need(DEST.read_bytes()==candidate,'exact accepted byte copy')")]
correspondence=[]
for name in ('install_freeze.py','check_installation.py'):
 old=(OLD/name).read_text();new=(W/name).read_text();projected=new
 old_line=[line for line in old.splitlines() if line.startswith('REPAIR=')];new_line=[line for line in new.splitlines() if line.startswith('REPAIR=')]
 need(len(old_line)==len(new_line)==1 and new_line[0]=='REPAIR='+rep,'exact new repair constant')
 if name=='install_freeze.py':
  for before,after in replacement_pairs:need(before not in new and new.count(after)==1,'exact one corrected byte comparison');projected=projected.replace(after,before)
  need('def same(a,b,msg):need(m.canonical(a)==m.canonical(b),msg)' in new,'unchanged JSON comparator')
 projected=projected.replace(new_line[0],old_line[0]).replace('ri218-freeze-byte-repair-x62withm','ri213-freeze-clock-repair-2xc_b29x').replace('ri218-freeze-install-operation-x62withm','ri213-freeze-install-operation-2xc_b29x')
 need(projected==old,'whole executable reverse projection '+name)
 need(len(new.splitlines())==len(old.splitlines()),'no unrelated line insertions')
 correspondence.append(dict(source=name,old=pin(OLD/name),new=pin(W/name),lines=len(new.splitlines()),entire_reverse_projection=True))
old_inst=(OLD/'install_freeze.py').read_text();new_inst=(W/'install_freeze.py').read_text()
for start,end in [(' # RI213: all safe receipt/error state',' OUT.mkdir(mode=0o700)'),('  # All eight ordinary tails above','  save(OUT/\'COMPLETE.json\',completion)'),('  def sources_tail():','  # All eight ordinary tails above')]:
 need(old_inst[old_inst.index(start):old_inst.index(end)]==new_inst[new_inst.index(start):new_inst.index(end)],'entire retained timing/tail span')
need("schema='ri213-installation-completion-v1'" in new_inst,'retained clock schema')
checker=(W/'check_installation.py').read_text();need("fields(timing,'initial final elapsed')" in checker and 'timing[\'final\'][\'value\']-timing[\'initial\'][\'value\']' in checker,'retained independent timing reconstruction')
diff=''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md'))
need((W/'SOURCE_DIFF.patch').read_text()==diff,'complete exact published delta')
future=dict(expected)
for r in manifest['files']+[pin(W/'SOURCE_PINS.json')]:need(r['path'] not in future,'fresh current source path');future[r['path']]=r
for p in (W.parent/'ROOT_SOURCE_REVIEW.json',W.parent/'INSTALL_BOOTSTRAP.py'):need(str(p) not in future,'distinct prospective root path');future[str(p)]=None
need(len(future)==857,'future closed source857 derivation, not observation')
for p in (W.parent/'ADMIT_INSTALL.json',W.parent/'DISPATCH.json',W.parent/'INSTALL_BOOTSTRAP.py',W.parent/'tmp',W.parent/'monitor',Path(assignment['future_operation'])):need(not os.path.lexists(p),'no operational object created')
result=dict(schema='ri218-administrative-source-check-v1',status='PASS_SOURCE_TEXT_AND_OPAQUE_PINS_NOT_EXECUTION',checks=checks,assignment=pin(R/'RI218_BYTE_REPAIR_ASSIGNMENT.json'),source_manifest=pin(W/'SOURCE_PINS.json'),base_inputs=806,repair_rows=43,distinct_opaque_inputs=849,preserved_historical_roles=810,preserved_old_packet_files=15,preserved_old_repair_rows=19,new_history_rows=9,prospective_source_count=857,complete_correspondence=correspondence,complete_clock_and_eight_tail_spans_unchanged=True,JSON_comparator_unchanged=True,exact_two_byte_comparisons_repaired=True,source_execution=False,fixture_execution=False,scientific_decode=False,qualification_credit=0,old_failure_partials_preserved=True,old_actual_preparation_failure=dict(chunk_id='cb9b00',exit_code=1))
b=canonical(result)
with (Path('/Volumes/AI_DATA/development/det-review-evidence/ri219-root-obstruction-review-la4j_k0f/RI218_ROOT_ADMIN_REPLAY_V2.json')).open('xb') as f:need(f.write(b)==len(b),'complete administrative report')
print(json.dumps(dict(report=pin(Path('/Volumes/AI_DATA/development/det-review-evidence/ri219-root-obstruction-review-la4j_k0f/RI218_ROOT_ADMIN_REPLAY_V2.json')),checks=result['checks'],status=result['status'])))
