"""RI158 unexecuted inert integration controls for F01/F02.
No process, runtime, scientific source/fixture or authentic credential is used.
The production post-authentication runner and mode-tail integration are real;
all boundary/action/runtime observer doubles are named in each retained result.
"""
import copy
from pathlib import Path
from types import SimpleNamespace

SOURCE_IDS=('A01_unchanged','A02_pre_module','A03_pre_manifest','A04_pre_adapter','A05_late_module','A06_late_manifest','A07_late_adapter')
OUTPUT_IDS=('O01_attempt_drift','O02_result_drift','O03_sidecars_unchanged','O04_inventory_drift','O05_selection_drift','O06_optional_drift','O07_dyld_drift','O08_host_drift','O09_mode_review_unchanged','O10_mode_review_drift','O11_partial_sidecars','O12_simultaneous_failures','O13_namespace_only_drift','O14_failure_before_action_output','O15_final_write_collision')
FIXTURE_IDS=('C01_fixture_trees_unchanged','C02_fixture_tree_drift')
MODE_IDS=('M01_unchanged','M02_final_root_drift','M03_primary_and_final_drift','M04_post_and_final_drift','M05_unverified_post')
FINAL_SINGLE_CASES={
    'L02_inert_bytes':('inert-fixtures','bytes'),
    'L03_inert_add':('inert-fixtures','add'),
    'L04_inert_delete':('inert-fixtures','delete'),
    'L05_inert_missing_root':('inert-fixtures','missing_root'),
    'L06_inert_file_type':('inert-fixtures','file_type'),
    'L07_inert_link':('inert-fixtures','link'),
    'L08_inert_root_file':('inert-fixtures','root_file'),
    'L09_inert_root_link':('inert-fixtures','root_link'),
    'L10_integration_bytes':('integration-fixtures','bytes'),
    'L11_integration_add':('integration-fixtures','add'),
    'L12_integration_delete':('integration-fixtures','delete'),
    'L13_integration_missing_root':('integration-fixtures','missing_root'),
    'L14_integration_file_type':('integration-fixtures','file_type'),
    'L15_integration_link':('integration-fixtures','link'),
    'L16_integration_root_file':('integration-fixtures','root_file'),
    'L17_integration_root_link':('integration-fixtures','root_link'),
}
FINAL_FIXTURE_IDS=('L01_both_unchanged', 'L02_inert_bytes', 'L03_inert_add', 'L04_inert_delete', 'L05_inert_missing_root', 'L06_inert_file_type', 'L07_inert_link', 'L08_inert_root_file', 'L09_inert_root_link', 'L10_integration_bytes', 'L11_integration_add', 'L12_integration_delete', 'L13_integration_missing_root', 'L14_integration_file_type', 'L15_integration_link', 'L16_integration_root_file', 'L17_integration_root_link', 'L18_primary_both', 'L19_ordinary_both', 'L20_primary_ordinary_both', 'L21_partial_no_expectations', 'L22_success_without_expectations')
CONTROL_IDS=SOURCE_IDS+OUTPUT_IDS+FIXTURE_IDS+MODE_IDS+FINAL_FIXTURE_IDS
SIDECARS=('runtime_inventory','selection','optional_namespaces','observed_dyld_routes','host_scope')


def need(ok,message):
    if not ok:raise AssertionError('RI158_CONTROL: '+message)


def exact(value,want,label,I):
    need(I.canonical(value)==I.canonical(want),label)


