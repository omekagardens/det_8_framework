"""RI156 complete saved metadata/custody verifier; no scientific reconstruction.
All collaborator objects are explicit interfaces loaded only after separately
root-authenticated source/admission. This module never dispatches a process.
"""
from pathlib import Path
import shlex

SUPERVISOR_FIELDS='schema mode phase context freeze limits command launcher_command environment before postchecks monitor_attempts samples peak_sampled_rss_kib child_exit_code child_elapsed_seconds final_sample_to_reap_gap_seconds final_sample_gap_passed stop_reason status error worker_check mode_relation retained_outputs full32_qualified actual_data_admitted ret_paused child_pid ownership_tail pre_receipt_namespace'.split()
WORKER_FIELDS='schema mode phase context freeze limits source_count actual_scientific_inputs entry entry_phase entry_invocations entry_returned target_load_witness before postchecks saved_custody namespace_after error status full32_qualified actual_data_admitted ret_paused captured_targets loaded_after_capture envelope_pin elapsed_seconds custody_pin'.split()
CUSTODY_FIELDS='schema mode phase freeze status error entry_invocations entry_returned envelope_pin saved_custody namespace_after full32_qualified actual_data_admitted'.split()
OUTPUTS=('stdout','stderr','worker_receipt','receipt','custody','claim')
ALARM='$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;'


def dispatch_spec(m,mode,IO):
    IO.need(mode in ('normal','optimized'),'mode dispatch')
    env=m['environment'];command=m['runs'][mode]['launcher_command']
    vector=['/usr/bin/env','-i']+[name+'='+env[name] for name in sorted(env)]+['/usr/bin/perl','-e',ALARM]+command
    return {'command':command,'environment':env,'cwd':m['root'],'external_timeout_seconds':960,
            'exec_command_arguments':{'cmd':shlex.join(vector),'workdir':m['root'],'login':False,'yield_time_ms':1000,'max_output_tokens':4000},
            'scope':'Exact external root invocation proposal only; this function executes nothing. Root authenticates env/perl/bootstrap suppliers and actual tool origin.'}


def genuine_outer(row,m,mode,IO):
    value=IO.read(row);spec=dispatch_spec(m,mode,IO)
    IO.keys(value,('schema','status','mode','command','environment','cwd','external_timeout_seconds','raw_tool_receipt','supervisor','mode_admission','dispatch_copies'),'whole genuine scientific outer')
    IO.same([value['schema'],value['status'],value['mode']],['ri156-root-genuine-white-outer-v1','ACTUAL_TOOL_COMPLETION',mode],'actual outer status')
    for key in ('command','environment','cwd','external_timeout_seconds'):IO.same(value[key],spec[key],'literal outer '+key)
    IO.same(value['supervisor'],IO.ref(m['runs'][mode]['receipt']),'whole supervisor outer binding')
    IO.same(value['mode_admission'],IO.ref(m['mode_admissions'][mode]),'whole genuinely dispatched mode card')
    dispatch=IO.read(value['dispatch_copies'])
    IO.same([dispatch['schema'],dispatch['root'],dispatch['stage']],['ri156-complete-copy-card-observation-v1',m['root'],mode+'_admitted'],'genuine dispatch exact copy domain')
    IO.same(dispatch['cards']['ADMIT_'+mode.upper()+'.json'],IO.observe(m['mode_admissions'][mode]),'genuine dispatch card selection')
    tool=IO.read(value['raw_tool_receipt'])
    IO.keys(tool,('schema','initial_arguments','initial_result','intermediate_calls','terminal_arguments','terminal_result'),'genuine tool transcript fields')
    IO.same(tool['schema'],'ri156-root-actual-tool-transcription-v1','genuine transcript schema')
    IO.same(tool['initial_arguments'],spec['exec_command_arguments'],'exact actual shell/cwd/env/deadline invocation')
    initial=tool['initial_result'];IO.need(type(initial) is dict and type(initial.get('chunk_id')) is str,'initial genuine tool identity')
    IO.need(type(tool['intermediate_calls']) is list and len(tool['intermediate_calls'])<=960,'bounded complete intermediate poll list')
    if initial.get('session_id') is None:
        IO.same(tool['intermediate_calls'],[],'no polls after immediate completion')
        IO.need(tool['terminal_arguments'] is None and tool['terminal_result'] is None,'no invented terminal call');final=initial
    else:
        session=initial['session_id'];IO.need(type(session) is int and session>0 and initial.get('exit_code') is None,'genuine pending session')
        for call in tool['intermediate_calls']:
            IO.keys(call,('arguments','result'),'complete intermediate tool call')
            IO.same(call['arguments'],{'session_id':session,'chars':'','yield_time_ms':1000,'max_output_tokens':4000},'literal intermediate poll')
            v=call['result'];IO.need(type(v) is dict and v.get('session_id')==session and v.get('exit_code') is None and v.get('output')=='' and type(v.get('chunk_id')) is str,'genuine pending intermediate result')
        IO.same(tool['terminal_arguments'],{'session_id':session,'chars':'','yield_time_ms':1000,'max_output_tokens':4000},'exact terminal call')
        final=tool['terminal_result'];IO.need(type(final) is dict and type(final.get('chunk_id')) is str and final.get('session_id') is None,'genuine final result')
    IO.need(type(final.get('exit_code')) is int and final['exit_code']==0 and final.get('output')=='','actual final zero and empty launcher stream')
    IO.need(initial.get('output')=='','empty initial launcher stream')
    return {'outer':row,'initial_chunk':initial['chunk_id'],'terminal_chunk':final['chunk_id'],'exit_code':0,
            'tool_origin_is_external_root_premise':True,'complete_intermediate_poll_count':len(tool['intermediate_calls']),'dispatch_copies':value['dispatch_copies']}


