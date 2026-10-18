"""RI156 source-only concrete inert administrative controls. Never science.
Every fixture is permanently marked inert. Whole saved-mode metadata is tested
with four explicitly named source/authority/role substitutes, never fake
historical hash authentication or genuine runtime/process evidence.
"""
import copy
from pathlib import Path
from types import SimpleNamespace

MONITOR_IDS=('monitor_positive','monitor_exit_race','monitor_missing','monitor_rss','monitor_gap','monitor_final_gap','monitor_exception','monitor_peak','monitor_bool_exit')
MODE_IDS=('mode_positive','mode_supervisor_extra','mode_worker_missing','mode_custody_missing','mode_loaded_origin','mode_parent_tail','mode_claim','mode_namespace','mode_command','mode_child_rss')
STAGE_IDS=('stage_positive','stage_missing_artifact','stage_missing_post','stage_tree_tail','relation_positive','relation_changed_file','relation_wrong_link','relation_extra_field')
IO_IDS=('io_positive','io_changed_pin','io_link','io_partial_json','io_duplicate_json','io_exclusive_output')
TAIL_IDS=('tail_first_preserved','tail_all_after_first','tail_output_failure')
SHAPE_IDS=('shape_supervisor','shape_worker','shape_custody','shape_mode_order')
BINDING_IDS=('copy_positive','copy_occupied','copy_bad_original','copy_changed_after','copy_tmp_member','observation_duplicate','observation_card_extra','observation_source_pin','observation_directory_missing','guard_path_positive','guard_path_changed_helper','guard_path_pending_controls','guard_path_false_execution','profile_wrong_environment','arithmetic_missing_field_reconstruction')
CONTROL_IDS=MONITOR_IDS+MODE_IDS+STAGE_IDS+IO_IDS+TAIL_IDS+SHAPE_IDS+BINDING_IDS


def demand(ok,reason):
    if not ok:raise AssertionError('RI156_CONTROL: '+reason)


def refuses(action,message):
    try:action()
    except ValueError as exc:
        demand(str(exc)==message,'first literal error mismatch: '+repr(str(exc)))
        return {'expected':message,'observed':str(exc),'type':'ValueError'}
    raise AssertionError('RI156_CONTROL: expected first refusal absent')


def monitor_fixture():
    return {'child_pid':321,'child_exit_code':0,'error':None,'stop_reason':None,
      'ownership_tail':{'close_stdout':{'value':None,'error':None},'close_stderr':{'value':None,'error':None}},
      'monitor_attempts':[{'elapsed_seconds':0.025,'returncode':0,'stdout':'32\n','stderr':''}],
      'samples':[{'elapsed_seconds':0.025,'rss_kib':32,'gap_seconds':0.025}],
      'child_elapsed_seconds':0.04,'peak_sampled_rss_kib':32,'final_sample_to_reap_gap_seconds':0.015,'final_sample_gap_passed':True}


def monitor_control(identifier,M):
    value=monitor_fixture();message=None
    if identifier=='monitor_exit_race':value['monitor_attempts'].append({'elapsed_seconds':0.035,'returncode':1,'stdout':'','stderr':''})
    elif identifier=='monitor_missing':value['samples']=[];message='complete attempts/samples'
    elif identifier=='monitor_rss':value['samples'][0]['rss_kib']=524289;value['monitor_attempts'][0]['stdout']='524289\n';message='exact bounded rss'
    elif identifier=='monitor_gap':value['samples'][0]['gap_seconds']=0.2;message='gap arithmetic'
    elif identifier=='monitor_final_gap':value['child_elapsed_seconds']=0.2;value['final_sample_to_reap_gap_seconds']=0.175;message='final sample deadline'
    elif identifier=='monitor_exception':value['monitor_attempts'][0]={'elapsed_seconds':0.025,'exception':'TimeoutExpired','message':'inert','stdout':'','stderr':''};message='closed raw monitor attempt'
    elif identifier=='monitor_peak':value['peak_sampled_rss_kib']=33;message='peak arithmetic'
    elif identifier=='monitor_bool_exit':value['child_exit_code']=False;message='genuine zero child exit'
    if message:return refuses(lambda:M.verify_monitor(value,M.LIMITS),'RI156_MONITOR: '+message)
    return M.verify_monitor(value,M.LIMITS)