def integration_case(identifier,root,mods,adapter):
    """Calls actual run_authenticated, replacing prior authenticate and action.
    Real filesystem, pin comparisons, ownership, result/failure/tail machinery.
    IO proxy only traces and injects stated deterministic post-boundary drift.
    """
    I=mods['custody_io'];root.mkdir();(root/'INERT_ONLY.txt').write_text('Explicit authentication/action substitutes; no accepted authority.\n')
    def save(name,value):return I.write(root/name,value)
    module=save('inert-module.json',{'inert_source':'module'});main=save('inert-adapter.json',{'inert_source':'adapter'})
    declaration=save('inert-manifest.json',{'inert_source':'manifest'})
    request=save('inert-request.json',{'inert_request':True});admission=save('inert-boundary.json',{'INERT_AUTHENTICATION_SUBSTITUTE':True})
    dependency=save('inert-dependency.json',{'inert_dependency':True})
    out=root/'owned-output';action_name='observe'
    if identifier in ('O03_sidecars_unchanged','O04_inventory_drift','O05_selection_drift','O06_optional_drift','O07_dyld_drift','O08_host_drift','O11_partial_sidecars','O14_failure_before_action_output'):action_name='sidecars'
    elif identifier in ('O09_mode_review_unchanged','O10_mode_review_drift'):action_name='verify_mode'
    elif identifier in FIXTURE_IDS:action_name='controls'
    a={'output':str(out),'action':action_name,'source_manifest':declaration,'request':request}
    manifest={'modules':{'inert_module':module},'adapter':main,'dependencies':[dependency]}
    paths={'inert_module':Path(module['path']),'manifest':Path(declaration['path']),'adapter':Path(main['path'])}
    source_labels={str(path):name for name,path in paths.items()};trace=[];mutations=[];namespace_mutated=False
    def mutate(path,label):
        path.write_bytes(I.canonical({'INERT_DRIFT':label}));mutations.append({'path':str(path),'label':label})
    if identifier in ('A02_pre_module','A03_pre_manifest','A04_pre_adapter'):
        name={'A02_pre_module':'inert_module','A03_pre_manifest':'manifest','A04_pre_adapter':'adapter'}[identifier];mutate(paths[name],identifier)
    proxy=SimpleNamespace(**{name:getattr(I,name) for name in dir(I) if not name.startswith('__')})
    def observe(path,*args,**kwargs):
        trace.append('observe:'+source_labels.get(str(path),Path(path).name));return I.observe(path,*args,**kwargs)
    def ref(path,*args,**kwargs):
        trace.append('ref:'+Path(path).name);return I.ref(path,*args,**kwargs)
    def body(row,*args,**kwargs):
        trace.append('body:'+Path(row['path']).name);return I.body(row,*args,**kwargs)
    def tree(path):
        nonlocal namespace_mutated
        trace.append('tree:'+Path(path).name)
        if identifier=='O13_namespace_only_drift' and Path(path)==out and not namespace_mutated:
            namespace_mutated=True;mutate(out/'RESULT.json',identifier)
        return I.tree(path)
    def write(path,value):
        name=Path(path).name;trace.append('write:'+name)
        if identifier=='O15_final_write_collision' and name=='COMPLETE.json':Path(path).write_bytes(b'INERT occupied final receipt\n')
        row=I.write(path,value)
        if name=='RESULT.json':
            target={'O01_attempt_drift':'ATTEMPT.json','O02_result_drift':'RESULT.json','O04_inventory_drift':'runtime_inventory.json',
              'O05_selection_drift':'selection.json','O06_optional_drift':'optional_namespaces.json','O07_dyld_drift':'observed_dyld_routes.json',
              'O08_host_drift':'host_scope.json','O10_mode_review_drift':'MODE_REVIEW.json'}.get(identifier)
            if target:mutate(out/target,identifier)
            if identifier=='C02_fixture_tree_drift':mutate(out/'inert-fixtures'/'tiny.json',identifier)
        return row
    proxy.observe=observe;proxy.ref=ref;proxy.body=body;proxy.tree=tree;proxy.write=write
    def action(name,q,directory,supplied,capture):
        trace.append('action:'+name)
        if identifier in ('A05_late_module','A06_late_manifest','A07_late_adapter'):
            target={'A05_late_module':'inert_module','A06_late_manifest':'manifest','A07_late_adapter':'adapter'}[identifier];mutate(paths[target],identifier)
        if identifier=='O12_simultaneous_failures':
            mutate(paths['inert_module'],identifier);mutate(Path(request['path']),identifier);mutate(out/'ATTEMPT.json',identifier)
            raise ValueError('INERT primary action failure')
        if identifier=='O14_failure_before_action_output':raise ValueError('INERT action before extra output')
        if name=='sidecars':
            values={}
            for index,role in enumerate(SIDECARS):
                value={'INERT_SIDECAR':role};row=proxy.write(directory/(role+'.json'),value);capture(role+'.json',row);values[role]=row
                if identifier=='O11_partial_sidecars' and index==1:
                    mutate(directory/'runtime_inventory.json',identifier);raise ValueError('INERT partial sidecar action failure')
            return values
        if name=='verify_mode':
            value={'INERT_MODE_REVIEW':True};proxy.write(directory/'MODE_REVIEW.json',value)
            capture('MODE_REVIEW.json',{'path':str(directory/'MODE_REVIEW.json'),**I.identity(I.canonical(value))});return value
        if name=='controls':
            trees={}
            for role in ('inert-fixtures','integration-fixtures'):
                d=directory/role;d.mkdir();I.write(d/'tiny.json',{'INERT_TREE':role});trees[role]=I.tree(d)
            return {'status':'ALL_DECLARED_PASSED','fixture_trees':trees,'INERT_CONTROLS_ACTION':True}
        return {'INERT_ADMIN_ACTION':True}
    caught=None;code=None
    try:code=adapter.run_authenticated(admission['path'],a,manifest,{'custody_io':proxy},{},admission,action)
    except BaseException as exc:caught={'type':type(exc).__name__,'message':str(exc)}
    pre_names={'A02_pre_module':'inert_module','A03_pre_manifest':'manifest','A04_pre_adapter':'adapter'}
    if identifier in pre_names:
        exact(caught,{'type':'ValueError','message':'RI156_IO: authenticated source baseline pin '+pre_names[identifier]},'exact preownership first pin refusal',I)
        exact(trace,['observe:inert_module','observe:adapter','observe:manifest'],'complete baseline then refusal before later observers',I)
        need(not out.exists() and code is None,'no output ownership or action after bad authenticated baseline')
        return {'caught':caught,'trace':trace,'mutations':mutations,'owned_output_absent':True,'authentication_boundary_substituted':True}
    # Exact integrated observer/action order. Direct I/O inside the explicitly
    # substituted action is separated from the runner's own observed boundaries.
    ordinary_trace=['observe:inert_module','observe:adapter','observe:manifest','ref:inert-boundary.json','ref:inert-boundary.json','write:ATTEMPT.json','action:'+action_name]
    produced_names=['ATTEMPT.json']
    if action_name=='sidecars' and identifier!='O14_failure_before_action_output':
        roles=SIDECARS[:2] if identifier=='O11_partial_sidecars' else SIDECARS
        ordinary_trace += ['write:'+role+'.json' for role in roles];produced_names += [role+'.json' for role in roles]
    if action_name=='verify_mode':ordinary_trace+=['write:MODE_REVIEW.json'];produced_names+=['MODE_REVIEW.json']
    action_failed=identifier in ('O11_partial_sidecars','O12_simultaneous_failures','O14_failure_before_action_output')
    if not action_failed:ordinary_trace+=['write:RESULT.json'];produced_names+=['RESULT.json']
    ordinary_trace += ['observe:inert_module','observe:adapter','observe:manifest','body:inert-boundary.json','body:inert-request.json','ref:inert-dependency.json']
    ordinary_trace += ['ref:'+name for name in sorted(produced_names)]
    if action_name=='controls':ordinary_trace += ['tree:inert-fixtures','tree:integration-fixtures']
    ordinary_trace += ['tree:owned-output','write:COMPLETE.json']
    exact(trace,ordinary_trace,'entire integrated observer and action trace',I)
    if identifier=='O15_final_write_collision':
        need(caught is not None and caught['type']=='FileExistsError' and code is None,'final exclusive write error escapes integration')
        need((out/'COMPLETE.json').read_bytes()==b'INERT occupied final receipt\n','no replacement of final output')
        need('tree:owned-output' in trace and trace[-1]=='write:COMPLETE.json','all tails precede escaped final write')
        return {'caught':caught,'trace':trace,'mutations':mutations,'complete_tree':I.tree(out),'final_write_is_external_failure':True}
    need(caught is None,'owned integration returned a receipt');report=I.read(I.ref(out/'COMPLETE.json'))
    # Exact full registered tail set, including all produced files and both
    # returned control trees. No direct-tail test is counted as this integration.
    expected_tails=['sources','admission','request','dependencies']+['output:'+name for name in sorted(report['produced_output_pins'])]
    if action_name=='controls':expected_tails+=['fixture:inert-fixtures','fixture:integration-fixtures']
    expected_tails+=['namespace'];exact(sorted(report['independent_tails']),sorted(expected_tails),'every independently registered tail retained',I)
    need(trace.count('action:'+action_name)==1 and trace.count('write:COMPLETE.json')==1,'one action and one final write')
    expected_error=None
    if identifier in ('A05_late_module','A06_late_manifest','A07_late_adapter'):expected_error='RI156_IO: all module source state stable'
    target={'O01_attempt_drift':'ATTEMPT.json','O02_result_drift':'RESULT.json','O04_inventory_drift':'runtime_inventory.json','O05_selection_drift':'selection.json',
      'O06_optional_drift':'optional_namespaces.json','O07_dyld_drift':'observed_dyld_routes.json','O08_host_drift':'host_scope.json','O10_mode_review_drift':'MODE_REVIEW.json'}.get(identifier)
    if target:expected_error='RI156_IO: produced output pin drift '+target
    if identifier=='O11_partial_sidecars':expected_error='INERT partial sidecar action failure'
    if identifier=='O12_simultaneous_failures':expected_error='INERT primary action failure'
    if identifier=='O13_namespace_only_drift':expected_error='RI156_IO: final namespace produced pin RESULT.json'
    if identifier=='O14_failure_before_action_output':expected_error='INERT action before extra output'
    if identifier=='C02_fixture_tree_drift':expected_error='RI156_IO: entire retained control fixture tree inert-fixtures'
    exact(report['first_error'],None if expected_error is None else {'type':'ValueError','message':expected_error},'exact integrated earliest error',I)
    need(code==(0 if expected_error is None else 1),'integrated return code')
    exact(report['status'],'COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW' if expected_error is None else 'REFUSED_RETAIN_ALL_PARTIALS','integrated status',I)
    if expected_error is None:need(all(row['error'] is None for row in report['independent_tails'].values()),'positive complete tails')
    if target:
        need(report['independent_tails']['output:'+target]['error'] is not None and report['independent_tails']['namespace']['error'] is not None,'both current pin and final namespace catch drift')
        need(any(x['name']==target for x in report['tail_observations']['namespace_output_mismatches']),'full mismatch retained')
    if identifier=='O13_namespace_only_drift':
        need(report['independent_tails']['output:RESULT.json']['error'] is None and report['independent_tails']['namespace']['error'] is not None,'late namespace comparison independently reaches drift')
    if identifier=='O11_partial_sidecars':
        exact(sorted(report['produced_output_pins']),['ATTEMPT.json','runtime_inventory.json','selection.json'],'only completed sidecars captured',I)
        need(report['independent_tails']['output:runtime_inventory.json']['error'] is not None and report['independent_tails']['output:selection.json']['error'] is None,'partial first and later output independently checked')
        need(not (out/'RESULT.json').exists(),'failed action has no invented result')
    if identifier=='O12_simultaneous_failures':
        for key in ('sources','request','output:ATTEMPT.json','namespace'):need(report['independent_tails'][key]['error'] is not None,'secondary failure retained '+key)
        need(report['independent_tails']['admission']['error'] is None and report['independent_tails']['dependencies']['error'] is None,'unaffected tails still run')
    if identifier=='O14_failure_before_action_output':exact(sorted(report['produced_output_pins']),['ATTEMPT.json'],'no invented action pin after early failure',I)
    if identifier=='C02_fixture_tree_drift':
        need(report['independent_tails']['fixture:inert-fixtures']['error'] is not None and report['independent_tails']['fixture:integration-fixtures']['error'] is None,'both independent tree tails reached')
    return {'report':report,'trace':trace,'mutations':mutations,'output_tree':I.tree(out),'authentication_and_action_substituted':True,
      'actual_runner_baseline_ownership_outputs_and_tails_used':True,'authentic_whole_entry_credit':False}