def loaded_origins(value,m,role,IO):
    IO.need(type(value) is dict,'complete loaded-origin map')
    inventory=IO.read({'path':m['runtime_inventory']['path'],**m['runtime_inventory']['pin']})
    allowed={x['path']:{k:x[k] for k in ('bytes','sha256')} for x in inventory['files']}
    allowed.update({x['path']:x['pin'] for x in m['helpers']});allowed.update({x['copy']:x['pin'] for x in m['sources']})
    for name,row in value.items():
        IO.need(type(name) is str,'loaded module name');IO.keys(row,('path','bytes','sha256'),'whole module-origin fields')
        IO.need(row['path'] in allowed,'loaded origin outside whole declared closure')
        IO.same({k:row[k] for k in ('bytes','sha256')},allowed[row['path']],'loaded origin full pin')
    required={'__main__':'launch.py' if role=='parent' else 'worker.py','ri130_control':'control.py','ri130_caller_contract':'caller_contract.py','ri130_runtime_support':'runtime_support.py','ri130_evidence':'evidence.py'}
    if role=='parent':required['ri130_monitor']='monitor.py'
    for name,relative in required.items():
        path=str(Path(m['root'])/relative);IO.same(value.get(name),{'path':path,**allowed[path]},'required actual helper origin '+name)
    return {'recorded_modules':len(value),'all_recorded_fields_checked':True,'unrecorded_nonfile_origins_rely_on_executed_source':True}


def expected_runtime(m,mode,IO):
    inventory=IO.read({'path':m['runtime_inventory']['path'],**m['runtime_inventory']['pin']})
    profile=dict(m['expected_runtime']);profile['optimize']=0 if mode=='normal' else 1
    return {'interpreter':m['interpreter'],'runtime_files_count':len(inventory['files']),
      'runtime_files_identity':IO.identity(IO.canonical(inventory['files'])),'inventory_pin':m['runtime_inventory']['pin']},profile