def inert_mode(root,mods,packet):
    """Whole metadata positive; no actual program or historical authority.
    C/E/L/M/IO and all substantive saved checks are real functions. Exactly
    K.validate_static/source_admission/mode_admission/stage_bindings substitute
    the unreachable authentic actual-body admission and source-role gates.
    """
    I=mods['custody_io'];C=mods['retained_control'];K=mods['retained_contract'];E=mods['retained_stage'];G=mods['retained_guards'];V=mods['mode_verify']
    root.mkdir();(root/'INERT_ONLY_NOT_A_SCIENTIFIC_OR_PROCESS_RESULT.txt').write_text('No scientific code, runtime or process executed. Four authority/source-role substitutes.\n')
    for name in ('runs','runs/normal','runs/optimized','tmp','fake-targets'):(root/name).mkdir()
    def put(path,value):path.write_bytes(I.canonical(value));return I.ref(path)
    source_names=list(K.HELPERS)
    helpers=[]
    for name in source_names:
        ref=put(root/name,{'inert_nonexecutable_helper':name});helpers.append({'path':ref['path'],'pin':{k:ref[k] for k in ('bytes','sha256')}})
    sources=[]
    relative_names=[relative for _,relative in K.MODULES]+['inert-extra-'+str(i) for i in range(22)]
    for i,relative in enumerate(relative_names):
        ref=put(root/'fake-targets'/str(i),{'inert_nonexecutable_source':relative});sources.append({'relative':relative,'original':ref['path'],'copy':ref['path'],'pin':{k:ref[k] for k in ('bytes','sha256')}})
    inv=put(root/'INERT_RUNTIME.json',{'files':[]});evidence=put(root/'INERT_AUTHORITY.json',{'inert_authority_substitution':True})
    m={'root':str(root),'helpers':helpers,'sources':sources,'limits':dict(K.LIMITS),'environment':K.environment(root),
       'interpreter':{'named_path':'/NONEXECUTED_INERT_INTERPRETER'},'runtime_inventory':{'path':inv['path'],'pin':{k:inv[k] for k in ('bytes','sha256')}},
       'expected_runtime':{'inert_profile':True,'optimize':0},'evidence':{'caller':evidence,'runtime':evidence},
       'runs':{mode:K.run_paths(root,'/NONEXECUTED_INERT_INTERPRETER',mode) for mode in ('normal','optimized')},
       'mode_admissions':{mode:str(root/('ADMIT_'+mode.upper()+'.json')) for mode in ('normal','optimized')}}
    freeze=put(root/'AUTHORIZED_FREEZE.json',{'INERT_ONLY_NOT_AUTHORIZED':True});fpin={k:freeze[k] for k in ('bytes','sha256')}
    mode='normal';run=m['runs'][mode]
    mode_ref=put(Path(m['mode_admissions'][mode]),{'INERT_ONLY_NOT_ADMITTED':True})
    admission={'path':mode_ref['path'],'pin':{k:mode_ref[k] for k in ('bytes','sha256')},'value':{'inert_admission_substitution':True}}
    source_acceptance={'inert_source_authority_substitution':True}
    envelope,bindings=G.metadata_stage(Path(run['stage']),packet,C,K,E)
    proxy=SimpleNamespace(**{name:getattr(K,name) for name in dir(K) if not name.startswith('__')})
    proxy.validate_static=lambda *args:None
    proxy.source_admission=lambda *args:copy.deepcopy(source_acceptance)
    proxy.mode_admission=lambda *args:copy.deepcopy(admission)
    proxy.stage_bindings=lambda *args:copy.deepcopy(bindings)
    source_check=C.verify_sources(m);runtime,profile=V.expected_runtime(m,mode,I)
    allowed={Path(x['path']).name:x for x in helpers}
    def loaded(role,targets=False):
        names={'__main__':'launch.py' if role=='parent' else 'worker.py','ri130_control':'control.py','ri130_caller_contract':'caller_contract.py','ri130_runtime_support':'runtime_support.py','ri130_evidence':'evidence.py'}
        if role=='parent':names['ri130_monitor']='monitor.py'
        out={name:{'path':allowed[file]['path'],**allowed[file]['pin']} for name,file in names.items()}
        if targets:
            by={x['relative']:x for x in sources}
            for name,rel in K.MODULES:out[name]={'path':by[rel]['copy'],**by[rel]['pin']}
        return out
    fixed={'sources':source_check,'source_admission':source_acceptance,'mode_admission':admission,'runtime':runtime,'profile':profile}
    envelope_ref=put(Path(run['stdout']),envelope);Path(run['stderr']).write_bytes(b'')
    put(Path(run['claim']),{'schema':'ri130-exclusive-white-attempt-v1','mode':mode,'phase':K.PHASE,'freeze':fpin,'mode_admission':admission,'no_retry_or_replacement':True})
    checked=E.inspect_success(envelope,run['stage'],bindings,C);by={x['relative']:x for x in sources}
    captures={name:by[rel]['pin'] for name,rel in K.MODULES}
    post={name:{'value':copy.deepcopy(value),'error':None} for name,value in fixed.items()}
    post.update(freeze={'value':fpin,'error':None},captured_targets={'value':captures,'error':None},loaded={'value':loaded('worker',True),'error':None},
                namespace={'value':envelope['namespace']['inventory'],'error':None},saved_custody={'value':checked,'error':None})
    worker={'schema':'ri130-white-worker-v1','mode':mode,'phase':K.PHASE,'context':K.CONTEXT,'freeze':fpin,'limits':m['limits'],'source_count':30,
      'actual_scientific_inputs':[],'entry':'qualify_white_only.run_white_qualification','entry_phase':'fabricated_qualification','entry_invocations':1,'entry_returned':True,
      'target_load_witness':[{'sequence':i,'module':name,'path':by[rel]['copy'],'pin':by[rel]['pin'],'state':'loaded'} for i,(name,rel) in enumerate(K.MODULES)],
      'before':{**copy.deepcopy(fixed),'loaded':loaded('worker')},'postchecks':post,'saved_custody':checked,'namespace_after':post['namespace'],'error':None,'status':'completed',
      'full32_qualified':False,'actual_data_admitted':False,'ret_paused':True,'captured_targets':captures,'loaded_after_capture':loaded('worker',True),
      'envelope_pin':C.file_pin(run['stdout']),'elapsed_seconds':0.01}
    custody={'schema':'ri130-white-worker-custody-v1','mode':mode,'phase':K.PHASE,'freeze':fpin,'status':'completed','error':None,'entry_invocations':1,'entry_returned':True,
      'envelope_pin':worker['envelope_pin'],'saved_custody':checked,'namespace_after':worker['namespace_after'],'full32_qualified':False,'actual_data_admitted':False}
    put(Path(run['custody']),custody);worker['custody_pin']=C.file_pin(run['custody']);put(Path(run['worker_receipt']),worker)
    parent={'schema':'ri130-white-supervisor-v1','mode':mode,'phase':K.PHASE,'context':K.CONTEXT,'freeze':fpin,'limits':m['limits'],'command':run['command'],
      'launcher_command':run['launcher_command'],'environment':m['environment'],'before':{**copy.deepcopy(fixed),'loaded':loaded('parent')},
      'postchecks':{name:{'value':copy.deepcopy(value),'error':None} for name,value in fixed.items()},
      'status':'completed_pending_external_custody_review','worker_check':{'status':'complete_saved_worker_and_stage_match','worker_pin':C.file_pin(run['worker_receipt']),
          'envelope_pin':C.file_pin(run['stdout']),'stage':checked},'mode_relation':None,'retained_outputs':{name:{'value':C.file_pin(run[name]),'error':None} for name in ('stdout','stderr','worker_receipt','custody','claim')},
      'full32_qualified':False,'actual_data_admitted':False,'ret_paused':True,**monitor_fixture()}
    parent['postchecks'].update(freeze={'value':fpin,'error':None},loaded={'value':loaded('parent'),'error':None},namespace={'value':envelope['namespace']['inventory'],'error':None})
    parent['pre_receipt_namespace']={'value':E.tree_snapshot(Path(run['receipt']).parent,C),'error':None};put(Path(run['receipt']),parent)
    dispatch=put(root/'INERT_DISPATCH_COPIES.json',{'schema':'ri156-complete-copy-card-observation-v1','root':str(root),'stage':'normal_admitted','cards':{'ADMIT_NORMAL.json':I.observe(m['mode_admissions']['normal'])}})
    spec=V.dispatch_spec(m,'normal',I)
    tool=put(root/'INERT_TOOL_NOT_GENUINE.json',{'schema':'ri156-root-actual-tool-transcription-v1','initial_arguments':spec['exec_command_arguments'],
      'initial_result':{'chunk_id':'INERT_NOT_A_REAL_TOOL','exit_code':0,'output':''},'intermediate_calls':[],'terminal_arguments':None,'terminal_result':None})
    outer={'schema':'ri156-root-genuine-white-outer-v1','status':'ACTUAL_TOOL_COMPLETION','mode':'normal',**{k:spec[k] for k in ('command','environment','cwd','external_timeout_seconds')},
      'raw_tool_receipt':tool,'supervisor':I.ref(run['receipt']),'mode_admission':I.ref(m['mode_admissions']['normal']),'dispatch_copies':dispatch}
    outer_ref=put(root/'INERT_OUTER_NOT_GENUINE.json',outer)
    return m,proxy,parent,worker,custody,outer,outer_ref


