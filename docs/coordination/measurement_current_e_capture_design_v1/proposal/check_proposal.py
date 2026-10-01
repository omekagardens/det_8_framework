"""RI236 administrative proposal check only. No subject imports or execution.
Reads a fixed explicit source/evidence list opaquely; selected administrative
records and this proposal only are JSON-decoded. Writes one exclusive report.
"""
from pathlib import Path
import hashlib
import json
import os
import shlex
import stat

W = Path(__file__).resolve().parent
B = W.parent.parent
R = B / 'ri234-root-reconciliation-tzop5ais'
P = B / 'ri141-white-bootstrap-source-h58ls076'
A = B / 'ri160-white-fixture-custody-repair-ufok1zpo'
H = B / 'ri170-current-e-root-records-proposed-gikj2giy'
labels = []
observed = {}

def need(ok, label):
    labels.append(label)
    if not ok:
        raise ValueError(label)

def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')

def state(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def raw(path):
    p = Path(path)
    info = p.lstat()
    need(p.is_absolute() and p.resolve(strict=True)==p and stat.S_ISREG(info.st_mode), 'literal regular '+str(p))
    need(0<=info.st_size<=67108864, 'bounded file '+str(p))
    with p.open('rb') as stream:
        need(state(os.fstat(stream.fileno()))==state(info), 'opened stable '+str(p))
        data = stream.read(67108865)
        need(state(os.fstat(stream.fileno()))==state(info), 'descriptor stable '+str(p))
    need(len(data)==info.st_size and state(p.lstat())==state(info), 'final stable '+str(p))
    value = dict(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),state=state(info))
    if str(p) in observed: need(observed[str(p)]==value, 'repeat entire identity '+str(p))
    observed[str(p)] = value
    return data

def pin(path):
    data=raw(path)
    return dict(path=str(path),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())

def load(path):
    def pairs(items):
        result={}
        for k,v in items:
            need(k not in result, 'unique administrative key')
            result[k]=v
        return result
    def nonfinite(value): raise ValueError('nonfinite administrative token '+value)
    data=raw(path);value=json.loads(data,object_pairs_hook=pairs,parse_constant=nonfinite)
    need(canonical(value)==data, 'canonical administrative record '+str(path))
    return value

def same(a,b,label): need(canonical(a)==canonical(b),label)

def fields(value,names,label): same(sorted(value),sorted(names),label)

