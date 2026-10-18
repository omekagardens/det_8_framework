"""Whole source/custody authentication for the narrow RI213 repair; no subject run."""
from pathlib import Path
import hashlib,importlib.util,difflib,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri215-root-margin-review-a1inhpxr';W=B/'ri213-freeze-clock-repair-2xc_b29x/worker_proposal';OLD=B/'ri209-freeze-installation-b3bokxbe/worker_proposal'
p=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=p.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
fresh={}
def check(r):
 v=m.verify(r['path'],r)
 if r['path'] in fresh:assert fresh[r['path']]==v
 fresh[r['path']]=v
h=m.ref(W/'HANDOFF.json');assert m.pure(h)==dict(bytes=7600,sha256='f8e4ab402fe4621352c7fe1f9b3d3bfeb6d5bc1194afcc7fb98cf34f8eb2f512');check(h)
H=m.load(W/'HANDOFF.json');assert sorted(H['namespace'])==sorted(p.name for p in W.iterdir())==sorted(['HANDOFF.json']+[Path(r['path']).name for r in H['files']])
for r in H['files']:check(r)
base=m.load(W/'INPUT_PINS.json');repair=m.load(W/'REPAIR_PROVENANCE.json')
assert (W/'INPUT_PINS.json').read_bytes()==(OLD/'INPUT_PINS.json').read_bytes()
refs={}
for r in base['files']+repair['files']:
 if r['path'] in refs:assert refs[r['path']]==r
 refs[r['path']]=r;check(r)
assert len(base['files'])==806 and len(repair['files'])==19 and len(refs)==825
assert len(base['prior_role_rows'])==810 and len(base['roles'])==20
for row in base['prior_role_rows']:assert {k:row[k] for k in ('path','bytes','sha256')}==refs[row['path']]
for row in base['roles'].values():assert row==refs[row['path']]
G=m.load(base['roles']['graph']['path']);assert [len(G[k]) for k in ('copied_files','history_originals','sources')]==[48,124,30]
for r in G['copied_files']:assert refs[r['source']['path']]==r['source'] and m.pure(refs[r['destination']])==m.pure(r['source'])
for r in G['history_originals']:assert refs[r['path']]==r
for r in G['sources']:assert m.pure(refs[r['original']])==r['pin']
old=m.load(OLD/'HANDOFF.json');assert sorted(old['namespace'])==sorted(p.name for p in OLD.iterdir())
for r in old['files']:check(r)
manifest=m.load(W/'SOURCE_PINS.json');assert set(manifest)=={'schema','status','files'} and manifest['status']=='SOURCE_ONLY_NOT_ADMISSION'
assert [Path(r['path']).name for r in manifest['files']]==['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_installation.py','install_freeze.py']
for r in manifest['files']:assert Path(r['path']).parent==W;check(r)
expected=''.join(''.join(difflib.unified_diff((OLD/n).read_text().splitlines(keepends=True),(W/n).read_text().splitlines(keepends=True),fromfile=str(OLD/n),tofile=str(W/n))) for n in ('install_freeze.py','check_installation.py','PROTOCOL.md'))
assert (W/'SOURCE_DIFF.patch').read_text()==expected
oldtext=(OLD/'install_freeze.py').read_text();newtext=(W/'install_freeze.py').read_text()
def tail(t):return t[t.index('  def sources_tail():'):t.index("  attempt('output_namespace',namespace)")+len("  attempt('output_namespace',namespace)\n")]
assert tail(newtext)==tail(oldtext)
admin=m.load(W/'ADMIN_CHECK.json');assert admin['checks']==3634 and H['actual_admin']['predicates']==3636
assert H['source_lines']=={'installer':237,'postchecker':141}
assert H['source_manifest']==m.ref(W/'SOURCE_PINS.json')
boundary=m.load(B/'ri214-root-installation-review-xlkw6cbw/MEASUREMENT_BOUNDARY.json');E=Path(boundary['E'])
assert sorted(str(p) for p in E.rglob('*') if p.is_dir())==boundary['subdirectories']
assert [m.identity(p) for p in sorted(E.rglob('*')) if p.is_file()]==boundary['files']
absences=[E/'AUTHORIZED_FREEZE.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json',B/'ri209-freeze-install-operation-b3bokxbe',B/'ri213-freeze-install-operation-2xc_b29x',W.parent/'ADMIT_INSTALL.json',W.parent/'INSTALL_BOOTSTRAP.py',W.parent/'tmp',W.parent/'monitor']
assert not any(os.path.lexists(p) for p in absences)
for r in fresh.values():assert m.identity(r['path'])==r
assert len(fresh)==840
with (D/'review_installation.py').open('xb') as f:f.write(Path(__file__).read_bytes())
print(m.save('RI213_ROOT_METADATA_CHECK.json',dict(schema='ri215-ri213-independent-source-metadata-v1',status='PASS_SOURCE_CUSTODY_NOT_EXECUTION',handoff=h,source_manifest=m.ref(W/'SOURCE_PINS.json'),fresh_identities=list(fresh.values()),declared_input_pins=825,base_input_pins=806,added_repair_pins=19,historical_roles=810,named_roles=20,copy_history_original_counts=[48,124,30],namespace=15,payloads=14,exact_diff=True,eight_tails_byte_identical=True,author_saved_predicates=3634,author_printed_predicates=3636,predicate_phase_explanation='Two source-manifest pin predicates occur after the saved checks value was captured; retain both accurately.',measurement_boundary=m.ref(B/'ri214-root-installation-review-xlkw6cbw/MEASUREMENT_BOUNDARY.json'),absent=[str(p) for p in absences],old_E_48files_8subdirectories_9includingroot_unchanged=True,subject_execution=False,scientific_body_decoded=False,runtime_admission=False)))