def mode_control(identifier,root,mods,packet):
    I=mods['custody_io'];C=mods['retained_control'];E=mods['retained_stage'];L=mods['retained_supervisor'];V=mods['mode_verify'];M=mods['monitor_checks']
    m,K,parent,worker,custody,outer,outer_ref=inert_mode(root,mods,packet);run=m['runs']['normal'];message=None
    if identifier=='mode_supervisor_extra':parent['extra']=True;message='RI156_IO: whole30 successful supervisor'
    elif identifier=='mode_worker_missing':worker.pop('full32_qualified');Path(run['worker_receipt']).write_bytes(I.canonical(worker));message='RI156_IO: whole27 worker'
    elif identifier=='mode_custody_missing':custody.pop('actual_data_admitted');Path(run['custody']).write_bytes(I.canonical(custody));message='RI156_IO: whole13 worker custody'
    elif identifier=='mode_loaded_origin':parent['before']['loaded']['alien']={'path':'/INERT_NOT_ALLOWED','bytes':1,'sha256':'0'*64};message='RI156_IO: loaded origin outside whole declared closure'
    elif identifier=='mode_parent_tail':parent['postchecks']['profile']['error']={'type':'INERT','message':'first'};message='RI156_IO: parent tail failure profile'
    elif identifier=='mode_claim':Path(run['claim']).write_bytes(I.canonical({'inert_changed_claim':True}));parent['retained_outputs']['claim']['value']=C.file_pin(run['claim']);message='RI156_IO: entire exclusive attempt'
    elif identifier=='mode_namespace':(Path(run['receipt']).parent/'unexpected').write_bytes(b'inert');message='RI156_IO: exact final namespace adds only supervisor receipt'
    elif identifier=='mode_command':parent['command']=[];message='RI156_IO: literal complete supervisor success header'
    elif identifier=='mode_child_rss':parent['samples'][0]['rss_kib']=524289;parent['monitor_attempts'][0]['stdout']='524289\n';message='RI156_MONITOR: exact bounded rss'
    Path(run['receipt']).write_bytes(I.canonical(parent));outer['supervisor']=I.ref(run['receipt']);Path(outer_ref['path']).write_bytes(I.canonical(outer));outer_ref=I.ref(outer_ref['path'])
    action=lambda:V.verify_mode(m,'normal',outer_ref,I,C,K,E,L,M)
    result=refuses(action,message) if message else action()
    return {'result':result,'actual_production_verifier_called':True,'source_authority_role_substitutes':['K.validate_static','K.source_admission','K.mode_admission','K.stage_bindings'],
      'genuine_process_records_are_explicit_inert_metadata':True,'scientific_execution':False,'whole_authentic_entry_qualified':False}