def current_runtime_record(ref,m,mode,phase,baseline_ref,copy_ref,IO):
    """Consume actual root/unchanged-collector observations, not current machine.
    Entire saved snapshots must match accepted new-environment baseline. This
    never turns candidate self-reporting into a genuine tool-origin claim.
    """
    r=IO.read(ref)
    IO.keys(r,('schema','phase','mode','freeze','runtime_acceptance','environment','snapshot','baseline','copy_observation','vendor_before','vendor_after','genuine_collection_tools','observed_dyld_routes'),'complete external runtime record')
    IO.same([r['schema'],r['phase'],r['mode']],['ri156-root-actual-mode-runtime-v1',phase,mode],'mode runtime scope')
    IO.same(r['freeze'],IO.file_pin(Path(m['root'])/'AUTHORIZED_FREEZE.json'),'runtime whole freeze')
    IO.same(r['runtime_acceptance'],m['evidence']['runtime'],'runtime accepted source')
    IO.same(r['environment'],m['environment'],'runtime current environment')
    IO.same(r['baseline'],baseline_ref,'accepted exact baseline ref');IO.same(r['copy_observation'],copy_ref,'actual source/card observation ref')
    accepted_runtime=IO.read(m['evidence']['runtime']);accepted_profiles=IO.read(accepted_runtime['profile_review'])
    IO.same([accepted_profiles['schema'],accepted_profiles['status'],accepted_profiles['stage'],accepted_profiles['environment_root']],
      ['ri133-root-preparation-stage-review-v1','ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE','profiles',m['root']],'runtime actual accepted new-environment profile chain')
    normal_completion=IO.read(accepted_profiles['completions']['profile_normal'])
    IO.same(baseline_ref,normal_completion['artifacts']['PRE'],'baseline is authentic accepted complete normal PRE')
    IO.same(normal_completion['environment'],m['environment'],'baseline actual environment')
    snapshot=IO.read(r['snapshot']);baseline=IO.read(baseline_ref);IO.same(snapshot,baseline,'whole current metadata equals accepted new-environment baseline')
    IO.same(snapshot['schema'],'ri133-complete-current-metadata-snapshot-v1','unmodified retained collector shape')
    IO.same(IO.read(r['observed_dyld_routes']),snapshot['preobserved_dyld_routes'],'nonnull whole dyld evidence')
    IO.same(IO.read(r['vendor_before']),IO.read(r['vendor_after']),'whole actual vendor bracket')
    IO.body(r['genuine_collection_tools']);IO.read(copy_ref)
    IO.same(snapshot['runtime_inventory'],IO.read({'path':m['runtime_inventory']['path'],**m['runtime_inventory']['pin']}),'whole frozen current inventory')
    IO.same(snapshot['interpreter'],m['interpreter'],'whole candidate binding')
    return {'whole_current_snapshot':r['snapshot'],'complete_selection_optional_native_dyld_host_source_checked':True,
            'genuine_root_collection_and_vendor_authentication_remain_external':True}


def pre_mode_record(m,mode,actual_ref,baseline_ref,copy_ref,IO):
    checked=current_runtime_record(actual_ref,m,mode,'pre',baseline_ref,copy_ref,IO)
    r=IO.read(actual_ref)
    return {'schema':'ri130-root-pre-mode-runtime-custody-v1','mode':mode,'freeze':IO.file_pin(Path(m['root'])/'AUTHORIZED_FREEZE.json'),
      'runtime_acceptance':m['evidence']['runtime'],'selection_unchanged':True,'optional_namespaces_unchanged':True,'host_identity_unchanged':True,
      'observed_dyld_routes':r['observed_dyld_routes'],'metadata_record':actual_ref}


