"""Reviewer-owned saved administrative evidence checks. No subject imports or runs.
Only reads stored evidence/source bytes. Never follows a saved vendor/runtime path.
Reconstructs metadata expectations from the reviewed contract, not parent recipes.
"""
from pathlib import Path
import json, hashlib, stat, copy, shlex, traceback
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri143-root-feasibility-review-b9bt7rgh';O=B/'ri144-genuine-bootstrap15-operation-iyywumt2'
Q=B/'ri144-bootstrap-guard-source-oaj1jvyt';R=B/'ri144-independent-actual15-review-rt_iv488'
C=O/'output/controls';P=O/'output'
REPO=Path('/Volumes/AI_DATA/development/det_8_framework-ret')
checks=[]; observations={}; case_results=[]
def ck(ok,label):
    if not ok: raise AssertionError(label)
    checks.append(label)
def canonical(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode()
def eq(a,b,label):ck(canonical(a)==canonical(b),label)
def pairs(rows):
    d={}
    for k,v in rows:
        if k in d:raise ValueError('duplicate key '+k)
        d[k]=v
    return d
def readbytes(p):
    p=Path(p);ck(p.is_relative_to(B) or p.is_relative_to(REPO),'read restricted to saved evidence '+str(p))
    ck(not p.is_symlink() and p.resolve()==p,'literal saved path '+str(p));s=p.stat();ck(stat.S_ISREG(s.st_mode),'regular '+str(p))
    raw=p.read_bytes();ck(s==p.stat(),'stable read '+str(p));return raw

def j(p):return json.loads(readbytes(p),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def pure(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def pin(p):return {'path':str(p),**pure(readbytes(p))}
def verify(ref):eq(pin(ref['path']),{k:ref[k] for k in ('path','bytes','sha256')},'opaque pin '+ref['path'])
def state(p):
    s=Path(p).lstat();return [getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]
def identity(p):return {**pin(p),'resolved_path':str(p),'state':state(p),'symlink_chain':[]}
def tree(root):
    out=[]
    for p in sorted(root.rglob('*')):
        ck(not p.is_symlink(),'no output link '+str(p))
        if p.is_dir():out.append({'kind':'directory','relative':str(p.relative_to(root))})
        else:out.append({'kind':'file','relative':str(p.relative_to(root)),**pure(readbytes(p))})
    return out

def run():
    input_ref={'path':str(D/'ACTUAL15_REVIEW_INPUT.json'),'bytes':28201,'sha256':'cc05c7cfc41891451003a946b8f632b3aee0fb5978aea32f1dea2fdc06ed2cfa'}
    verify(input_ref);inp=j(input_ref['path'])
    for v in inp.values():
        if type(v) is dict and set(v)=={'path','bytes','sha256'}:verify(v)
    deps=j(Q/'DEPENDENCIES.source-only.json');handoff=j(Q/'HANDOFF.json');source_root=j(D/'ROOT_MEASUREMENT_SOURCE_CHECK.json')
    refs=handoff['files']+[pin(Q/'HANDOFF.json')]+deps['opaque_files']
    ck(len(refs)==482 and len({r['path'] for r in refs})==482,'482 distinct source and dependency files')
    eq(sorted(p.name for p in Q.iterdir()),handoff['exact_namespace'],'exact ten-file source namespace')
    for r in refs:verify(r)
    expected_map={r['path']:r for r in refs};eq(sorted(expected_map),sorted(x['path'] for x in source_root['observations']),'root source observation exact domain')
    for row in source_root['observations']:
        eq(identity(row['path']),row,'full preserved source state '+row['path'])
    observations['source']={'packet':10,'dependencies':472,'dependency_bytes':sum(r['bytes'] for r in deps['opaque_files']),'all_full_saved_states_equal':482}
    rows=tree(O);eq(len(rows),52,'whole operation52');ck(sum(x['kind']=='file' for x in rows)==32,'operation32files')
    expected_rows=[]
    for x in inp['operation_tree']:
        if x['kind']=='directory':expected_rows.append(x)
        else:
            p=O/x['relative'];eq(identity(p),x['identity'],'operation saved fullstate '+x['relative'])
            expected_rows.append({'kind':'file','relative':x['relative'],**{k:x['identity'][k] for k in ('bytes','sha256')}})
    eq(rows,expected_rows,'whole operation exact52domain and file identities')
    pc=j(O/'cards/launcher.json');cc=j(O/'cards/controls.json');pf=j(O/'cards/preflight.json');dispatch=j(D/'ROOT_DISPATCH.json')
    for r in dispatch['cards']:verify(r)
    for row in dispatch['copies']:verify(row['original']);verify(row['operational']);eq(readbytes(row['original']['path']).hex(),readbytes(row['operational']['path']).hex(),'original/copy exact '+row['operational']['path'])
    ids=['B01','B02','B03','B04','B05','B06','B07_path','B07_resolved_path','B07_symlink_chain','B07_bytes','B07_sha256','B07_state','B08','B09','B10']
    bp='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
    base={'path':bp,'resolved_path':bp,'bytes':102352,'sha256':'1e78c38b861b64659075942e1d9bdfa083dbb1eb23bd96bd5d166756c1795524','state':[16777232,172336345,33261,1,102352,1762508227000000000,1763521990665808991],'symlink_chain':[]}
    eq(deps['selected_bootstrap_binding'],base,'authentic historical baseline exactsixfields');eq(pf['selected_interpreter_binding'],base,'genuine current preflight selected sixfields')
    env={'LC_ALL':'C','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PATH':'/usr/bin:/bin','TMPDIR':str(O/'environment/tmp'),'TZ':'UTC','VECLIB_MAXIMUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
    limits={'child_rss_kib':524288,'child_seconds':180,'file_bytes':67108864,'genuine_outer_timeout_seconds':960,'maximum_sample_gap_seconds':0.1,'namespace_bytes':536870912,'namespace_entries':25000,'parent_soft_seconds':900,'poll_seconds':0.025,'ps_timeout_seconds':0.05,'stream_bytes':67108864}
    premises={k:True for k in ['apple_loader_and_cache_external','genuine_bootstrap_host_preflight_external','genuine_tool_completion_external','sampled_child_only_not_parent_or_group_quota','saved_parent_pid_not_authenticated_child_identity','stable_supplier_host_and_no_descendants']}
    cmd=[bp,'-I','-B',str(Q/'bootstrap_controls.source-only.py'),'--admission',str(O/'cards/controls.json'),'--output',str(C)]
    parent_cmd=[bp,'-I','-B',str(Q/'launch_controls.source-only.py'),'--admission',str(O/'cards/launcher.json')]
    sources={n:pure(readbytes(Q/n)) for n in ['DEPENDENCIES.source-only.json','bootstrap_controls.source-only.py','launch_controls.source-only.py']}
    eq(cc,{'schema':'ri144-root-bootstrap-control-admission-v1','status':'AUTHORIZE_ONLY_FIFTEEN_ISOLATED_BOOTSTRAP_EXPECTATIONS','launcher_handoff':pin(Q/'HANDOFF.json'),'target_handoff':deps['target_handoff'],'sources':sources,'controls':ids,'output':str(C),'environment_root':str(O/'environment'),'command':cmd,'independent_source_review':deps['target_review'],'genuine_outer_required':True},'entire closed child card')
    eq(pc,{'schema':'ri144-root-bootstrap-launcher-admission-v1','status':'AUTHORIZE_ONLY_RI144_FIFTEEN_BOOTSTRAP_GUARDS','launcher_handoff':pin(Q/'HANDOFF.json'),'launcher_review':pin(O/'cards/review.json'),'launcher_adjudication':pin(O/'cards/adjudication.json'),'bootstrap_host_preflight':pin(O/'cards/preflight.json'),'controls_admission':pin(O/'cards/controls.json'),'output':str(P),'environment_root':str(O/'environment'),'launcher_command':parent_cmd,'child_command':cmd,'environment':env,'limits':limits,'external_premises':premises},'entire closed parent card')
    eq(pf['actual_environment'],env,'preflight ten environment fields');eq(tree(O/'environment'),[{'kind':'directory','relative':'tmp'}],'empty stable controlled environment')
    rd=j(O/'cards/adjudication.json');ck(rd['source_accepted'] is True and rd['execution_admitted'] is False and rd['controls_executed']==0,'source acceptance not retrospective execution authority')
    ck(dispatch['actual_completion_at_admission'] is False and dispatch['retry_authorized'] is False and dispatch['prior_attempt_remains_rejected'] is True,'single new operation without retry or repaired history')
    tool=j(D/'GENUINE_TOOL_COMPLETE.json');eq(tool['invocation'],dispatch['invocation'],'actual tool exact admitted invocation')
    eq(tool['result'],{'chunk_id':'32ad3f','wall_time_seconds':0.613061834,'exit_code':0,'original_token_count':0,'output':''},'genuine final immediate exit0 receipt; no session')
    outer=shlex.split(tool['invocation']['cmd']);eq(outer[:3],['exec','/usr/bin/env','-i'],'clean outer env primitive')
    eq(outer[3:13],[k+'='+v for k,v in sorted(env.items())],'actual tool ten env tokens')
    # shlex retains the single-quoted Perl expression with its literal double quotes.
    eq(outer[13:15],['/usr/bin/perl','-e'],'literal deadline process')
    eq(outer[15],'$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;','fixed actual deadline expression')
    eq(outer[16:],parent_cmd,'direct vendor parent argv');eq(tool['invocation']['workdir'],str(O),'actual operation cwd');ck(tool['invocation']['login'] is False,'no login environment')
    rep=j(C/'REPORT.json');ck(readbytes(C/'REPORT.json')==canonical(rep),'canonical complete report')
    # Independently listed ordered gates, inferred from retained real target and reader.
    trace_template=[('g','bootstrap selection provenance absent from closure'),('o','private_provenance_read')]+[('g',n) for n in ['closed metadata FilePin','literal source/metadata path','bounded regular source/metadata','metadata opened drift','metadata descriptor drift','metadata read drift','metadata reference drift']]+[('g','duplicate metadata key')]*8+[('g','canonical metadata framing')]+[('g',n) for n in ['accepted direct bootstrap selection provenance','closed selected interpreter binding','genuine preflight selected interpreter identity','literal direct bootstrap selection']]+[('o','supplier_bytes'),('g','opaque evidence reference drift'),('o','supplier_lstat'),('g','selected interpreter state drift'),('o','interpreter_descriptor'),('g','direct interpreter descriptor')]
    stops=[28,1,9,19,20,20,21,21,21,21,21,21,24,26,28]
    exp_cases=[]
    for index,name in enumerate(ids):
        private_path=C/name/'PROVENANCE_DOUBLE.json'
        body={'schema':'ri144-private-provenance-double-v1','selected_bootstrap_binding':copy.deepcopy(base)}
        changed=copy.deepcopy(body);changed['selected_bootstrap_binding']['bytes']=102353
        actual_body=changed if name in ('B03','B04') else body
        expected_private=canonical(actual_body);ck(readbytes(private_path)==expected_private,'full canonical private body '+name)
        declared_body=changed if name=='B04' else body
        declared={'path':str(private_path),**pure(canonical(declared_body))}
        selected=copy.deepcopy(base)
        if name=='B05':selected.pop('state')
        if name=='B06':selected['extra']=True
        if name.startswith('B07_'):
            field=name[4:]
            mutations={'path':bp+'.changed','resolved_path':bp+'.changed','symlink_chain':[{'path':bp+'.alias','target':bp}],'bytes':102353,'sha256':'0'*64,'state':[16777232,172336346,33261,1,102352,1762508227000000000,1763521990665808991]}
            selected[field]=mutations[field]
        obs={'bytes':{k:base[k] for k in ('path','bytes','sha256')},'state':copy.deepcopy(base['state']),'descriptor':bp}
        if name=='B08':obs['bytes']['bytes']=102353
        if name=='B09':obs['state'][1]=172336346
        if name=='B10':obs['descriptor']=bp+'.changed'
        trace=[{'kind':'observer','name':n} if kind=='o' else {'kind':'gate','name':n,'passed':True} for kind,n in trace_template[:stops[index]]]
        refusal=None;returned=copy.deepcopy(base) if name=='B01' else None
        if name!='B01':trace[-1]['passed']=False;refusal={'type':'ValueError','message':trace[-1]['name']}
        e={'baseline_binding':base,'dependency_operand':{'bootstrap_selection_provenance':declared,'opaque_files':[] if name=='B02' else [declared],'selected_bootstrap_binding':base},'preflight_operand':{'selected_interpreter_binding':selected},'observer_doubles':obs,'private_provenance_declared':declared,'private_provenance_actual':pin(private_path),'complete_loaded_module':deps['target_module'],'captured_loaded_bytes':{k:deps['target_module'][k] for k in ('bytes','sha256')},'trace':trace,'returned_binding':returned,'first_refusal':refusal,'inputs_unchanged':True,'substitutions':['private provenance file and closure operand','supplier byte observation','supplier lstat observation','sys.executable descriptor'],'real_private_reader_parser_and_comparisons':True,'actual_supplier_observed':False,'production_authenticate_called':False,'expected_trace':trace,'expected_first_refusal':refusal,'expected_returned_binding':returned}
        expected={'id':name,'passed':True,'error':None,'evidence':e};eq(rep['controls'][index],expected,'complete independent case reconstruction '+name)
        exp_cases.append(expected);case_results.append({'id':name,'full_envelope':True,'full_private_bytes':True,'trace_entries':len(trace),'observed_observers':[t['name'] for t in trace if t['kind']=='observer'],'first_refusal':refusal,'returned_binding':returned})
    expected_rep={'schema':'ri144-fifteen-bootstrap-control-report-v1','status':'FIFTEEN_EXPECTATIONS_PASSED','order':ids,'controls':exp_cases,'counts':{'total':15,'passed':15,'failed':0},'sources':sources,'target_handoff':deps['target_handoff'],'target_module':deps['target_module'],'admission':pin(O/'cards/controls.json'),'output':str(C),'first_error':None,'independent_tail_errors':[],'actual_supplier_observed':False,'production_authenticate_called':False,'old25_rerun':False,'scientific_execution':False,'current_runtime_qualified':False,'ret_paused':True,'elapsed_seconds':rep['elapsed_seconds']}
    eq(rep,expected_rep,'whole report closed fields');ck(type(rep['elapsed_seconds']) is float and 0<rep['elapsed_seconds']<180,'bounded report elapsed')
    eq(j(C/'ATTEMPT.json'),{'schema':'ri144-controls-attempt-v1','admission':pin(O/'cards/controls.json'),'target':deps['target_module'],'controls':ids,'old25_rerun':False,'supplier_observation_is_double':True},'whole child attempt')
    childtree=tree(C);expected_domain={n:'file' for n in ('ATTEMPT.json','REPORT.json','NAMESPACE.json')}
    for name in ids:expected_domain[name]='directory';expected_domain[name+'/PROVENANCE_DOUBLE.json']='file'
    eq({x['relative']:x['kind'] for x in childtree},expected_domain,'child33 exact closed domain')
    eq(j(C/'NAMESPACE.json'),{'schema':'ri144-control-namespace-v1','root':str(C),'entries':[x for x in childtree if x['relative']!='NAMESPACE.json'],'excluded_not_yet_written':['NAMESPACE.json'],'all_partials_retained':True},'whole child namespace32plusfinal1')
    parenttree=tree(P);expected_parent={'controls':'directory',**{'controls/'+k:v for k,v in expected_domain.items()},**{n:'file' for n in ['ADMINISTRATIVE_CHECKS.json','ATTEMPT.json','BOOTSTRAP15.ATTEMPT.json','BOOTSTRAP15.COMPLETION.json','BOOTSTRAP15.stderr','BOOTSTRAP15.stdout','COMPLETE.json','ENVELOPE_CHECKS.json','NAMESPACE.json']}}
    eq({x['relative']:x['kind'] for x in parenttree},expected_parent,'parent43 exact closed domain')
    eq(j(P/'NAMESPACE.json'),{'schema':'ri144-retained-launcher-namespace-v1','root':str(P),'entries':[x for x in parenttree if x['relative'] not in ['NAMESPACE.json','COMPLETE.json']],'excluded_not_yet_written':['NAMESPACE.json','COMPLETE.json'],'all_partials_retained':True},'whole parent namespace41plusfinal2')
    admin={'report':pin(C/'REPORT.json'),'namespace':pin(C/'NAMESPACE.json'),'controls':ids,'count':15,'complete_administrative_envelopes_checked':True,'scientific_evaluation':False}
    eq(j(P/'ADMINISTRATIVE_CHECKS.json'),admin,'whole parent administrative return');eq(j(P/'ENVELOPE_CHECKS.json'),{'report':pin(C/'REPORT.json'),'checks':[{'id':n,'error':None} for n in ids]},'all15 parent recorded envelope checks')
    eq(j(P/'ATTEMPT.json'),{'schema':'ri144-bootstrap-launcher-attempt-v1','admission':pin(O/'cards/launcher.json'),'child_command':cmd,'environment':env,'limits':limits,'external_premises':premises,'loaded_module':deps['ri135_module'],'captured_loaded_bytes':{k:deps['ri135_module'][k] for k in ('bytes','sha256')},'scientific_execution':False},'whole parent attempt loaded monitor identity')
    attempt=j(P/'BOOTSTRAP15.ATTEMPT.json');ck(type(attempt['pid_owner']) is int and attempt['pid_owner']>0,'saved parent pid positive; not child credential');eq(attempt,{'command':cmd,'environment':env,'wall_seconds':180,'pid_owner':attempt['pid_owner'],'scientific_target_entry':False},'whole monitor attempt')
    mon=j(P/'BOOTSTRAP15.COMPLETION.json');ck(len(mon['samples'])==len(mon['monitor_attempts'])==10,'allten samples and attempts')
    previous=0.0
    for i,(raw,sample) in enumerate(zip(mon['monitor_attempts'],mon['samples'])):
        eq(set(raw).__len__(),4,'raw monitor closed cardinality '+str(i));eq(sorted(raw),['elapsed_seconds','returncode','stderr','stdout'],'raw keys '+str(i))
        ck(type(raw['returncode']) is int and raw['returncode']==0 and raw['stderr']=='','ps actual return '+str(i));ck(raw['stdout'].strip().isdigit(),'numeric raw ps '+str(i))
        t=raw['elapsed_seconds'];ck(type(t) is float and t>previous,'monotone sample '+str(i));rss=int(raw['stdout'].strip());gap=t-previous
        eq(sample,{'elapsed_seconds':t,'rss_kib':rss,'gap_seconds':gap},'entire sample exact reconstruction '+str(i));ck(gap<=.1 and rss<=524288,'unchanged gap and memory threshold '+str(i));previous=t
    peak=max(s['rss_kib'] for s in mon['samples']);reap=mon['elapsed_seconds']-previous;ck(0<=reap<=.1,'bounded final reap gap')
    expected_mon={'command':cmd,'environment':env,'wall_seconds':180,'samples':mon['samples'],'monitor_attempts':mon['monitor_attempts'],'peak_sampled_rss_kib':peak,'stop_reason':None,'child_exit_code':0,'first_error':None,'tail_errors':[],'elapsed_seconds':mon['elapsed_seconds'],'final_sample_to_reap_gap_seconds':reap,'final_sample_gap_passed':True,'stdout':pin(P/'BOOTSTRAP15.stdout'),'stderr':pin(P/'BOOTSTRAP15.stderr'),'passed':True}
    eq(mon,expected_mon,'whole monitor completion no hidden termination or tails');ck(0<mon['elapsed_seconds']<=180,'child wall bound');ck(readbytes(P/'BOOTSTRAP15.stdout')==readbytes(P/'BOOTSTRAP15.stderr')==b'','both zero streams')
    complete=j(P/'COMPLETE.json');eq(complete,{'schema':'ri144-bootstrap-launcher-completion-v1','status':'CAPTURED_FOR_ROOT_REVIEW','admission':pin(O/'cards/launcher.json'),'launcher_command':parent_cmd,'child_command':cmd,'environment':env,'limits':limits,'external_premises':premises,'first_error':None,'independent_tail_errors':[],'checks':{'card':'PASS','controls':admin,'dependency':'PASS','namespace':pin(P/'NAMESPACE.json'),'source':'PASS'},'artifacts':{'administrative_checks':pin(P/'ADMINISTRATIVE_CHECKS.json'),'attempt':pin(P/'ATTEMPT.json')},'child':mon,'elapsed_seconds':complete['elapsed_seconds'],'scientific_execution':False,'runtime_qualification':False,'ri130_65_guards_executed':False,'genuine_tool_completion_created':False,'ret_paused':True},'whole parent completion and every independent-tail result');ck(mon['elapsed_seconds']<=complete['elapsed_seconds']<=900,'parent soft deadline')
    observations['monitor']={'attempts':10,'samples':10,'elapsed_seconds':mon['elapsed_seconds'],'peak_sampled_rss_kib':peak,'maximum_gap_seconds':max(s['gap_seconds'] for s in mon['samples']),'final_reap_gap_seconds':reap,'parent_elapsed_seconds':complete['elapsed_seconds'],'child_elapsed_excludes_preallocation_authentication':True,'genuine_outer_exit':0}
    ck(len(parenttree)==43 and len(childtree)==33,'full namespace counts');ck(sum(x.get('bytes',0) for x in parenttree)<=536870912 and max(x.get('bytes',0) for x in parenttree)<=67108864,'all output namespace and file byte bounds')
    observations['namespace']={'operation_entries':52,'operation_files':32,'operation_directories':20,'parent_entries':43,'parent_recorded_entries':41,'child_entries':33,'child_recorded_entries':32,'output_file_bytes':sum(x.get('bytes',0) for x in parenttree)}
    # Entire saved supplier observations are compared; NEVER re-observe vendor files.
    pre=j(D/'BOOTSTRAP_PRE.json');post=j(D/'BOOTSTRAP_POST.json');ck(readbytes(D/'BOOTSTRAP_PRE.json')==readbytes(D/'BOOTSTRAP_POST.json'),'complete supplier PRE POST byteidentity')
    eq(pre['selected_interpreter_binding'],base,'PRE POST selected direct binding');eq(pre['actual_environment'],env,'PRE POST actual controlled environment');eq(pre['trusted_premises'],pf['trusted_premises'],'host stable premises retained');ck(pre['target_or_launcher_execution'] is False,'prepost collector not science entry')
    for k in ['collector','metadata_helper']:verify(pre[k])
    framework=pre['framework_namespace'];fm={r['path']:r for r in framework};ck(len(fm)==len(framework)==2004,'full2004 unique framework records')
    ck(all(p.startswith(pre['prefix']+'/') for p in fm),'framework literal declared domain')
    kinds={k:sum(r['kind']==k for r in framework) for k in ['file','directory','symlink']};eq(kinds,{'file':1810,'directory':184,'symlink':10},'full saved framework kinds')
    total=0
    for row in framework:
        ck('..' not in Path(row['path']).parts,'saved framework no traversal')
        if row['kind']=='file':
            ident=row['identity'];eq(sorted(ident),['bytes','path','resolved_path','sha256','state','symlink_chain'],'closed saved vendor identity');eq(ident['path'],row['path'],'vendor same path');ck(ident['bytes']==ident['state'][4] and len(ident['state'])==7 and len(ident['sha256'])==64,'saved vendor identity shape');total+=ident['bytes']
    eq(total,48024515,'full saved vendor byte sum');eq(total,pre['framework_file_bytes'],'reported vendor byte sum')
    eq(fm[bp]['identity'],base,'direct vendor full saved namespace binding')
    descriptor=pre['bootstrap_descriptor'];eq({k:v for k,v in descriptor.items() if k not in ['modules','version']},{'dont_write_bytecode':1,'executable':bp,'isolated':1,'optimize':0,'path':[pre['prefix']+'/lib/python39.zip',pre['prefix']+'/lib/python3.9',pre['prefix']+'/lib/python3.9/lib-dynload',pre['prefix']+'/lib/python3.9/site-packages'],'prefix':pre['prefix']},'complete recorded startup descriptor scope')
    modules=descriptor['modules'];ck(len(modules)==len({m['name'] for m in modules})==92,'all92 unique startup module records');cache_names=[];filemods=[];frozen=[]
    for m in modules:
        if m.get('identity'):
            ident=m['identity'];eq(ident['path'],m['file'],'module file binding '+m['name']);filemods.append(m['name'])
            if m['file'] in fm:eq(ident,fm[m['file']]['identity'],'whole module inventory identity '+m['name'])
            else:
                ck(m['file'] in [pre['collector']['path'],pre['metadata_helper']['path']],'only recorded external collector/helper '+m['name']);eq(identity(m['file']),ident,'external metadata module fullidentity '+m['name'])
        else:ck(m['file'] is None and m['origin'] in [None,'built-in','frozen'],'nonfile origins limited '+m['name'])
        if m['origin']=='frozen':frozen.append(m['name'])
        elif m['origin'] not in [None,'built-in']:eq(m['origin'],m['file'],'module origin/file '+m['name'])
        if m['cached']:
            ck(m['cached'].startswith(pre['prefix']+'/') and m['cached'] not in fm,'cached name saved absent '+m['name']);cache_names.append(m['cached'])
    bindings={r['path']:r for r in pre['bindings']};ck(len(bindings)==9,'nine unique bootstrap/tool bindings')
    ck(set(['/usr/bin/env','/usr/bin/perl','/usr/bin/python3','/bin/ps','/usr/bin/xcode-select','/usr/bin/xcrun','/System/Library/CoreServices/SystemVersion.plist','/Applications/Xcode.app/Contents/Developer/usr/bin/python3',pre['prefix']+'/Python3'])==set(bindings),'exactnine saved binding names')
    alias=bindings['/Applications/Xcode.app/Contents/Developer/usr/bin/python3'];eq({k:alias[k] for k in ['bytes','sha256','state','resolved_path']},{k:base[k] for k in ['bytes','sha256','state','resolved_path']},'alias reaches authentic exact vendor');eq(alias['symlink_chain'],[{'path':'/Applications/Xcode.app/Contents/Developer/usr/bin/python3','target':'../../Library/Frameworks/Python3.framework/Versions/3.9/bin/python3'},{'path':pre['prefix']+'/bin/python3','target':'python3.9'}],'exact saved alias chain')
    eq(pre['absences'],[pre['prefix']+'/lib/python39.zip','/Library/Python/3.9/site-packages'],'two recorded absences; no current probes')
    eq(pre['commands'],[{'command':['/usr/bin/xcode-select','-p'],'exit_code':0,'stderr':'','stdout':'/Applications/Xcode.app/Contents/Developer\n'},{'command':['/usr/bin/xcrun','--find','python3'],'exit_code':0,'stderr':'','stdout':'/Applications/Xcode.app/Contents/Developer/usr/bin/python3\n'}],'actual saved selection observations')
    for stage,chunk in [('PRE','9396f4'),('POST','de81e8')]:
        t=j(D/('BOOTSTRAP_'+stage+'_TOOL.json'));ck(t['result']['exit_code']==0 and t['result']['chunk_id']==chunk and 'session_id' not in t['result'],'genuine saved '+stage+' terminalreceipt')
        argv=shlex.split(t['invocation']['cmd']);eq(argv[:15],outer[:15],'bootstrap '+stage+' same env and deadline primitive');eq(argv[15],'$SIG{ALRM}="DEFAULT"; alarm 240; exec @ARGV; die $!;','bootstrap '+stage+' deadline');eq(argv[16:],[bp,'-I','-B',pre['collector']['path'],stage],'bootstrap '+stage+' exact collector command');ck(pin(D/('BOOTSTRAP_'+stage+'.json'))['sha256'] in t['result']['output'],'bootstrap '+stage+' returned digest')
    observations['saved_bootstrap']={'pre_post_bytes':len(readbytes(D/'BOOTSTRAP_PRE.json')),'pre_post_sha256':pin(D/'BOOTSTRAP_PRE.json')['sha256'],'framework_entries':2004,'kinds':kinds,'file_bytes':total,'startup_modules':len(modules),'module_file_identities':len(filemods),'cached_names_recorded_absent':len(cache_names),'frozen_origins':frozen,'saved_bindings':9,'recorded_absences':2,'current_runtime_or_vendor_probed_by_reviewer':False,'tool_origin_remains_root_observed_external_premise':True}
    # All objects read opaque or parsed as administrative saved evidence are stable at end.
    for r in refs:verify(r)
    eq(tree(O),rows,'complete operation preserved through review')
    return {'schema':'ri144-independent-saved-actual15-check-v1','status':'PASS','input':input_ref,'observations':observations,'case_results':case_results,'checks_passed':len(checks),'check_log':checks,'execution_performed_by_reviewer':False,'scientific_body_decoded':False,'current_supplier_observation':False}
if __name__=='__main__':
    try:result=run()
    except BaseException as exc:
        result={'schema':'ri144-independent-saved-actual15-check-v1','status':'REVIEWER_CHECK_FAILED','error':{'type':type(exc).__name__,'message':str(exc)},'traceback':traceback.format_exc(),'checks_passed':len(checks),'check_log':checks,'observations':observations,'case_results':case_results}
        (R/'CHECK_FAILED_02.json').write_bytes(canonical(result));print(result['traceback']);raise SystemExit(1)
    (R/'SAVED_ACTUAL_CHECKS.json').write_bytes(canonical(result));print(json.dumps({'status':result['status'],'checks_passed':len(checks),'observations':observations},indent=2))