def stage_control(identifier,root,mods,packet):
    C=mods['retained_control'];K=mods['retained_contract'];E=mods['retained_stage'];G=mods['retained_guards']
    root.mkdir();(root/'INERT_ONLY.txt').write_text('Metadata-only stage double; no scientific recipes.\n')
    normal,bindings=G.metadata_stage(root/'normal',packet,C,K,E)
    if identifier.startswith('relation_'):
        opt,_=G.metadata_stage(root/'optimized',packet,C,K,E,marker='different' if identifier=='relation_changed_file' else 'same',bad_link=identifier=='relation_wrong_link')
        if identifier=='relation_extra_field':opt['extra']=True
        action=lambda:E.compare_modes(normal,opt,root/'normal',root/'optimized',bindings,C)
        messages={'relation_changed_file':'exact mode file identity W11-primary.json','relation_wrong_link':'every control-tree field under exact link relation','relation_extra_field':'closed qualifier return envelope'}
    else:
        if identifier=='stage_missing_artifact':normal['artifacts'].pop()
        elif identifier=='stage_missing_post':normal['postchecks'].pop()
        elif identifier=='stage_tree_tail':normal['tree_postchecks'][0]['unchanged']=False
        action=lambda:E.inspect_success(normal,root/'normal',bindings,C)
        messages={'stage_missing_artifact':'all57 artifact files','stage_missing_post':'all74 exact source/artifact postchecks','stage_tree_tail':'all3 exact tree postchecks'}
    return refuses(action,messages[identifier]) if identifier in messages else action()