def verify_mode(m,mode,outer_ref,IO,C,K,E,L,M):
    """Whole27/13/30 plus full57/74/3 metadata; never calls reconstruct_saved.
    Numerical validity remains separately admitted independent saved arithmetic.
    """
    root=Path(m['root']);K.validate_static(m,root,C);fpin=C.file_pin(root/'AUTHORIZED_FREEZE.json')
    expected_source=C.verify_sources(m);accepted=K.source_admission(m,C);admission=K.mode_admission(m,mode,C)
    run=m['runs'][mode];p=IO.read(IO.ref(run['receipt']));IO.keys(p,SUPERVISOR_FIELDS,'whole30 successful supervisor')
    IO.same({k:p[k] for k in ('schema','mode','phase','context','freeze','limits','command','launcher_command','environment','child_exit_code','stop_reason','status','error','full32_qualified','actual_data_admitted','ret_paused')},
      {'schema':'ri130-white-supervisor-v1','mode':mode,'phase':K.PHASE,'context':K.CONTEXT,'freeze':fpin,'limits':m['limits'],'command':run['command'],'launcher_command':run['launcher_command'],'environment':m['environment'],
       'child_exit_code':0,'stop_reason':None,'status':'completed_pending_external_custody_review','error':None,'full32_qualified':False,'actual_data_admitted':False,'ret_paused':True},'literal complete supervisor success header')
    runtime,profile=expected_runtime(m,mode,IO)
    IO.keys(p['before'],('sources','source_admission','mode_admission','runtime','profile','loaded'),'complete parent before')
    fixed={'sources':expected_source,'source_admission':accepted,'mode_admission':admission,'runtime':runtime,'profile':profile}
    for name,value in fixed.items():IO.same(p['before'][name],value,'whole parent before '+name)
    parent_before_loaded=loaded_origins(p['before']['loaded'],m,'parent',IO)
    IO.keys(p['postchecks'],('freeze','sources','source_admission','mode_admission','runtime','profile','loaded','namespace'),'all8 parent tails')
    for name,row in p['postchecks'].items():IO.keys(row,('value','error'),'closed parent postcheck');IO.need(row['error'] is None,'parent tail failure '+name)
    for name,value in fixed.items():IO.same(p['postchecks'][name]['value'],value,'whole parent tail '+name)
    IO.same(p['postchecks']['freeze']['value'],fpin,'parent freeze stable')
    parent_after_loaded=loaded_origins(p['postchecks']['loaded']['value'],m,'parent',IO)
    w=IO.read(IO.ref(run['worker_receipt']));custody=IO.read(IO.ref(run['custody']))
    IO.keys(w,WORKER_FIELDS,'whole27 worker');IO.keys(custody,CUSTODY_FIELDS,'whole13 worker custody')
    checked=L.check_worker(m,mode,fpin,p['before'],C,K,E)
    IO.same(w,checked['worker'],'same whole worker read');envelope=checked['envelope']
    worker_maps={}
    for label,value in [('before',w['before']['loaded']),('after_capture',w['loaded_after_capture']),('after',w['postchecks']['loaded']['value'])]:worker_maps[label]=loaded_origins(value,m,'worker',IO)
    IO.same(p['postchecks']['namespace']['value'],envelope['namespace']['inventory'],'entire parent stage namespace')
    IO.same(p['worker_check'],{'status':'complete_saved_worker_and_stage_match','worker_pin':C.file_pin(run['worker_receipt']),
      'envelope_pin':C.file_pin(run['stdout']),'stage':checked['checked']},'entire supervisor worker check')
    IO.keys(p['retained_outputs'],('stdout','stderr','worker_receipt','custody','claim'),'five retained caller files')
    for name,row in p['retained_outputs'].items():IO.same(row,{'value':C.file_pin(run[name]),'error':None},'whole retained output '+name)
    claim=IO.read(IO.ref(run['claim']));IO.same(claim,{'schema':'ri130-exclusive-white-attempt-v1','mode':mode,'phase':K.PHASE,'freeze':fpin,'mode_admission':admission,'no_retry_or_replacement':True},'entire exclusive attempt')
    mon=M.verify_monitor(p,m['limits']);IO.need(w['elapsed_seconds']<=p['child_elapsed_seconds'],'worker interval inside owned child duration');outer=genuine_outer(outer_ref,m,mode,IO)
    IO.keys(p['pre_receipt_namespace'],('value','error'),'whole pre-receipt namespace attempt');IO.need(p['pre_receipt_namespace']['error'] is None,'pre-receipt namespace succeeded')
    final=E.tree_snapshot(Path(run['receipt']).parent,C);before=p['pre_receipt_namespace']['value']
    expected_records=before['records']+[{'name':Path(run['receipt']).name,'kind':'file','pin':C.file_pin(run['receipt']),'target':None}]
    IO.same(sorted(final['records'],key=lambda x:x['name']),sorted(expected_records,key=lambda x:x['name']),'exact final namespace adds only supervisor receipt')
    top=sorted(x['name'] for x in final['records'] if x['name']!='.' and '/' not in x['name'])
    IO.same(top,sorted([Path(run[x]).name for x in OUTPUTS]+['white-stage']),'whole final six caller files and one stage')
    relation=None
    if mode=='normal':IO.need(p['mode_relation'] is None,'normal has no future relation')
    else:
        normal=m['runs']['normal'];normal_envelope=IO.read(IO.ref(normal['stdout']))
        relation=E.compare_modes(normal_envelope,envelope,normal['stage'],run['stage'],K.stage_bindings(m,C),C)
        IO.same(p['mode_relation'],relation,'whole optimized mode relation')
    # Complete independent metadata rereads. Every successful comparison uses
    # immutable source/card pins; no current supplier is observed by this API.
    IO.same(C.verify_sources(m),expected_source,'source final reread');IO.same(K.source_admission(m,C),accepted,'acceptances final reread')
    IO.same(K.mode_admission(m,mode,C),admission,'mode and six normal outputs final reread')
    IO.same(IO.read(IO.ref(run['receipt'])),p,'whole supervisor stable');IO.same(IO.read(IO.ref(run['worker_receipt'])),w,'whole worker stable')
    IO.same(IO.read(IO.ref(run['custody'])),custody,'whole custody stable')
    return {'schema':'ri156-complete-saved-mode-metadata-v1','mode':mode,'status':'METADATA_MATCHES_PENDING_EXTERNAL_AND_ARITHMETIC_ACCEPTANCE',
      'outputs':{name:IO.ref(run[name]) for name in OUTPUTS},'freeze':fpin,'whole_worker_fields':27,'whole_custody_fields':13,'whole_supervisor_fields':30,
      'stage':checked['checked'],'monitor':mon,'genuine_outer':outer,'loaded_maps':{'parent_before':parent_before_loaded,'parent_after':parent_after_loaded,'worker':worker_maps},
      'final_namespace_pin':IO.identity(IO.canonical(final)),'mode_relation':relation,'arithmetic_recomputed':False,'scientific_qualification_accepted':False,'full32_qualified':False,'actual_data_admitted':False}


