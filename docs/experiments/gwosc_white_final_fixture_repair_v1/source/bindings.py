"""RI156 concrete exact relocation, observations and acyclic card builders.
These functions are unexecuted source. They create no root authority. The caller
must authenticate this source and supplied root decisions before invoking them.
"""
from pathlib import Path
import os

GRAPH={'path':'/Volumes/AI_DATA/development/det-review-evidence/ri154-white-mode-preparation-42_uvw15/BINDING_GRAPH.source-only.json','bytes':86813,'sha256':'7be820c27d7a7b5f5b1661a49e5119b7922a1c49f4f24fa2d4567d1f2e5942bf'}
ORIGINAL='/Volumes/AI_DATA/development/det-review-evidence/ri130-white-qualification-caller-source-Q4Aq7hZg'
ENV_OLD='/Volumes/AI_DATA/development/det-review-evidence/ri146-genuine-current-capture-heib6de2/environment'
LIMITS={'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05}


def graph(IO):
    g=IO.read(GRAPH)
    IO.same(g['status'],'SOURCE_PREPARATION_ONLY_NOT_AUTHORIZATION','graph is preparation only')
    IO.need(len(g['copied_files'])==48 and len(g['sources'])==30 and len(g['helpers'])==11 and len(g['history_originals'])==124 and len(g['stage_bindings'])==17,'whole graph domains')
    root=IO.literal(g['prospective_root']);IO.need(str(root)!=ORIGINAL and str(root)!=ENV_OLD,'fresh graph root')
    for row in g['copied_files']:
        rel=row['relative'];IO.need(type(rel) is str and not Path(rel).is_absolute() and '..' not in Path(rel).parts,'copy relative')
        IO.same(row['source']['path'],str(Path(ORIGINAL)/rel),'original copy source')
        IO.same(row['destination'],str(root/rel),'new copy destination')
    return g


def expected_copy_states(g,IO):
    result=[]
    for row in g['copied_files']:
        original=IO.observe(row['source']['path']);copy=IO.observe(row['destination'])
        IO.same({k:original[k] for k in ('path','bytes','sha256')},row['source'],'complete original copy bytes')
        IO.same({k:copy[k] for k in ('bytes','sha256')},{k:row['source'][k] for k in ('bytes','sha256')},'complete relocated copy bytes')
        result.append({'relative':row['relative'],'original':original,'copy':copy})
    history=[]
    for row in g['history_originals']:
        item=IO.observe(row['path']);IO.same({k:item[k] for k in ('path','bytes','sha256')},row,'complete124 opaque history');history.append(item)
    targets=[]
    for row in g['sources']:
        item=IO.observe(row['original']);IO.same({k:item[k] for k in ('bytes','sha256')},row['pin'],'target original bytes');targets.append(item)
    return {'copies':result,'history':history,'target_originals':targets}


def validate_observation(g,value,IO):
    """Complete saved observation predicate; no runtime observation or trust grant."""
    IO.keys(value,('schema','root','stage','source_states','cards','tree','tmp_empty','scientific_body_decoded','source_acceptance_created'),'whole copy observation')
    stage=value['stage'];IO.need(stage in ('copied','frozen','normal_admitted','normal_completed','optimized_admitted','optimized_completed'),'root observation stage')
    IO.same([value['schema'],value['root'],value['tmp_empty'],value['scientific_body_decoded'],value['source_acceptance_created']],
      ['ri156-complete-copy-card-observation-v1',g['prospective_root'],True,False,False],'copy observation scope')
    root=Path(g['prospective_root']);fixed={x['relative']:x for x in g['copied_files']}
    directories={'.','science','science/primary','science/qualifier','science/validator','tmp','runs','runs/normal','runs/optimized'}
    cards=[]
    if stage!='copied':cards.append('AUTHORIZED_FREEZE.json')
    if stage in ('normal_admitted','normal_completed','optimized_admitted','optimized_completed'):cards.append('ADMIT_NORMAL.json')
    if stage in ('optimized_admitted','optimized_completed'):cards.append('ADMIT_OPTIMIZED.json')
    IO.keys(value['cards'],cards,'whole stage card domain')
    allow_normal=stage in ('normal_completed','optimized_admitted','optimized_completed');allow_opt=stage=='optimized_completed'
    tree=value['tree'];IO.need(type(tree) is list and len(tree)<=IO.TREE_CAP,'bounded saved whole tree')
    names=[];by={};total=0
    for row in tree:
        IO.need(type(row) is dict and type(row.get('relative')) is str,'saved tree row')
        name=row['relative'];path=Path(name)
        IO.need(name=='.' or (not path.is_absolute() and str(path)==name and '..' not in path.parts),'saved tree literal relative')
        IO.need(name not in by,'duplicate saved tree member');by[name]=row;names.append(name)
        if row.get('kind')=='directory':IO.keys(row,('relative','kind'),'saved directory row')
        elif row.get('kind')=='file':
            IO.keys(row,('relative','kind','bytes','sha256'),'saved file row');IO.pin_shape({k:row[k] for k in ('bytes','sha256')},True);total+=row['bytes']
        else:
            IO.keys(row,('relative','kind','target'),'saved link row');IO.need(row['kind']=='symlink' and type(row['target']) is str and len(row['target'])<=4096,'saved link type')
        allowed_run=(allow_normal and name.startswith('runs/normal/')) or (allow_opt and name.startswith('runs/optimized/'))
        IO.need(allowed_run or name in set(fixed)|directories|set(cards),'unexpected root member '+name)
    IO.same(names,sorted(names),'complete sorted saved tree');IO.need(total<=IO.TREE_BYTES,'saved tree aggregate bytes')
    IO.need(set(fixed)|directories|set(cards)<=set(by),'complete copy/card/root domain')
    for name in directories:IO.same(by[name]['kind'],'directory','expected source directory')
    for name in by:
        if name!='.':IO.need(str(Path(name).parent) in by and by[str(Path(name).parent)]['kind']=='directory','saved tree parent directory')
    for name,row in fixed.items():IO.same(by[name],{'relative':name,'kind':'file',**{k:row['source'][k] for k in ('bytes','sha256')}},'complete source tree pin')
    def state_record(row,path,pin):
        IO.keys(row,('path','bytes','sha256','state'),'complete source/card state');IO.same(row['path'],path,'source/card literal selection')
        IO.same({k:row[k] for k in ('bytes','sha256')},pin,'source/card exact pin')
        IO.need(type(row['state']) is list and len(row['state'])==7 and all(type(x) is int for x in row['state']),'whole7 selection state')
        IO.need(row['state'][4]==row['bytes'],'selection size matches body')
    for name,row in value['cards'].items():
        IO.pin_shape({k:row[k] for k in ('bytes','sha256')});state_record(row,str(root/name),{k:row[k] for k in ('bytes','sha256')})
        IO.same(by[name],{'relative':name,'kind':'file',**{k:row[k] for k in ('bytes','sha256')}},'complete card tree pin')
    source=value['source_states'];IO.keys(source,('copies','history','target_originals'),'complete source state domains')
    IO.need(len(source['copies'])==len(g['copied_files']) and len(source['history'])==len(g['history_originals']) and len(source['target_originals'])==len(g['sources']),'whole saved source counts')
    for row,decl in zip(source['copies'],g['copied_files']):
        IO.keys(row,('relative','original','copy'),'whole source copy pair');IO.same(row['relative'],decl['relative'],'ordered copy role')
        pin={k:decl['source'][k] for k in ('bytes','sha256')};state_record(row['original'],decl['source']['path'],pin);state_record(row['copy'],decl['destination'],pin)
    for row,decl in zip(source['history'],g['history_originals']):state_record(row,decl['path'],{k:decl[k] for k in ('bytes','sha256')})
    for row,decl in zip(source['target_originals'],g['sources']):state_record(row,decl['original'],decl['pin'])
    return value


def observe_root(g,stage,IO):
    root=IO.literal(g['prospective_root']);observed=expected_copy_states(g,IO)
    cards=[]
    if stage!='copied':cards.append('AUTHORIZED_FREEZE.json')
    if stage in ('normal_admitted','normal_completed','optimized_admitted','optimized_completed'):cards.append('ADMIT_NORMAL.json')
    if stage in ('optimized_admitted','optimized_completed'):cards.append('ADMIT_OPTIMIZED.json')
    value={'schema':'ri156-complete-copy-card-observation-v1','root':str(root),'stage':stage,'source_states':observed,
      'cards':{name:IO.observe(root/name,empty=False) for name in cards},'tree':IO.tree(root),'tmp_empty':True,
      'scientific_body_decoded':False,'source_acceptance_created':False}
    return validate_observation(g,value,IO)


def copy_sources(g,destination_admission,IO):
    """One exclusively owned copy installation, future separate root admission.
    Every body is checked before mkdir. Failure retains all partial copies and
    attempts each independent original/copy/namespace tail; never resumes.
    """
    a=destination_admission;IO.keys(a,('schema','status','graph','root','source_review'),'copy admission fields')
    IO.same([a['schema'],a['status'],a['graph'],a['root']],['ri156-root-copy-admission-v1','AUTHORIZE_ONE_EXACT_SOURCE_COPY_ONLY',GRAPH,g['prospective_root']],'copy authority boundary')
    IO.body(a['source_review']);root=IO.literal(g['prospective_root']);IO.need(not os.path.lexists(root),'fresh absent copy root')
    IO.need(sum(row['source']['bytes'] for row in g['copied_files'])<=IO.CAP,'complete copied-source capture cap')
    bodies=[]
    for row in g['copied_files']:bodies.append((row,IO.body(row['source'])))
    root.mkdir(mode=0o700);first=None;result=None
    try:
        for name in ('science','science/primary','science/qualifier','science/validator','tmp','runs','runs/normal','runs/optimized'):(root/name).mkdir(mode=0o700)
        for row,data in bodies:
            with Path(row['destination']).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        result=observe_root(g,'copied',IO)
    except BaseException as exc:first={'type':type(exc).__name__,'message':str(exc)[:2048]}
    actions=[('originals',lambda:[IO.body(row['source']) and row['source'] for row in g['copied_files']]),
             ('complete_copies',lambda:expected_copy_states(g,IO)),('full_namespace',lambda:IO.tree(root))]
    tails,first=IO.tails(actions,first)
    return {'schema':'ri156-copy-result-v1','status':'COPIED_PENDING_ROOT_REVIEW' if first is None else 'REFUSED_RETAIN_PARTIALS',
            'root':str(root),'first_error':first,'independent_tails':tails,'observation':result,'no_retry':True}


def guard_path_applicability(g,decision_ref,IO):
    decision=IO.read(decision_ref);old=IO.read(g['evidence']['guard_acceptance']);report=IO.read(old['report'])
    IO.keys(decision,('schema','status','graph','old_guard_acceptance','source_review','independent_review','helpers','root','guard_code_unchanged','path_sensitive_review_complete','additional_required_controls','new_guard_execution_claimed'),'guard relocation decision')
    IO.same([decision['schema'],decision['status'],decision['graph'],decision['old_guard_acceptance'],decision['helpers'],decision['root']],
      ['ri156-root-guard-path-applicability-v1','ACCEPT_EXACT_CODE_AND_REVIEWED_PATH_APPLICABILITY',GRAPH,g['evidence']['guard_acceptance'],g['helpers'],g['prospective_root']],'guard relocation bindings')
    IO.need(decision['guard_code_unchanged'] is True and decision['path_sensitive_review_complete'] is True and decision['new_guard_execution_claimed'] is False,'guard interpretation flags')
    IO.same(decision['additional_required_controls'],[],'additional path controls unresolved')
    for name in ('source_review','independent_review'):IO.body(decision[name])
    IO.same(report['packet'],ORIGINAL,'retain actual original guard packet')
    IO.same(old['helpers'],g['prior_original_guard_helpers'],'old complete11 helper path binding')
    for left,right in zip(old['helpers'],g['helpers']):
        IO.same(Path(left['path']).name,Path(right['path']).name,'helper basename relation');IO.same(left['pin'],right['pin'],'exact guard code relation')
    for role in ('genuine_outer','independent_review','report'):IO.body(old[role])
    return {**old,'helpers':g['helpers']}


def preparation_profiles(g,accepted_ref,IO):
    a=IO.read(accepted_ref)
    IO.keys(a,('schema','status','stage','sources','packet','environment_root','completions','genuine_outer','independent_review','scientific_execution'),'complete current profile acceptance')
    IO.same([a['schema'],a['status'],a['stage'],a['packet'],a['environment_root']],
      ['ri133-root-preparation-stage-review-v1','ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE','profiles',ORIGINAL,g['prospective_root']],'new environment profile applicability')
    IO.need(a['scientific_execution'] is False,'profile science boundary');IO.body(a['independent_review'])
    original_acceptance=IO.read(g['evidence']['profiles_acceptance']);IO.same(a['sources'],original_acceptance['sources'],'unchanged accepted RI141 source')
    IO.same(sorted(a['completions']),['profile_normal','profile_optimized'],'both profile completions')
    IO.same(sorted(a['genuine_outer']),['profile_normal','profile_optimized'],'both genuine profile records')
    result={}
    for phase in ('profile_normal','profile_optimized'):
        c=IO.read(a['completions'][phase]);outer=IO.read(a['genuine_outer'][phase])
        IO.need(c['status']=='CAPTURED_FOR_INDEPENDENT_REVIEW' and c['phase']==phase and c['first_error'] is None and c['independent_tail_errors']==[],'genuine accepted profile completion')
        IO.same(c['environment'],g['proposed_environment'],'actual profile new environment');IO.same(c['sources'],a['sources'],'profile whole source maps')
        IO.same(outer['completion'],a['completions'][phase],'profile outer completion');IO.same(outer['command'],c['command'],'profile exact command');IO.same(outer['environment'],c['environment'],'profile exact environment')
        IO.need(type(outer['exit_code']) is int and outer['exit_code']==0 and outer['status']=='ACTUAL_TOOL_COMPLETION','profile actual outer success');IO.body(outer['raw_tool_receipt'])
        before=IO.read(c['artifacts']['PRE']);after=IO.read(c['artifacts']['POST']);IO.same(before,after,'whole accepted profile runtime stability')
        report=IO.read(c['artifacts']['PROFILE']);checks=IO.read(c['artifacts']['checks'])
        IO.same(report['profile_before'],report['profile_after'],'whole observed profile stable');expected=checks['profile']['expected_runtime']
        IO.same(expected,report['profile_before'],'accepted complete profile correspondence');IO.same(expected['optimize'],0 if phase=='profile_normal' else 1,'actual profile optimize flag')
        result[phase]={'completion':c,'snapshot':before,'report':report,'checks':checks['profile']}
    normal=result['profile_normal'];opt=result['profile_optimized'];IO.same(normal['snapshot'],opt['snapshot'],'both full accepted snapshots')
    adjusted=dict(opt['report']['profile_before']);adjusted['optimize']=0;IO.same(adjusted,normal['report']['profile_before'],'only optimize profile relation')
    for key in ('ordered_actual_dyld_attempts','hash_algorithm_names'):IO.same(normal['checks'][key],opt['checks'][key],'complete accepted profile relation '+key)
    return result


def acceptance_adapters(g,root_decisions,profiles_ref,sidecars,IO,K):
    """Return records; never signs, accepts or writes them. Root must review.
    sidecars are exact saved current observations under the new environment.
    """
    IO.keys(root_decisions,('source_review','independent_source_review','packet_handoff','guard_path_review','runtime_applicability'),'root decision inputs')
    for row in root_decisions.values():IO.body(row)
    source_decision=IO.read(root_decisions['source_review'])
    IO.same([source_decision['schema'],source_decision['status'],source_decision['graph'],source_decision['helpers'],source_decision['sources'],source_decision['limits'],source_decision['independent_review']],
      ['ri156-root-relocated-source-decision-v1','ACCEPT_EXACT_RELOCATED_WHITE_SOURCE',GRAPH,g['helpers'],g['sources'],LIMITS,root_decisions['independent_source_review']],'root accepted exact relocated source')
    IO.need(source_decision['target_executed'] is False,'source-only root decision')
    applicability=IO.read(root_decisions['runtime_applicability'])
    IO.same([applicability['schema'],applicability['status'],applicability['root'],applicability['profiles_acceptance'],applicability['helpers'],applicability['sources']],
      ['ri156-root-current-runtime-applicability-v1','ACCEPT_CURRENT_RELOCATED_RUNTIME_APPLICABILITY',g['prospective_root'],profiles_ref,g['helpers'],g['sources']],'root current runtime applicability')
    IO.body(applicability['independent_review'])
    profiles=preparation_profiles(g,profiles_ref,IO);snapshot=profiles['profile_normal']['snapshot']
    IO.keys(sidecars,('runtime_inventory','selection','optional_namespaces','observed_dyld_routes','host_scope'),'complete current runtime sidecars')
    for field,part in [('runtime_inventory','runtime_inventory'),('selection','selection'),('optional_namespaces','optional_namespaces'),('observed_dyld_routes','preobserved_dyld_routes'),('host_scope','host_bootstrap')]:
        IO.same(IO.read(sidecars[field]),snapshot[part],'whole exact current sidecar '+field)
    caller={'schema':'ri130-root-caller-source-review-v1','status':'ACCEPT_RI130_WHITE_FABRICATED_CALLER_SOURCE_ONLY','helpers':g['helpers'],'sources':g['sources'],
            'history':K.HISTORY_PIN,'targets':K.TARGET_PIN,'limits':LIMITS,'source_review':root_decisions['independent_source_review'],'packet_handoff':root_decisions['packet_handoff'],'target_executed':False,'ret_paused':True}
    guards=guard_path_applicability(g,root_decisions['guard_path_review'],IO)
    runtime={'schema':'ri130-root-current-runtime-review-v1','status':'ACCEPT_CURRENT_WHITE_CALLER_RUNTIME','helpers':g['helpers'],'sources':g['sources'],
      'runtime_inventory':{'path':sidecars['runtime_inventory']['path'],'pin':{k:sidecars['runtime_inventory'][k] for k in ('bytes','sha256')}},
      'expected_runtime':profiles['profile_normal']['report']['profile_before'],'interpreter':snapshot['interpreter'],
      'scientific_targets_executed':False,'profile_normal':profiles['profile_normal']['completion']['artifacts']['PROFILE'],
      'profile_optimized':profiles['profile_optimized']['completion']['artifacts']['PROFILE'],'profile_review':profiles_ref,
      'selection':sidecars['selection'],'optional_namespaces':sidecars['optional_namespaces'],'observed_dyld_routes':sidecars['observed_dyld_routes'],'host_scope':sidecars['host_scope']}
    for key in ('complete_pure_python_stdlib','site_startup_surface_bound','non_os_shared_library_closure_bound','fresh_actual_profile_checked','source_cache_selection_checked','optional_native_namespaces_checked','observed_dyld_routes_checked','trusted_host_scope_explicit'):
        IO.need(applicability[key] is True,'explicit reviewed current runtime premise '+key);runtime[key]=True
    # These flags require the separately authenticated root acceptance of the
    # source/runtime premises; the returned JSON is not its own authority.
    return {'caller':caller,'guards':guards,'runtime':runtime}


def freeze_record(g,accepted_refs,IO,K):
    IO.keys(accepted_refs,('caller','guards','runtime'),'three root accepted adapters')
    runtime=IO.read(accepted_refs['runtime']);root=Path(g['prospective_root'])
    result={'schema':'ri130-white-fabricated-freeze-v1','status':'ROOT_AUTHORIZED_WHITE_FABRICATED_ONLY','phase':K.PHASE,'context':K.CONTEXT,'claim':K.CLAIM,
      'root':str(root),'inputs':[],'sources':g['sources'],'helpers':g['helpers'],'limits':LIMITS,'environment':g['proposed_environment'],
      'interpreter':runtime['interpreter'],'runtime_inventory':runtime['runtime_inventory'],'expected_runtime':runtime['expected_runtime'],
      'evidence':{'integration':g['integrated_root'],**accepted_refs},'runs':{},'mode_admissions':{}}
    for mode in ('normal','optimized'):
        result['runs'][mode]=K.run_paths(root,result['interpreter']['named_path'],mode)
        result['mode_admissions'][mode]=str(root/('ADMIT_'+mode.upper()+'.json'))
    K.validate_static(result,root,IO);K.source_admission(result,IO)
    return result


def mode_record(m,mode,pre_ref,normal_acceptance_ref,IO,K):
    IO.need(mode in ('normal','optimized'),'mode')
    IO.need((normal_acceptance_ref is None)==(mode=='normal'),'separate accepted normal before optimized')
    if normal_acceptance_ref is not None:IO.read(normal_acceptance_ref)
    pre=IO.read(pre_ref);freeze=IO.file_pin(Path(m['root'])/'AUTHORIZED_FREEZE.json')
    IO.same(pre['freeze'],freeze,'preexisting freeze pin')
    IO.need(pre['schema']=='ri130-root-pre-mode-runtime-custody-v1' and pre['mode']==mode and pre['runtime_acceptance']==m['evidence']['runtime'] and pre['selection_unchanged'] is True and pre['optional_namespaces_unchanged'] is True and pre['host_identity_unchanged'] is True,'complete actual pre-mode custody')
    for name in ('observed_dyld_routes','metadata_record'):IO.body(pre[name])
    if mode=='optimized':
        n=IO.read(normal_acceptance_ref)
        IO.need(n['schema']=='ri130-root-normal-white-review-v1' and n['status']=='ACCEPT_NORMAL_WHITE_EXECUTION_AND_CUSTODY' and n['freeze']==freeze,'accepted exact normal predecessor')
        for name in ('all15_cases_and_W09_assembly','both179_controls','complete_saved_reconstruction','all57_artifacts_74_postchecks_3_trees','runtime_post_custody_passed'):IO.need(n[name] is True,'normal predecessor incomplete '+name)
        for name in ('genuine_outer','independent_review','post_runtime_metadata'):IO.body(n[name])
        IO.keys(n['outputs'],('stdout','stderr','worker_receipt','receipt','custody','claim'),'six complete normal outputs')
        for name,row in n['outputs'].items():IO.same(row,IO.ref(m['runs']['normal'][name]),'normal complete output drift '+name)
    return {'schema':'ri130-root-white-mode-admission-v1','status':'AUTHORIZE_ONE_WHITE_FABRICATED_MODE','mode':mode,'phase':K.PHASE,
      'freeze':freeze,'caller_source_acceptance':m['evidence']['caller'],'command':m['runs'][mode]['command'],'launcher_command':m['runs'][mode]['launcher_command'],
      'pre_runtime_metadata':pre_ref,'normal_acceptance':normal_acceptance_ref}
