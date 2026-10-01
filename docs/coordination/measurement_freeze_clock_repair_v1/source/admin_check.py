"""Administrative opaque-pin and complete literal correspondence check only.
No source imports, compile, AST parsing, probes, clocks, fixtures or proposals.
"""
from pathlib import Path
import hashlib,json,stat,difflib,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
OLD=B/'ri209-freeze-installation-b3bokxbe/worker_proposal';W=B/'ri213-freeze-clock-repair-2xc_b29x/worker_proposal'
checks=0

def need(ok,msg):
 global checks
 checks+=1
 if not ok:raise ValueError(msg)
def pin(path):
 p=Path(path);a=p.lstat();need(stat.S_ISREG(a.st_mode) and not p.is_symlink(),'regular no-link opaque input');digest=hashlib.sha256();n=0
 with p.open('rb') as f:
  for data in iter(lambda:f.read(65536),b''):n+=len(data);digest.update(data)
 z=p.lstat();need((a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'stable opaque hash');return dict(path=str(p),bytes=n,sha256=digest.hexdigest())
def load(p):return json.loads(Path(p).read_bytes())
def save(n,v):
 with (W/n).open('x') as f:json.dump(v,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
oldseal=load(OLD/'HANDOFF.json');need(set(p.name for p in OLD.iterdir())==set(oldseal['namespace']),'whole RI209 namespace preserved')
for row in oldseal['files']:need(pin(row['path'])==row,'original RI209 payload unchanged')
base=load(W/'INPUT_PINS.json');need((W/'INPUT_PINS.json').read_bytes()==(OLD/'INPUT_PINS.json').read_bytes(),'complete original806 and810 declarations unchanged')
repair=load(W/'REPAIR_PROVENANCE.json');need(len(base['files'])==806 and len(base['prior_role_rows'])==810 and len(repair['files'])==19,'exact base/provenance counts')
refs={r['path']:r for r in base['files']+repair['files']};need(len(refs)==825,'complete distinct opaque closure')
for row in refs.values():need(pin(row['path'])==row,'entire retained FilePin '+row['path'])
for row in base['prior_role_rows']:need({k:row[k] for k in ('path','bytes','sha256')}==refs[row['path']],'preserved historical role')
for row in base['roles'].values():need(row==refs[row['path']],'preserved named role')
g=load(base['roles']['graph']['path']);need((len(g['copied_files']),len(g['history_originals']),len(g['sources']))==(48,124,30),'unchanged graph dimensions')
for row in g['copied_files']:
 need(refs[row['source']['path']]==row['source'],'original copy declaration');need({k:refs[row['destination']][k] for k in ('bytes','sha256')}=={k:row['source'][k] for k in ('bytes','sha256')},'relocated copy pin')
for row in g['history_originals']:need(refs[row['path']]==row,'all history pins')
for row in g['sources']:need({k:refs[row['original']][k] for k in ('bytes','sha256')}==row['pin'],'all target-original pins')
texts={n:(W/n).read_text() for n in ('install_freeze.py','check_installation.py')}
oldtexts={n:(OLD/n).read_text() for n in texts}
# Full reverse projection to immutable RI209. These are text replacements only,
# not an AST/compile/test of the subject. Every other byte must be unchanged.
def common(s):
 s=s.replace('ri213-freeze-clock-repair-2xc_b29x','ri209-freeze-installation-b3bokxbe').replace('ri213-freeze-install-operation-2xc_b29x','ri209-freeze-install-operation-b3bokxbe')
 s=''.join(line for line in s.splitlines(keepends=True) if not line.startswith('REPAIR='))
 s=s.replace("'PROTOCOL.md','REPAIR_PROVENANCE.json',", "'PROTOCOL.md',")
 s=s.replace('inputs=load(INPUT);repair=load(REPAIR);g=','inputs=load(INPUT);g=')
 s=s.replace("inputs['files']+repair['files']+manifest['files']", "inputs['files']+manifest['files']")
 return s
s=common(texts['install_freeze.py']);old=oldtexts['install_freeze.py']
start=s.index(' # RI213: all safe receipt/error state and closures exist before ownership.')
end=s.index(' def remember(exc):',start)
s=s[:start]+" OUT.mkdir(mode=0o700);start=time.monotonic();first=None;tails={};produced={};install=None\n"+s[end:]
start=s.index(' OUT.mkdir(mode=0o700)\n try:\n');end=s.index("  same(m.ref(args.admission),a_ref,'admission after ownership')",start)
s=s[:start]+' try:\n'+s[end:]
start=s.index('  # All eight ordinary tails above were attempted before final timing.')
end=s.index('  completion=dict(',start)
s=s[:start]+"  elapsed=time.monotonic()-start\n  if elapsed>180:attempt('soft_deadline',lambda:need(False,'installation soft wall exceeded'))\n"+s[end:]
s=s.replace("schema='ri213-installation-completion-v1'","schema='ri209-installation-completion-v1'").replace('elapsed_seconds_before_complete_write=elapsed,timing=timing,','elapsed_seconds_before_complete_write=elapsed,')
need(s==old,'whole installer reverse projection equality')
s=common(texts['check_installation.py']);old=oldtexts['check_installation.py']
s=s.replace('elapsed_seconds_before_complete_write timing complete_not_self_hashed','elapsed_seconds_before_complete_write complete_not_self_hashed').replace("'ri213-installation-completion-v1'","'ri209-installation-completion-v1'")
start=s.index(" timing=c['timing'];fields(timing,'initial final elapsed')\n");end=s.index(" names=['ATTEMPT.json'",start)
s=s[:start]+s[end:];need(s==old,'whole postchecker reverse projection equality')
i=texts['install_freeze.py'];c=texts['check_installation.py']
need(i.count('time.monotonic()')==2,'only initial and final source clock calls')
need(i.index(' start=None;finish=None;elapsed=None;first=None')<i.index(' OUT.mkdir(mode=0o700)\n'),'safe state before ownership')
need(i.index(' def remember(exc):')<i.index(' OUT.mkdir(mode=0o700)\n') and i.index(' def attempt(name,fn):')<i.index(' OUT.mkdir(mode=0o700)\n') and i.index(' def output(name,value):')<i.index(' OUT.mkdir(mode=0o700)\n'),'safe closures before ownership')
need(" OUT.mkdir(mode=0o700)\n try:\n" in i,'first post-mkdir statement protected')
need(i.index("attempt('output_namespace',namespace)")<i.rindex('reading=time.monotonic()')<i.index("save(OUT/'COMPLETE.json',completion)"),'eight tails precede protected final timing and final receipt')
need("if first is None:first=e" in i,'earliest error retention unchanged')
need("timing['initial']['error']=remember(exc);raise" in i and "timing['final']['error']=remember(exc)" in i and "timing['elapsed']['error']=remember(exc)" in i,'separate timing error records')
need("if elapsed is not None and elapsed>180" in i,'unchanged bound only for actual valid elapsed')
need("float('-inf')<reading<float('inf')" in i and "0<=duration<float('inf')" in i,'finite timing/valid interval guards')
need("eq(timing['final']['value']-timing['initial']['value'],timing['elapsed']['value']" in c and "eq(timing['elapsed']['value'],c['elapsed_seconds_before_complete_write']" in c,'complete successful saved timing reconstruction')
# Exact unchanged tail-function/call block; ownership and timing alone surround it.
def middle(t):return t[t.index('  def sources_tail():'):t.index("  attempt('output_namespace',namespace)")+len("  attempt('output_namespace',namespace)\n")]
need(middle(i)==middle(oldtexts['install_freeze.py']),'all eight tail bodies and order byte-identical')
completion_line=next(line for line in c.splitlines() if "fields(c,'schema status admission" in line)
fieldtext=completion_line.split("fields(c,'",1)[1].split("'",1)[0];need(len(fieldtext.split())==14,'exact repaired complete14 field inventory')
need('original13 fields plus `timing` (14 total)' in (W/'PROTOCOL.md').read_text(),'protocol exact completion count')
for p in (B/'ri209-freeze-install-operation-b3bokxbe',B/'ri213-freeze-install-operation-2xc_b29x',W.parent/'ADMIT_INSTALL.json',W.parent/'INSTALL_BOOTSTRAP.py',W.parent/'tmp',W.parent/'monitor'):need(not os.path.lexists(p),'prospective operation/admission/bootstrap absent')
expected_diff=''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md'))
need((W/'SOURCE_DIFF.patch').read_text()==expected_diff,'complete exact source/protocol diff')
files=[pin(W/n) for n in ('INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py')]
save('SOURCE_PINS.json',dict(schema='ri209-proposal-source-pins-v1',status='SOURCE_ONLY_NOT_ADMISSION',files=files))
save('ADMIN_CHECK.json',dict(schema='ri213-author-administrative-correspondence-v1',status='PASS_OPAQUE_PINS_AND_COMPLETE_REVERSE_PROJECTION_ONLY',checks=checks,base_input_pins=806,repair_provenance_pins=19,distinct_opaque_pins=825,preserved_roles=810,copies=48,history=124,target_originals=30,whole_installer_reverse_projection=True,whole_postchecker_reverse_projection=True,eight_tail_block_byte_identical=True,source_lines={n:len(t.splitlines()) for n,t in texts.items()},source_manifest=pin(W/'SOURCE_PINS.json'),original_namespace_files=15,old_and_new_operation_absence_checked=True,source_import_compile_AST_probe_execute=False,clock_or_fixture_evaluation=False,scientific_decode=False,runtime_or_host_observation=False,E_modified=False,admission_created=False))
print(json.dumps(dict(status='PASS_ADMINISTRATIVE_ONLY',checks=checks,opaque_identities=825,admin_check=pin(W/'ADMIN_CHECK.json'),source_manifest=pin(W/'SOURCE_PINS.json'))))