def review_with_tails(operation,m,mode,g,IO,C,K,E,L,M,B,
                      runtime_check=current_runtime_record,saved_check=verify_mode):
    """Actual external observations are supplied records. All independent tails
    execute after an earlier rejection; final-write failure escapes to root.
    """
    IO.keys(operation,('outer','pre','post','baseline','pre_copies','post_copies','review_output'),'closed mode review operation')
    output=IO.literal(operation['review_output']);root=Path(m['root'])
    IO.need(output.parent!=root and root not in output.parents and output!=root and not output.exists() and not output.is_symlink(),'external exclusive review output')
    first=None;result=None;before=None;verified_post=None;late_observations={}
    try:
        before=B.expected_copy_states(g,IO)
        pre_copy=IO.read(operation['pre_copies']);post_copy=IO.read(operation['post_copies'])
        for label,copy in [('pre',pre_copy),('post',post_copy)]:
            B.validate_observation(g,copy,IO)
            IO.same([copy['schema'],copy['root'],copy['tmp_empty'],copy['scientific_body_decoded'],copy['source_acceptance_created']],['ri156-complete-copy-card-observation-v1',m['root'],True,False,False],'copy observation scope')
            IO.same(copy['source_states'],before,'full original/copy/history selection '+label)
        IO.same(pre_copy['stage'],'frozen' if mode=='normal' else 'normal_completed','acyclic pre-card observation')
        IO.same(post_copy,B.observe_root(g,mode+'_completed',IO),'complete actual post-copy/root namespace')
        verified_post=post_copy
        runtime_check(operation['pre'],m,mode,'pre',operation['baseline'],operation['pre_copies'],IO)
        result=saved_check(m,mode,operation['outer'],IO,C,K,E,L,M)
        dispatch_copy=B.validate_observation(g,IO.read(result['genuine_outer']['dispatch_copies']),IO)
        IO.same(dispatch_copy['source_states'],before,'whole source selection at actual dispatch')
        for name,state in pre_copy['cards'].items():
            IO.same(dispatch_copy['cards'].get(name),state,'acyclic existing card stable at dispatch')
            IO.same(post_copy['cards'].get(name),state,'acyclic existing card stable after mode')
        IO.same(dispatch_copy['cards'],post_copy['cards'],'entire dispatch mode card selections stable')
    except BaseException as exc:first={'type':type(exc).__name__,'message':str(exc)[:2048]}
    def final_root_tail():
        current=B.observe_root(g,mode+'_completed',IO);late_observations['full_root_namespace']=current
        if verified_post is not None:IO.same(current,verified_post,'whole final root matches verified post-copy observation')
        return current
    actions=[('post_runtime',lambda:runtime_check(operation['post'],m,mode,'post',operation['baseline'],operation['post_copies'],IO)),
      ('source_copies',lambda:B.expected_copy_states(g,IO)),('source_admission',lambda:K.source_admission(m,C)),
      ('mode_admission',lambda:K.mode_admission(m,mode,C)),('full_root_namespace',final_root_tail)]
    tails,first=IO.tails(actions,first)
    if before is not None and tails['source_copies']['error'] is None:
        try:IO.same(tails['source_copies']['value'],before,'whole external source selection stable')
        except BaseException as exc:
            error={'type':type(exc).__name__,'message':str(exc)[:2048]};tails['source_stability']={'value':None,'error':error}
            if first is None:first=error
    receipt={'schema':'ri156-mode-review-result-v1','mode':mode,'status':'METADATA_REVIEW_COMPLETE_NOT_SCIENTIFIC_ACCEPTANCE' if first is None else 'REFUSED_RETAIN_ALL_EVIDENCE',
      'first_error':first,'independent_tails':tails,'metadata_result':result,'operation':operation,
      'verified_post_observation':operation['post_copies'] if verified_post is not None else None,'late_observations':late_observations,'arithmetic_recomputed':False,'qualification_accepted':False,'ret_paused':True}
    IO.write(output,receipt)
    return receipt


