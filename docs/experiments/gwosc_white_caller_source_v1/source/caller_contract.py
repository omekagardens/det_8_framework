"""RI130 WHITE fabricated caller guards and capture/load source; UNEXECUTED.

This code creates no authorization. Root must separately authenticate every
admission and the already executing bootstrap bytes before this entry is used.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

CAP = 67108864
PHASE = 'fabricated_white_qualification'
CONTEXT = 'RI125_FABRICATED_ONLY_NOT_HISTORICAL'
CLAIM = 'Fixed fabricated WHITE qualification only; full32 application, actual data and physical claims remain unqualified; RET paused.'
LIMITS = {'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,
          'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05}
STAGE_LIMITS = {'seconds':180,'sampled_rss_kib':524288,'poll_ms':25,'max_gap_ms':100,
                'ps_timeout_ms':50,'file_bytes':CAP,'capture_row_bytes':8388608,'completed_integer_bits':262144}
TARGET_PIN = {'bytes':10760,'sha256':'69d927acb494c05ee45326b8e02159c99a583b7ee2533c947a1762b550b1ed83'}
HISTORY_PIN = {'bytes': 29806, 'sha256': 'f78ca32b9de47f5390d20c4de44a87aa462b871ba1b51b3bc1329e08c8c6aafa'}
MODULES = (
 ('white_kernel','science/primary/white_kernel.py'),
 ('white_path','science/primary/white_path.py'),
 ('white_controls','science/primary/white_controls.py'),
 ('white_fixtures','science/qualifier/white_fixtures.py'),
 ('kernel_controls','science/qualifier/kernel_controls.py'),
 ('white_validator','science/validator/white_validator.py'),
 ('validator_controls','science/validator/validator_controls.py'),
 ('qualify_white_only','science/qualifier/qualify_white_only.py'))
HELPERS = ('control.py','runtime_support.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py',
           'profile_observe.source-only.py','guard_controls.source-only.py',
           'TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json')
ROLE_FILES = {'white_kernel':'science/primary/white_kernel.py','white_path':'science/primary/white_path.py',
 'wrapper_controls':'science/primary/white_controls.py','white_contract':'science/primary/CONTRACT.md',
 'cases':'science/primary/CASES.md','kernel_refusals':'science/primary/KERNEL_REFUSALS.md',
 'fabricated_interfaces':'science/primary/FABRICATED_INTERFACES.md','white_refusals_text':'science/primary/WHITE_REFUSALS.md',
 'white_source_handoff':'science/primary/HANDOFF.json','fixtures':'science/qualifier/white_fixtures.py',
 'kernel_controls':'science/qualifier/kernel_controls.py','orchestrator':'science/qualifier/qualify_white_only.py',
 'stage_contract':'science/qualifier/STAGE_CONTRACT.md','control_expectations':'science/qualifier/CONTROL_EXPECTATIONS.json',
 'validator':'science/validator/white_validator.py','validator_controls':'science/validator/validator_controls.py'}

GUARD_IDS = tuple([side+'_'+kind for side in ('parent','worker') for kind in ('source','caller','runtime_acceptance','mode','late','late_postcheck')]
 +['capture_'+x for x in ('positive','changed_copy','buffer_drift','occupied')]
 +['monitor_'+x for x in ('positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap')]
 +['runtime_'+x for x in ('positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config')]
 +['static_'+x for x in ('positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command')]
 +['acceptance_'+x for x in ('positive','source_execution','caller_binding','caller_history','caller_ret','guards_absent','runtime_binding','runtime_loader','runtime_profile')]
 +['mode_'+x for x in ('normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift')]
 +['relation_'+x for x in ('positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped')])


def need(ok, message):
    if not ok: raise ValueError(message)


def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')


def same(left,right,message):
    need(canonical(left)==canonical(right),message)


def keys(value,names,message):
    need(type(value) is dict and set(value)==set(names),message)


def literal(value):
    need(type(value) is str,'literal path type')
    p=Path(value)
    need(p.is_absolute() and str(p)==value and p==p.resolve(),'literal resolved path required')
    return p


def pin(value):
    keys(value,('bytes','sha256'),'exact pin fields')
    need(type(value['bytes']) is int and 0<value['bytes']<=CAP and type(value['sha256']) is str
         and len(value['sha256'])==64 and all(c in '0123456789abcdef' for c in value['sha256']),'bounded exact pin')


def bounded_file_pin(path,C,empty=False):
    value=C.file_pin(path)
    need(type(value['bytes']) is int and (0 if empty else 1)<=value['bytes']<=CAP,'bounded current caller artifact')
    return value


def row_body(row,C):
    keys(row,('path','bytes','sha256'),'exact evidence reference')
    path=literal(row['path']);p={k:row[k] for k in ('bytes','sha256')};pin(p)
    return C.verified_body(path,p)


def parsed_row(row,C):
    body=row_body(row,C);value=C.parse_json(body)
    same(C.identity(body),C.identity(canonical(value)),'canonical metadata evidence required')
    return value


def source_declarations(root,C):
    t=C.parse_json(C.verified_body(root/'TARGET_CLOSURE.source-only.json',TARGET_PIN))
    h=C.parse_json(C.verified_body(root/'HISTORY_CLOSURE.source-only.json',HISTORY_PIN))
    need(t['schema']=='ri130-white-target-source-closure-v1' and t['status']=='UNEXECUTED_SOURCE_DECLARATION_ONLY','target source declaration')
    same(t['packet_counts'],{'primary':13,'validator':8,'qualifier':9},'complete target packet counts')
    need(len(t['sources'])==30 and len({x['relative'] for x in t['sources']})==30,'complete30 original/copy source records')
    sources=[{'relative':x['relative'],'original':x['original'],'copy':str(root/x['relative']),'pin':x['pin']} for x in t['sources']]
    return t,h,sources


def commands(root,interpreter,mode):
    need(mode in ('normal','optimized'),'fixed mode')
    prefix=[interpreter,'-I','-B']+(['-O'] if mode=='optimized' else [])
    freeze=str(root/'AUTHORIZED_FREEZE.json')
    return {'command':prefix+[str(root/'worker.py'),freeze,mode],
            'launcher_command':prefix+[str(root/'launch.py'),freeze,mode]}


def run_paths(root,interpreter,mode):
    directory=root/'runs'/mode
    return {**commands(root,interpreter,mode),'stdout':str(directory/'CALLER_ENVELOPE.json'),
            'stderr':str(directory/'stderr'),'worker_receipt':str(directory/'WORKER.json'),
            'receipt':str(directory/'SUPERVISOR.json'),'claim':str(directory/'ATTEMPT.json'),
            'custody':str(directory/'CUSTODY.json'),'stage':str(directory/'white-stage')}


def environment(root):
    return {'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(root/'tmp'),
            'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1',
            'VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}


def validate_static(m,root,C):
    keys(m,('schema','status','phase','context','claim','root','inputs','sources','helpers','limits','environment',
            'interpreter','runtime_inventory','expected_runtime','evidence','runs','mode_admissions'),'closed WHITE caller freeze')
    same([m['schema'],m['status'],m['phase'],m['context']],
         ['ri130-white-fabricated-freeze-v1','ROOT_AUTHORIZED_WHITE_FABRICATED_ONLY',PHASE,CONTEXT],'WHITE fabricated authorization boundary')
    same(m['claim'],CLAIM,'WHITE claim boundary');same(m['inputs'],[],'no actual scientific inputs')
    same(m['root'],str(root),'caller root binding');same(m['limits'],LIMITS,'unchanged supervisor limits')
    same(m['environment'],environment(root),'exact controlled environment')
    declaration,history,sources=source_declarations(root,C)
    same(m['sources'],sources,'complete exact30 original/copy sources')
    need(type(m['helpers']) is list and [Path(x['path']).name for x in m['helpers']]==list(HELPERS),'complete caller helper inventory')
    for entry,name in zip(m['helpers'],HELPERS):
        keys(entry,('path','pin'),'helper reference fields');pin(entry['pin'])
        same(entry['path'],str(root/name),'helper path binding')
    keys(m['evidence'],('integration','caller','runtime','guards'),'all independent acceptance prerequisites')
    same(m['evidence']['integration'],declaration['integrated_root'],'accepted RI128 integration identity')
    for row in m['evidence'].values():
        keys(row,('path','bytes','sha256'),'acceptance FilePin');pin({k:row[k] for k in ('bytes','sha256')});literal(row['path'])
    keys(m['runs'],('normal','optimized'),'both ordered mode domains')
    keys(m['mode_admissions'],('normal','optimized'),'separate mode admissions')
    for mode in ('normal','optimized'):
        same(m['runs'][mode],run_paths(root,m['interpreter']['named_path'],mode),'exact mode output/command namespace')
        same(m['mode_admissions'][mode],str(root/('ADMIT_'+mode.upper()+'.json')),'separate mode card path')
    return declaration,history


def source_admission(m,C):
    root=literal(m['root']);decl,history=validate_static(m,root,C)
    for row in history:
        keys(row,('path','bytes','sha256'),'opaque historical FilePin')
        need(type(row['bytes']) is int and 0<=row['bytes']<=CAP,'bounded historical byte length')
        need(type(row['sha256']) is str and len(row['sha256'])==64 and all(x in '0123456789abcdef' for x in row['sha256']),'historical sha256')
        C.verified_body(literal(row['path']),{k:row[k] for k in ('bytes','sha256')})
    integration=parsed_row(m['evidence']['integration'],C)
    need(integration['status']=='ACCEPT_BOUNDED_UNEXECUTED_WHITE_VALIDATOR_AND_QUALIFIER_INTEGRATION'
         and integration['source_execution'] is False and integration['qualification_accepted'] is False,'bounded source-only integration acceptance')
    caller=parsed_row(m['evidence']['caller'],C)
    keys(caller,('schema','status','helpers','sources','history','targets','limits','source_review','packet_handoff','target_executed','ret_paused'),'caller source acceptance fields')
    same(caller['schema'],'ri130-root-caller-source-review-v1','caller review schema')
    same(caller['status'],'ACCEPT_RI130_WHITE_FABRICATED_CALLER_SOURCE_ONLY','caller review status')
    for k in ('helpers','sources','limits'):same(caller[k],m[k],'caller reviewed '+k)
    same(caller['history'],HISTORY_PIN,'caller reviewed complete history');same(caller['targets'],TARGET_PIN,'caller reviewed complete targets')
    need(caller['target_executed'] is False and caller['ret_paused'] is True,'caller review execution boundary')
    row_body(caller['source_review'],C);row_body(caller['packet_handoff'],C)
    guards=parsed_row(m['evidence']['guards'],C)
    need(guards['schema']=='ri130-root-guard-qualification-v1' and guards['status']=='ACCEPT_EXACT_CALLER_GUARD_EXECUTION'
         and guards['helpers']==m['helpers'] and guards['all_declared_guards_passed'] is True
         and guards['scientific_targets_executed'] is False,'actual changed-caller guard qualification absent')
    report=parsed_row(guards['report'],C)
    same(report['schema'],'ri130-nonscientific-caller-guards-v1','changed guard report schema')
    same(report['control_order'],list(GUARD_IDS),'every declared caller guard ordered')
    same(report['counts'],{'total':len(GUARD_IDS),'passed':len(GUARD_IDS),'failed':0},'every declared caller guard count')
    need(report['status']=='all_declared_guards_passed' and report['helpers_unchanged'] is True
         and report['target_or_scientific_helper_imported'] is False
         and report['scientific_fixtures_or_controls_executed'] is False,'changed guard report scope/status')
    same([x['id'] for x in report['controls']],list(GUARD_IDS),'all actual guard records')
    need(all(x['passed'] is True for x in report['controls']),'all actual guard outcomes')
    helper_names=('control.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','runtime_support.py')
    helper_pins={Path(x['path']).name:x['pin'] for x in m['helpers'] if Path(x['path']).name in helper_names}
    same(report['helpers_before'],helper_pins,'actual guard helper identities')
    same(report['helpers_after'],helper_pins,'actual guard helper postchecks')
    row_body(guards['genuine_outer'],C);row_body(guards['independent_review'],C)
    runtime=parsed_row(m['evidence']['runtime'],C)
    need(runtime['schema']=='ri130-root-current-runtime-review-v1' and runtime['status']=='ACCEPT_CURRENT_WHITE_CALLER_RUNTIME'
         and runtime['helpers']==m['helpers'] and runtime['sources']==m['sources'],'current exact-target runtime applicability')
    for name in ('runtime_inventory','expected_runtime','interpreter'):same(runtime[name],m[name],'current runtime '+name)
    for name in ('complete_pure_python_stdlib','site_startup_surface_bound','non_os_shared_library_closure_bound',
                 'fresh_actual_profile_checked','source_cache_selection_checked','optional_native_namespaces_checked',
                 'observed_dyld_routes_checked','trusted_host_scope_explicit'):
        need(runtime[name] is True,'runtime premise missing: '+name)
    need(runtime['scientific_targets_executed'] is False,'runtime qualification is not science')
    for name in ('profile_normal','profile_optimized','profile_review','selection','optional_namespaces','observed_dyld_routes','host_scope'):
        row_body(runtime[name],C)
    return {'evidence':m['evidence'],'history':HISTORY_PIN,'targets':TARGET_PIN,'source_count':30,'inputs':[]}


def stage_bindings(m,C):
    decl,_,_=source_declarations(literal(m['root']),C)
    sources={r['relative']:r for r in m['sources']}
    values={role:{'path':sources[relative]['copy'],'pin':sources[relative]['pin']} for role,relative in ROLE_FILES.items()}
    row=decl['white_root'];values['white_root_disposition']={'path':row['path'],'pin':{k:row[k] for k in ('bytes','sha256')}}
    return values


def load_captured(name,path,body):
    need(name not in sys.modules,'captured module name already installed')
    spec=importlib.util.spec_from_file_location(name,path)
    need(spec is not None and spec.loader is not None,'captured module unavailable')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(body,str(path),'exec'),module.__dict__)
    return module


def load_helper(m,name,C):
    row=next(x for x in m['helpers'] if Path(x['path']).name==name)
    return load_captured('ri130_'+name.replace('.py',''),row['path'],C.verified_body(row['path'],row['pin']))


def capture_targets(m,C):
    by_name={x['relative']:x for x in m['sources']}
    # All complete executable bodies captured and pinned BEFORE the first target import.
    return {name:C.verified_body(by_name[relative]['copy'],by_name[relative]['pin']) for name,relative in MODULES}


def load_targets(m,captured,C,witness):
    by_name={x['relative']:x for x in m['sources']};modules={}
    need(all(name not in sys.modules for name,_ in MODULES),'target module namespace already occupied')
    for index,(name,relative) in enumerate(MODULES):
        row=by_name[relative];same(C.identity(captured[name]),row['pin'],'whole captured target pin')
        entry={'sequence':index,'module':name,'path':row['copy'],'pin':row['pin'],'state':'loading'};witness.append(entry)
        modules[name]=load_captured(name,row['copy'],captured[name]);entry['state']='loaded'
    return modules


def attempt_all(actions,first=None):
    records={}
    for name,fn in actions:
        try:records[name]={'value':fn(),'error':None}
        except BaseException as exc:
            records[name]={'value':None,'error':{'type':type(exc).__name__,'message':str(exc)[:2048]}}
            if first is None:first=exc
    return records,first


def same_after(actual,expected,label):
    same(actual,expected,label+' changed');return actual


def mode_admission(m,mode,C):
    path=literal(m['mode_admissions'][mode]);body=C.verified_body(path,bounded_file_pin(path,C));value=C.parse_json(body)
    same(body.decode('ascii'),canonical(value).decode('ascii'),'canonical mode admission')
    keys(value,('schema','status','mode','phase','freeze','caller_source_acceptance','command','launcher_command',
                'pre_runtime_metadata','normal_acceptance'),'separate mode card fields')
    expected={'schema':'ri130-root-white-mode-admission-v1','status':'AUTHORIZE_ONE_WHITE_FABRICATED_MODE',
              'mode':mode,'phase':PHASE,'freeze':C.file_pin(Path(m['root'])/'AUTHORIZED_FREEZE.json'),
              'caller_source_acceptance':m['evidence']['caller'],'command':m['runs'][mode]['command'],
              'launcher_command':m['runs'][mode]['launcher_command'],'pre_runtime_metadata':value['pre_runtime_metadata'],
              'normal_acceptance':value['normal_acceptance']}
    same(value,expected,'exact mode admission binding')
    pre=parsed_row(value['pre_runtime_metadata'],C)
    need(pre['schema']=='ri130-root-pre-mode-runtime-custody-v1' and pre['mode']==mode and pre['freeze']==value['freeze']
         and pre['runtime_acceptance']==m['evidence']['runtime'] and pre['selection_unchanged'] is True
         and pre['optional_namespaces_unchanged'] is True and pre['host_identity_unchanged'] is True,'fresh pre-mode runtime sidecars absent')
    row_body(pre['observed_dyld_routes'],C);row_body(pre['metadata_record'],C)
    if mode=='normal':need(value['normal_acceptance'] is None,'normal cannot claim future acceptance')
    else:
        normal=parsed_row(value['normal_acceptance'],C)
        need(normal['schema']=='ri130-root-normal-white-review-v1' and normal['status']=='ACCEPT_NORMAL_WHITE_EXECUTION_AND_CUSTODY'
             and normal['freeze']==value['freeze'] and normal['all15_cases_and_W09_assembly'] is True
             and normal['both179_controls'] is True and normal['complete_saved_reconstruction'] is True
             and normal['all57_artifacts_74_postchecks_3_trees'] is True and normal['runtime_post_custody_passed'] is True,'optimized lacks complete accepted normal predecessor')
        for name in ('genuine_outer','independent_review','post_runtime_metadata'):row_body(normal[name],C)
        for name in ('stdout','stderr','worker_receipt','receipt','custody','claim'):
            same(normal['outputs'][name],{'path':m['runs']['normal'][name],**C.file_pin(m['runs']['normal'][name])},'normal retained '+name)
    return {'path':str(path),'pin':C.identity(body),'value':value}
