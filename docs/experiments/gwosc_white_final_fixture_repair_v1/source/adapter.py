"""RI156 bounded concrete metadata adapter. UNEXECUTED SOURCE.
Root authenticates interpreter/host/source/admission and observes the actual
outer command/deadline. This adapter NEVER launches science or runtime probes.
It returns/writes prospective records only for its explicitly admitted action.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
BOOTSTRAP='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
MODULES=('custody_io','retained_control','retained_contract','retained_stage','retained_supervisor','monitor_checks','bindings','mode_verify','retained_guards','inert_controls','integration_controls')
ACTIONS=('copy','observe','sidecars','adapters','freeze','pre_mode','mode_card','dispatch_spec','verify_mode','normal_acceptance','controls')
BOUNDS={'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864}


def need(ok,message):
    if not ok:raise ValueError('RI156_BOOTSTRAP: '+message)

def canonical(value):return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def identity(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def initial_read(path):
    p=Path(path);need(p.is_absolute() and p.resolve(strict=True)==p and not p.is_symlink(),'literal initial metadata')
    before=p.lstat();need(p.is_file() and 0<before.st_size<=67108864,'bounded initial file')
    with p.open('rb') as stream:data=stream.read(67108865)
    after=p.lstat()
    state=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    need(state(before)==state(after) and len(data)==before.st_size,'initial read drift')
    def pairs(rows):
        result={}
        for k,v in rows:need(k not in result,'duplicate initial key');result[k]=v
        return result
    def bad(_):raise ValueError('RI156_BOOTSTRAP: nonfinite initial token')
    value=json.loads(data,object_pairs_hook=pairs,parse_constant=bad);need(canonical(value)==data,'canonical initial metadata')
    return data,value


def authenticate(path):
    raw,a=initial_read(path)
    need(type(a) is dict and set(a)=={'schema','status','action','source_manifest','source_review','qualification','request','output','environment','bootstrap_preflight','bounds','genuine_outer_required'},'closed root adapter admission')
    need(a['schema']=='ri156-root-adapter-admission-v1' and a['status']=='AUTHORIZE_ONE_BOUNDED_METADATA_ACTION' and a['action'] in ACTIONS,'root metadata action')
    need(a['bounds']==BOUNDS and canonical(a['bounds'])==canonical(BOUNDS) and a['genuine_outer_required'] is True,'unchanged metadata action bounds')
    need(sys.executable==BOOTSTRAP and sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==0,'exact normal isolated direct bootstrap')
    need(dict(os.environ)==a['environment'],'exact external bootstrap environment')
    need(set(a['environment'])=={'PATH','LC_ALL','TZ','TMPDIR','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','__CF_USER_TEXT_ENCODING'},'complete10 environment')
    expected={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
    need(all(a['environment'][k]==v for k,v in expected.items()),'fixed environment values')
    manifest_data,manifest=initial_read(a['source_manifest']['path']);need({'path':a['source_manifest']['path'],**identity(manifest_data)}==a['source_manifest'],'manifest pin')
    need(type(manifest) is dict and set(manifest)=={'schema','status','adapter','modules','dependencies','bootstrap_binding','bootstrap_provenance'},'closed complete source set')
    need(manifest['schema']=='ri156-complete-source-set-v1' and manifest['status']=='UNEXECUTED_SOURCE_NOT_ADMISSION','source declaration scope')
    need(set(manifest['modules'])==set(MODULES) and manifest['adapter']=={'path':str(HERE/'adapter.py'),**identity((HERE/'adapter.py').read_bytes())},'complete adapter/source module map')
    # Authenticate concrete source-review, selected bootstrap and every declared
    # dependency before loading any non-main module. External card/tool origin
    # and the vendor/host preflight are still genuine root responsibilities.
    def pinned(row):
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'initial FilePin fields')
        p=Path(row['path']);need(p.is_absolute() and p.resolve(strict=True)==p and not p.is_symlink(),'initial dependency literal')
        before=p.lstat();need(p.is_file() and 0<=before.st_size<=67108864,'bounded initial dependency')
        with p.open('rb') as stream:data=stream.read(67108865)
        after=p.lstat()
        state=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
        need(state(before)==state(after) and {'path':str(p),**identity(data)}==row,'initial dependency identity')
        return data
    pinned(a['source_review']);pinned(a['bootstrap_preflight'])
    _,pre=initial_read(a['bootstrap_preflight']['path']);selected=pre['selected_interpreter_binding']
    need(canonical(selected)==canonical(manifest['bootstrap_binding']),'pre-load accepted bootstrap selection provenance')
    need(manifest['bootstrap_provenance'] in manifest['dependencies'],'bootstrap provenance in complete closure')
    pinned(manifest['bootstrap_provenance'])
    need([selected['path'],selected['resolved_path'],selected['symlink_chain']]==[BOOTSTRAP,BOOTSTRAP,[]],'pre-load direct bootstrap selection')
    bootstrap=Path(BOOTSTRAP);before_bootstrap=bootstrap.lstat();pinned({k:selected[k] for k in ('path','bytes','sha256')})
    state=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
    need(state(before_bootstrap)==state(bootstrap.lstat())==selected['state'],'pre-load bootstrap full state')
    for row in manifest['dependencies']:pinned(row)
    bodies={}
    for name in MODULES:
        row=manifest['modules'][name];p=HERE/(name+'.py');need(row['path']==str(p) and p.resolve(strict=True)==p and not p.is_symlink(),'literal module source')
        with p.open('rb') as stream:data=stream.read(67108865)
        need(len(data)<=67108864 and {'path':str(p),**identity(data)}==row,'complete module bytes');bodies[name]=data
    loaded={}
    for name in MODULES:
        qualified='ri156_'+name;need(qualified not in sys.modules,'fresh adapter module names')
        p=HERE/(name+'.py');spec=importlib.util.spec_from_file_location(qualified,p);need(spec is not None and spec.loader is not None,'module loader')
        module=importlib.util.module_from_spec(spec);sys.modules[qualified]=module
        exec(compile(bodies[name],str(p),'exec'),module.__dict__);loaded[name]=module
    IO=loaded['custody_io']
    IO.body(a['source_review']);pre=IO.read(a['bootstrap_preflight'])
    selected=pre['selected_interpreter_binding'];IO.same([selected['path'],selected['resolved_path'],selected['symlink_chain']],[BOOTSTRAP,BOOTSTRAP,[]],'actual direct bootstrap preflight')
    current=IO.observe(BOOTSTRAP);IO.same({k:current[k] for k in ('path','bytes','sha256','state')},{k:selected[k] for k in ('path','bytes','sha256','state')},'whole bootstrap current selection')
    for name,row in manifest['modules'].items():IO.same(IO.ref(row['path']),row,'source after complete load')
    for row in manifest['dependencies']:IO.body(row,empty=row['bytes']==0)
    if a['action']=='controls':IO.need(a['qualification'] is None,'controls cannot cite future qualification')
    else:
        q=IO.read(a['qualification'])
        IO.need(q['schema']=='ri156-root-inert-controls-review-v1' and q['status']=='ACCEPT_EXACT_INERT_ADAPTER_CONTROLS' and q['source_manifest']==a['source_manifest'],'separately qualified adapter source')
        for name in ('report','genuine_outer','independent_review'):IO.body(q[name])
        IO.same(q['controls'],list(loaded['inert_controls'].CONTROL_IDS)+list(loaded['integration_controls'].CONTROL_IDS),'entire required adapter control list')
        IO.need(q['all_passed'] is True and q['scientific_execution'] is False,'actual inert controls accepted')
    root=IO.literal(a['output']);IO.need(root.parent==HERE.parent and root.name.startswith('ri156-operation-') and not os.path.lexists(root),'fresh disjoint immediate external action output')
    request=IO.read(a['request']);return a,manifest,loaded,request,{'path':str(Path(path)),**identity(raw)}


def execute_action(action,q,out,mods,capture_output):
    I=mods['custody_io'];C=mods['retained_control'];K=mods['retained_contract'];E=mods['retained_stage'];L=mods['retained_supervisor'];B=mods['bindings'];V=mods['mode_verify'];M=mods['monitor_checks']
    if action=='controls':
        I.keys(q,('phase',),'controls request');I.same(q['phase'],'INERT_METADATA_ONLY','controls scope')
        return mods['integration_controls'].run_all_controls(out,mods,sys.modules[__name__],HERE)
    g=B.graph(I)
    if action=='copy':
        I.keys(q,('copy_admission',),'copy request');return B.copy_sources(g,I.read(q['copy_admission']),I)
    if action=='observe':
        I.keys(q,('stage',),'observe request');return B.observe_root(g,q['stage'],I)
    if action=='sidecars':
        I.keys(q,('profiles_acceptance',),'sidecars request');p=B.preparation_profiles(g,q['profiles_acceptance'],I);snapshot=p['profile_normal']['snapshot']
        names={'runtime_inventory':'runtime_inventory','selection':'selection','optional_namespaces':'optional_namespaces','observed_dyld_routes':'preobserved_dyld_routes','host_scope':'host_bootstrap'}
        result={}
        for name,field in names.items():
            row=I.write(out/(name+'.json'),snapshot[field]);expected={'path':str(out/(name+'.json')),**I.identity(I.canonical(snapshot[field]))}
            capture_output(name+'.json',expected);I.same(row,expected,'complete action output written value '+name);result[name]=row
        return result
    if action=='adapters':
        I.keys(q,('root_decisions','profiles_acceptance','sidecars'),'adapter request');return B.acceptance_adapters(g,q['root_decisions'],q['profiles_acceptance'],q['sidecars'],I,K)
    if action=='freeze':
        I.keys(q,('accepted_adapters',),'freeze request');return B.freeze_record(g,q['accepted_adapters'],I,K)
    I.need('freeze' in q and 'mode' in q,'mode request');m=I.read(q['freeze']);K.validate_static(m,Path(m['root']),C)
    I.same(m['root'],g['prospective_root'],'mode exact reviewed root');I.same(q['freeze'],I.ref(Path(m['root'])/'AUTHORIZED_FREEZE.json'),'whole existing freeze')
    mode=q['mode'];I.need(mode in ('normal','optimized'),'exact mode')
    if action=='pre_mode':
        I.keys(q,('freeze','mode','actual_runtime','baseline','copies'),'pre-mode request')
        observed=B.validate_observation(g,I.read(q['copies']),I)
        I.same(observed,B.observe_root(g,'frozen' if mode=='normal' else 'normal_completed',I),'complete pre-card current copy observation')
        return V.pre_mode_record(m,mode,q['actual_runtime'],q['baseline'],q['copies'],I)
    if action=='mode_card':
        I.keys(q,('freeze','mode','pre','normal_acceptance'),'mode-card request');return B.mode_record(m,mode,q['pre'],q['normal_acceptance'],I,K)
    if action=='dispatch_spec':
        I.keys(q,('freeze','mode'),'dispatch request');K.source_admission(m,C);K.mode_admission(m,mode,C);return V.dispatch_spec(m,mode,I)
    if action=='verify_mode':
        I.keys(q,('freeze','mode','operation'),'mode verification request');I.same(q['operation']['review_output'],str(out/'MODE_REVIEW.json'),'owned exact review output')
        value=V.review_with_tails(q['operation'],m,mode,g,I,C,K,E,L,M,B)
        capture_output('MODE_REVIEW.json',{'path':str(out/'MODE_REVIEW.json'),**I.identity(I.canonical(value))})
        return value
    I.keys(q,('freeze','mode','mode_review','arithmetic_acceptance','independent_review','post','outer'),'normal acceptance request');I.same(mode,'normal','only normal acceptance before optimized')
    return V.normal_acceptance_record(m,q['mode_review'],q['arithmetic_acceptance'],q['independent_review'],q['post'],q['outer'],I)


def run_authenticated(path,a,manifest,mods,q,admission_ref,action):
    """Production post-authentication integration, with explicit collaborators.
    run supplies authenticate's actual outputs and execute_action, never request
    selected callbacks. Inert controls substitute only that prior boundary/action.
    """
    I=mods['custody_io'];out=I.literal(a['output']);started=time.monotonic()
    all_source_rows={**manifest['modules'],'adapter':manifest['adapter'],'manifest':a['source_manifest']}
    source_before={name:I.observe(row['path']) for name,row in all_source_rows.items()}
    for name,row in all_source_rows.items():
        I.same({k:source_before[name][k] for k in ('path','bytes','sha256')},row,'authenticated source baseline pin '+name)
    I.same(I.ref(path),admission_ref,'admission stable before ownership')
    # Safe receipt state exists before ownership. mkdir failure is preownership;
    # every fallible operation after successful mkdir is in the protected body.
    first=None;value=None;artifacts={};produced={};observations={}
    def capture_output(name,row):
        allowed={'runtime_inventory.json','selection.json','optional_namespaces.json','observed_dyld_routes.json','host_scope.json'} if a['action']=='sidecars' else {'MODE_REVIEW.json'} if a['action']=='verify_mode' else set()
        I.need(name in allowed and name not in produced,'declared action output capture '+name)
        I.keys(row,('path','bytes','sha256'),'produced output FilePin');I.pin_shape({k:row[k] for k in ('bytes','sha256')},True)
        I.same(row['path'],str(out/name),'produced output exact path');produced[name]=dict(row)
    out.mkdir(mode=0o700)
    try:
        I.same(I.ref(path),admission_ref,'admission stable after ownership')
        attempt={'schema':'ri156-exclusive-metadata-attempt-v1','admission':admission_ref,'action':a['action'],'no_retry':True,'scientific_execution':False}
        artifacts['attempt']=I.write(out/'ATTEMPT.json',attempt)
        produced['ATTEMPT.json']={'path':str(out/'ATTEMPT.json'),**I.identity(I.canonical(attempt))}
        I.same(artifacts['attempt'],produced['ATTEMPT.json'],'complete ATTEMPT written value')
        value=action(a['action'],q,out,mods,capture_output)
        if type(value) is dict and value.get('first_error') is not None:first=value['first_error']
        if a['action']=='controls' and value['status']!='ALL_DECLARED_PASSED':first={'type':'ValueError','message':'RI156_IO: one or more required inert controls failed'}
        artifacts['result']=I.write(out/'RESULT.json',value)
        produced['RESULT.json']={'path':str(out/'RESULT.json'),**I.identity(I.canonical(value))}
        I.same(artifacts['result'],produced['RESULT.json'],'complete RESULT written value')
    except BaseException as exc:
        if first is None:first={'type':type(exc).__name__,'message':str(exc)[:2048]}
    def source_tail():
        after={name:I.observe(row['path']) for name,row in all_source_rows.items()};observations['sources']=after
        I.same(after,source_before,'all module source state stable');return after
    def output_tail(name,row):
        actual=I.ref(out/name);observations.setdefault('outputs',{})[name]=actual
        I.same(actual,row,'produced output pin drift '+name);return actual
    def namespace_tail():
        tree=I.tree(out);observations['namespace']=tree;allowed={'.','ATTEMPT.json','RESULT.json'}
        if a['action']=='sidecars':allowed.update(name+'.json' for name in ('runtime_inventory','selection','optional_namespaces','observed_dyld_routes','host_scope'))
        if a['action']=='verify_mode':allowed.add('MODE_REVIEW.json')
        if a['action']=='controls':allowed.update(('inert-fixtures','integration-fixtures'))
        # Retain structural errors without suppressing other comparisons that
        # this already-completed final scan can supply. Original first-error
        # ordering remains member checks, produced pins, then fixture trees.
        member_mismatches=[]
        for row in tree:
            name=row['relative'];within=a['action']=='controls' and (name.startswith('inert-fixtures/') or name.startswith('integration-fixtures/'))
            try:
                I.need(within or name in allowed,'unexpected metadata output '+name)
                if not within:I.same(row['kind'],'directory' if name in ('.','inert-fixtures','integration-fixtures') else 'file','output member type')
            except BaseException as exc:member_mismatches.append({'name':name,'type':type(exc).__name__,'message':str(exc)[:2048]})
        observations['namespace_member_mismatches']=member_mismatches
        by={row['relative']:row for row in tree}
        # Always reconcile every successfully captured output, including when
        # the action subsequently failed. Missing partial outputs have no invented
        # expected pin. Their actual names/bytes remain in the retained tree.
        mismatches=[]
        for name,pin in sorted(produced.items()):
            try:I.same(by.get(name),{'relative':name,'kind':'file',**{k:pin[k] for k in ('bytes','sha256')}},'final namespace produced pin '+name)
            except BaseException as exc:mismatches.append({'name':name,'type':type(exc).__name__,'message':str(exc)[:2048]})
        observations['namespace_output_mismatches']=mismatches
        fixture_mismatches=[]
        if a['action']=='controls':
            expected_trees=value.get('fixture_trees') if type(value) is dict else None
            final_trees={};comparisons={}
            observations['namespace_fixture_trees']=final_trees
            observations['namespace_fixture_comparisons']=comparisons
            for name in ('inert-fixtures','integration-fixtures'):
                # Same tree observation; change only its literal prefix/root
                # label. Preserve the entire ordered row and every other field.
                actual=[dict(row,relative='.' if row['relative']==name else row['relative'][len(name)+1:])
                        for row in tree if row['relative']==name or row['relative'].startswith(name+'/')]
                final_trees[name]=actual
                expected=expected_trees.get(name) if type(expected_trees) is dict else None
                available=type(expected) is list and len(expected)>0 and expected[0]=={'relative':'.','kind':'directory'}
                comparisons[name]={'expected_available':available,'compared':False,'matched':None}
                try:
                    if available:
                        comparisons[name]['compared']=True
                        comparisons[name]['matched']=I.canonical(actual)==I.canonical(expected)
                        I.same(actual,expected,'final namespace control fixture tree '+name)
                    elif first is None:
                        I.need(False,'complete captured control fixture expectation '+name)
                    # After a primary failure, an absent/incomplete expectation
                    # is explicitly unavailable. The observed partial remains;
                    # it cannot become invented equality or erase that failure.
                except BaseException as exc:fixture_mismatches.append({'name':name,'type':type(exc).__name__,'message':str(exc)[:2048]})
        observations['namespace_fixture_mismatches']=fixture_mismatches
        all_mismatches=member_mismatches+mismatches+fixture_mismatches
        if all_mismatches:raise ValueError(all_mismatches[0]['message'])
        if first is None:
            names=set(by);I.need({'ATTEMPT.json','RESULT.json'}<=names,'complete metadata success outputs')
            if a['action']=='sidecars':I.need(allowed<=names,'all five sidecar outputs')
            if a['action']=='verify_mode':I.need('MODE_REVIEW.json' in names,'complete saved mode review output')

        return tree
    actions=[('sources',source_tail),('admission',lambda:I.body(admission_ref)),('request',lambda:I.body(a['request'])),
             ('dependencies',lambda:[I.ref(row['path']) for row in manifest['dependencies']])]
    actions += [('output:'+name,lambda name=name,row=row:output_tail(name,row)) for name,row in sorted(produced.items())]
    if a['action']=='controls' and type(value) is dict and 'fixture_trees' in value:
        def fixture_tail(name):
            I.keys(value['fixture_trees'],('inert-fixtures','integration-fixtures'),'both complete control fixture trees')
            actual=I.tree(out/name);observations.setdefault('fixture_trees',{})[name]=actual
            I.same(actual,value['fixture_trees'][name],'entire retained control fixture tree '+name);return actual
        actions += [('fixture:'+name,lambda name=name:fixture_tail(name)) for name in ('inert-fixtures','integration-fixtures')]
    actions.append(('namespace',namespace_tail))
    tails,first=I.tails(actions,first)
    for name in ('admission','request'):
        if tails[name]['error'] is None:tails[name]['value']=admission_ref if name=='admission' else a['request']
    if tails['dependencies']['error'] is None:
        try:I.same(tails['dependencies']['value'],manifest['dependencies'],'all dependency post pins')
        except BaseException as exc:
            error={'type':type(exc).__name__,'message':str(exc)[:2048]};tails['dependencies']['error']=error
            if first is None:first=error
    elapsed=time.monotonic()-started
    if elapsed>180:
        error={'type':'ValueError','message':'RI156_IO: metadata action wall exceeded'};tails['soft_deadline']={'value':elapsed,'error':error}
        if first is None:first=error
    result={'schema':'ri156-adapter-completion-v1','action':a['action'],'status':'COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW' if first is None else 'REFUSED_RETAIN_ALL_PARTIALS',
      'admission':admission_ref,'artifacts':artifacts,'first_error':first,'independent_tails':tails,'elapsed_seconds_before_complete_write':elapsed,
      'authenticated_source_before':source_before,'produced_output_pins':produced,'tail_observations':observations,
      'scientific_execution':False,'root_acceptance_created':False,'ret_paused':True}
    I.write(out/'COMPLETE.json',result);return 0 if first is None else 1


def run(path):
    a,manifest,mods,q,admission_ref=authenticate(path)
    return run_authenticated(path,a,manifest,mods,q,admission_ref,execute_action)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--admission',required=True);args=parser.parse_args()
    return run(args.admission)

if __name__=='__main__':raise SystemExit(main())