def normal_acceptance_record(m,review_ref,arithmetic_acceptance_ref,independent_review_ref,post_ref,outer_ref,IO):
    """Root-only candidate record; requires separately accepted actual arithmetic.
    No arithmetic function is called and no acceptance is created on disk.
    """
    r=IO.read(review_ref);IO.same([r['status'],r['mode'],r['first_error']],['METADATA_REVIEW_COMPLETE_NOT_SCIENTIFIC_ACCEPTANCE','normal',None],'normal metadata prerequisites')
    arithmetic=IO.read(arithmetic_acceptance_ref)
    IO.keys(arithmetic,('schema','status','mode','freeze','outputs','source_review','genuine_completion','independent_review','all15_cases_and_W09_assembly','all_fields_independently_reconstructed','controls_reexecuted'),'separate arithmetic root acceptance')
    IO.same([arithmetic['schema'],arithmetic['status'],arithmetic['mode'],arithmetic['freeze']],['ri156-root-independent-saved-arithmetic-acceptance-v1','ACCEPT_COMPLETE_SAVED_ARITHMETIC','normal',r['metadata_result']['freeze']],'accepted separate arithmetic scope')
    IO.need(arithmetic['all15_cases_and_W09_assembly'] is True and arithmetic['all_fields_independently_reconstructed'] is True and arithmetic['controls_reexecuted'] is False,'separate actual arithmetic outcomes')
    IO.same(arithmetic['outputs'],r['metadata_result']['outputs'],'arithmetic exact saved operands/output set')
    for name in ('source_review','genuine_completion','independent_review'):IO.body(arithmetic[name])
    for row in (independent_review_ref,post_ref,outer_ref):IO.body(row)
    IO.same(r['independent_tails']['post_runtime']['error'],None,'mandatory external post custody')
    IO.same([post_ref,outer_ref],[r['operation']['post'],r['operation']['outer']],'whole accepted post/outer references')
    for name,row in r['metadata_result']['outputs'].items():IO.same(row,IO.ref(m['runs']['normal'][name]),'normal outputs stable before acceptance')
    return {'schema':'ri130-root-normal-white-review-v1','status':'ACCEPT_NORMAL_WHITE_EXECUTION_AND_CUSTODY','freeze':r['metadata_result']['freeze'],
      'all15_cases_and_W09_assembly':True,'both179_controls':True,'complete_saved_reconstruction':True,'all57_artifacts_74_postchecks_3_trees':True,
      'runtime_post_custody_passed':True,'genuine_outer':outer_ref,'independent_review':independent_review_ref,'post_runtime_metadata':post_ref,'outputs':r['metadata_result']['outputs']}
