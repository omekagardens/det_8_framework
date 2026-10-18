"""RI170 finite author check: administrative JSON and opaque bytes only.
Never import/compile/AST/execute subjects, inspect supplier runtime, or decode
fixture/scientific JSON. This file is not an operational helper or admission.
"""
import hashlib
import json
import os
import shlex
import stat
from pathlib import Path

H = Path('/Volumes/AI_DATA/development/det-review-evidence/ri170-measurement-current-e-preflight-gikj2giy')
E = Path('/Volumes/AI_DATA/development/det-review-evidence')
rows = []
checks = []
reads = []

def need(ok, label):
    if not ok:
        raise ValueError(label)
    checks.append(label)

def decode(path):
    path = Path(path)
    reads.append(str(path))
    return json.loads(path.read_text())

def canonical(obj):
    return (json.dumps(obj, indent=2, sort_keys=True)+'\n').encode()

def filepin(path):
    path = Path(path)
    s = path.lstat()
    need(stat.S_ISREG(s.st_mode) and not path.is_symlink(), 'regular file '+str(path))
    h = hashlib.sha256(); total = 0
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''):
            total += len(b); h.update(b)
    t = path.lstat()
    fields = ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
    need(all(getattr(s,k)==getattr(t,k) for k in fields), 'stable read '+str(path))
    return {'path':str(path),'bytes':total,'sha256':h.hexdigest()}

def verify(row, role):
    p = row['path']
    need(p.startswith(str(E)+'/') or p.startswith('/Volumes/AI_DATA/development/det_8_framework-ret/docs/'), 'source/history path only '+role)
    got=filepin(p)
    need(got['bytes']==row['bytes'] and got['sha256']==row['sha256'], 'exact declared bytes '+role)
    rows.append({'role':role,**got})