def mode_case(identifier,root,mods):
    """Actual review_with_tails uses explicit saved/runtime/B/K observers.
    Only final reconciliation and first-error/eligibility integration are tested.
    No authentic 27/13/30, numerical objects, runtime or root authority is faked.
    """
    I=mods['custody_io'];V=mods['mode_verify'];root.mkdir();(root/'INERT_ONLY.txt').write_text('Explicit saved/runtime/source/card observer doubles.\n')
    science=root/'inert-mode-root';science.mkdir();trace=[];source={'INERT_SOURCE_OBSERVER':True}
    def obs(stage,cards):return {'schema':'ri156-complete-copy-card-observation-v1','root':str(science),'stage':stage,'source_states':source,
      'cards':cards,'tree':[],'tmp_empty':True,'scientific_body_decoded':False,'source_acceptance_created':False}
    pre=obs('frozen',{'AUTHORIZED_FREEZE.json':'INERT_FREEZE_STATE'});post=obs('normal_completed',{'AUTHORIZED_FREEZE.json':'INERT_FREEZE_STATE','ADMIT_NORMAL.json':'INERT_MODE_STATE'})
    dispatch=obs('normal_admitted',post['cards']);pre_ref=I.write(root/'inert-pre.json',pre);post_ref=I.write(root/'inert-post.json',post);dispatch_ref=I.write(root/'inert-dispatch.json',dispatch)
    operation={'outer':'INERT_OUTER_SENTINEL','pre':'INERT_PRE_SENTINEL','post':'INERT_POST_SENTINEL','baseline':'INERT_BASELINE_SENTINEL',
      'pre_copies':pre_ref,'post_copies':post_ref,'review_output':str(root/'MODE_REVIEW.json')}
    observations=0
    def copies(g,io):trace.append('copy_states');return copy.deepcopy(source)
    def validate(g,value,io):trace.append('validate:'+value['stage']);return value
    def observe(g,stage,io):
        nonlocal observations
        observations+=1;trace.append('root_observe:'+str(observations));value=copy.deepcopy(post)
        if (observations==1 and identifier=='M05_unverified_post') or (observations==2 and identifier!='M01_unchanged'):value['tree']=[{'INERT_LATE_MEMBER':observations}]
        return value
    def runtime(*args):
        phase=args[3];trace.append('runtime:'+phase)
        if phase=='post' and identifier=='M04_post_and_final_drift':raise ValueError('INERT post-runtime first failure')
        return {'INERT_RUNTIME_OBSERVER':phase}
    def saved(*args):
        trace.append('saved_check')
        if identifier=='M03_primary_and_final_drift':raise ValueError('INERT saved-check first failure')
        return {'genuine_outer':{'dispatch_copies':dispatch_ref},'INERT_SAVED_CHECK':True}
    def accepted_source(*args):trace.append('source_admission');return {'INERT_SOURCE_ADMISSION_OBSERVER':True}
    def accepted_mode(*args):trace.append('mode_admission');return {'INERT_MODE_ADMISSION_OBSERVER':True}
    B=SimpleNamespace(expected_copy_states=copies,validate_observation=validate,observe_root=observe)
    K=SimpleNamespace(source_admission=accepted_source,mode_admission=accepted_mode)
    result=V.review_with_tails(operation,{'root':str(science)},'normal',{},I,None,K,None,None,None,B,runtime_check=runtime,saved_check=saved)
    exact(I.read(I.ref(root/'MODE_REVIEW.json')),result,'complete real written mode-review value',I)
    expected={'M01_unchanged':None,'M02_final_root_drift':'RI156_IO: whole final root matches verified post-copy observation',
      'M03_primary_and_final_drift':'INERT saved-check first failure','M04_post_and_final_drift':'INERT post-runtime first failure',
      'M05_unverified_post':'RI156_IO: complete actual post-copy/root namespace'}[identifier]
    exact(result['first_error'],None if expected is None else {'type':'ValueError','message':expected},'exact saved-mode first refusal',I)
    exact(sorted(result['independent_tails']),sorted(['post_runtime','source_copies','source_admission','mode_admission','full_root_namespace']),'all5 actual registered mode tails',I)
    expected_trace=['copy_states','validate:frozen','validate:normal_completed','root_observe:1']
    if identifier!='M05_unverified_post':expected_trace+=['runtime:pre','saved_check']
    if identifier not in ('M03_primary_and_final_drift','M05_unverified_post'):expected_trace+=['validate:normal_admitted']
    expected_trace+=['runtime:post','copy_states','source_admission','mode_admission','root_observe:2']
    exact(trace,expected_trace,'complete real main/tail call ordering',I)
    root_error=result['independent_tails']['full_root_namespace']['error']
    if identifier in ('M02_final_root_drift','M03_primary_and_final_drift','M04_post_and_final_drift'):
        exact(root_error,{'type':'ValueError','message':'RI156_IO: whole final root matches verified post-copy observation'},'root drift retained even after earlier failure',I)
    else:need(root_error is None,'no inapplicable final comparison failure')
    exact(result['verified_post_observation'],None if identifier=='M05_unverified_post' else post_ref,'only genuinely verified expected post promoted',I)
    need('full_root_namespace' in result['late_observations'],'complete final observation retained even after comparison failure')
    return {'result':result,'trace':trace,'runtime_saved_source_and_card_observers_substituted':True,'actual_final_comparison_and_independent_tail_integration':True,
      'authentic_mode_or_science_credit':False}


