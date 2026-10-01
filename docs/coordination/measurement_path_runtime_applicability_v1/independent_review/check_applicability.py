"""RI194 saved administrative reconciliation only; no subject import or execution.
Run with Homebrew administrative Python -I -B. Writes only a new exclusive result.
The manual path proof and inherited independently accepted semantics are separate.
"""
import hashlib, json, os, stat, sys
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri194-path-runtime-applicability-review-zqqw4q78'
O=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
E=B/'ri154-white-execution-proposed-42_uvw15'
A=B/'ri192-root-optimized-profile-gtsq3_01/RI194_REVIEW_ASSIGNMENT.json'
G=B/'ri154-white-mode-preparation-42_uvw15/BINDING_GRAPH.source-only.json'
CHECKS=[]; IDENTITIES={}; DECODED=[]
def need(ok,label):
    CHECKS.append({'check':label,'passed':bool(ok)})
    if not ok: raise ValueError(label)
def canonical(v): return (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def same(a,b,label): need(canonical(a)==canonical(b),label)
def pure(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p,expected=None):
    p=Path(p); s=p.lstat(); need(p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode),'literal regular '+str(p))
    need(s.st_size<=67108864,'bounded administrative/opaque file '+str(p))
    state=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    with p.open('rb') as f:
        same(state(os.fstat(f.fileno())),state(s),'opened same state '+str(p)); body=f.read()
        same(state(os.fstat(f.fileno())),state(s),'opened final state '+str(p))
    same(state(p.lstat()),state(s),'final same state '+str(p)); pin=pure(body)
    if expected is not None:same(pin,expected,'expected bytes '+str(p))
    IDENTITIES[str(p)]={'path':str(p),'resolved_path':str(p),'symlink_chain':[],**pin,'state':state(s)}
    return body

def refread(r):return read(r['path'],r.get('pin',{k:r[k] for k in ('bytes','sha256')} if 'bytes' in r else None))
def parse(body):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'unique administrative JSON key');out[k]=v
        return out
    def bad(v):raise ValueError('nonfinite JSON')
    v=json.loads(body,object_pairs_hook=pairs,parse_constant=bad);same(body.decode('ascii'),canonical(v).decode('ascii'),'canonical administrative JSON');return v

def load(p,expected=None):
    DECODED.append(str(p));return parse(read(p,expected))
def loadref(r):
    DECODED.append(r['path']);return parse(refread(r))
def refs(value):
    if type(value)is dict:
        if set(value)=={'path','bytes','sha256'}:yield value
        else:
            for x in value.values():yield from refs(x)
    elif type(value)is list:
        for x in value:yield from refs(x)

