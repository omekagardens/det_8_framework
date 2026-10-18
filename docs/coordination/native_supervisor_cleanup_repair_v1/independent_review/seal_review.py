"""Administrative review sealing only; no reviewed source module is loaded."""
from pathlib import Path
import hashlib,json,os,stat
D=Path('/Volumes/AI_DATA/development/det-review-evidence/ri184-compound-independent-review-yju68l4m')
S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri182-compound-cleanup-oracle-repair-6835ytb8')
def save(n,v):
    b=(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with (D/n).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(p):
    p=Path(p);before=p.lstat()
    if not p.is_absolute() or not stat.S_ISREG(before.st_mode) or any(x.is_symlink() for x in [p,*p.parents]):raise ValueError('invalid identity path')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);digest=hashlib.sha256();size=0
    try:
        if state(os.fstat(fd))!=state(before):raise ValueError('opened identity')
        while True:
            b=os.read(fd,1048576)
            if not b:break
            digest.update(b);size+=len(b)
        if state(os.fstat(fd))!=state(before):raise ValueError('descriptor drift')
    finally:os.close(fd)
    if state(p.lstat())!=state(before) or size!=before.st_size:raise ValueError('path drift')
    return dict(path=str(p),bytes=size,sha256=digest.hexdigest(),state=state(before))
def pure(r):return {k:r[k] for k in ('path','bytes','sha256')}
ap=identity(D/'ADMIN_CHECK.json')
if (ap['bytes'],ap['sha256'])!=(607712,'7d3d5a145fc489738981fe52c941a8f7fd4f04ae424098dc1368f7ded1a6d6e5'):raise ValueError('admin pin')
a=json.loads((D/'ADMIN_CHECK.json').read_text())
subject=dict(path=str(S/'HANDOFF.json'),bytes=13764,sha256='55f33b57bb11d1633b8410c64574cebccfa17846397fb6aacc27fe4a23d6bd26')
save('VERDICT.json',dict(schema='ri184-independent-source-verdict-v1',recommendation='ACCEPT_EXACT_UNEXECUTED_NARROW_F04_R_SOURCE_REPAIR',subject=subject,remaining_source_blockers=[],F04_R='SOURCE_REPAIR_SUFFICIENT_SUBJECT_TO_ROOT_ADJUDICATION',findings_resolved=['Exact caller primary/unregister/pipe-close prefix and matching source-error order','Single selected-role acquired lifetime; both failed pipe and sibling checked','Failed first close then one successful retry; no later unregister/close attempts, including failed repeats without another success','Preserved observer secondary strings, exact order, bounded subject reap and independent recovery'],locations=['check_saved.py:196-224','check_saved.py:490-505','check_saved.py:607-613','case_worker.py:344-408','RI169/supervise_native.py:116-136'],nonauthor=True,prior_roles='Independent RI171/RI180 reviewer and unrelated WHITE validator/caller/bootstrap author; no authorship of RI182 or RI165/167/169 qualification supervisor.',cases=92,recipes=34,groups=13,mutation_families=35,executed_cases=0,executed_mutations=0,administrative_checks=7255,observed_identities=139,qualification_accepted=False,execution_authorized=False,current_runtime_observed=False,scientific_acceptance=False,root_owns_disposition_admission_publication=True,ret_paused=True))
rows=[('0e369c','Authenticated and read exact assignment; confirmed empty exclusive reservation'),('081874','Authenticated exact28/27 subject seal; read full contract, response,35-family plan, schemas and author record'),('a81777','Read complete source diff'),('0e1bd1','Read complete added checker logic and surrounding compound branches, worker process/pipe/selector source and unchanged stop_pipe'),('bacbf6','Read administrative metadata inventories, full actual tool records, prospective invocation and complete author checker source'),('b8bb7c','Created and ran independent administrative checker only;7255 predicates/139 identities passed'),('f25cde','Read complete root repair assignment and predecessor decision'),('2b4228','Wrote complete independent narrative')]
save('COMMAND_OUTCOMES.json',dict(schema='ri184-genuine-administrative-outcomes-v1',records=[dict(chunk_id=k,exit_code=0,description=v) for k,v in rows],exact_check_command='/opt/homebrew/bin/python3 -I -B '+str(D/'check_metadata.py'),check_stdout=dict(status='EXACT_SOURCE_CORRESPONDENCE_NOT_RUNTIME_QUALIFICATION',bytes=607712,checks=7255,identities=139,sha256=ap['sha256'],cases_executed=0),failed_commands=[],truncated_displays=[],subject_vendor_control_executed=False,scope='Actual conversation tool-result references, not fabricated operational cards. Final sealing and read-only verification receipts are returned separately to root.'))
observed=[]
for row in a['observed_identities']:
    got=identity(row['path'])
    if got!=row:raise ValueError('input changed '+row['path'])
    observed.append(got)
if sorted(x.name for x in S.iterdir())!=a['subject_namespace']:raise ValueError('subject namespace changed')
base=['ADMIN_CHECK.json','COMMAND_OUTCOMES.json','INDEPENDENT_REVIEW.md','VERDICT.json','check_metadata.py','seal_review.py']
if sorted(x.name for x in D.iterdir())!=sorted(base):raise ValueError('review namespace')
save('FINAL_IDENTITY_CHECK.json',dict(schema='ri184-final-source-identity-check-v1',status='ALL139_REVIEWED_INPUTS_UNCHANGED',original_count=139,final_count=len(observed),complete_rows_equal=True,observed_identities=observed,subject_namespace=a['subject_namespace'],review_files_before_this_record=[pure(identity(D/n)) for n in base],executed_cases=0,executed_mutations=0,current_runtime_observed=False))
namespace=sorted(base+['FINAL_IDENTITY_CHECK.json','HANDOFF.json']);payloads=[pure(identity(D/n)) for n in namespace if n!='HANDOFF.json']
save('HANDOFF.json',dict(schema='ri184-independent-review-handoff-v1',reservation=str(D),subject=subject,recommendation='ACCEPT_EXACT_UNEXECUTED_NARROW_F04_R_SOURCE_REPAIR',remaining_source_blockers=[],namespace=namespace,payloads=payloads,review='INDEPENDENT_REVIEW.md',verdict='VERDICT.json',actual_admin_check='ADMIN_CHECK.json',actual_commands='COMMAND_OUTCOMES.json',administrative_checker='check_metadata.py',final_identity_check='FINAL_IDENTITY_CHECK.json',compact_publication_subset=namespace,external_only_diagnostics=[],cases=92,recipes=34,prospective_mutation_families=35,executed_cases=0,executed_mutations=0,source_only=True,subject_import_compile_AST_probe_run=False,scientific_decode=False,runtime_cards_admission=False,repository_git_mutation=False,new_agents=False,all_predecessors_unchanged=True,root_owns_disposition_admission_publication=True,ret_paused=True,immutable_after_seal=True))
if sorted(p.name for p in D.iterdir())!=namespace:raise ValueError('final namespace')
for row in payloads:
    if pure(identity(row['path']))!=row:raise ValueError('sealed payload drift')
print(json.dumps(dict(status='SEALED_RECOMMEND_ACCEPT_UNEXECUTED_F04_R_REPAIR',namespace=len(namespace),payloads=len(payloads),handoff=pure(identity(D/'HANDOFF.json')),final_identity_check=pure(identity(D/'FINAL_IDENTITY_CHECK.json')),executed_cases=0),sort_keys=True))
