"""Administrative immutable review seal. No reviewed subject is loaded or evaluated."""
from pathlib import Path
import hashlib,json,os,stat
D=Path('/Volumes/AI_DATA/development/det-review-evidence/ri180-supervisor-independent-review-4xwmvctt')
S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri176-supervisor-qualification-repair-3ausb2jo')
def save(name,v):
    b=(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with (D/name).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(p):
    p=Path(p);before=p.lstat()
    if not p.is_absolute() or not stat.S_ISREG(before.st_mode) or any(x.is_symlink() for x in [p,*p.parents]):raise ValueError('path/regular/symlink')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();size=0
    try:
        if state(os.fstat(fd))!=state(before):raise ValueError('open identity')
        while True:
            b=os.read(fd,1048576)
            if not b:break
            size+=len(b);h.update(b)
        if state(os.fstat(fd))!=state(before):raise ValueError('descriptor drift')
    finally:os.close(fd)
    if state(p.lstat())!=state(before) or size!=before.st_size:raise ValueError('path drift')
    return dict(path=str(p),bytes=size,sha256=h.hexdigest(),state=state(before))
def pure(v):return {k:v[k] for k in ('path','bytes','sha256')}
pin=identity(D/'ADMIN_CHECK.json')
if (pin['bytes'],pin['sha256'])!=(534125,'0f7a30d60bd2776c9ae7341b289a060a6802f51313957096949760f51450ef2c'):raise ValueError('administrative result pin')
a=json.loads((D/'ADMIN_CHECK.json').read_text())
subject=dict(path=str(S/'HANDOFF.json'),bytes=14679,sha256='572fe0bfc79489dc3b9c4a6df9bc4d7bbb0ff455de1c68eb2fbb00e6d870421e')
finding=dict(id='F04-R',severity='blocking',title='Complete compound cleanup receipt and once-closed lifecycle assertions remain missing',caller_cases=['S10.caller.stdout.unregister_close','S10.caller.stderr.unregister_close'],lifecycle_cases=['S10.caller.stdout.unregister_close','S10.caller.stderr.unregister_close','S10.ps.stdout.unregister_close','S10.ps.stderr.unregister_close'],locations=['check_saved.py:272-276','check_saved.py:461-465','check_saved.py:568-570','case_worker.py:201-203','case_worker.py:350-358','case_worker.py:399-403','RI169/supervise_native.py:116-136'],counterpaths=['Omit caller unregister and/or pipe_close secondary triples from consistently rebound candidate/completion while retaining exact injected events, primary, buffers, reap and ordinary terminal evidence. No caller predicate rejects the lost subject errors.','Retain one successful retry, then add subsequent same-pipe unregister/close attempts; current any-later-close predicates do not enforce the inherited successful-closes-not-repeated requirement.'],required_repair=['Require both exact caller secondary triples in their source-derived order after primary.','Require eventual successful retry and no unregister/close attempts after success for the compound failed pipe and successfully closed sibling.','Add isolated prospective caller-error-removal and repeat-after-success oracle mutations, preserving actual matched positive and separate synthetic admission boundaries.'],executed_counterexample=False)
save('VERDICT.json',dict(schema='ri180-independent-source-verdict-v1',decision='REQUIRE_NARROW_F04_R_REPAIR_BEFORE_QUALIFICATION_ADMISSION',subject=subject,findings=[finding],prior_findings={'F01':'MAIN_SOURCE_DEFECT_REPAIRED','F02':'MAIN_SOURCE_DEFECT_REPAIRED','F03':'MAIN_SOURCE_DEFECT_REPAIRED','F04':'MAIN_BUFFER_KILL_REAP_RECOVERY_REPAIRS_PRESENT_WITH_F04_R_RESIDUAL','F05':'MAIN_SOURCE_DEFECT_REPAIRED'},nonauthor=True,prior_roles='Independent RI171/RI165 reviewer; unrelated earlier WHITE validator/caller/bootstrap author.',new_source_lines_read=1576,unchanged_subject_lines_read=588,cases=92,recipes=34,mutation_plan_families=26,actual_case_outcomes=0,actual_mutation_outcomes=0,qualification_accepted=False,source_execution=False,root_owns_adjudication_repairs_admission_publication=True,ret_paused=True))
rows=[('981d49',0,'Authenticated complete assignment and handoff; read both'),('3a0e1c',0,'Authenticated exact33/32 namespace; reservation empty; read all six main source/contracts/author documents'),('7ef7ad',0,'Read checker1-180 including all92 literal obligations'),('ac6776',0,'Read checker181-345'),('7cd3c4',0,'Read checker346-520'),('968abb',0,'Read checker521-661'),('5a5c0d',0,'Read worker1-255'),('f2a6da',0,'Read worker256-499'),('6e0af2',0,'Read unchanged RI169 supervisor1-250'),('0f9943',0,'Read unchanged RI169 supervisor251-588'),('a90dfd',0,'Read complete protocol/controller/payload'),('fdbdf3',0,'Read metadata schemas, complete declared tool records and author administrative checker'),('8101e3',0,'Read complete selected compound/fallback/journal/kill/receipt case records'),('ff585f',1,'Own administrative V1 rejected textual unified-diff alignment; failure source and diagnostic preserved'),('70e5da',0,'Preserved V1 diagnostic; created V2 literal-hunk reconstruction; V2 passed6972 predicates/98 identities'),('25c380',0,'Read complete original repair assignment/root decision, all92 case mapping and remaining complete inherited recipes'),('df5893',0,'Wrote complete independent narrative')]
save('COMMAND_OUTCOMES.json',dict(schema='ri180-actual-administrative-outcomes-v1',records=[dict(chunk_id=k,exit_code=e,description=t) for k,e,t in rows],exact_v1_command='/opt/homebrew/bin/python3 -I -B '+str(D/'check_metadata.py'),exact_v2_command='/opt/homebrew/bin/python3 -I -B '+str(D/'check_metadata_v2.py'),failed_attempts_preserved=['check_metadata.py','FAILED_ADMIN_V1.json'],own_displays_truncated=False,successful_result=dict(checks=6972,identities=98,bytes=534125,sha256=pin['sha256'],executed_cases=0),scope='Actual conversation tool references, not fabricated operation/admission cards. Final sealing and final read-only verification tool results are supplied separately to root.',subject_or_vendor_execution=False))
final=[]
for row in a['observed_identities']:
    got=identity(row['path'])
    if got!=row:raise ValueError('reviewed identity changed '+row['path'])
    final.append(got)
if sorted(p.name for p in S.iterdir())!=a['subject_namespace']:raise ValueError('subject namespace changed')
base=['ADMIN_CHECK.json','COMMAND_OUTCOMES.json','FAILED_ADMIN_V1.json','INDEPENDENT_REVIEW.md','VERDICT.json','check_metadata.py','check_metadata_v2.py','seal_review.py']
if sorted(p.name for p in D.iterdir())!=sorted(base):raise ValueError('unexpected review namespace')
own=[pure(identity(D/n)) for n in base]
save('FINAL_IDENTITY_CHECK.json',dict(schema='ri180-independent-final-identity-window-v1',status='ALL98_INPUTS_UNCHANGED_EXACT_REVIEW_NAMESPACE',original_observed_count=98,final_observed_count=len(final),complete_identity_rows_equal=True,observed_identities=final,subject_namespace=a['subject_namespace'],review_files_before_this_check=own,subject_control_vendor_executed=False,actual_case_outcomes=0))
namespace=sorted(base+['FINAL_IDENTITY_CHECK.json','HANDOFF.json'])
payloads=[pure(identity(D/n)) for n in namespace if n!='HANDOFF.json']
save('HANDOFF.json',dict(schema='ri180-independent-review-handoff-v1',reservation=str(D),subject=subject,decision='REQUIRE_NARROW_F04_R_REPAIR_BEFORE_QUALIFICATION_ADMISSION',findings=['F04-R'],namespace=namespace,payloads=payloads,complete_review='INDEPENDENT_REVIEW.md',verdict='VERDICT.json',actual_checks='ADMIN_CHECK.json',actual_commands='COMMAND_OUTCOMES.json',preserved_failed_attempt=['check_metadata.py','FAILED_ADMIN_V1.json'],successful_checker='check_metadata_v2.py',final_identity_check='FINAL_IDENTITY_CHECK.json',compact_publication_subset=namespace,external_only_diagnostics=[],cases=92,recipes=34,prospective_mutation_families=26,executed_cases=0,executed_mutations=0,source_only=True,subject_import_compile_AST_probe_execution=False,scientific_decode=False,runtime_cards_or_admission=False,repository_git_mutation=False,new_agents=False,root_owns_disposition_repairs_admission_publication=True,ret_paused=True,immutable_after_seal=True))
if sorted(p.name for p in D.iterdir())!=namespace:raise ValueError('seal namespace')
for row in payloads:
    if pure(identity(row['path']))!=row:raise ValueError('payload changed')
print(json.dumps(dict(status='SEALED_F04_R_SOURCE_REVIEW',namespace=len(namespace),payloads=len(payloads),handoff=pure(identity(D/'HANDOFF.json')),final_identity_check=pure(identity(D/'FINAL_IDENTITY_CHECK.json')),executed_cases=0),sort_keys=True))