def run_controls(directory,mods,adapter):
    I=mods['custody_io'];root=Path(directory);need(root.is_absolute() and root.resolve()==root and not root.exists(),'exclusive inert integration root');root.mkdir()
    (root/'INERT_ONLY.txt').write_text('RI160 unqualified integration fixtures. No source authentication, runtime or science execution.\n')
    rows=[]
    for identifier in CONTROL_IDS:
        try:
            evidence=final_fixture_case(identifier,root/identifier,mods,adapter) if identifier in FINAL_FIXTURE_IDS else mode_case(identifier,root/identifier,mods) if identifier in MODE_IDS else integration_case(identifier,root/identifier,mods,adapter)
            rows.append({'id':identifier,'passed':True,'evidence':evidence,'error':None})
        except BaseException as exc:rows.append({'id':identifier,'passed':False,'evidence':None,'error':{'type':type(exc).__name__,'message':str(exc)[:2048]}})
    return {'schema':'ri160-inert-custody-integration-controls-v1','order':list(CONTROL_IDS),'controls':rows,
      'counts':{'total':len(rows),'passed':sum(x['passed'] for x in rows),'failed':sum(not x['passed'] for x in rows)},
      'status':'ALL_DECLARED_PASSED' if all(x['passed'] for x in rows) else 'FAILED_RETAIN_ALL_FIXTURES','fixture_tree':I.tree(root),
      'actual_authentication_or_runtime_credit':False,'scientific_execution':False}


