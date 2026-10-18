"""Independent saved administrative review; never imports/runs subjects or observes runtime paths."""
from pathlib import Path
import json, hashlib, stat, shlex, re, traceback
B=Path('/Volumes/AI_DATA/development/det-review-evidence');REPO=Path('/Volumes/AI_DATA/development/det_8_framework-ret')
R=B/'ri146-independent-capture-review-i7o8n5j_';D=B/'ri146-root-current-capture-9bfi4u8s';O=B/'ri146-genuine-current-capture-heib6de2';P=O/'output';Q=B/'ri141-white-bootstrap-source-h58ls076'
log=[];summary={};used={}
def canon(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode()
def ck(ok,msg):
 if not ok:raise AssertionError(msg)
 log.append(msg)
def eq(a,b,msg):ck(canon(a)==canon(b),msg)
def pure(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def data(p):
 p=Path(p);ck(p.is_relative_to(B) or p.is_relative_to(REPO),'saved evidence path only '+str(p));ck('/env/' not in str(p),'never read candidate environment '+str(p));ck(not p.is_symlink() and p.resolve()==p,'literal saved file '+str(p));s=p.stat();ck(stat.S_ISREG(s.st_mode),'regular saved file '+str(p));raw=p.read_bytes();ck(s==p.stat(),'stable saved file '+str(p));used[str(p)]={'path':str(p),**pure(raw)};return raw

def pairs(x):
 d={}
 for k,v in x:
  if k in d:raise ValueError('duplicate '+k)
  d[k]=v
 return d
def j(p):return json.loads(data(p),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def pin(p):return {'path':str(p),**pure(data(p))}
def verify(r):eq(pin(r['path']),{k:r[k] for k in ('path','bytes','sha256')},'exact pin '+r['path'])
def ident(p):
 s=Path(p).lstat();return {**pin(p),'resolved_path':str(p),'symlink_chain':[],'state':[getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]}
def tree(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  ck(not p.is_symlink(),'no link in sealed evidence tree '+str(p))
  rows.append({'relative':str(p.relative_to(root)),'kind':'directory'} if p.is_dir() else {'relative':str(p.relative_to(root)),'kind':'file',**pure(data(p))})
 return rows

def run():
 source=j(D/'SOURCE_PRE.json');eq(pure(data(D/'SOURCE_PRE.json')),{'bytes':277180,'sha256':'a22eb8d4dd4a48db35e6f7cfab557f17c7ea11a3e602251bfa6b7a72c4adfd79'},'assigned pre-source exact identity')
 deps=j(Q/'DEPENDENCIES.source-only.json');h=j(Q/'HANDOFF.json');qreview=Path(B/'ri141-bootstrap-independent-review-k5bss5xp');rh=j(qreview/'HANDOFF.json')
 refs=h['files']+[pin(Q/'HANDOFF.json')]+rh['files']+[pin(qreview/'HANDOFF.json')]+deps['opaque_files']
 extra=[B/'ri140-root-source-adjudication-8796wh9l/RI141_ROOT_ADJUDICATION.json',B/'ri143-root-feasibility-review-b9bt7rgh/RI144_ROOT_ACTUAL_ADJUDICATION.json',B/'ri143-root-feasibility-review-b9bt7rgh/ROOT_ACTUAL_REVIEW_CORRECTION.json',B/'ri144-independent-actual15-review-rt_iv488/HANDOFF.json']
 refs.extend(pin(p) for p in extra);ck(len(refs)==471 and len({x['path'] for x in refs})==471,'closed471source dependency domain')
 eq(sorted(x['path'] for x in refs),[x['path'] for x in source['identities']],'source471 sorted exact domain')
 for x in refs:verify(x)
 for row in source['identities']:eq(ident(row['path']),row,'fresh saved471 fullstate '+row['path'])
 for ns in source['namespaces']:eq(sorted(p.name for p in Path(ns['path']).iterdir()),ns['names'],'exact source/review namespace '+ns['path'])
 postsource=j(D/'SOURCE_POST.json');eq(postsource,{'identities':source['identities'],'unchanged':True},'root471 post equality');summary['source']={'full_states':471,'dependency_files':442,'dependency_bytes':sum(x['bytes'] for x in deps['opaque_files']),'source_namespace':15,'review_namespace':10}
 card=j(O/'CAPTURE_ADMISSION.json');layout=j(D/'OPERATION_LAYOUT.json');adjud=j(D/'CAPTURE_SOURCE_ADJUDICATION.json');custody=j(D/'ADMISSION_CUSTODY.json');complete=j(P/'COMPLETE.json')
 for field in ['card','source_review']:eq(ident(custody[field]['path']),custody[field],'actual retained admission '+field)
 verify(custody['source_pre']);eq(custody['genuine_operation_count'],1,'one genuine operation');eq(custody['operation'],str(O),'operation ownership')
 for value in adjud.values():
  if type(value) is dict and set(value)=={'path','bytes','sha256'}:verify(value)
 bp='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9';base=deps['selected_bootstrap_binding'];eq(base,layout['selected_interpreter_binding'],'baseline and fresh selected binding')
 env={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(O/'environment/tmp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
 eq(layout['environment'],env,'exact controlled environment layout')
 sources={n:pure(data(Q/n)) for n in ['prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json']}
 bounds={'snapshot_seconds':180,'profile_seconds':30,'guard_seconds':180,'rss_kib':524288,'target_poll_seconds':.025,'maximum_sample_gap_seconds':.1,'ps_timeout_seconds':.05,'file_bytes':67108864,'driver_soft_seconds':900,'genuine_outer_timeout_seconds':960}
 vendor=j(D/'BOOTSTRAP_PRE.json');ck(data(D/'BOOTSTRAP_PRE.json')==data(D/'BOOTSTRAP_POST.json'),'full vendor observations byteidentity');eq(vendor['selected_interpreter_binding'],base,'fresh vendor selected sixfields');eq(vendor['actual_environment'],env,'fresh vendor actual environment')
 selected={'named_path':bp,'resolved_path':bp,'symlink_chain':[],'target':{k:base[k] for k in ('bytes','sha256')}}
 host={'uname':vendor['host'],'system_version':{k:next(x for x in vendor['bindings'] if x['path']=='/System/Library/CoreServices/SystemVersion.plist')[k] for k in ('path','bytes','sha256')}}
 expected_card={'schema':'ri141-root-preparation-admission-v1','status':'AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION','phase':'capture','sources':sources,'source_review':pin(D/'CAPTURE_SOURCE_ADJUDICATION.json'),'packet':deps['packet_root'],'output':str(P),'environment_root':str(O/'environment'),'bootstrap':selected,'bootstrap_host_preflight':pin(D/'BOOTSTRAP_PRE.json'),'host':host,'baseline_acceptance':None,'normal_acceptance':None,'profiles_acceptance':None,'guard_admission':None,'bounds':bounds,'genuine_outer_required':True}
 eq(card,expected_card,'entire closed17field capture admission');ck(len(card)==17 and data(O/'CAPTURE_ADMISSION.json')==canon(card),'17field canonical card')
 eq(tree(O/'environment'),[{'kind':'directory','relative':'tmp'}],'empty environment tmp retained');eq(j(P/'ATTEMPT.json'),{'schema':'ri133-preparation-attempt-v1','admission':pin(O/'CAPTURE_ADMISSION.json'),'sources':sources,'phase':'capture','environment':env,'scientific_execution':False},'entire parent attempt')
 parentcmd=[bp,'-I','-B',str(Q/'prepare.py'),'--admission',str(O/'CAPTURE_ADMISSION.json')];childcmd=[bp,'-I','-B',str(Q/'prepare.py'),'--snapshot',str(O/'CAPTURE_ADMISSION.json')]
 tool=j(D/'GENUINE_TOOL_COMPLETE.json');args=j(D/'GENUINE_TOOL_ARGUMENTS.json');eq(tool['command'],args['initial_call']['arguments']['cmd'],'genuine saved command matches initial actual arguments');tokens=shlex.split(tool['command']);eq(tokens[:3],['exec','/usr/bin/env','-i'],'outer controlled primitive');eq(tokens[3:13],[k+'='+v for k,v in env.items()],'all10 ordered environment tokens');eq(tokens[13:16],['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;'],'literal unchanged outer deadline');eq(tokens[16:],parentcmd,'actual direct vendor invocation')
 eq(args['initial_call']['returned_chunk'],'3d59d7','genuine initial chunk');eq(args['initial_call']['returned_session_id'],81040,'genuine initial session');eq(tool['initial']['session_id'],81040,'raw initial session');eq(args['terminal_call']['arguments'],{'session_id':81040,'chars':'','yield_time_ms':1000,'max_output_tokens':1800},'actual terminal session polling arguments');eq(args['terminal_call']['returned_chunk'],'c78edf','actual terminal chunk');eq(tool['terminal']['chunk_id'],'c78edf','raw terminal chunk');ck(tool['terminal']['exit_code']==0 and type(tool['terminal']['exit_code']) is int,'terminal actual success');ck(tool['initial']['output']==tool['terminal']['output']=='','genuine empty outer outputs');eq(args['initial_call']['omitted_workdir_default'],str(REPO),'genuine parent default cwd');ck(args['initial_call']['arguments']['login'] is False,'actual nonlogin invocation')
 eq(j(D/'GENUINE_OUTER.json'),{'schema':'ri133-root-genuine-outer-v1','status':'ACTUAL_TOOL_COMPLETION','command':parentcmd,'environment':env,'exit_code':0,'completion':pin(P/'COMPLETE.json'),'raw_tool_receipt':pin(D/'GENUINE_TOOL_COMPLETE.json'),'external_timeout_seconds':960},'complete root outer wrapper')
 monitors=[];pids=[]
 for label in ['PRE','POST']:
  a=j(P/(label+'.ATTEMPT.json'));ck(type(a['pid_owner']) is int and a['pid_owner']>0,'positive parent owner '+label);pids.append(a['pid_owner']);eq(a,{'command':childcmd,'environment':env,'wall_seconds':180,'pid_owner':a['pid_owner'],'scientific_target_entry':False},'whole owned attempt '+label)
  m=j(P/(label+'.COMPLETION.json'));eq(m['command'],childcmd,'child exact snapshot command '+label);eq(m['environment'],env,'child complete environment '+label)
  n=98 if label=='PRE' else 50;ck(len(m['monitor_attempts'])==len(m['samples'])==n,'all raw and numeric observations '+label)
  previous=0.;maximum_residual=0.
  for i,(raw,s) in enumerate(zip(m['monitor_attempts'],m['samples'])):
   eq(sorted(raw),['elapsed_seconds','returncode','stderr','stdout'],'closed raw attempt '+label+str(i));ck(type(raw['returncode']) is int and raw['returncode']==0 and raw['stderr']=='' and raw['stdout'].strip().isdigit(),'actual ps outcome '+label+str(i));eq(sorted(s),['elapsed_seconds','gap_seconds','rss_kib'],'closed sample '+label+str(i));eq(s['elapsed_seconds'],raw['elapsed_seconds'],'sample raw timestamp '+label+str(i));eq(s['rss_kib'],int(raw['stdout'].strip()),'sample raw RSS '+label+str(i));ck(type(s['rss_kib']) is int and 0<=s['rss_kib']<=524288,'memory bound '+label+str(i));ck(s['elapsed_seconds']>=previous and 0<=s['gap_seconds']<=.1,'raw time and unchanged gap bound '+label+str(i));res=abs(s['gap_seconds']-(s['elapsed_seconds']-previous));maximum_residual=max(maximum_residual,res);ck(res<1e-9,'source arithmetic reconciliation tolerance only '+label+str(i));previous=s['elapsed_seconds']
  final=m['elapsed_seconds']-previous;eq(m['final_sample_to_reap_gap_seconds'],final,'exact reap gap '+label);ck(0<=final<=.1 and 0<=m['elapsed_seconds']<=180,'final/time bound '+label);peak=max(x['rss_kib'] for x in m['samples'])
  expected={'command':childcmd,'environment':env,'wall_seconds':180,'samples':m['samples'],'monitor_attempts':m['monitor_attempts'],'peak_sampled_rss_kib':peak,'stop_reason':None,'child_exit_code':0,'first_error':None,'tail_errors':[],'elapsed_seconds':m['elapsed_seconds'],'final_sample_to_reap_gap_seconds':final,'final_sample_gap_passed':True,'stdout':pin(P/(label+'.stdout')),'stderr':pin(P/(label+'.stderr')),'passed':True}
  eq(m,expected,'entire monitor completion '+label);ck(data(P/(label+'.stderr'))==b'','retained empty stderr '+label);ck(m['stdout']['bytes']<=67108864,'whole stream cap '+label)
  monitors.append({'label':label,'raw_attempts':n,'samples':n,'elapsed_seconds':m['elapsed_seconds'],'peak_rss_kib':peak,'maximum_gap_seconds':max(s['gap_seconds'] for s in m['samples']),'final_gap_seconds':final,'maximum_subtraction_residual_seconds':maximum_residual,'zero_RSS_samples':sum(s['rss_kib']==0 for s in m['samples']),'owned_child_timer_includes_startup_and_authentication':True})
 eq(pids[0],pids[1],'same parent PID observer; not child identity credential');summary['monitors']=monitors
 snap=j(P/'PRE.stdout');post=j(P/'POST.stdout');ck(data(P/'PRE.stdout')==data(P/'POST.stdout')==canon(snap),'whole canonical snapshots byteequal');eq(pure(data(P/'PRE.stdout')),{'bytes':7142026,'sha256':'ee672c5014d38656e19230bdd10c9831fabf71387e30248e600a8b6d2d8f378e'},'assigned actual snapshot identity')
 for name in ['historical_runtime','historical_optional_namespaces','historical_interpreter','historical_interpreter_provenance']:verify(deps[name])
 historic=j(deps['historical_runtime']['path']);eq(snap['runtime_inventory'],historic,'entire actual runtime matches exact historical object')
 iprov=j(deps['historical_interpreter_provenance']['path']);eq(iprov['schema'],'ri121-reviewed-runtime-metadata-candidate-handoff-v1','interpreter provenance schema');eq(iprov['status'],'METADATA_CANDIDATE_INDEPENDENTLY_VERIFIED_NOT_RUNTIME_ADMITTED','interpreter provenance scope');eq([r for r in iprov['files'] if r['path']==deps['historical_interpreter']['path']],[deps['historical_interpreter']],'authentic original interpreter binding pin');eq(snap['interpreter'],j(deps['historical_interpreter']['path']),'whole actual interpreter binding matches authentic provenance')
 eq(snap['optional_namespaces'],{'directories':j(deps['historical_optional_namespaces']['path'])['directories']},'complete three optional namespaces; historic administrative wrapper excluded')
 inv=snap['runtime_inventory'];files={x['path']:x for x in inv['files']};sel=snap['selection'];sm={x['path']:x for x in sel['files']};ck(len(files)==len(inv['files'])==len(sm)==len(sel['files'])==9923,'9923 distinct exact file and selection domains');eq(list(files),sorted(files),'sorted runtime domain');eq(list(sm),list(files),'whole ordered selection domain')
 eq(sel['status'],'CURRENT_OPAQUE_SELECTION_NOT_PROVEN_IMPORT_TRACE','selection scope')
 pyc=0;total=0
 for path,f in files.items():
  eq(sorted(f),['bytes','path','sha256'],'closed runtime FilePin '+path);ck(type(f['bytes']) is int and 0<=f['bytes']<=67108864 and re.fullmatch('[0-9a-f]{64}',f['sha256']) is not None,'runtime purepin syntax/cap '+path);total+=f['bytes'];s=sm[path];expected_keys=['path','device','inode','mode','bytes','mtime_ns','ctime_ns']
  if path.endswith('.pyc'):
   pyc+=1;expected_keys+=['pyc_first16_hex','pyc_payload_not_parsed_or_executed'];ck(re.fullmatch('[0-9a-f]{32}',s['pyc_first16_hex']) is not None and s['pyc_payload_not_parsed_or_executed'] is True,'opaque header shape only '+path)
  eq(sorted(s),sorted(expected_keys),'closed selection metadata '+path);eq(s['bytes'],f['bytes'],'selection/pin bytes '+path);ck(all(type(s[k]) is int for k in ['device','inode','mode','bytes','mtime_ns','ctime_ns']) and stat.S_ISREG(s['mode']),'typed regular selection '+path)
 roots=inv['roots'];eq(snap['root_counts'],[{'root':root,'regular_files':sum(p.startswith(root+'/') for p in files)} for root in roots],'all three root counts from full saved path domain');eq([r['regular_files'] for r in snap['root_counts']],[2878,5313,1719],'historical root counts');eq(sorted(set(files)-{p for p in files if any(p.startswith(root+'/') for root in roots)}),sorted(inv['extra_files']),'13 exact outside-root extras');ck(len(inv['extra_files'])==13,'13 extras count')
 eq(len(inv['symlinks']),3,'three historical tree links');eq(len(inv['absent_paths']),8,'eight historical absences');eq(len(inv['loader_bindings']),8,'eight native bindings');ck(all(p not in files for p in inv['absent_paths']),'required absent names not in saved files')
 for binding in inv['loader_bindings']+[snap['interpreter']]:
  eq(sorted(binding),['named_path','resolved_path','symlink_chain','target'],'closed component binding '+binding['named_path']);eq(binding['target'],{k:files[binding['resolved_path']][k] for k in ['bytes','sha256']},'component resolved target actual inventory '+binding['named_path'])
 hist_sel_ref=next(x for x in deps['opaque_files'] if x['path'].endswith('/FILE_SELECTION_METADATA.candidate.json'));verify(hist_sel_ref);hs=j(hist_sel_ref['path']);hsmap={r['path']:r for r in hs['files']};eq(sorted(hsmap),sorted(sm),'historical selection same domain');selection_diffs=[p for p in sm if canon(sm[p])!=canon(hsmap[p])]
 root_runtime=j(D/'RUNTIME_POST_IDENTITIES.json');ck(root_runtime['scientific_body_decode'] is False and root_runtime['subject_execution'] is False,'root independent opaque recheck scope');rm={r['path']:r for r in root_runtime['identities']};eq(sorted(rm),sorted(files),'entire root fresh9923 saved identity domain')
 for path,f in files.items():
  x=rm[path];eq({k:x[k] for k in ['path','bytes','sha256']},f,'root saved fresh opaque file '+path);eq(x['resolved_path'],path,'root literal resolved file '+path);eq(x['symlink_chain'],[],'root regular target no aliases '+path);s=sm[path];eq([s[k] for k in ['device','inode','mode','bytes','mtime_ns','ctime_ns']],[x['state'][i] for i in [0,1,2,4,5,6]],'root fresh selection stat '+path)
 routes=sorted(set(inv['absent_paths'][4:]+['/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib','/opt/homebrew/Cellar/mpdecimal/4.0.1/lib/libmpdec.3.dylib','/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/Cellar/mpdecimal/4.0.1/lib/libmpdec.3.dylib']))
 eq(snap['preobserved_dyld_routes'],{'schema':'ri133-preobserved-dyld-route-domain-v1','absent_paths':routes,'symlinks':[{'path':'/opt/homebrew/opt/mpdecimal','target':'../Cellar/mpdecimal/4.0.1'}],'scope':'All predeclared routes; actual ordered attempts must be fully parsed and be contained here. No retrospective precheck credit.'},'whole seven preobserved routes and alias')
 eq(snap['sources'],{'opaque_files':deps['opaque_files'],'packet_namespace':deps['packet_namespace'],'science_files_opened_as_opaque_hash_streams_only':True,'scientific_body_decode':False},'whole captured442source and packet52metadata');eq(tree(Path(deps['packet_root'])),deps['packet_namespace'],'actual preserved RI130 namespace52 complete')
 expected_keys=['actual_data_admission','cache_scope','host_bootstrap','interpreter','optional_namespaces','preobserved_dyld_routes','root_counts','runtime_inventory','schema','scientific_execution','selection','sources'];eq(sorted(snap),expected_keys,'complete snapshot12field schema');eq(snap['schema'],'ri133-complete-current-metadata-snapshot-v1','snapshot schema');ck(snap['scientific_execution'] is False and snap['actual_data_admission'] is False,'snapshot scope false');eq(snap['cache_scope'],'All pyc bytes pinned; first16 opaque only. Source/cache equivalence, actual execution route and trusted supplier remain separate premises.','whole cache boundary')
 hb=snap['host_bootstrap'];eq(sorted(hb),['bootstrap','scope','system_version','uname'],'whole host snapshot schema');eq({k:hb[k] for k in ['uname','system_version']},host,'actual snapshot host ties current real preflight');boot=hb['bootstrap'];vd=vendor['bootstrap_descriptor'];eq({k:v for k,v in boot.items() if k!='modules'},{'named':selected,'actual':selected,'version':vd['version'],'executable':bp,'prefix':vendor['prefix'],'base_prefix':vendor['prefix'],'path':vd['path'],'isolated':1,'dont_write_bytecode':1,'optimize':0},'complete actual bootstrap descriptors')
 framework={x['path']:x for x in vendor['framework_namespace']};ck(len(framework)==2004,'complete current vendor namespace2004');eq(sum(x['identity']['bytes'] for x in framework.values() if x['kind']=='file'),vendor['framework_file_bytes'],'whole vendor filebyte sum');eq(framework[bp]['identity'],base,'current vendor namespace executable matches declaration')
 def source_binding(p):return {'named_path':p,'resolved_path':p,'symlink_chain':[],'target':{k:pin(p)[k] for k in ['bytes','sha256']}}
 mods=boot['modules'];ck(len(mods)==len({m['name'] for m in mods})==103,'all103 child bootstrap module descriptors');filemods=0;cached=0;frozen=[]
 for m in mods:
  expkeys=['name','file','origin','cached','loader_type']+(['binding'] if m['file'] is not None else []);eq(sorted(m),sorted(expkeys),'complete module descriptor '+m['name'])
  if m['file'] is not None:
   filemods+=1;p=m['file']
   if p in framework:
    i=framework[p]['identity'];expected={'named_path':p,'resolved_path':i['resolved_path'],'symlink_chain':i['symlink_chain'],'target':{k:i[k] for k in ['bytes','sha256']}}
   else:ck(p in [str(Q/'prepare.py'),str(Q/'runtime_metadata.py')],'only accepted target/helper bootstrap file '+m['name']);expected=source_binding(p)
   eq(m['binding'],expected,'whole actual loaded module binding '+m['name'])
  else:ck(m['origin'] in [None,'built-in','frozen'] and m['cached'] is None,'nonfile builtin/frozen module '+m['name'])
  if m['origin']=='frozen':frozen.append(m['name'])
  elif m['origin'] not in [None,'built-in']:eq(m['origin'],m['file'],'origin/file descriptor '+m['name'])
  if m['cached']:
   cached+=1;p=m['cached'];ck(p not in framework,'bootstrap cached name absent from saved vendor '+m['name']);ck(p.startswith(vendor['prefix']+'/') or p==str(Q/'__pycache__/runtime_metadata.cpython-39.pyc'),'cache name declared domain '+m['name'])
 # Full vendor observation corresponds to saved current metadata only; no vendor file opens.
 for k in ['collector','metadata_helper']:verify(vendor[k])
 for stage,chunk in [('PRE','a6bbb0'),('POST','c5b761')]:
  vt=j(D/('BOOTSTRAP_'+stage+'_TOOL.json'));av=shlex.split(vt['command']);eq(av[:15],tokens[:15],'vendor '+stage+' environment/deadline primitives');eq(av[15],'$SIG{ALRM}="DEFAULT"; alarm 240; exec @ARGV; die $!;','vendor '+stage+' separate limit');eq(av[16:],[bp,'-I','-B',vendor['collector']['path'],stage],'vendor '+stage+' collector command');ck(vt['result']['exit_code']==0 and vt['result']['chunk_id']==chunk,'vendor '+stage+' genuine result');ck(pin(D/('BOOTSTRAP_'+stage+'.json'))['sha256'] in vt['result']['output'],'vendor '+stage+' exact saved digest')
 outrows=tree(P);expected_names=['ATTEMPT.json','CHECKS.json','NAMESPACE.json','COMPLETE.json']+[label+s for label in ['PRE','POST'] for s in ['.ATTEMPT.json','.COMPLETION.json','.stdout','.stderr']];eq(sorted(x['relative'] for x in outrows),sorted(expected_names),'exact12output files domain');ck(all(x['kind']=='file' for x in outrows),'output only regular files')
 eq(j(P/'NAMESPACE.json'),{'schema':'ri133-retained-namespace-v1','root':str(P),'entries':[x for x in outrows if x['relative'] not in ['NAMESPACE.json','COMPLETE.json']],'excluded_not_yet_written':['NAMESPACE.json','COMPLETE.json']},'complete10namespace plus exacttwo final exclusions')
 eq(j(P/'CHECKS.json'),{'post_metadata':'PASS','source_and_admission_postcheck':'PASS'},'whole phase checks no profile or guard credit')
 art={label:pin(P/(label+'.stdout')) for label in ['PRE','POST']};art.update({label+'_completion':pin(P/(label+'.COMPLETION.json')) for label in ['PRE','POST']});art.update({'checks':pin(P/'CHECKS.json'),'namespace':pin(P/'NAMESPACE.json')})
 exp_complete={'schema':'ri133-preparation-completion-v1','phase':'capture','status':'CAPTURED_FOR_INDEPENDENT_REVIEW','command':parentcmd,'environment':env,'admission':pin(O/'CAPTURE_ADMISSION.json'),'sources':sources,'artifacts':art,'first_error':None,'independent_tail_errors':[],'elapsed_seconds':complete['elapsed_seconds'],'scientific_targets_executed':False,'actual_data_admitted':False,'full32_qualified':False,'ret_paused':True,'runtime_acceptance_created':False,'genuine_outer_created':False};eq(complete,exp_complete,'whole18field parent completion and all6artifacts');ck(sum(m['elapsed_seconds'] for m in monitors)<=complete['elapsed_seconds']<=900,'parent internal timer covers both children within soft900')
 opfinal=j(D/'OPERATION_FINAL_IDENTITIES.json');eq(tree(O),opfinal['entries'],'whole16operation domain');eq(opfinal['root'],str(O),'root final operation owner');ck(len(opfinal['entries'])==16 and len(opfinal['identities'])==13,'16entries13files3dirs');
 for x in opfinal['identities']:eq(ident(x['path']),x,'current operation fullstate '+x['path'])
 for x in source['identities']:eq(ident(x['path']),x,'final471source fullstate '+x['path'])
 summary['runtime_metadata']={'files':9923,'bytes':total,'opaque_pyc_headers':pyc,'roots':snap['root_counts'],'extras':13,'fixed_absences':8,'tree_links':3,'loader_bindings':8,'optional_native_directories':len(snap['optional_namespaces']['directories']),'optional_members':[len(x['recursive_members_no_symlink_traversal']) for x in snap['optional_namespaces']['directories']],'preobserved_dyld_routes':7,'historical_runtime_whole_object_equal':True,'historical_selection_difference_count':len(selection_diffs),'historical_selection_difference_paths':selection_diffs,'root_current_saved_runtime_identities_matched':9923,'reviewer_current_runtime_files_opened':0}
 summary['bootstrap']={'vendor_record_bytes':len(data(D/'BOOTSTRAP_PRE.json')),'vendor_record_sha256':pin(D/'BOOTSTRAP_PRE.json')['sha256'],'vendor_whole_pre_post_equal':True,'vendor_namespace_entries':2004,'vendor_file_bytes':vendor['framework_file_bytes'],'child_descriptor_modules':103,'child_module_file_bindings':filemods,'cached_names_saved_absent':cached,'frozen_origins':frozen,'current_vendor_files_opened_by_reviewer':0}
 summary['outcome']={'snapshot_bytes':7142026,'snapshot_sha256':pin(P/'PRE.stdout')['sha256'],'whole_snapshots_equal':True,'parent_elapsed_seconds':complete['elapsed_seconds'],'owned_child_timers_include_startup_and_authentication':True,'parent_preownership_authentication_outside_internal_timer':True,'genuine_outer_960_seconds_covers_parent_startup':True,'output_entries':12,'operation_entries':16,'operation_files':13,'operation_directories':3,'output_bytes':sum(x.get('bytes',0) for x in outrows),'genuine_initial_session':81040,'genuine_terminal_exit_code':0,'candidate_interpreter_executed':False,'scientific_credit':False}
 return {'schema':'ri146-independent-saved-capture-check-v1','status':'PASS','summary':summary,'checks_passed':len(log),'checks_are_metadata_predicates_not_controls':True,'log':log,'read_inputs':list(used.values()),'reviewer_subject_helper_execution':False,'current_runtime_or_vendor_observation':False,'scientific_body_decode':False}
if __name__=='__main__':
 try:result=run()
 except BaseException as e:
  result={'status':'REVIEWER_CHECK_FAILED','error':{'type':type(e).__name__,'message':str(e)},'traceback':traceback.format_exc(),'log':log,'summary':summary,'read_inputs':list(used.values())};p=R/('FAILED_CHECK_'+str(len(list(R.glob('FAILED_CHECK_*.json')))+1).zfill(2)+'.json');p.write_bytes(canon(result));print(result['traceback']);raise SystemExit(1)
 with (R/'SAVED_CAPTURE_CHECKS.json').open('xb') as f:f.write(canon(result))
 print(json.dumps({'status':'PASS','checks':len(log),'summary':summary},indent=2))