def io_control(identifier,root,I):
    root.mkdir();p=root/'inert.json';p.write_bytes(I.canonical({'inert':True}));ref=I.ref(p)
    if identifier=='io_positive':return I.read(ref)
    if identifier=='io_changed_pin':p.write_bytes(b'changed');return refuses(lambda:I.read(ref),'RI156_IO: FilePin drift')
    if identifier=='io_link':link=root/'link';link.symlink_to(p);return refuses(lambda:I.observe(link),'RI156_IO: literal resolved path')
    if identifier=='io_partial_json':
        try:I.parse(b'{')
        except ValueError as exc:return {'actual_type':type(exc).__name__,'message':str(exc),'framing_refused':True}
        raise AssertionError('partial JSON not refused')
    if identifier=='io_duplicate_json':return refuses(lambda:I.parse(b'{"a":1,"a":1}'),'RI156_IO: duplicate metadata key')
    try:I.write(p,{'inert':False})
    except FileExistsError:return {'exclusive_output_collision_preserved':True,'original':I.read(ref)}
    raise AssertionError('exclusive output replaced')


def tail_control(identifier,root,I):
    trace=[]
    def fail():trace.append('first');raise ValueError('inert first')
    def second():trace.append('second');return 'retained'
    def third():trace.append('third');raise ValueError('inert third')
    rows,first=I.tails([('first',fail),('second',second),('third',third)],{'type':'INERT','message':'earlier'} if identifier=='tail_first_preserved' else None)
    demand(trace==['first','second','third'],'every independent tail reached')
    demand(first==({'type':'INERT','message':'earlier'} if identifier=='tail_first_preserved' else {'type':'ValueError','message':'inert first'}),'first error preserved')
    if identifier=='tail_output_failure':
        root.mkdir();out=root/'occupied';out.write_bytes(b'inert')
        try:I.write(out,rows)
        except FileExistsError:return {'rows':rows,'first':first,'final_write_failure_escapes':True}
        raise AssertionError('final output collision hidden')
    return {'rows':rows,'first':first,'complete_trace':trace,'direct_tail_boundary_not_whole_driver':True}