def main():
    recipe=load(W/'CAPTURE_RECIPE.json');contract=load(W/'CURRENT_E_AND_MODE_CONTRACT.json')
    closure=load(W/'DEPENDENCIES.json');correspondence=load(W/'SOURCE_CORRESPONDENCE.json')
    selecting=load(R/'RI236_MEASUREMENT_NEXT_STEP.json');old=load(H/'ADMIT_CAPTURE.json')
    deps=load(P/'DEPENDENCIES.source-only.json');aset=load(A/'SOURCE_SET.json')
    need(recipe['status']=='PROPOSAL_ONLY_NOT_A_CAPTURE_ADMISSION' and recipe['operationally_usable'] is False,'no live admission')
    need(contract['status']=='PROSPECTIVE_COMPLETE_CONTRACT_NOT_ACCEPTANCE','no mode authority')
    same(recipe['selection'],pin(R/'RI236_MEASUREMENT_NEXT_STEP.json'),'exact selection')
    same(recipe['frozen_acceptance'],selecting['predecessor'],'accepted current frozen prerequisite')
    acceptance=load(recipe['frozen_acceptance']['path'])
    need(acceptance['status']=='ACCEPT_CURRENT_FROZEN_CUSTODY_BY_READ_ONLY_RECONCILIATION' and acceptance['original_installation_retroactively_accepted'] is False,'actual acceptance boundary')
    same(recipe['bounds'],old['bounds'],'all ten original bounds unchanged')
    fields(recipe['admission_field_recipe'],old,'exact17-field card recipe')
    need(len(old)==recipe['future_card_field_count']==17,'seventeen actual fields')
    for name in recipe['four_null_predecessors']:same(recipe['admission_field_recipe'][name],{'literal':None},'null predecessor '+name)
    same(recipe['admission_field_recipe']['phase'],{'literal':'capture'},'capture only')
    changes={'output','source_review','bootstrap_host_preflight','bootstrap','host'}
    for name in set(old)-changes:same(recipe['admission_field_recipe'][name],{'literal':old[name]},'fixed historical field '+name)
    same(recipe['source_roles'],{name:{k:pin(P/name)[k] for k in ('bytes','sha256')} for name in old['sources']},'unchanged three source roles')
    same(recipe['admission_field_recipe']['bootstrap']['fresh_observation_equals_historical'],old['bootstrap'],'correct bootstrap shape')
    same(recipe['admission_field_recipe']['host']['fresh_observation_equals_historical'],old['host'],'exact host target')
    same(recipe['admission_field_recipe']['bootstrap_host_preflight']['selected_interpreter_binding_exact_historical'],deps['selected_bootstrap_binding'],'exact actual required selection')
    env=recipe['environment'];need(len(env)==10 and env['TMPDIR']==recipe['paths']['environment_root']+'/tmp','exact10 E environment')
    normal=load(closure['roles']['normal_completion']['path']);same(env,normal['environment'],'accepted exact current-E environment')
    same(contract['baseline'],normal['artifacts']['PRE'],'literal genuine normal baseline reference')
    same(contract['actual_runtime_record']['baseline'],contract['baseline'],'same baseline at13-field contract')
    vendor=old['bootstrap']['named_path'];card=recipe['paths']['future_admission']
    same(recipe['parent_command'],[vendor,'-I','-B',str(P/'prepare.py'),'--admission',card],'exact unchanged parent')
    same(recipe['snapshot_child_command'],[vendor,'-I','-B',str(P/'prepare.py'),'--snapshot',card],'exact unchanged children')
    same(recipe['cwd']['outer'],str(W.parent),'outerD')
    same(recipe['cwd']['PRE_POST_children'],recipe['paths']['capture_output'],'child cwd output')
    vector=['/usr/bin/env','-i']+[k+'='+env[k] for k in sorted(env)]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;']+recipe['parent_command']
    same(recipe['outer_argv'],vector,'whole outer vector')
    same(recipe['proposed_exec_command_arguments'],{'cmd':shlex.join(vector),'workdir':str(W.parent),'login':False,'yield_time_ms':1000,'max_output_tokens':4000},'literal genuine tool proposal')
    expected_files=sorted(['ATTEMPT.json','CHECKS.json','NAMESPACE.json','COMPLETE.json']+[label+suffix for label in ('PRE','POST') for suffix in ('.ATTEMPT.json','.COMPLETION.json','.stdout','.stderr')])
    same(contract['capture_outputs'],expected_files,'exact12 outputs')
    need(len(contract['capture_completion_fields'])==len(set(contract['capture_completion_fields']))==17,'whole17 completion')
    need(len(contract['capture_artifact_roles'])==6,'six artifact roles')
    same(contract['namespace_exclusions'],['NAMESPACE.json','COMPLETE.json'],'exacttwo exclusions')
    for name,n in [('actual_runtime_record',13),('pre_mode_request',5),('pre_mode_result',9),('mode_card_request',4),('mode_card_candidate',10)]:
        need(len(contract[name]['fields'])==len(set(contract[name]['fields']))==n,'closed mode fields '+name)
    same(contract['mode_card_request']['normal_acceptance'],None,'no future normal acceptance')
    same(contract['current_E']['accepted_frozen_observation'],acceptance['frozen_observation'],'whole frozen predecessor')
    need(contract['current_E']['files']==49 and contract['current_E']['directories_including_root']==9,'frozenE49/9')
    transition=contract['card_insertion_is_later']
    need(transition['before_files']==49 and transition['after_files']==50 and transition['directories']==9 and transition['sole_added_member']=='ADMIT_NORMAL.json','exact later onefile transition')
    need(transition['no_cross_write_directory_nlink_equality'] and transition['no_predicted_nlink_increment'] and transition['root_device_inode_mode_unchanged'] and transition['all_prior_files_and_nonroot_directories_unchanged'],'strict platform-aware transition')
    sets=closure['role_sets']
    same(sets['ri141_opaque_dependencies_442'],deps['opaque_files'],'all442 in order')
    same(sets['ri160_opaque_dependencies_567'],aset['dependencies'],'all567 in order')
    oldsources=load(closure['roles']['accepted_reconciliation_sources']['path'])
    same(sets['reconciliation_source_roles_971'],[{k:r[k] for k in ('path','bytes','sha256')} for r in oldsources],'all971 prior roles in order')
    union={}
    for name,rows in sets.items():
        need(closure['counts'][name]==len(rows),'role count '+name)
        for row in rows:
            if row['path'] in union:same(union[row['path']],row,'compatible repeated source role')
            union[row['path']]=row
    same(closure['unique'],sorted(union.values(),key=lambda r:r['path']),'whole declared union')
    need(closure['counts']['unique']==len(union)==986,'986 fixed inputs')
    for row in closure['unique']:same(pin(row['path']),row,'opaque whole bound input '+row['path'])
    for role,row in closure['roles'].items():same(union[row['path']],row,'all direct role references '+role)
    for row in correspondence['entries']:
        data=raw(row['source']['path']);piece=b''.join(data.splitlines(keepends=True)[row['first_line']-1:row['last_line']])
        same({'bytes':len(piece),'sha256':hashlib.sha256(piece).hexdigest()},row['span'],'literal source read slice '+row['role'])
    prepare=raw(P/'prepare.py').decode('utf-8');mode=raw(A/'mode_verify.py').decode('utf-8')
    for token in ['cwd=out, env=env, start_new_session=True','if phase == \'capture\':','before = snapshot(\'PRE\')','after = snapshot(\'POST\')']:
        need(token in prepare,'literal retained execution boundary '+token)
    need("IO.same(snapshot,baseline,'whole current metadata equals accepted new-environment baseline')" in mode,'whole external mode baseline guard')
    proposal_files=['CAPTURE_RECIPE.json','CURRENT_E_AND_MODE_CONTRACT.json','DEPENDENCIES.json','SOURCE_CORRESPONDENCE.json','PROTOCOL.md','check_proposal.py']
    proposal_pins=[pin(W/name) for name in proposal_files]
    for path,value in list(observed.items()):need(state(Path(path).lstat())==value['state'],'final stable observation '+path)
    result={'schema':'ri236-actual-administrative-proposal-check-v1','status':'PASS_SOURCE_RECIPE_METADATA_ONLY','predicates':len(labels),'checks':labels,'observed_files':list(observed.values()),'counts':{'distinct_files':len(observed),'fixed_dependency_union':986,'capture_card_fields':17,'capture_outputs':12,'capture_artifact_roles':6,'capture_children':2,'runtime_record_fields':13,'pre_mode_request_fields':5,'pre_mode_result_fields':9,'mode_card_candidate_fields':10},'proposal_pins':proposal_pins,'current_runtime_or_E_inventory_observed':False,'target_or_proposal_execution':False,'operational_files_created':False,'scientific_body_decoded':False,'admission_issued':False}
    encoded=canonical(result)
    with (W/'CHECK_RESULT.json').open('xb') as f:f.write(encoded);f.flush();os.fsync(f.fileno())
    need((W/'CHECK_RESULT.json').read_bytes()==encoded,'exact report readback')
    print(json.dumps({'report':{'path':str(W/'CHECK_RESULT.json'),'bytes':len(encoded),'sha256':hashlib.sha256(encoded).hexdigest()},'report_predicates':result['predicates'],'plus_report_readback':1,'distinct_files':len(observed),'status':result['status']}))

if __name__=='__main__':
    main()