def run_all_controls(out,mods,adapter,here):
    # The existing55 implementation and order remain byte-identical. They are
    # real future calls, not copied previous outcomes; neither group has run yet.
    old=mods['inert_controls'].run_controls(out/'inert-fixtures',mods,here)
    new=run_controls(out/'integration-fixtures',mods,adapter)
    order=list(mods['inert_controls'].CONTROL_IDS)+list(CONTROL_IDS);rows=old['controls']+new['controls']
    return {'schema':'ri160-combined-inert-adapter-controls-v1','order':order,'controls':rows,
      'counts':{'total':len(rows),'passed':sum(x['passed'] for x in rows),'failed':sum(not x['passed'] for x in rows)},
      'status':'ALL_DECLARED_PASSED' if all(x['passed'] for x in rows) else 'FAILED_RETAIN_ALL_FIXTURES',
      'groups':{'retained55':old,'integration51':new},'fixture_trees':{'inert-fixtures':old['fixture_tree'],'integration-fixtures':new['fixture_tree']},
      'scientific_execution':False,'runtime_or_tool_evidence_genuine':False,'actual_admission_coverage':False,'arithmetic_or_15_case_credit':False,'full32_credit':False,'ri131_credit':False}


def final_fixture_case(identifier,root,mods,adapter):
    """RI160: real post-authentication runner, inert credentials/action only.
    Mutation occurs on the final whole-tree entry, after successful individual
    output/fixture tails. No scientific or accepted historical body is present.
    """
    I=mods['custody_io'];root.mkdir();(root/'INERT_ONLY.txt').write_text('RI160 private authentication/action substitutes. No authority or science.\n')
    def save(name,value):return I.write(root/name,value)
    module=save('inert-module.json',{'inert_source':'module'});main=save('inert-adapter.json',{'inert_source':'adapter'})
    declaration=save('inert-manifest.json',{'inert_source':'manifest'});dependency=save('inert-dependency.json',{'inert_dependency':True})
    request=save('inert-request.json',{'inert_request':True});admission=save('inert-boundary.json',{'INERT_AUTHENTICATION_SUBSTITUTE':True})
    out=root/'owned-output';a={'output':str(out),'action':'controls','source_manifest':declaration,'request':request}
    manifest={'modules':{'inert_module':module},'adapter':main,'dependencies':[dependency]}
    labels={module['path']:'inert_module',main['path']:'adapter',declaration['path']:'manifest'}
    roles=('inert-fixtures','integration-fixtures');trace=[];mutations=[];expected={};late_tree=None
    primary=identifier in ('L18_primary_both','L20_primary_ordinary_both','L21_partial_no_expectations')
    partial=identifier=='L21_partial_no_expectations';missing=identifier=='L22_success_without_expectations'
    ordinary=identifier in ('L19_ordinary_both','L20_primary_ordinary_both')
    changes={}
    if identifier in FINAL_SINGLE_CASES:
        role,kind=FINAL_SINGLE_CASES[identifier];changes[role]=kind
    elif identifier in ('L18_primary_both','L19_ordinary_both','L20_primary_ordinary_both'):
        changes={'inert-fixtures':'bytes','integration-fixtures':'link'}
    original_body=b'INERT fixture alpha\n';changed_body=b'INERT fixture beta\n';added_body=b'INERT new member\n';root_body=b'INERT root replacement\n'
    base_rows=[{'relative':'.','kind':'directory'},
               {'relative':'alpha.txt','kind':'file',**I.identity(original_body)},
               {'relative':'link','kind':'symlink','target':'alpha.txt'},
               {'relative':'nested','kind':'directory'}]
    def changed_rows(role):
        rows=copy.deepcopy(base_rows);kind=changes.get(role)
        if kind=='bytes':rows[1]={'relative':'alpha.txt','kind':'file',**I.identity(changed_body)}
        elif kind=='add':rows.append({'relative':'extra.txt','kind':'file',**I.identity(added_body)})
        elif kind=='delete':rows=[r for r in rows if r['relative']!='alpha.txt']
        elif kind=='missing_root':rows=[]
        elif kind=='file_type':rows[1]={'relative':'alpha.txt','kind':'directory'}
        elif kind=='link':rows[2]={'relative':'link','kind':'symlink','target':'nested'}
        elif kind=='root_file':rows=[{'relative':'.','kind':'file',**I.identity(root_body)}]
        elif kind=='root_link':rows=[{'relative':'.','kind':'symlink','target':'INERT_missing_target'}]
        return sorted(rows,key=lambda r:r['relative'])
    def mutate(role,kind):
        d=out/role;kept=root/('retained-before-late-'+role+'-'+kind)
        if kind=='bytes':(d/'alpha.txt').write_bytes(changed_body)
        elif kind=='add':(d/'extra.txt').write_bytes(added_body)
        elif kind=='delete':(d/'alpha.txt').rename(kept)
        elif kind=='missing_root':d.rename(kept)
        elif kind=='file_type':(d/'alpha.txt').rename(kept);(d/'alpha.txt').mkdir()
        elif kind=='link':(d/'link').rename(kept);(d/'link').symlink_to('nested')
        elif kind=='root_file':d.rename(kept);d.write_bytes(root_body)
        elif kind=='root_link':d.rename(kept);d.symlink_to('INERT_missing_target')
        else:raise AssertionError('unknown literal RI160 mutation')
        mutations.append({'root':role,'kind':kind,'timing':'final_whole_tree_entry_after_individual_tails'})
    proxy=SimpleNamespace(**{name:getattr(I,name) for name in dir(I) if not name.startswith('__')})
    def observe(path,*args,**kwargs):
        trace.append('observe:'+labels.get(str(path),Path(path).name));return I.observe(path,*args,**kwargs)
    def ref(path,*args,**kwargs):trace.append('ref:'+Path(path).name);return I.ref(path,*args,**kwargs)
    def body(row,*args,**kwargs):trace.append('body:'+Path(row['path']).name);return I.body(row,*args,**kwargs)
    def write(path,value):trace.append('write:'+Path(path).name);return I.write(path,value)
    def tree(path):
        nonlocal late_tree
        trace.append('tree:'+Path(path).name)
        if Path(path)==out:
            need(late_tree is None,'one final whole-tree observation')
            if not (partial or missing):
                exact(trace[-3:],['tree:inert-fixtures','tree:integration-fixtures','tree:owned-output'],'mutation follows both individual fixture observers',I)
            for role in roles:
                if role in changes:mutate(role,changes[role])
            if ordinary:
                (out/'RESULT.json').write_bytes(b'INERT late ordinary output\n')
                mutations.append({'root':'RESULT.json','kind':'bytes','timing':'final_whole_tree_entry_after_individual_tails'})
            late_tree=I.tree(path);return late_tree
        return I.tree(path)
    proxy.observe=observe;proxy.ref=ref;proxy.body=body;proxy.write=write;proxy.tree=tree
    def action(name,q,directory,supplied,capture):
        trace.append('action:'+name)
        for role in roles:
            d=directory/role;d.mkdir();(d/'alpha.txt').write_bytes(original_body);(d/'nested').mkdir();(d/'link').symlink_to('alpha.txt')
            expected[role]=I.tree(d);exact(expected[role],base_rows,'full independent fixed inert fixture rows '+role,I)
        if partial:raise ValueError('INERT primary fixture action failure')
        result={'status':'ALL_DECLARED_PASSED','INERT_CONTROLS_ACTION':True}
        if not missing:result['fixture_trees']=copy.deepcopy(expected)
        if primary:result['first_error']={'type':'ValueError','message':'INERT primary fixture action failure'}
        return result
    code=adapter.run_authenticated(admission['path'],a,manifest,{'custody_io':proxy},{},admission,action)
    report=I.read(I.ref(out/'COMPLETE.json'));obs=report['tail_observations'];tails=report['independent_tails']
    expected_trace=['observe:inert_module','observe:adapter','observe:manifest','ref:inert-boundary.json','ref:inert-boundary.json','write:ATTEMPT.json','action:controls']
    produced=['ATTEMPT.json']
    if not partial:expected_trace+=['write:RESULT.json'];produced+=['RESULT.json']
    expected_trace+=['observe:inert_module','observe:adapter','observe:manifest','body:inert-boundary.json','body:inert-request.json','ref:inert-dependency.json']
    expected_trace+=['ref:'+name for name in produced]
    if not (partial or missing):expected_trace+=['tree:inert-fixtures','tree:integration-fixtures']
    expected_trace+=['tree:owned-output','write:COMPLETE.json']
    exact(trace,expected_trace,'complete real runner trace and single final scan',I)
    expected_tails=['sources','admission','request','dependencies']+['output:'+name for name in produced]
    if not (partial or missing):expected_tails+=['fixture:'+name for name in roles]
    expected_tails+=['namespace'];exact(sorted(tails),sorted(expected_tails),'complete actual independent tail set',I)
    for name in expected_tails:
        if name!='namespace':exact(tails[name]['error'],None,'every earlier eligible tail succeeded '+name,I)
    if not (partial or missing):
        for role in roles:
            exact(tails['fixture:'+role]['value'],base_rows,'earlier whole fixture tail equality '+role,I)
            exact(obs['fixture_trees'][role],base_rows,'earlier captured observation retained '+role,I)
    else:need('fixture_trees' not in obs,'no invented earlier fixture-tail observations')
    exact(obs['namespace'],late_tree,'receipt retains exact final whole scan',I)
    wanted_members=[];wanted_fixture_errors=[];wanted_output_errors=[]
    for role in roles:
        rows=changed_rows(role);exact(obs['namespace_fixture_trees'][role],rows,'all final normalized rows and fields '+role,I)
        # Independent full-tree projection also verifies raw prefixed membership;
        # only the role prefix/root changes, no recorded field is discarded.
        prefix_rows=[dict(row,relative=role if row['relative']=='.' else role+'/'+row['relative']) for row in rows]
        exact([r for r in late_tree if r['relative']==role or r['relative'].startswith(role+'/')],prefix_rows,'complete raw prefixed rows '+role,I)
        availability=not (partial or missing)
        exact(obs['namespace_fixture_comparisons'][role],{'expected_available':availability,'compared':availability,'matched':(role not in changes) if availability else None},'explicit comparison eligibility '+role,I)
        if changes.get(role) in ('root_file','root_link'):
            wanted_members.append({'name':role,'type':'ValueError','message':'RI156_IO: output member type'})
        if role in changes or missing:
            label='complete captured control fixture expectation ' if missing else 'final namespace control fixture tree '
            wanted_fixture_errors.append({'name':role,'type':'ValueError','message':'RI156_IO: '+label+role})
    if ordinary:wanted_output_errors=[{'name':'RESULT.json','type':'ValueError','message':'RI156_IO: final namespace produced pin RESULT.json'}]
    exact(obs['namespace_member_mismatches'],sorted(wanted_members,key=lambda r:r['name']),'all structural mismatch records',I)
    exact(obs['namespace_output_mismatches'],wanted_output_errors,'ordinary mismatch does not suppress fixtures',I)
    exact(obs['namespace_fixture_mismatches'],wanted_fixture_errors,'both fixture mismatches retained in fixed root order',I)
    late_errors=sorted(wanted_members,key=lambda r:r['name'])+wanted_output_errors+wanted_fixture_errors
    late_error={k:late_errors[0][k] for k in ('type','message')} if late_errors else None
    exact(tails['namespace']['error'],late_error,'exact first final-namespace refusal',I)
    expected_first={'type':'ValueError','message':'INERT primary fixture action failure'} if primary else late_error
    exact(report['first_error'],expected_first,'primary versus independent late failure order',I)
    exact(code,1 if expected_first else 0,'actual integrated return code',I)
    exact(report['status'],'REFUSED_RETAIN_ALL_PARTIALS' if expected_first else 'COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW','actual integrated completion scope',I)
    exact(sorted(report['produced_output_pins']),produced,'only completed ordinary expectations',I)
    if partial:need(not (out/'RESULT.json').exists(),'earlier failure has no invented result')
    if late_error is None:exact(tails['namespace']['value'],late_tree,'successful namespace tail retains all partial records',I)
    else:need(tails['namespace']['value'] is None and obs['namespace']==late_tree,'late refusal preserves complete observed tree separately')
    return {'report':report,'trace':trace,'mutations':mutations,'expected_fixed_rows':base_rows,'final_scan':late_tree,'complete_case_tree':I.tree(root),
      'authentication_and_action_substituted':True,'actual_runner_and_final_comparison_used':True,'authentic_whole_entry_credit':False,
      'current_runtime_or_science_credit':False,'individual_tails_succeeded_before_late_mutation':not (partial or missing)}