def shape_control(identifier,mods):
    I=mods['custody_io'];V=mods['mode_verify'];B=mods['bindings']
    if identifier=='shape_mode_order':return refuses(lambda:B.mode_record({},'optimized',None,None,I,None),'RI156_IO: separate accepted normal before optimized')
    fields={'shape_supervisor':V.SUPERVISOR_FIELDS,'shape_worker':V.WORKER_FIELDS,'shape_custody':V.CUSTODY_FIELDS}[identifier]
    value={x:None for x in fields};I.keys(value,fields,'inert exact field shape');value['unreviewed']=None
    return refuses(lambda:I.keys(value,fields,'inert exact field shape'),'RI156_IO: inert exact field shape')


def binding_control(identifier,root,mods):
    """Exact direct production boundary with a visibly reduced inert graph, or
    an explicit read/body observer double. Never creates authentic cards or
    substitutes a historical fixed pin. Root/whole-entry authentication stays
    outside these tests; every path is under the inert fixture tree.
    """
    I=mods['custody_io'];B=mods['bindings'];V=mods['mode_verify'];root.mkdir()
    (root/'INERT_ONLY_BOUNDARY.txt').write_text('Reduced graph or explicit read/body model; never historical credentials.\n')
    if identifier.startswith('copy_') or identifier.startswith('observation_'):
        original=root/'source';original.write_bytes(b'inert source bytes; not Python or scientific data\n')
        review=root/'review';review.write_bytes(b'INERT direct function call, not accepted source review\n')
        target=root/'copy';source=I.ref(original)
        g={'prospective_root':str(target),'copied_files':[{'relative':'inert-source','source':source,'destination':str(target/'inert-source')}],
           'history_originals':[],'sources':[]}
        admission={'schema':'ri156-root-copy-admission-v1','status':'AUTHORIZE_ONE_EXACT_SOURCE_COPY_ONLY','graph':B.GRAPH,'root':str(target),'source_review':I.ref(review)}
        # The exact root authority function is not being qualified: B.graph is
        # deliberately not called. This admitted direct-function operand is a
        # one-file inert graph with an external INERT marker, not an E copy.
        if identifier=='copy_occupied':target.mkdir();return refuses(lambda:B.copy_sources(g,admission,I),'RI156_IO: fresh absent copy root')
        if identifier=='copy_bad_original':original.write_bytes(b'changed');return refuses(lambda:B.copy_sources(g,admission,I),'RI156_IO: FilePin drift')
        result=B.copy_sources(g,admission,I);demand(result['first_error'] is None,'inert copy positive')
        if identifier=='copy_changed_after':
            (target/'inert-source').write_bytes(b'changed');return refuses(lambda:B.observe_root(g,'copied',I),'RI156_IO: complete relocated copy bytes')
        if identifier=='copy_tmp_member':
            (target/'tmp'/'unexpected').write_bytes(b'inert');return refuses(lambda:B.observe_root(g,'copied',I),'RI156_IO: unexpected root member tmp/unexpected')
        value=result['observation'];message=None
        if identifier=='observation_duplicate':value['tree'].append(copy.deepcopy(value['tree'][0]));message='duplicate saved tree member'
        elif identifier=='observation_card_extra':value['cards']['UNDECLARED']={};message='whole stage card domain'
        elif identifier=='observation_source_pin':value['tree'][next(i for i,x in enumerate(value['tree']) if x['relative']=='inert-source')]['sha256']='0'*64;message='complete source tree pin'
        elif identifier=='observation_directory_missing':value['tree']=[x for x in value['tree'] if x['relative']!='tmp'];message='complete copy/card/root domain'
        checked=refuses(lambda:B.validate_observation(g,value,I),'RI156_IO: '+message) if message else B.validate_observation(g,value,I)
        return {'result':checked,'direct_function_reduced_graph':True,'actual48_source_or_authority_coverage':False,'entire_tree':I.tree(target)}
    trace=[]
    # Literal sentinel keys identify private read/body doubles, never FilePins.
    # Only the exact pure downstream policy predicates get coverage here.
    old_helpers=[{'path':B.ORIGINAL+'/helper.py','pin':{'inert_identity':'same'}}]
    new_helpers=[{'path':'INERT_NEW/helper.py','pin':{'inert_identity':'same'}}]
    g={'evidence':{'guard_acceptance':'INERT_OLD','profiles_acceptance':'INERT_PROFILES'},'helpers':new_helpers,
       'prospective_root':'INERT_NEW','prior_original_guard_helpers':old_helpers}
    old={'helpers':old_helpers,'report':'INERT_REPORT','genuine_outer':'INERT_OUTER','independent_review':'INERT_REVIEW'}
    d={'schema':'ri156-root-guard-path-applicability-v1','status':'ACCEPT_EXACT_CODE_AND_REVIEWED_PATH_APPLICABILITY',
       'graph':B.GRAPH,'old_guard_acceptance':'INERT_OLD','source_review':'INERT_SOURCE_REVIEW','independent_review':'INERT_REVIEW',
       'helpers':new_helpers,'root':'INERT_NEW','guard_code_unchanged':True,'path_sensitive_review_complete':True,
       'additional_required_controls':[],'new_guard_execution_claimed':False}
    model={'INERT_DECISION':d,'INERT_OLD':old,'INERT_REPORT':{'packet':B.ORIGINAL}}
    def read(key):trace.append(['read',key]);return copy.deepcopy(model[key])
    def body(key,*args,**kwargs):trace.append(['body',key]);return b'INERT OBSERVER SUBSTITUTE'
    proxy=SimpleNamespace(**{name:getattr(I,name) for name in dir(I) if not name.startswith('__')});proxy.read=read;proxy.body=body
    if identifier=='profile_wrong_environment':
        model['INERT_PROFILE']={'schema':'ri133-root-preparation-stage-review-v1','status':'ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE','stage':'profiles',
          'sources':{},'packet':B.ORIGINAL,'environment_root':B.ENV_OLD,'completions':{},'genuine_outer':{},'independent_review':'INERT_REVIEW','scientific_execution':False}
        result=refuses(lambda:B.preparation_profiles(g,'INERT_PROFILE',proxy),'RI156_IO: new environment profile applicability')
        demand(trace==[['read','INERT_PROFILE']],'environment refusal before later reads')
    elif identifier=='arithmetic_missing_field_reconstruction':
        model['INERT_MODE_REVIEW']={'status':'METADATA_REVIEW_COMPLETE_NOT_SCIENTIFIC_ACCEPTANCE','mode':'normal','first_error':None,'metadata_result':{'freeze':'INERT_FREEZE'}}
        model['INERT_ARITHMETIC']={'schema':'ri156-root-independent-saved-arithmetic-acceptance-v1','status':'ACCEPT_COMPLETE_SAVED_ARITHMETIC','mode':'normal','freeze':'INERT_FREEZE',
          'outputs':{},'source_review':'INERT_SOURCE','genuine_completion':'INERT_OUTER','independent_review':'INERT_REVIEW','all15_cases_and_W09_assembly':True,
          'all_fields_independently_reconstructed':False,'controls_reexecuted':False}
        result=refuses(lambda:V.normal_acceptance_record({},'INERT_MODE_REVIEW','INERT_ARITHMETIC',None,None,None,proxy),'RI156_IO: separate actual arithmetic outcomes')
        demand(trace==[['read','INERT_MODE_REVIEW'],['read','INERT_ARITHMETIC']],'arithmetic refusal before output/auth reads')
    else:
        if identifier=='guard_path_changed_helper':d['helpers']=[{'path':'INERT_WRONG/helper.py','pin':{'inert_identity':'same'}}];message='guard relocation bindings'
        elif identifier=='guard_path_pending_controls':d['additional_required_controls']=['INERT_MISSING_CONTROL'];message='additional path controls unresolved'
        elif identifier=='guard_path_false_execution':d['new_guard_execution_claimed']=True;message='guard interpretation flags'
        else:message=None
        result=refuses(lambda:B.guard_path_applicability(g,'INERT_DECISION',proxy),'RI156_IO: '+message) if message else B.guard_path_applicability(g,'INERT_DECISION',proxy)
        if message:demand(trace==[['read','INERT_DECISION'],['read','INERT_OLD'],['read','INERT_REPORT']],'exact earliest policy refusal trace')
    return {'result':result,'read_body_observer_substitutes':True,'trace':trace,'authentic_historical_or_runtime_traversal':False,'whole_entry_credit':False}


