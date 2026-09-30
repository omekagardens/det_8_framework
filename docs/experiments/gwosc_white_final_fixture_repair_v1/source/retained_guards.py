"""RI130 isolated nonscientific caller controls, UNEXECUTED source.

Run only under a separately authenticated root guard admission. Imports only
caller/runtime helpers, never any WHITE target or scientific helper. Metadata
doubles intentionally exercise framing/custody rather than scientific truth.
All fixture trees and every failed control remain retained. No cleanup/retry.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

HELPERS=('control.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','runtime_support.py')
BODIES={}


def need(ok,message):
    if not ok:raise ValueError(message)


def canonical(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def pin(path):
    path=Path(path);need(path==path.resolve() and path.is_file() and not path.is_symlink(),'regular literal guard file')
    body=path.read_bytes();return {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}


def module(path,name):
    # Bodies were all captured and checked against the externally admitted packet
    # before the first helper import. These are nonscientific helper bodies only.
    path=Path(path);body=BODIES[path.name]
    need(pin(path)=={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()},'captured guard helper drift')
    spec=importlib.util.spec_from_file_location(name,path);value=importlib.util.module_from_spec(spec)
    sys.modules[name]=value
    exec(compile(body,str(path),'exec'),value.__dict__)
    return value


def refusal(action,message):
    try:action()
    except ValueError as exc:
        need(str(exc)==message,'unexpected first message: '+str(exc));return
    raise ValueError('expected refusal absent: '+message)


def failure_case(packet,base,side,reason,postfail=False):
    root=Path(tempfile.mkdtemp(prefix=side+'-'+reason+'-',dir=base));(root/'runs'/'normal').mkdir(parents=True);(root/'tmp').mkdir()
    C=module(packet/'control.py','guard_failure_control')
    K=module(packet/'caller_contract.py','guard_failure_contract')
    W=module(packet/'worker.py','guard_failure_worker');L=module(packet/'launch.py','guard_failure_launch')
    m={'root':str(root),'runs':{'normal':K.run_paths(root,'/nonexecuted/guard-interpreter','normal')},'limits':dict(K.LIMITS),
       'environment':K.environment(root),'sources':[],'helpers':[]}
    freeze=root/'AUTHORIZED_FREEZE.json';freeze.write_bytes(canonical({'guard_metadata_double_only':True}))
    counts={'helpers':0,'runtime':0,'profile':0,'loaded':0,'sources':0,'science':0,'child':0}
    expected='isolated_'+reason
    def sources(manifest):
        counts['sources']+=1
        if reason=='source':raise ValueError(expected)
        return [{'guard_only':True}]
    def admission(manifest,ctrl):
        if reason in ('caller','runtime_acceptance'):raise ValueError(expected)
        return {'guard_only':'source/runtime acceptances substituted'}
    def mode_admission(manifest,mode,ctrl):
        if reason=='mode':raise ValueError(expected)
        return {'guard_only':'mode acceptance substituted'}
    def verify(manifest,ctrl):
        counts['runtime']+=1
        if postfail and counts['runtime']>1:raise ValueError('isolated_runtime_tail_failure')
        return {'guard_only':'runtime verification substituted'}
    def profile(manifest,mode,ctrl):counts['profile']+=1;return {'guard_only':'profile substituted'}
    def loaded(manifest,ctrl):
        counts['loaded']+=1
        if counts['loaded']==1:raise ValueError(expected)
        return {'guard_only':'loaded-file observation substituted'}
    runtime=SimpleNamespace(verify=verify,profile=profile,loaded_files=loaded)
    def helper(manifest,name,ctrl):
        counts['helpers']+=1
        return runtime if name=='runtime_support.py' else SimpleNamespace()
    def no_science(*args,**kwargs):counts['science']+=1;raise ValueError('forbidden scientific entry in caller control')
    def no_child(*args,**kwargs):counts['child']+=1;raise ValueError('forbidden child in caller control')
    C.verify_sources=sources;K.source_admission=admission;K.mode_admission=mode_admission;K.load_helper=helper;K.capture_targets=no_science
    with patch.object(L.subprocess,'Popen',no_child):
        code=(W.execute if side=='worker' else L.launch)(m,'normal',C,K,C.file_pin(freeze))
    name='worker_receipt' if side=='worker' else 'receipt';path=Path(m['runs']['normal'][name]);record=C.parse_json(path.read_bytes())
    checks={'refused':code==1,'first_error_preserved':record['error']=={'type':'ValueError','message':expected},
            'no_scientific_entry':counts['science']==0,'no_child':counts['child']==0,'both_source_attempts':counts['sources']==2}
    if reason!='late':checks.update(no_first_helper_in_tail=counts['helpers']==0,no_runtime_in_tail=counts['runtime']==0)
    else:
        checks.update(retained_runtime_attempted_twice=counts['runtime']==2,profile_attempted_twice=counts['profile']==2,
                      loaded_attempted_twice=counts['loaded']==2)
        if postfail:checks['tail_error_retained']=record['postchecks']['runtime']['error']=={'type':'ValueError','message':'isolated_runtime_tail_failure'}
    need(all(checks.values()),'caller failure-order or independent-tail regression')
    return {'checks':checks,'counts':counts,'receipt':{'path':str(path),**pin(path)}}


def capture_case(packet,kind):
    C=module(packet/'control.py','guard_capture_control');K=module(packet/'caller_contract.py','guard_capture_contract')
    m={'sources':[{'relative':rel,'copy':'/opaque-guard/'+name,'pin':C.identity(b'opaque-'+name.encode())} for name,rel in K.MODULES]}
    expected={name:b'opaque-'+name.encode() for name,_ in K.MODULES};reads=[];loads=[]
    def body(path,want):
        name=Path(path).name;reads.append(name)
        if kind=='changed_copy' and name=='kernel_controls':raise ValueError('isolated copy drift')
        value=expected[name];K.same(C.identity(value),want,'opaque capture pin');return value
    C.verified_body=body
    if kind=='changed_copy':refusal(lambda:K.capture_targets(m,C),'isolated copy drift');need(not loads,'load before full capture');return {'reads':reads,'loads':loads}
    captured=K.capture_targets(m,C)
    need(reads==[x[0] for x in K.MODULES],'all8 captures before first load')
    if kind=='buffer_drift':captured['white_kernel']=b'changed';refusal(lambda:K.load_targets(m,captured,C,[]),'whole captured target pin')
    elif kind=='occupied':
        with patch.dict(sys.modules,{'white_kernel':SimpleNamespace()}):
            refusal(lambda:K.load_targets(m,captured,C,[]),'target module namespace already occupied')
    else:
        def load(name,path,body):
            need(len(reads)==8,'first load preceded whole capture');loads.append(name);return SimpleNamespace(__file__=path)
        K.load_captured=load;witness=[];K.load_targets(m,captured,C,witness)
        need(loads==[x[0] for x in K.MODULES] and all(x['state']=='loaded' for x in witness),'complete capture/load witness')
    return {'reads':reads,'loads':loads,'scientific_module_imported':False}


def monitor_case(packet,kind):
    M=module(packet/'monitor.py','guard_monitor');clock=[0.0];signals=[];observations=[]
    record={'samples':[],'monitor_attempts':[],'peak_sampled_rss_kib':0,'child_exit_code':None,'child_elapsed_seconds':None,'stop_reason':None}
    class Child:
        pid=424242
        done=(kind=='no_sample')
        def poll(self):return 0 if self.done else None
        def wait(self):self.done=True;return 0
    child=Child()
    def now():
        if kind=='wall':return 181.0
        if kind=='initial_gap':return 0.101
        return clock[0]
    def ps(argv,**kwargs):
        need(argv==['/bin/ps','-o','rss=','-p','424242'] and kwargs['timeout']==0.05 and kwargs['check'] is False,'exact monitor route/deadline')
        observations.append(argv)
        if kind=='timeout':raise subprocess.TimeoutExpired(argv,0.05,output=b'partial',stderr=b'timed out')
        if kind=='sample_gap':clock[0]=0.101
        else:clock[0]+=0.001
        if kind=='positive':child.done=True
        if kind=='final_gap':child.done=True;clock[0]=0.001
        return SimpleNamespace(returncode=1 if kind=='nonzero' else 0,stdout=b'bad' if kind=='malformed' else (b'524289' if kind=='rss' else b'1'),stderr=b'')
    def kill(pid,sig):need(pid==child.pid,'only owned group');signals.append(pid);child.done=True
    observed=None
    with patch.object(M.time,'monotonic',now),patch.object(M.time,'sleep',lambda value:clock.__setitem__(0,clock[0]+value)),patch.object(M.subprocess,'run',ps),patch.object(M.os,'killpg',kill):
        try:
            M.supervise(child,record,0.0)
            if kind=='final_gap':
                # Exercise the actual final-gap guard with the same owned child;
                # the initial pass is a positive sampled completion.
                record['child_elapsed_seconds']=0.102;record['stop_reason']=None;M.reap_owned(child,record,0.0)
        except BaseException as exc:
            observed={'type':type(exc).__name__,'message':str(exc)};M.reap_owned(child,record,0.0)
    reasons={'positive':None,'no_sample':'no_rss_sample','wall':'wall_time_limit','initial_gap':'rss_sample_deadline_missed',
       'sample_gap':'rss_sample_deadline_missed','rss':'sampled_resident_memory_limit','nonzero':'rss_monitor_unavailable',
       'malformed':'rss_monitor_unavailable','timeout':'no_rss_sample','final_gap':'rss_final_sample_deadline_missed'}
    need(record['stop_reason']==reasons[kind] and record['child_exit_code']==0,'actual monitor refusal/completion semantics')
    if kind=='timeout':need(observed and observed['type']=='TimeoutExpired' and record['monitor_attempts'][0]['stdout']=='partial','timeout diagnostic preserved')
    else:need(observed is None,'unexpected monitor exception')
    return {'record':record,'observed_exception':observed,'owned_signals':signals,'actual_child_started':False}


def runtime_case(packet,base,kind):
    root=Path(tempfile.mkdtemp(prefix='runtime-'+kind+'-',dir=base))
    control=module(packet/'control.py','ri121_fixture_runtime_control')
    runtime=module(packet/'runtime_support.py','ri121_fixture_runtime')
    roots=[root/'stdlib',root/'venv_site',root/'system_site']
    for path in roots:path.mkdir()
    (roots[0]/'tiny.py').write_bytes(b'fixture only\n')
    config=root/'openssl.cnf';config.write_bytes(b'# isolated inactive configuration\n')
    lib=root/'libcrypto.fixture';lib.write_bytes(b'not an executable library\n')
    alias=root/'libcrypto.alias';alias.symlink_to(lib.name)
    absent=[str(root/('absent-'+str(i))) for i in range(8)]
    binding=control.binding(str(alias))
    runtime.ROOTS=[str(x) for x in roots];runtime.REQUIRED_FILES=[str(config)]
    runtime.ALLOWED_LINKS=[];runtime.ABSENT_PATHS=absent;runtime.REQUIRED_LOADER_BINDINGS=[binding]
    inventory={'schema':'ri121-complete-stdlib-runtime-inventory-v2','roots':runtime.ROOTS,
               'extra_files':sorted([str(config),str(lib)]),'files':[], 'symlinks':[],
               'absent_paths':absent,'loader_bindings':[binding],'scope':'isolated nonscientific regression fixture'}
    expected=None
    if kind=='absent_file':Path(absent[1]).write_bytes(b'appeared\n');expected='previously absent startup/import/loader path appeared'
    elif kind=='absent_dangling_link':Path(absent[1]).symlink_to('missing');expected='previously absent startup/import/loader path appeared'
    elif kind=='missing_loader':inventory['loader_bindings']=[];expected='mandatory loader binding omitted or changed'
    elif kind=='changed_loader_declaration':inventory['loader_bindings']=[{**binding,'resolved_path':str(root/'wrong')}];expected='mandatory loader binding omitted or changed'
    elif kind=='changed_loader_path':
        other=root/'other-lib';other.write_bytes(b'changed\n');alias.unlink();alias.symlink_to(other.name);expected='non-OS loader binding changed'
    elif kind=='missing_config':inventory['extra_files'].remove(str(config));expected='interpreter/framework/monitor/config runtime files omitted'
    observed=None;rows=None
    try:
        rows=runtime.scan(inventory,control)
        if kind=='positive':
            inventory['files']=rows
            ip=root/'fixture-inventory.json';ip.write_bytes(canonical(inventory))
            executable=root/'interpreter.fixture';executable.write_bytes(b'not executable\n')
            manifest={'runtime_inventory':{'path':str(ip),'pin':pin(ip)},'interpreter':control.binding(str(executable))}
            result=runtime.verify(manifest,control)
            need(result['runtime_files_count']==3,'fixture verify count differs')
    except BaseException as exc:observed={'type':type(exc).__name__,'message':str(exc)}
    passed=(observed is None and rows is not None) if expected is None else observed=={'type':'ValueError','message':expected}
    return {'id':'runtime_'+kind,'fixture_root':str(root),'pass':passed,'expected_failure':expected,'observed_failure':observed,
            'actual_scanner_and_verify_used':True,'substituted_domain_constants':['ROOTS','REQUIRED_FILES','ALLOWED_LINKS','ABSENT_PATHS','REQUIRED_LOADER_BINDINGS']}


def static_case(packet,kind):
    C=module(packet/'control.py','guard_static_control');K=module(packet/'caller_contract.py','guard_static_contract')
    declaration,history,sources=K.source_declarations(packet,C)
    ref={'path':str(packet/'TARGET_CLOSURE.source-only.json'),**pin(packet/'TARGET_CLOSURE.source-only.json')}
    m={'schema':'ri130-white-fabricated-freeze-v1','status':'ROOT_AUTHORIZED_WHITE_FABRICATED_ONLY',
       'phase':K.PHASE,'context':K.CONTEXT,'claim':K.CLAIM,'root':str(packet),'inputs':[],
       'sources':sources,'helpers':[{'path':str(packet/name),'pin':pin(packet/name)} for name in K.HELPERS],
       'limits':dict(K.LIMITS),'environment':K.environment(packet),'interpreter':{'named_path':'/nonexecuted/guard-interpreter'},
       'runtime_inventory':{},'expected_runtime':{},'evidence':{'integration':declaration['integrated_root'],'caller':ref,'runtime':ref,'guards':ref},
       'runs':{mode:K.run_paths(packet,'/nonexecuted/guard-interpreter',mode) for mode in ('normal','optimized')},
       'mode_admissions':{mode:str(packet/('ADMIT_'+mode.upper()+'.json')) for mode in ('normal','optimized')}}
    # This is an in-memory guard double, never serialized as an active card.
    message=None
    if kind=='actual':m['phase']='actual';message='WHITE fabricated authorization boundary'
    elif kind=='extra':m['extra']=True;message='closed WHITE caller freeze'
    elif kind=='bool_limit':m['limits']['wall_seconds']=True;message='unchanged supervisor limits'
    elif kind=='source_omitted':m['sources']=m['sources'][:-1];message='complete exact30 original/copy sources'
    elif kind=='source_copy':m['sources']=copy.deepcopy(m['sources']);m['sources'][0]['copy']+='-wrong';message='complete exact30 original/copy sources'
    elif kind=='helper_omitted':m['helpers']=m['helpers'][:-1];message='complete caller helper inventory'
    elif kind=='mode_command':m['runs']['optimized']['command'].remove('-O');message='exact mode output/command namespace'
    if message:refusal(lambda:K.validate_static(m,packet,C),message)
    else:K.validate_static(m,packet,C)
    return {'actual_static_validator_used':True,'card_written':False,'kind':kind}


def acceptance_case(packet,kind):
    C=module(packet/'control.py','guard_acceptance_control');K=module(packet/'caller_contract.py','guard_acceptance_contract')
    m={'root':str(packet),'helpers':[],'sources':[],'limits':dict(K.LIMITS),'runtime_inventory':{},'expected_runtime':{},'interpreter':{},
       'evidence':{x:{'path':'/guard/'+x} for x in ('integration','caller','runtime','guards')}}
    opaque={'path':'/guard/opaque'}
    caller={'schema':'ri130-root-caller-source-review-v1','status':'ACCEPT_RI130_WHITE_FABRICATED_CALLER_SOURCE_ONLY',
       'helpers':[],'sources':[],'limits':dict(K.LIMITS),'history':K.HISTORY_PIN,'targets':K.TARGET_PIN,
       'source_review':opaque,'packet_handoff':opaque,'target_executed':False,'ret_paused':True}
    runtime={'schema':'ri130-root-current-runtime-review-v1','status':'ACCEPT_CURRENT_WHITE_CALLER_RUNTIME',
       'helpers':[],'sources':[],'runtime_inventory':{},'expected_runtime':{},'interpreter':{},'scientific_targets_executed':False}
    for field in ('complete_pure_python_stdlib','site_startup_surface_bound','non_os_shared_library_closure_bound','fresh_actual_profile_checked',
       'source_cache_selection_checked','optional_native_namespaces_checked','observed_dyld_routes_checked','trusted_host_scope_explicit'):runtime[field]=True
    for field in ('profile_normal','profile_optimized','profile_review','selection','optional_namespaces','observed_dyld_routes','host_scope'):runtime[field]=opaque
    values={'integration':{'status':'ACCEPT_BOUNDED_UNEXECUTED_WHITE_VALIDATOR_AND_QUALIFIER_INTEGRATION','source_execution':False,'qualification_accepted':False},
       'caller':caller,'runtime':runtime,'guards':{'schema':'ri130-root-guard-qualification-v1','status':'ACCEPT_EXACT_CALLER_GUARD_EXECUTION',
       'helpers':[],'all_declared_guards_passed':True,'scientific_targets_executed':False,'report':{'path':'/guard/guard_report'},'genuine_outer':opaque,'independent_review':opaque}}
    values['guard_report']={'schema':'ri130-nonscientific-caller-guards-v1','control_order':list(K.GUARD_IDS),'counts':{'total':len(K.GUARD_IDS),'passed':len(K.GUARD_IDS),'failed':0},
       'status':'all_declared_guards_passed','helpers_unchanged':True,'target_or_scientific_helper_imported':False,'scientific_fixtures_or_controls_executed':False,
       'controls':[{'id':x,'passed':True} for x in K.GUARD_IDS],'helpers_before':{},'helpers_after':{}}
    message=None
    if kind=='source_execution':values['integration']['source_execution']=True;message='bounded source-only integration acceptance'
    elif kind=='caller_binding':caller['sources']=[{}];message='caller reviewed sources'
    elif kind=='caller_history':caller['history']={};message='caller reviewed complete history'
    elif kind=='caller_ret':caller['ret_paused']=False;message='caller review execution boundary'
    elif kind=='guards_absent':values['guards']['all_declared_guards_passed']=False;message='actual changed-caller guard qualification absent'
    elif kind=='runtime_binding':runtime['helpers']=[{}];message='current exact-target runtime applicability'
    elif kind=='runtime_loader':runtime['observed_dyld_routes_checked']=False;message='runtime premise missing: observed_dyld_routes_checked'
    elif kind=='runtime_profile':runtime['expected_runtime']={'bad':True};message='current runtime expected_runtime'
    K.validate_static=lambda manifest,root,ctrl:({},[])
    K.parsed_row=lambda row,ctrl:values[Path(row['path']).name]
    reads=[];K.row_body=lambda row,ctrl:reads.append(row['path'])
    if message:refusal(lambda:K.source_admission(m,C),message)
    else:K.source_admission(m,C);need(len(reads)==11,'all caller/guard/runtime evidence references')
    return {'actual_source_acceptance_semantics_used':True,'opaque_io_and_static_layer_substituted':True,'reads':reads}


def metadata_stage(root,packet,C,K,E,marker='same',bad_link=False):
    """Isolated metadata double ONLY: no scientific recipe/validator is called."""
    root.mkdir()
    spec_path=packet/'science/qualifier/CONTROL_EXPECTATIONS.json';spec=C.parse_json(spec_path.read_bytes())
    source_roles=tuple(K.ROLE_FILES)+('white_root_disposition',)
    bindings={name:{'path':str(spec_path),'pin':C.file_pin(spec_path)} for name in source_roles}
    def save(name,value):
        (root/name).write_bytes(canonical(value));return {'name':name,'pin':C.file_pin(root/name)}
    for name in E.CASE_FILES:
        body={'isolated_nonscientific_caller_guard':True,'marker':marker if name in ('W11-primary.json','W11-independent.json') else 'same'}
        if name=='W09-operand.json':body['gram']={'isolated_guard_gram':True}
        save(name,body)
    save(E.ASSEMBLY_FILES[0],{'isolated_guard_capture':True})
    for name in E.ASSEMBLY_FILES[1:]:save(name,{'isolated_guard_assembly':True})
    for tree,name in zip(E.TREES,E.TREE_FILES):
        directory=root/tree;directory.mkdir()
        if tree in E.TREES[1:]:
            seed=directory/'WC19-seed.fabricated';seed.write_bytes(b'a')
            (directory/'WC19-link.fabricated').symlink_to(str(seed)+('-wrong' if bad_link else ''))
        save(name,E.tree_snapshot(directory,C))
    posts=[{'role':'first','pin':None,'unchanged':False,'error':'GUARD ONLY: changed'},
           {'role':'second','pin':C.identity(b'b'),'unchanged':True,'error':None}]
    controls=[{'id':x['id'],'expected_code':x['code'],'expected_message':x['message'],'observed_code':x['code'],
               'observed_message':x['message'],'passed':True} for x in spec['refusals']]
    controls.append({'id':'WT01','passed':True,'postchecks':posts})
    for identifier,code,message in (('WT02','EXACT','first-error'),('WT03','CUSTODY','one or more final source/input postchecks failed')):
        controls.append({'id':identifier,'passed':True,'refusal':{'schema':'ri125-application-refusal-v1','status':'REFUSED','phase':'fixed_saved_application',
         'stage':'white','code':code,'message':'GUARD ONLY: '+code+': '+message,'scientific_disposition_emitted':False,'postchecks':posts}})
    def control(schema,rows,independent=False):return {'schema':schema,'phase':'fabricated_qualification','context':E.CONTEXT,
       'actual_scientific_input_opened':False,'independent_validator_run':independent,'controls':rows,
       'counts':{'total':len(rows),'passed':len(rows),'failed':0},'status':'all_declared_controls_passed'}
    save(E.CONTROL_FILES[0],control('ri125-primary-kernel-controls-v1',controls[:37]))
    save(E.CONTROL_FILES[1],control('ri125-primary-white-controls-v1',controls[37:]))
    save(E.CONTROL_FILES[2],control('ri125-primary-complete-white-controls-v1',controls))
    save(E.CONTROL_FILES[3],control('ri125-independent-white-controls-v1',controls,True))
    def ref(name):return {'name':name,'pin':C.file_pin(root/name)}
    cases=[]
    six=['fixed_operand_schema_and_recipe','complete_result_shape','literal_case_anchor','full_directed_shift_consistency','correct_gram_presence_and_inherited_gate','correct_response_presence_and_new_gate']
    four=['fixed_bound_operand_recipe','complete_bound_result_shape','literal_predicate_results','fabricated_identity_only']
    for i,cid in enumerate(E.CASE_IDS,1):
        ids=four if i==10 else six
        cases.append({'id':cid,'kind':'bound_predicate_only' if i==10 else 'white_primitive','operand':ref(f'W{i:02d}-operand.json'),
          'primary':ref(f'W{i:02d}-primary.json'),'independent':ref(f'W{i:02d}-independent.json'),'full_fields_match':True,
          'expected_checks':{'inventory':ids,'counts':{'total':len(ids),'passed':len(ids),'failed':0},'results':[{'id':x,'passed':True} for x in ids]}})
    save('FRESH_SAVED_COMPARISON.json',{'schema':'ri125-white-only-fresh-saved-comparison-v1','phase':'fabricated_qualification',
      'cases':[{'id':row['id'],'fresh_result_pin':row['independent']['pin'],'all_fields_match':True} for row in cases],
      'assembly':{'id':E.CASE_IDS[8],'fresh_result_pin':ref(E.ASSEMBLY_FILES[2])['pin'],'all_fields_match':True},
      'saved_control_envelopes_fully_checked':True,'controls_rerun_by_comparator':False,'actual_data_evaluated':False,'full_application_qualified':False})
    artifacts=[ref(name) for name in E.ARTIFACT_NAMES[:-1]]
    report={'schema':'ri125-white-only-qualification-v1','phase':'fabricated_qualification','status':'all_white_only_gates_passed','context':E.CONTEXT,
      'scope':{'white_case_ids':list(E.CASE_IDS),'white_case_count':15,'full_application_case_count':32,'full_application_qualified':False,
               'actual_data_admitted':False,'periodic_mean_or_join_executed':False,'physical_claim':False},
      'limits':dict(K.STAGE_LIMITS),'source_bindings':bindings,'cases':cases,
      'complete_capture_assembly':{'id':E.CASE_IDS[8],'capture':ref(E.ASSEMBLY_FILES[0]),'gram_pin':C.identity(canonical({'isolated_guard_gram':True})),
          'primary':ref(E.ASSEMBLY_FILES[1]),'independent':ref(E.ASSEMBLY_FILES[2]),'full_fields_match':True},
      'controls':{'order':E.CONTROLS,'per_implementation':179,'kernel_per_implementation':38,'wrapper_and_tail_per_implementation':141,
        'primary_kernel':ref(E.CONTROL_FILES[0]),'primary_wrapper':ref(E.CONTROL_FILES[1]),'primary_complete':ref(E.CONTROL_FILES[2]),
        'independent_complete':ref(E.CONTROL_FILES[3]),'both_exact_inventories_and_first_refusals_passed':True,
        'trees':[{'name':tree,'inventory':ref(name)} for tree,name in zip(E.TREES,E.TREE_FILES)]},
      'fresh_saved_comparison':ref('FRESH_SAVED_COMPARISON.json'),'artifacts':artifacts[:],
      'limitations':['Only W01-W15 and their white controls are covered.',
       'The full 32-case application, periodic/mean/join paths and actual-data admission remain pending.',
       'Separate root source/runtime/history/caller custody and genuine completion remain required.',
       'Exact fabricated arithmetic is not detector covariance, calibration, native geometry/gravity or physical validation.',
       'Original precision, domain, resource and protected-validation boundaries remain; RET is paused.']}
    saved=save('WHITE_ONLY_QUALIFICATION.json',report);artifacts.append(saved)
    order=('white_kernel','white_path','wrapper_controls','white_contract','cases','kernel_refusals','fabricated_interfaces','white_refusals_text',
           'white_source_handoff','white_root_disposition','fixtures','kernel_controls','orchestrator','stage_contract','control_expectations','validator','validator_controls')
    envelope={'result':report,'report_pin':saved['pin'],'artifacts':artifacts,
      'postchecks':[{'role':'source:'+role,'pin':bindings[role]['pin'],'unchanged':True,'error':None} for role in order]
         +[{'role':'artifact:'+row['name'],'pin':row['pin'],'unchanged':True,'error':None} for row in artifacts],
      'tree_postchecks':[{'name':tree,'unchanged':True,'error':None} for tree in E.TREES],
      'namespace':{'inventory':E.tree_snapshot(root,C),'error':None},'refusal':None}
    return envelope,bindings


def relation_case(packet,base,kind):
    root=Path(tempfile.mkdtemp(prefix='metadata-relation-'+kind+'-',dir=base))
    (root/'GUARD_ONLY_NOT_QUALIFICATION.txt').write_text('Metadata double only; no scientific fixture, control, reconstruction or qualification executed.\n')
    C=module(packet/'control.py','guard_relation_control');K=module(packet/'caller_contract.py','guard_relation_contract');E=module(packet/'evidence.py','guard_relation_evidence')
    normal,bindings=metadata_stage(root/'normal',packet,C,K,E)
    optimized,_=metadata_stage(root/'optimized',packet,C,K,E,marker='different' if kind=='science_file' else 'same',bad_link=kind=='wrong_link')
    E.inspect_success(normal,root/'normal',bindings,C);E.inspect_success(optimized,root/'optimized',bindings,C)
    message=None
    if kind=='science_file':message='exact mode file identity W11-primary.json'
    elif kind=='wrong_link':message='every control-tree field under exact link relation'
    elif kind=='extra_envelope':optimized['unlisted']=True;message='closed qualifier return envelope'
    elif kind=='missing_artifact':optimized['artifacts']=optimized['artifacts'][:-1];message='all57 artifact files'
    elif kind=='postcheck':optimized['postchecks'][-1]['unchanged']=False;message='all74 exact source/artifact postchecks'
    elif kind=='extra_namespace':(root/'optimized'/'unexpected').write_bytes(b'guard');message='complete final namespace custody'
    elif kind=='control_message':
        spec=C.parse_json((packet/'science/qualifier/CONTROL_EXPECTATIONS.json').read_bytes())
        value=C.parse_json((root/'optimized'/E.CONTROL_FILES[2]).read_bytes());value['controls'][0]['observed_message']='wrong'
        refusal(lambda:E.control_report(value,spec,False),'literal first refusal WK01');return {'isolated_metadata_only':True,'kind':kind}
    elif kind=='tail_dropped':
        spec=C.parse_json((packet/'science/qualifier/CONTROL_EXPECTATIONS.json').read_bytes())
        value=C.parse_json((root/'optimized'/E.CONTROL_FILES[2]).read_bytes());value['controls'][-3]['postchecks'].pop()
        refusal(lambda:E.control_report(value,spec,False),'two full independent postchecks');return {'isolated_metadata_only':True,'kind':kind}
    if message:refusal(lambda:E.compare_modes(normal,optimized,root/'normal',root/'optimized',bindings,C),message)
    else:
        relation=E.compare_modes(normal,optimized,root/'normal',root/'optimized',bindings,C)
        need(relation['complete_envelopes_compared'] is True and relation['scientific_fields_omitted'] is False and len(relation['byte_identical_artifacts'])==53,'full closed mode mapping')
    return {'isolated_metadata_only':True,'kind':kind,'all_fixture_files_retained':True}


def mode_case(packet,base,kind):
    C=module(packet/'control.py','guard_mode_control');K=module(packet/'caller_contract.py','guard_mode_contract')
    root=Path(tempfile.mkdtemp(prefix='mode-'+kind+'-',dir=base))
    def save(name,value):
        path=root/name;path.write_bytes(canonical(value));return {'path':str(path),**pin(path)}
    freeze=save('AUTHORIZED_FREEZE.json',{'isolated_guard_only':True})
    opaque=save('OPAQUE_GUARD_ONLY.json',{'isolated_guard_only':True})
    mode='normal' if kind in ('normal_positive','wrong_command','pre_missing') else 'optimized'
    m={'root':str(root),'evidence':{'caller':opaque,'runtime':opaque},
       'runs':{x:K.run_paths(root,'/nonexecuted/guard-interpreter',x) for x in ('normal','optimized')},
       'mode_admissions':{x:str(root/('ADMIT_'+x.upper()+'.json')) for x in ('normal','optimized')}}
    pre={'schema':'ri130-root-pre-mode-runtime-custody-v1','mode':mode,'freeze':{k:freeze[k] for k in ('bytes','sha256')},
       'runtime_acceptance':opaque,'selection_unchanged':True,'optional_namespaces_unchanged':True,'host_identity_unchanged':True,
       'observed_dyld_routes':opaque,'metadata_record':opaque}
    if kind=='pre_missing':pre['selection_unchanged']=False
    normal_ref=None
    if mode=='optimized':
        (root/'runs'/'normal').mkdir(parents=True)
        outputs={}
        for name in ('stdout','stderr','worker_receipt','receipt','custody','claim'):
            path=Path(m['runs']['normal'][name]);path.write_bytes(b'guard only\n');outputs[name]={'path':str(path),**pin(path)}
        normal={'schema':'ri130-root-normal-white-review-v1','status':'ACCEPT_NORMAL_WHITE_EXECUTION_AND_CUSTODY',
          'freeze':pre['freeze'],'all15_cases_and_W09_assembly':True,'both179_controls':True,'complete_saved_reconstruction':True,
          'all57_artifacts_74_postchecks_3_trees':True,'runtime_post_custody_passed':True,'genuine_outer':opaque,
          'independent_review':opaque,'post_runtime_metadata':opaque,'outputs':outputs}
        if kind=='normal_incomplete':normal['both179_controls']=False
        normal_ref=save('NORMAL_GUARD_ONLY.json',normal)
        if kind=='normal_drift':Path(m['runs']['normal']['stdout']).write_bytes(b'changed guard\n')
    admission={'schema':'ri130-root-white-mode-admission-v1','status':'AUTHORIZE_ONE_WHITE_FABRICATED_MODE',
       'mode':mode,'phase':K.PHASE,'freeze':pre['freeze'],'caller_source_acceptance':opaque,'command':m['runs'][mode]['command'],
       'launcher_command':m['runs'][mode]['launcher_command'],'pre_runtime_metadata':save('PRE_GUARD_ONLY.json',pre),'normal_acceptance':normal_ref}
    if kind=='wrong_command':admission['command']=[]
    save('ADMIT_'+mode.upper()+'.json',admission)
    messages={'wrong_command':'exact mode admission binding','pre_missing':'fresh pre-mode runtime sidecars absent',
       'normal_incomplete':'optimized lacks complete accepted normal predecessor','normal_drift':'normal retained stdout'}
    if kind in messages:refusal(lambda:K.mode_admission(m,mode,C),messages[kind])
    else:K.mode_admission(m,mode,C)
    return {'actual_mode_admission_parser_used':True,'isolated_guard_metadata_only':True,'no_real_stage_admitted':True}


FAILURE_KINDS=('source','caller','runtime_acceptance','mode','late','late_postcheck')
CAPTURE_KINDS=('positive','changed_copy','buffer_drift','occupied')
MONITOR_KINDS=('positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap')
RUNTIME_KINDS=('positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config')
STATIC_KINDS=('positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command')
ACCEPTANCE_KINDS=('positive','source_execution','caller_binding','caller_history','caller_ret','guards_absent','runtime_binding','runtime_loader','runtime_profile')
MODE_KINDS=('normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift')
RELATION_KINDS=('positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped')
CONTROL_IDS=tuple([side+'_'+kind for side in ('parent','worker') for kind in FAILURE_KINDS]
 +['capture_'+x for x in CAPTURE_KINDS]+['monitor_'+x for x in MONITOR_KINDS]+['runtime_'+x for x in RUNTIME_KINDS]
 +['static_'+x for x in STATIC_KINDS]+['acceptance_'+x for x in ACCEPTANCE_KINDS]+['mode_'+x for x in MODE_KINDS]+['relation_'+x for x in RELATION_KINDS])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--admission',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();packet=args.packet.resolve()
    need(args.packet==packet,'literal packet root')
    admission=json.loads(args.admission.read_bytes())
    need(set(admission)=={'schema','status','packet','harness','helpers','controls','output','source_review','genuine_outer_required'},'closed separate guard admission')
    need(admission['schema']=='ri130-root-guard-admission-v1' and admission['status']=='AUTHORIZE_RI130_NONSCIENTIFIC_CALLER_GUARDS_ONLY'
         and admission['packet']==str(packet) and admission['harness']==pin(__file__) and admission['controls']==list(CONTROL_IDS)
         and admission['output']==str(args.output) and admission['genuine_outer_required'] is True,'root nonscientific guard admission')
    before={name:pin(packet/name) for name in HELPERS}
    need(admission['helpers']==before,'all guard helper identities')
    ref=admission['source_review'];need(pin(ref['path'])=={k:ref[k] for k in ('bytes','sha256')},'independent caller source review pin')
    need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==0,'separate normal isolated guard interpreter')
    need(args.output.is_absolute() and args.output==args.output.resolve() and not os.path.lexists(args.output),'fresh literal guard output')
    global BODIES
    BODIES={name:(packet/name).read_bytes() for name in HELPERS}
    need({name:{'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()} for name,body in BODIES.items()}==before,'all guard bodies captured before import')
    target_names=('white_kernel','white_path','white_controls','white_fixtures','kernel_controls','white_validator','validator_controls','qualify_white_only')
    need(not any(name in sys.modules for name in target_names),'scientific namespace occupied before caller guards')
    base=Path(tempfile.mkdtemp(prefix='ri130-nonscientific-guards-',dir=args.output.parent));rows=[]
    def attempt(identifier,action):
        try:rows.append({'id':identifier,'passed':True,'evidence':action(),'error':None})
        except BaseException as exc:rows.append({'id':identifier,'passed':False,'evidence':None,'error':{'type':type(exc).__name__,'message':str(exc)[:2048]}})
    for side in ('parent','worker'):
        for kind in FAILURE_KINDS:attempt(side+'_'+kind,lambda side=side,kind=kind:failure_case(packet,base,side,'late' if kind=='late_postcheck' else kind,kind=='late_postcheck'))
    for kind in CAPTURE_KINDS:attempt('capture_'+kind,lambda kind=kind:capture_case(packet,kind))
    for kind in MONITOR_KINDS:attempt('monitor_'+kind,lambda kind=kind:monitor_case(packet,kind))
    for kind in RUNTIME_KINDS:attempt('runtime_'+kind,lambda kind=kind:runtime_case(packet,base,kind))
    for kind in STATIC_KINDS:attempt('static_'+kind,lambda kind=kind:static_case(packet,kind))
    for kind in ACCEPTANCE_KINDS:attempt('acceptance_'+kind,lambda kind=kind:acceptance_case(packet,kind))
    for kind in MODE_KINDS:attempt('mode_'+kind,lambda kind=kind:mode_case(packet,base,kind))
    for kind in RELATION_KINDS:attempt('relation_'+kind,lambda kind=kind:relation_case(packet,base,kind))
    after={name:pin(packet/name) for name in HELPERS}
    need(not any(name in sys.modules for name in target_names),'scientific namespace appeared during caller guards')
    # runtime_case returns its own pass flag; never let a returned failure become
    # a harness success merely because the legacy helper did not raise.
    for row in rows:
        if row['id'].startswith('runtime_') and row['evidence'] is not None:
            row['passed']=row['evidence']['pass'] is True
    report={'schema':'ri130-nonscientific-caller-guards-v1','status':'all_declared_guards_passed' if before==after and all(x['passed'] for x in rows) else 'guard_failure',
      'packet':str(packet),'helpers_before':before,'helpers_after':after,'helpers_unchanged':before==after,'controls':rows,
      'control_order':list(CONTROL_IDS),'counts':{'total':len(rows),'passed':sum(x['passed'] for x in rows),'failed':sum(not x['passed'] for x in rows)},
      'fixture_root':str(base),'admission':{'path':str(args.admission),**pin(args.admission)},'target_or_scientific_helper_imported':False,
      'scientific_fixtures_or_controls_executed':False,'runtime_observation_substitutions_explicit':True,
      'production_runtime_qualified':False,'actual_data_admitted':False,'full32_qualified':False,'ret_paused':True}
    need([x['id'] for x in rows]==list(CONTROL_IDS),'all exact declared guard IDs retained')
    with args.output.open('xb') as stream:stream.write(canonical(report));stream.flush();os.fsync(stream.fileno())
    return 0 if report['status']=='all_declared_guards_passed' else 1


if __name__=='__main__':raise SystemExit(main())
