"""Exclusive administrative review sealing; hashes sources, never imports a subject."""
import hashlib
import json
import os
from pathlib import Path
import stat

D = Path('/Volumes/AI_DATA/development/det-review-evidence/ri171-independent-supervisor-source-review-fw3b83xu')
S = Path('/Volumes/AI_DATA/development/det-review-evidence/ri171-supervisor-qualification-source-zksymhs1')

def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()

def save(name, value):
    with (D / name).open('xb') as f:
        f.write(encode(value)); f.flush(); os.fsync(f.fileno())

def state(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def identity(p):
    p = Path(p)
    if not p.is_absolute() or any(x.is_symlink() for x in [p, *p.parents]):
        raise ValueError('absolute nonsymlink identity required: ' + str(p))
    before = p.lstat()
    if not stat.S_ISREG(before.st_mode): raise ValueError('regular file required')
    digest = hashlib.sha256(); total = 0
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if state(os.fstat(fd)) != state(before): raise ValueError('open state drift')
        while True:
            b = os.read(fd, 1048576)
            if not b: break
            digest.update(b); total += len(b)
        if state(os.fstat(fd)) != state(before): raise ValueError('descriptor drift')
    finally:
        os.close(fd)
    if state(p.lstat()) != state(before) or total != before.st_size:
        raise ValueError('path drift')
    return dict(path=str(p), bytes=total, sha256=digest.hexdigest(), fresh_state=state(before))

def pure(row): return {k:row[k] for k in ('path','bytes','sha256')}

admin_pin = identity(D / 'ADMIN_CHECK.json')
if (admin_pin['bytes'], admin_pin['sha256']) != (269609, '14ef68bdea792a4b5a17161c381d632d49cbbcf9d73e2807a03e887fa9281da5'):
    raise ValueError('independent administrative result changed')
admin = json.loads((D / 'ADMIN_CHECK.json').read_text())
findings = [
    dict(id='F01', severity='blocking', title='Caller read injections select the observer; transient cases can falsely pass', locations=['case_worker.py:71-77','case_worker.py:332-345','check_saved.py:212-226','RI169/supervise_native.py:423-447'], required_repair='Exact role-and-stream injection plus independently checked error tag and same-pipe ordering.'),
    dict(id='F02', severity='blocking', title='late_observer is shadowed by both generic late-file branches', locations=['check_saved.py:234-260','check_saved.py:305-308','case_worker.py:254-263'], required_repair='Closed late-file fault set and reachable dedicated second-observer refusal oracle.'),
    dict(id='F03', severity='blocking', title='Ordinary failed cases can pass with only a candidate receipt after unrelated terminal escape', locations=['check_saved.py:97-130','check_saved.py:234-247','case_worker.py:453-480','qualify_supervisor.py:94-113','RI169/supervise_native.py:570-580'], required_repair='Case-specific terminal requirements: expected return, no unrelated escape, durable full saved receipt for ordinary cases; explicit partial semantics only where declared.'),
    dict(id='F04', severity='blocking', title='Inherited defining faults, healthy captures, subject reap and recovery completeness are not fully asserted', locations=['check_saved.py:297-318','check_saved.py:342-355','check_saved.py:389-394','case_worker.py:300-328','case_worker.py:370-375'], required_repair='Finite complete per-case obligations and identity-complete recovery reconciliation; retain deliberate incomplete deadline/nonreap outcomes without claiming successful cleanup.'),
    dict(id='F05', severity='blocking', title='stderr hash-drift test changes file size', locations=['inert_payload.py:117-125','case_worker.py:137-154','check_saved.py:305-307'], required_repair='Nonempty deterministic stderr with unchanged intended first error; verify same length and actual byte/hash mutation separately from size mutation.')
]
subject_pin = dict(path=str(S / 'HANDOFF.json'), bytes=14569, sha256='b83a4588d780d552cbf665263a599e514e8c6944d41d3237bce1bd1180b01078')
save('VERDICT.json', dict(schema='ri171-independent-source-verdict-v1', decision='REQUIRE_SOURCE_REPAIRS_BEFORE_QUALIFICATION_ADMISSION', subject=subject_pin, findings=findings, source_modules_read=5, new_source_lines_read=1310, unchanged_supervisor_lines_read=588, defined_cases=92, executed_cases=0, administrative_checks=3525, observed_identities=55, reviewer_authored_subject=False, prior_roles='Earlier separate WHITE validator/caller/bootstrap author and independent RI165 reviewer; no authorship of RI165/167/169 supervisor or RI171.', qualification_accepted=False, native_scientific_acceptance=False, actual_runtime_observed=False, historical_325_references_freshly_walked=False, remaining_root_actions=['Adjudicate exact source findings','Assign narrow repair to original author','Obtain fresh independent review of repaired source','Separately determine genuine per-case admission, timing, custody and recovery; no execution authorized by this review'], ret_paused=True))
rows = [
 ('6f4111','Authenticated exclusive reservation, assignment and handoff; read assignment/schema/namespace'),
 ('cf6a03','Authenticated exact30/29 and read source pins plus complete protocol/schema/invocation'),
 ('8d92c2','Read complete protocol, controller and inert payload'),
 ('5c3b96','Read worker lines1-250'),
 ('8b2990','Read worker lines250-485 and unchanged RI169 lines1-220'),
 ('5fd073','Read unchanged RI169 lines220-588'),
 ('f5dca0','Read saved checker lines1-155'),
 ('c84bae','Read saved checker lines155-305'),
 ('4256b5','Read saved checker lines305-410; combined manifest display truncated and not credited complete'),
 ('2be246','Recovered manifest header and complete cases28-58'),
 ('085732','Recovered complete manifest cases59-86'),
 ('70313a','Read author record, failure and administrative schemas'),
 ('20e85e','Read dependency roles,24 paths and manifest cases87-92'),
 ('3ed3f0','Read predecessor bindings, recipe fields and full actual author tool records'),
 ('e2a549','Read original assignment, root decision, full metadata checker, metadata result and coverage'),
 ('dbc07b','Recovered complete manifest cases1-27'),
 ('85987e','Created own read-only check_admin.py'),
 ('59ddad','Executed own bounded read-only administrative checker only'),
 ('f855b0','Created complete narrative review'),
 ('163161','Listed review reservation after continuation; three expected files'),
 ('1cb89e','Read own complete administrative checker'),
 ('fca7ee','Read own complete narrative before seal')
]
save('COMMAND_OUTCOMES.json', dict(schema='ri171-independent-tool-outcomes-v1', records=[dict(chunk_id=k, exit_code=0, description=v, output_truncated=(k=='4256b5')) for k,v in rows], exact_checker_command='/opt/homebrew/bin/python3 -I -B ' + str(D / 'check_admin.py'), checker_stdout=dict(bytes=269609,cases=92,checks=3525,identities=55,sha256=admin_pin['sha256'],status='IDENTITIES_AND_LITERAL_INVENTORIES_MATCH_NOT_QUALIFICATION'), own_failed_commands=[], display_recovery=dict(truncated_chunk='4256b5', recovered_by=['dbc07b','2be246','085732','20e85e'], no_truncated_complete_read_credit=True), subject_original_failures_preserved=['72a8b8 exit1 FilePin property-order administrative failure','Original RI165 system-Python startup deviation: no qualification credit'], subject_correction='880ec6 exit0 administrative only', actual_control_outcomes=0, tool_record_scope='These are genuine tool-result references from this review conversation, not created execution/admission cards. Final sealing and read-only verification results are returned directly to root.'))
observed = []
for row in admin['observed_identities']:
    got = identity(row['path'])
    if got != row: raise ValueError('reviewed input changed: ' + row['path'])
    observed.append(got)
if sorted(p.name for p in S.iterdir()) != sorted(admin['subject_namespace']):
    raise ValueError('subject namespace changed')
expected_before = ['ADMIN_CHECK.json','COMMAND_OUTCOMES.json','INDEPENDENT_REVIEW.md','VERDICT.json','check_admin.py','seal_review.py']
if sorted(p.name for p in D.iterdir()) != sorted(expected_before):
    raise ValueError('unexpected review namespace')
own = [identity(D / n) for n in expected_before]
save('FINAL_IDENTITY_CHECK.json', dict(schema='ri171-independent-final-read-window-v1', status='UNCHANGED_INPUTS_AND_EXACT_REVIEW_NAMESPACE', subject_namespace=admin['subject_namespace'], original_observed_identity_count=55, final_observed_identity_count=len(observed), original_and_final_rows_identical=True, final_identities=observed, review_files_before_this_check=[pure(r) for r in own], subject_control_helper_vendor_executed=False, actual_outcomes=0, no_runtime_or_admission_truth_created=True))
namespace = sorted(expected_before + ['FINAL_IDENTITY_CHECK.json','HANDOFF.json'])
payloads = [pure(identity(D / n)) for n in namespace if n != 'HANDOFF.json']
save('HANDOFF.json', dict(schema='ri171-independent-source-review-handoff-v1', reservation=str(D), subject=subject_pin, verdict='REQUIRE_SOURCE_REPAIRS_BEFORE_QUALIFICATION_ADMISSION', findings=['F01','F02','F03','F04','F05'], namespace=namespace, payloads=payloads, complete_review='INDEPENDENT_REVIEW.md', structured_verdict='VERDICT.json', administrative_checks='ADMIN_CHECK.json', final_identity_check='FINAL_IDENTITY_CHECK.json', actual_command_outcomes='COMMAND_OUTCOMES.json', administrative_checker='check_admin.py', administrative_seal_source='seal_review.py', compact_publication_subset=namespace, external_only_diagnostics=[], source_only=True, target_import_compile_AST_probe_execution=False, executed_case_count=0, fixtures_created=False, scientific_body_decoded=False, runtime_observed=False, operational_cards_created=False, repository_or_git_mutated=False, root_owns_adjudication_repairs_admission_publication=True, ret_paused=True, immutable_after_seal=True))
if sorted(p.name for p in D.iterdir()) != namespace: raise ValueError('final namespace mismatch')
for row in payloads:
    if pure(identity(row['path'])) != row: raise ValueError('sealed payload drift')
print(json.dumps(dict(status='SEALED_SOURCE_REVIEW_REQUIRES_F01_F05_REPAIRS', namespace_count=len(namespace), payload_count=len(payloads), handoff=pure(identity(D / 'HANDOFF.json')), final_check=pure(identity(D / 'FINAL_IDENTITY_CHECK.json')), actual_controls=0), sort_keys=True))