def run_controls(directory,mods,here):
    root=Path(directory);demand(root.is_absolute() and root.resolve()==root and not root.exists() and not root.is_symlink(),'fresh inert-control root');root.mkdir()
    (root/'INERT_ONLY_NOT_QUALIFICATION.txt').write_text('No scientific fixtures, numerical results, actual process, installed runtime or accepted credentials.\n')
    packet=Path('/Volumes/AI_DATA/development/det-review-evidence/ri130-white-qualification-caller-source-Q4Aq7hZg')
    rows=[];I=mods['custody_io']
    for identifier in CONTROL_IDS:
        try:
            if identifier in MONITOR_IDS:evidence=monitor_control(identifier,mods['monitor_checks'])
            elif identifier in MODE_IDS:evidence=mode_control(identifier,root/identifier,mods,packet)
            elif identifier in STAGE_IDS:evidence=stage_control(identifier,root/identifier,mods,packet)
            elif identifier in IO_IDS:evidence=io_control(identifier,root/identifier,I)
            elif identifier in TAIL_IDS:evidence=tail_control(identifier,root/identifier,I)
            elif identifier in BINDING_IDS:evidence=binding_control(identifier,root/identifier,mods)
            else:evidence=shape_control(identifier,mods)
            rows.append({'id':identifier,'passed':True,'evidence':evidence,'error':None})
        except BaseException as exc:rows.append({'id':identifier,'passed':False,'evidence':None,'error':{'type':type(exc).__name__,'message':str(exc)[:2048]}})
    return {'schema':'ri156-inert-adapter-controls-v1','order':list(CONTROL_IDS),'controls':rows,'counts':{'total':len(rows),'passed':sum(x['passed'] for x in rows),'failed':sum(not x['passed'] for x in rows)},
      'status':'ALL_DECLARED_PASSED' if all(x['passed'] for x in rows) else 'FAILED_RETAIN_ALL_FIXTURES','fixture_tree':I.tree(root),'scientific_execution':False,
      'runtime_or_tool_evidence_genuine':False,'actual_admission_coverage':False,'arithmetic_or_15_case_credit':False,'full32_credit':False,'ri131_credit':False}