try:
    refs = decode(H/'REFERENCE_BINDINGS.json')
    proposal = decode(H/'PREFLIGHT_PROPOSAL.json')
    commands = decode(H/'COMMAND_PROPOSALS.json')
    for name,ref in refs['references'].items(): verify(ref,'reference:'+name)
    R=refs['references']
    source=decode(R['source_manifest']['path'])
    graph=decode(R['binding_graph']['path'])
    deps=decode(R['ri141_dependencies']['path'])
    decision=decode(R['actual_inert106_root_decision']['path'])
    inventory=decode(R['inert_inventory']['path'])
    baseline=decode(R['old_baseline']['path'])
    profiles=decode(R['old_profiles']['path'])
    guards=decode(R['old_guards']['path'])
    need(proposal['source_bindings']==R,'exact shared proposal/reference bindings')
    need(proposal['current_execution_authorized'] is False,'no execution authority')
    need(all(v is True for v in proposal['prohibited_and_not_performed'].values()),'prohibited actions not performed')
    need(decision['status']=='ACCEPT_ONE_GENUINE_INERT_METADATA_QUALIFICATION' and decision['accepted_action']=='controls' and decision['accepted_controls']==106,'exact accepted actual inert106 scope')
    need(decision['actual_data_admitted'] is False and decision['scientific_qualification_accepted'] is False,'no scientific acceptance inferred')
    need(decision['source_manifest']==R['source_manifest'] and decision['original_source_acceptance']==R['source_adjudication'],'actual/source acceptance binding')
    for name in ('actual_summary','genuine_initial','genuine_terminal','independent_review'):
        verify(decision[name],'actual decision:'+name)
    need(len(source['dependencies'])==567 and len(source['modules'])==11,'567 dependencies and11 module identities')
    verify(source['adapter'],'source adapter')
    for k,v in source['modules'].items(): verify(v,'source module:'+k)
    for i,v in enumerate(source['dependencies']): verify(v,'source dependency:'+str(i))
    need(source['bootstrap_binding']==refs['declared_selected_bootstrap_from_accepted_source']==deps['selected_bootstrap_binding'],'historical declared vendor equality without observation')
    need(refs['no_current_supplier_observation'] is True,'supplier is explicitly unobserved here')
    need(len(deps['opaque_files'])==442,'442 opaque historical source roles')
    for i,v in enumerate(deps['opaque_files']): verify(v,'RI141 opaque:'+str(i))
    P=Path(R['ri141_prepare']['path']).parent
    for name,pin in refs['ri141_exact_source_map'].items(): verify({'path':str(P/name),**pin},'RI141 source:'+name)
    need(len(graph['copied_files'])==48 and graph['copied_file_count']==48,'exact48 copy map')
    destinations={v['destination']:v['source'] for v in graph['copied_files']}
    need(len(destinations)==48,'copy destinations unique')
    current=Path(graph['prospective_root'])
    need(str(current)==proposal['paths_proposed_not_created']['current_E'],'literal accepted E unchanged')
    for i,v in enumerate(graph['copied_files']):
        need(v['destination']==str(current/v['relative']),'exact relative destination:'+str(i))
        verify(v['source'],'copy source:'+str(i))
    need(len(graph['sources'])==30 and graph['target_count']==30,'30 target source pairs')
    for i,v in enumerate(graph['sources']):
        verify({'path':v['original'],**v['pin']},'target original:'+str(i))
        need({k:destinations[v['copy']][k] for k in ('bytes','sha256')}==v['pin'],'target mapped bytes:'+str(i))
        need(destinations[v['copy']]['path']==str(Path(deps['packet_root'])/v['relative']),'copy chain through accepted original packet:'+str(i))
    need(len(graph['helpers'])==11 and graph['helper_count']==11,'11 helper destinations')
    for v in graph['helpers']:
        need({k:destinations[v['path']][k] for k in ('bytes','sha256')}==v['pin'],'mapped helper '+v['path'])
    need(len(graph['history_originals'])==124 and graph['history_count']==124,'124 history roles')
    for i,v in enumerate(graph['history_originals']): verify(v,'graph history:'+str(i))
    need(len(graph['stage_bindings'])==17 and graph['stage_role_count']==17,'17 stage bindings')
    for name,v in graph['stage_bindings'].items():
        if v['path'] in destinations:
            need({k:destinations[v['path']][k] for k in ('bytes','sha256')}==v['pin'],'stage mapped bytes:'+name)
        else:
            need(name=='white_root_disposition','only accepted original stage disposition')
            verify({'path':v['path'],**v['pin']},'original stage:'+name)
    for name,v in graph['evidence'].items(): verify(v,'graph evidence:'+name)
    order=inventory['combined_order']
    need(len(order)==106 and len(set(order))==106,'106 unique literal control IDs')
    need(order==inventory['retained84_order']+inventory['new22_order'],'exact retained84/new22 ordered split')
    need(inventory['counts']=={'executed':0,'new':22,'retained':84,'total':106},'historical inventory source-only counts preserved')
    need(profiles['sources']==baseline['sources']==refs['ri141_exact_source_map'],'historical profiles and baseline exact3-source map')
    need(profiles['environment_root']==baseline['environment_root']==graph['old_environment_root'] and profiles['environment_root']!=str(current),'old environment cannot satisfy new E')
    need(guards['helpers']==graph['prior_original_guard_helpers'],'old guard11 exact original paths')
    need([(Path(v['path']).name,v['pin']) for v in guards['helpers']]==[(Path(v['path']).name,v['pin']) for v in graph['helpers']],'guard same bytes relocated paths')
    need(all(a['path']!=b['path'] for a,b in zip(guards['helpers'],graph['helpers'])),'R01 path change remains real')
    paths=proposal['paths_proposed_not_created']
    need(len(set(paths.values()))==8,'eight unique proposed roots')
    for name,path in paths.items():
        need(Path(path).parent==E and not os.path.lexists(path),'prospective path absent:'+name)
    need(not str(Path(paths['copy_environment'])/'tmp').startswith(str(current)+'/'),'copy TMPDIR disjoint from E')
    need(commands['do_not_dispatch_from_this_file'] is True and set(commands['commands'])=={'copy','capture','profile_normal','profile_optimized'},'only four nonoperative proposals')
    vendor=refs['declared_selected_bootstrap_from_accepted_source']['path']
    for name,c in commands['commands'].items():
        need(c['login'] is False and c['cwd']==paths['root_records'] and c['external_timeout_seconds']==960,'exact outer envelope:'+name)
        need(c['inner_argv'][:3]==[vendor,'-I','-B'],'isolated normal vendor parent:'+name)
        env=dict(graph['proposed_environment'])
        if name=='copy': env['TMPDIR']=str(Path(paths['copy_environment'])/'tmp')
        need(c['exact_environment']==env and len(env)==10,'exact ten-field environment:'+name)
        outer=['/usr/bin/env','-i']+[k+'='+env[k] for k in sorted(env)]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;']+c['inner_argv']
        need(c['outer_argv']==outer and shlex.split(c['shell_command'])==outer,'literal shell/argv equality:'+name)
        if name!='copy':
            card=paths['root_records']+'/ADMIT_'+name.upper()+'.json'
            need(c['inner_argv']==[vendor,'-I','-B',str(P/'prepare.py'),'--admission',card],'exact unchanged phase command:'+name)
            need(c['PRE_and_POST_child_argv']==[vendor,'-I','-B',str(P/'prepare.py'),'--snapshot',card],'exact snapshot commands:'+name)
            need(c['snapshot_child_seconds']==180 and c['separate_stage_admission_required'] is True,'separate180-second snapshot scope:'+name)
            if name.startswith('profile_'):
                need(c['profile_child_seconds']==30,'fixed30-second profile:'+name)
                need(c['profile_child_argv'][1:3]==['-I','-B'] and ('-O' in c['profile_child_argv'])==(name=='profile_optimized'),'profile mode flag:'+name)
    c=commands['commands']['copy']
    verify(c['bootstrap_text'],'copy literal proposal text')
    need(c['monitor_source']==R['ri141_prepare'],'unchanged complete monitor source')
    need(c['inner_argv']==[vendor,'-I','-B','-c',Path(c['bootstrap_text']['path']).read_text()],'entire text captured in proposed argv')
    need(c['monitored_child_argv']==[vendor,'-I','-B',R['adapter']['path'],'--admission',paths['root_records']+'/ADMIT_COPY_ADAPTER.json'],'exact copy adapter child')
    need(proposal['limits']['sampled_child_rss_kib']==524288 and proposal['limits']['copy_and_snapshot_child_seconds']==180 and proposal['limits']['profile_child_seconds']==30,'limits unchanged')
    outcome={'schema':'ri170-author-finite-metadata-check-v1','status':'PASS_SOURCE_PROPOSAL_ONLY',
      'not_independent_acceptance':True,'decoded_administrative_files':reads,
      'checks_passed':len(checks),'source_history_role_observations':len(rows),
      'unique_source_history_files':len({r['path'] for r in rows}),
      'role_observation_canonical_sha256':hashlib.sha256(canonical(rows)).hexdigest(),
      'counts':{'adapter_modules':11,'adapter_dependencies':567,'RI141_opaque_dependencies':442,'copied_originals':48,'target_originals':30,'helper_destinations':11,'historical_roles':124,'stage_bindings':17,'literal_controls':106,'proposed_absent_roots':8},
      'no_subject_import_compile_AST_or_execution':True,'no_scientific_or_fixture_JSON_decoding':True,'no_current_runtime_observation':True,'no_actual_cards_or_admission':True,'proposed_operational_paths_absent':paths,
      'checker':filepin(__file__)}
except BaseException as exc:
    outcome={'schema':'ri170-author-finite-metadata-check-v1','status':'FAIL_PRESERVED','error':{'type':type(exc).__name__,'message':str(exc)},'checks_completed':checks,'decoded_administrative_files':reads,'source_history_role_observations_completed':len(rows),'checker':filepin(__file__)}
    path=H/'CHECK_FAILURE.third.json'
    with path.open('xb') as f:f.write(canonical(outcome))
    print(json.dumps({'status':outcome['status'],'error':outcome['error'],'path':str(path)}))
    raise
with (H/'METADATA_CHECK.json').open('xb') as f:f.write(canonical(outcome))
print(json.dumps({'status':outcome['status'],'checks':outcome['checks_passed'],'observations':len(rows),'unique_files':outcome['unique_source_history_files'],'output':filepin(H/'METADATA_CHECK.json')}))
