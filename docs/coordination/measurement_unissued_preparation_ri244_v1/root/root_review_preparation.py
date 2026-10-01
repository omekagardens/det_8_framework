from pathlib import Path
import hashlib,importlib.util,os,stat
hp=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');b=hp.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);R=m.B/'ri247-root-hook-branch-review-6fgw5qd9';m.D=R;D=m.B/'ri244-current-normal-premode-2kfsmiea';E=m.B/'ri154-white-execution-proposed-42_uvw15'
t=m.load('/private/tmp/ri247-preparation-tools.json');assert t['initial']['result']['session_id']==74730 and t['terminal']['exit_code']==0 and not t['terminal'].get('session_id');tr=m.save('RI244_GENUINE_PREPARATION_TOOLS.json',t)
st=lambda p:[(s:=p.lstat()).st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
names=['ADMISSION_CANDIDATE.json','BOOTSTRAP_PREFLIGHT.json','CUSTODY_BEFORE.json','E_BEFORE.json','PREPARATION_ATTEMPT.json','PREPARATION_COMPLETE.json','PRE_MODE_BOOTSTRAP.proposal.py','SUPPLIER_BEFORE.json']
assert sorted(x.name for x in D.iterdir())==sorted(names+['tmp','monitor']);assert D.resolve()==D and not D.is_symlink()
outputs=[m.identity(D/n) for n in names]
assert all(r['resolved_path']==r['path'] and not r['symlink_chain'] and stat.S_ISREG(r['state'][2]) for r in outputs)
dirs=[]
for n in ['tmp','monitor']:
 p=D/n;a=st(p);assert stat.S_ISDIR(a[2]) and p.resolve()==p and not p.is_symlink() and list(p.iterdir())==[] and st(p)==a;dirs.append(dict(path=str(p),state=a,entries=[]))
c=m.load(D/'PREPARATION_COMPLETE.json');assert c['status']=='UNISSUED_PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW' and c['first_error'] is None and c['operational_authorization'] is False and c['subject_executed'] is False and c['installed_freeze_decoded'] is False and c['E_written'] is False
assert sorted(c['independent_tails'])==sorted(['inputs','supplier','E','authority_absences','outputs','namespace']) and all(x['error'] is None for x in c['independent_tails'].values())
assert len(c['artifacts'])==7
for row in c['artifacts'].values():m.verify(row['path'],row)
before=m.load(D/'CUSTODY_BEFORE.json');assert c['input_count']==len(before['identities'])==c['independent_tails']['inputs']['value'] and c['tail_observations']['inputs']['values']==before['identities'] and c['tail_observations']['inputs']['errors']==[]
for row in before['identities']:assert m.identity(row['path'])==row
v=m.load(D/'SUPPLIER_BEFORE.json');vp=c['tail_observations']['supplier'];assert {k:x for k,x in v.items() if k!='observed_at_unix_ns'}=={k:x for k,x in vp.items() if k!='observed_at_unix_ns'}
assert len(v['vendor'])==1810 and sum(x['bytes'] for x in v['vendor'])==48024515 and len(v['tools'])==4 and len(v['namespace'])==195 and len(v['absent'])==2
for row in [*v['vendor'],*v['tools']]:assert m.identity(row['path'])==row
for row in v['namespace']:
 p=Path(row['path']);assert st(p)==row['state']
 if row['kind']=='directory':assert stat.S_ISDIR(st(p)[2]) and sorted(x.name for x in p.iterdir())==row['entries']
 else:assert row['kind']=='symlink' and p.is_symlink() and os.readlink(p)==row['target']
 assert st(p)==row['state']
for p in v['absent']:assert not os.path.lexists(p)
et=m.load(D/'E_BEFORE.json');old=m.B/'ri239-root-current-e-capture-mk6vocq1/POST_E.json';m.verify(old,dict(bytes=43288,sha256='d8bde2568a8b117ad67255e8c12f5e41183b93eb2df04800e43db973b27a52e4'));assert et==m.load(old)==c['independent_tails']['E']['value'];assert len(et)==58 and sum(r['kind']=='file' for r in et)==49
for row in et:
 p=E/row['relative'];assert not p.is_symlink() and st(p)==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
 else:assert m.identity(p)==row['identity']
 assert st(p)==row['state']
for p in [D/'ADMIT_PRE_MODE.json',D/'DISPATCH.json',m.B/'ri156-operation-ri244-premode-2kfsmiea',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:assert not os.path.lexists(p)
candidate=m.load(D/'ADMISSION_CANDIDATE.json');assert candidate['status']=='UNISSUED_NOT_OPERATIONAL_AUTHORITY' and candidate['operational_authorization'] is False;card=candidate['candidate'];assert len(card)==12 and card['action']=='pre_mode' and card['genuine_outer_required'] is True;assert card['bootstrap_preflight']==m.ref(D/'BOOTSTRAP_PREFLIGHT.json');assert card['output']==str(m.B/'ri156-operation-ri244-premode-2kfsmiea');assert card['environment']==v['environment']
assert (D/'PRE_MODE_BOOTSTRAP.proposal.py').read_bytes()==Path('/private/tmp/ri244-preparation-proposal-3udz0imk/PRE_MODE_BOOTSTRAP.proposal.txt').read_bytes()
startup=m.load(R/'RI244_ADMINISTRATIVE_STARTUP_BINDING.json')
for key in ['writer','ordinary_administrative_interpreter']:assert m.identity(startup[key]['path'])==startup[key]
for row in outputs:assert m.identity(row['path'])==row
for row in dirs:assert st(Path(row['path']))==row['state'] and list(Path(row['path']).iterdir())==[]
assert sorted(x.name for x in D.iterdir())==sorted(names+['tmp','monitor'])
print(m.save('RI244_ROOT_PREPARATION_CHECK.json',dict(schema='ri247-root-unissued-preparation-check-v1',status='PASS_COMPLETE_PREPARATION_CUSTODY_ONLY',genuine_tools=tr,decision=m.ref(R/'RI244_PREPARATION_DECISION.json'),complete=m.ref(D/'PREPARATION_COMPLETE.json'),outputs=outputs,directories=dirs,whole_input_identities=c['input_count'],independent_tails=6,all_tails_pass=True,supplier_files=1810,supplier_bytes=48024515,supplier_tools=4,supplier_namespace=195,supplier_absent=2,E_files=49,E_directories=9,E_unchanged=True,writer_and_admin_binding_unchanged=True,literal_regular_final_outputs=True,exact_candidate_fields=12,exact_bootstrap_bytes=True,operational_authorization=False,scientific_execution=False,sole_child_monitor_executed=False,complete_atomic_snapshot_claim=False)))