def check_main():
    assignment=load(A,{'bytes':4022,'sha256':'d53ea24ff9bc42e629dc821d44116ee62b6e90948ef8d970a15650ada674394e'})
    same(assignment['reservation'],str(D),'exclusive review reservation')
    for r in [assignment['predecessor'],assignment['profiles_card'],assignment['selection']]+assignment['source_refs']:refread(r)
    g=load(G,{'bytes':86813,'sha256':'7be820c27d7a7b5f5b1661a49e5119b7922a1c49f4f24fa2d4567d1f2e5942bf'})
    same(g['prospective_root'],str(E),'literal E');same(g['source_changes'],False,'no source changes')
    same([len(g[k]) for k in ('copied_files','sources','helpers','history_originals')],[48,30,11,124],'full mapping counts')
    for r in g['evidence'].values():refread(r)
    for row in g['copied_files']:
        same(row['source']['path'],str(O/row['relative']),'copy original relative path')
        same(row['destination'],str(E/row['relative']),'copy E relative path')
        same(read(row['destination']),refread(row['source']),'complete copy bytes '+row['relative'])
    for row in g['sources']:
        same(row['copy'],str(E/row['relative']),'target copy path')
        same(read(row['copy'],row['pin']),read(row['original'],row['pin']),'original target and copy opaque equality')
    for r in g['history_originals']:refread(r)
    actualfiles=[];actualdirs=['.']
    for parent,dirs,names in os.walk(E,followlinks=False):
        for name in dirs:
            p=Path(parent)/name;need(not p.is_symlink(),'E directory not alias');actualdirs.append(str(p.relative_to(E)))
        for name in names:
            p=Path(parent)/name;need(not p.is_symlink(),'E file not alias');actualfiles.append(str(p.relative_to(E)))
    same(sorted(actualfiles),sorted(r['relative'] for r in g['copied_files']),'exact installed48 namespace')
    same(sorted(actualdirs),sorted(['.','science','science/primary','science/qualifier','science/validator','tmp','runs','runs/normal','runs/optimized']),'exact nine E directories; no mode output')
    helpermap=[]
    for old,new in zip(g['prior_original_guard_helpers'],g['helpers']):
        name=Path(old['path']).name;same(old['path'],str(O/name),'old helper path');same(new['path'],str(E/name),'new helper path')
        same(old['pin'],new['pin'],'same helper pin');same(refread(old),refread(new),'complete helper bytes')
        helpermap.append({'name':name,'old':old,'new':new})
    # The actual adapter is a separately reviewed copy of the original contract.
    same(read(B/'ri160-white-fixture-custody-repair-ufok1zpo/retained_contract.py'),read(O/'caller_contract.py'),'retained exact caller contract')
    tc=load(O/'TARGET_CLOSURE.source-only.json');hc=load(O/'HISTORY_CLOSURE.source-only.json')
    # Only declaration metadata is decoded; none of its scientific referents.
    old=loadref(g['evidence']['guard_acceptance']);same(old['helpers'],g['prior_original_guard_helpers'],'immutable old11 guard paths')
    need(old['scientific_targets_executed'] is False and old['all_declared_guards_passed'] is True,'old guard scope')
    for key in ('genuine_outer','independent_review'):refread(old[key])
    report=loadref(old['report']);same(report['packet'],str(O),'actual report keeps O')
    families=[('parent',['source','caller','runtime_acceptance','mode','late','late_postcheck']),('worker',['source','caller','runtime_acceptance','mode','late','late_postcheck']),('capture',['positive','changed_copy','buffer_drift','occupied']),('monitor',['positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap']),('runtime',['positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config']),('static',['positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command']),('acceptance',['positive','source_execution','caller_binding','caller_history','caller_ret','guards_absent','runtime_binding','runtime_loader','runtime_profile']),('mode',['normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift']),('relation',['positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped'])]
    ids=[family+'_'+kind for family,kinds in families for kind in kinds]
    same(len(ids),65,'manual source-derived65');same(report['control_order'],ids,'literal full65 order');same([r['id'] for r in report['controls']],ids,'complete65 record order')
    same(report['counts'],{'total':65,'passed':65,'failed':0},'original65 counts')
    for flag in ('target_or_scientific_helper_imported','scientific_fixtures_or_controls_executed','production_runtime_qualified','actual_data_admitted','full32_qualified'):need(report[flag] is False,'original false '+flag)
    same(report['helpers_before'],report['helpers_after'],'original helper custody')
    need(report['helpers_unchanged'] is True and report['runtime_observation_substitutions_explicit'] is True,'old explicit substitutions')
    for name,pin in report['helpers_before'].items():same(pin,next(r['pin'] for r in g['helpers'] if Path(r['path']).name==name),'all seven actual helper pins')
    familyrows=[]
    for row in report['controls']:
        same(sorted(row),['error','evidence','id','passed'],'closed actual guard row');need(row['passed'] is True and row['error'] is None and type(row['evidence'])is dict,'actual record success '+row['id'])
        e=row['evidence'];identifier=row['id']
        if identifier.startswith(('parent_','worker_')):
            need(all(x is True for x in e['checks'].values()),'all first-error/tail checks '+identifier)
            side,kind=identifier.split('_',1);late=kind.startswith('late')
            same(e['counts'],{'sources':2,'science':0,'child':0,'helpers':(3 if side=='parent' else 2) if late else 0,'runtime':2 if late else 0,'profile':2 if late else 0,'loaded':2 if late else 0},'entire counters '+identifier)
            receipt=loadref(e['receipt']);same(receipt['error'],{'type':'ValueError','message':'isolated_'+('late' if late else kind)},'actual first error '+identifier)
            if kind=='late_postcheck':same(receipt['postchecks']['runtime']['error'],{'type':'ValueError','message':'isolated_runtime_tail_failure'},'independent runtime tail '+identifier)
        if identifier.startswith('runtime_'):
            need(e['pass'] is True,'runtime returned pass propagated');same(e['observed_failure'],None if e['expected_failure'] is None else {'type':'ValueError','message':e['expected_failure']},'runtime exact first failure')
        if identifier.startswith('static_'):same(e,{'actual_static_validator_used':True,'card_written':False,'kind':identifier[7:]},'static whole result')
        if identifier.startswith('mode_'):same(e,{'actual_mode_admission_parser_used':True,'isolated_guard_metadata_only':True,'no_real_stage_admitted':True},'mode whole result')
        familyrows.append({'id':identifier,'original_evidence_pin':pure(canonical(e)),'path_applicability':'manual source covariance; original execution only'})
    root65=loadref(g['evidence']['guard_root_actual']);need(root65['status']=='ACCEPT_GENUINE_65_NONSCIENTIFIC_CALLER_GUARDS','root old65 status')
    oldcheck=loadref(root65['independent_complete_check']);same(len(oldcheck['checks']),87358,'accepted full old independent check retained')
    need(all(r['passed'] is True for r in oldcheck['checks']),'old complete check predicates');same(oldcheck['summary']['guard_report'],old['report'],'accepted full review exact old report')
    for r in refs(root65):refread(r)
    # Complete current profile snapshots, source/card/outer and selected descriptors.
    pc=loadref(assignment['profiles_card']);same(pc['packet'],str(O),'profiles original observer packet');same(pc['environment_root'],str(E),'profiles E environment')
    need(pc['scientific_execution'] is False,'profiles no science')
    for r in refs(pc):refread(r)
    profiles={};snapshots=[];profilefiles=[]
    for mode in ('normal','optimized'):
        phase='profile_'+mode;c=loadref(pc['completions'][phase]);outer=loadref(pc['genuine_outer'][phase]);refread(outer['raw_tool_receipt'])
        same(c['environment'],g['proposed_environment'],'complete E10 environment '+mode);same(c['sources'],pc['sources'],'profile exact RI1413 sources')
        need(c['first_error'] is None and c['independent_tail_errors']==[] and c['status']=='CAPTURED_FOR_INDEPENDENT_REVIEW','accepted profile completion')
        same(outer['completion'],pc['completions'][phase],'outer entire completion');same(outer['command'],c['command'],'outer command');same(outer['environment'],c['environment'],'outer environment');need(type(outer['exit_code'])is int and outer['exit_code']==0,'outer actual exit0')
        for r in c['artifacts'].values():refread(r)
        output=Path(pc['completions'][phase]['path']).parent;need(len(list(output.iterdir()))==16,'complete16 profile namespace')
        for p in sorted(output.iterdir()):read(p)
        before=loadref(c['artifacts']['PRE']);after=loadref(c['artifacts']['POST']);same(before,after,'full PRE POST '+mode)
        p=loadref(c['artifacts']['PROFILE']);q=loadref(c['artifacts']['checks'])['profile'];same(p['profile_before'],p['profile_after'],'whole runtime profile stable');same(p['profile_before'],q['expected_runtime'],'profile checked expectation')
        same(p['profile_before']['optimize'],0 if mode=='normal' else 1,'actual modeflag');need(str(E) not in p['profile_before']['path'] and str(O) not in p['profile_before']['path'],'isolated import path excludes both packet roots')
        same(p['startup'],{'enable_user_site':False,'site_prefixes':[p['profile_before']['prefix']],'distutils_hook_loaded':True,'sitecustomize_loaded':True,'usercustomize_loaded':False},'complete startup branch')
        need(p['scientific_targets_imported_or_executed'] is False and q['scientific_qualification'] is False and q['full_import_trace_claim'] is False,'profile finite scope')
        same(q['preobserved_domain'],before['preobserved_dyld_routes'],'whole observed-route pre-domain');same(q['full_dyld_error'],p['decimal']['extension_import_error'],'whole actual decimal error retained')
        need(len(q['ordered_actual_dyld_attempts'])==10 and len(p['modules'])==71 and len(q['all_descriptors'])==213,'full10routes71modules213descriptors')
        inventory={r['path']:r for r in before['runtime_inventory']['files']}
        for desc in q['all_descriptors']:
            raw=p['modules'][desc['module']][desc['field']]
            if 'binding' in desc:
                binding=desc['binding'];same(binding['named_path'],raw,'exact named descriptor');same(binding['target'],{k:inventory[binding['resolved_path']][k] for k in ('bytes','sha256')},'descriptor complete runtime membership')
            elif 'identity' in desc:
                same(raw,str(O/'profile_observe.source-only.py'),'original observer file');refread(desc['identity'])
            elif 'absent_from_complete_inventory' in desc:
                same(desc['path'],raw,'absent descriptor literal');need(raw not in inventory and desc['field']=='cached' and desc['absent_from_complete_inventory'] is True,'absent cache alternative')
            else:same(desc['value'],raw,'full sentinel descriptor')
        snapshots.append(before);profiles[mode]={'completion':c,'report':p,'check':q,'reference':c['artifacts']['PROFILE']};profilefiles.append(c['artifacts']['PRE'])
    same(snapshots[0],snapshots[1],'whole both-mode snapshot equality')
    same(read(profilefiles[0]['path']),read(root65['summary']['snapshot']['path']),'current/old guards full snapshot bytes')
    normal=profiles['normal'];optimized=profiles['optimized'];adjusted=dict(optimized['report']['profile_before']);adjusted['optimize']=0;same(adjusted,normal['report']['profile_before'],'only optimize runtime profile')
    differences=[]
    def differ(a,b,path):
        if type(a)is dict and type(b)is dict:
            same(sorted(a),sorted(b),'both-report complete field keys '+path)
            for key in a:differ(a[key],b[key],path+'/'+key)
        elif type(a)is list and type(b)is list:
            same(len(a),len(b),'both-report whole list length '+path)
            for i,(x,y) in enumerate(zip(a,b)):differ(x,y,path+'/'+str(i))
        elif canonical(a)!=canonical(b):differences.append({'path':path,'normal':a,'optimized':b})
    differ(normal['report'],optimized['report'],'')
    need(len(differences)==32,'exact full report32 differences')
    for row in differences:
        if row['path'] in ('/profile_before/optimize','/profile_after/optimize'):same([row['normal'],row['optimized']],[0,1],'exact optimize difference')
        else:need(row['path'].startswith('/modules/') and row['path'].endswith('/cached') and row['normal'].endswith('.cpython-311.pyc') and row['optimized']==row['normal'][:-4]+'.opt-1.pyc','exact declared cache path alternative')
    for key in ('ordered_actual_dyld_attempts','hash_algorithm_names','full_dyld_error','preobserved_domain'):same(normal['check'][key],optimized['check'][key],'both-mode whole '+key)
    deps=load(B/'ri141-white-bootstrap-source-h58ls076/DEPENDENCIES.source-only.json',pc['sources']['dependencies'] if 'dependencies' in pc['sources'] else None)
    # Authentic historical closure, independently accepted earlier, is unchanged.
    snap=snapshots[0]
    same(snap['runtime_inventory'],loadref(deps['historical_runtime']),'whole historical runtime inventory')
    same(snap['interpreter'],loadref(deps['historical_interpreter']),'full authentic candidate interpreter binding')
    same(snap['optional_namespaces'],loadref(deps['historical_optional_namespaces']),'whole accepted optional namespace')
    runtime=snap['runtime_inventory'];same([len(runtime[k]) for k in ('roots','extra_files','files','symlinks','absent_paths','loader_bindings')],[3,13,9923,3,8,8],'complete finite runtime counts')
    selection=snap['selection']['files'];same([r['path'] for r in selection],[r['path'] for r in runtime['files']],'every runtime selection member')
    need(sum('pyc_first16_hex' in r for r in selection)==3394,'all3394 opaque cache headers')
    for key in ('sources','root_counts','host_bootstrap','cache_scope'):need(key in snap,'retained snapshot '+key)
    sidecars={}
    for field,key in [('runtime_inventory','runtime_inventory'),('selection','selection'),('optional_namespaces','optional_namespaces'),('observed_dyld_routes','preobserved_dyld_routes'),('host_scope','host_bootstrap')]:
        sidecars[field]={'snapshot':profilefiles[0],'json_pointer':'/'+key,'canonical_whole_field_pin':pure(canonical(snap[key])),'same_in_optimized_snapshot':True,'operational_sidecar_created':False}
    # Pin accepted source/static premise records without re-running any source.
    for rel in ['ri141-white-bootstrap-source-h58ls076/PROTOCOL.md','ri141-white-bootstrap-source-h58ls076/runtime_metadata.py','ri141-white-bootstrap-source-h58ls076/prepare.py','ri121-static-runtime-closure-ulnsAMI8/STARTUP_IMPORT_REVIEW.md','ri121-static-runtime-closure-ulnsAMI8/STATIC_CLOSURE_REVIEW.md','ri121-root-caller-review-e6_dha8i/ROOT_STATIC_CLOSURE_REVIEW.json','ri121-root-runtime-qualification-jsf0o3_x/ROOT_RUNTIME_ADJUDICATION.json','ri193-current-e-optimized-review-p2ylnt9f/HANDOFF.json','ri193-current-e-optimized-review-p2ylnt9f/INDEPENDENT_REVIEW.md']:
        read(B/rel)
    prior=load(B/'ri121-root-runtime-qualification-jsf0o3_x/ROOT_RUNTIME_ADJUDICATION.json')
    same(prior['expected_runtime'],normal['report']['profile_before'],'retained admitted candidate profile');same(prior['interpreter'],snap['interpreter'],'same original candidate interpreter')
    for row in deps['opaque_files']:refread(row)
    # Fixed literal source anchors; no parse, AST, compile or subject execution.
    anchors={
      'worker.py':["root=path.parent;control=root/'control.py'","K.same(sys.argv,[str(root/'worker.py'),str(path),mode],'worker argv')","K.capture_targets(m,C)","phase='fabricated_qualification'"],
      'launch.py':["cwd=str(root),env=m['environment'],start_new_session=True)","root=path.parent;control=root/'control.py'"],
      'runtime_support.py':["allowed.update({item['path']:item['pin'] for item in manifest['helpers']})","allowed.update({item['copy']:item['pin'] for item in manifest['sources']})"],
      'evidence.py':["str(a/tree/'WC19-seed.fabricated')","str(b/tree/'WC19-seed.fabricated')"],
      'guard_controls.source-only.py':["dir=args.output.parent","exec(compile(body,str(path),'exec'),value.__dict__)","refusal(lambda:K.validate_static(m,packet,C),message)"]}
    for name,strings in anchors.items():
        text=read(O/name).decode('utf-8')
        for anchor in strings:need(anchor in text,'manual-reviewed literal anchor '+name+' '+anchor)
    return {'schema':'ri194-saved-administrative-applicability-check-v1','status':'PASS_ADMINISTRATIVE_RECONCILIATION_NOT_OPERATIONAL_ADMISSION','helper_correspondence':helpermap,'guard_family_counts':{name:len(kinds) for name,kinds in families},'guard_records':familyrows,'guard_new_execution_claimed':False,'additional_required_controls':[],'sidecar_mapping':sidecars,'whole_profile_differences':differences,'profile_references':{k:v['reference'] for k,v in profiles.items()},'original_guard_report':old['report'],'runtime_counts':{'files':9923,'bytes':sum(r['bytes'] for r in runtime['files']),'cache_headers':3394,'loader_bindings':8,'fixed_absences':8,'optional_namespaces':3},'scope':'Source applicability plus saved metadata only; manual reasoning and inherited independent acceptance remain explicit. No actual runtime capture, target/control execution, numerical decode, card or admission.'}

if __name__=='__main__':
    result=None
    try:result=check_main()
    except BaseException as exc:
        result={'schema':'ri194-saved-administrative-applicability-check-v1','status':'FAILED_ADMINISTRATIVE_CHECK','error':{'type':type(exc).__name__,'message':str(exc)}}
        raise
    finally:
        result.update(checks=CHECKS,identities=list(IDENTITIES.values()),decoded_administrative_files=DECODED,administrative_python=sys.executable)
        out=D/(sys.argv[1] if len(sys.argv)>1 else 'ADMIN_CHECK.json')
        need(out.parent==D,'exclusive reviewer output')
        with out.open('xb') as f:f.write(canonical(result));f.flush();os.fsync(f.fileno())
        print(json.dumps({'status':result['status'],'checks':len(CHECKS),'identities':len(IDENTITIES),'output':str(out)}))
