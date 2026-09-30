"""RI150 independent administrative SAVED-evidence review. No target imports/runtime reads."""
from pathlib import Path
import hashlib,json,os,stat,collections,re,traceback
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri150-independent-optimized-review-zlcd4ret';D=B/'ri150-root-optimized-profile-0ydjxad3'
O=B/'ri150-genuine-optimized-profile-eb4vq_ba';P=O/'output'
N=B/'ri148-genuine-normal-profile-yfilag7e/output';NR=B/'ri148-independent-normal-review-fbnud7fq'
Q=B/'ri141-white-bootstrap-source-h58ls076';S=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
PRIOR=B/'ri146-root-current-capture-9bfi4u8s'
V=str(B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env')
L='/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/lib/python3.11'
BOOT='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
checks=[];reads={};summary={};extras={}
def canon(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def ok(v,label):
 checks.append({'check':label,'passed':bool(v)})
 if not v:raise AssertionError(label)
def same(a,b,label):
 if type(a) is bytes or type(b) is bytes:ok(type(a) is bytes and type(b) is bytes and a==b,label)
 else:ok(canon(a)==canon(b),label)
def fields(x,n,label):same(sorted(x),sorted(n.split()),label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def data(p):
 p=Path(p);ok(p.is_absolute() and (p.is_relative_to(B) or p.is_relative_to(Path('/Volumes/AI_DATA/development/det_8_framework-ret'))) and '/env/' not in str(p),'review read is external saved/source evidence: '+str(p))
 s=p.lstat();ok(stat.S_ISREG(s.st_mode) and p.resolve()==p,'literal saved regular file: '+str(p))
 with p.open('rb') as f:b=f.read()
 same(state(p.lstat()),state(s),'saved read stable: '+str(p))
 reads[str(p)]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 return b
 def_unreachable=None
def ref(p):data(p);return reads[str(p)]
def pure(x):return {k:x[k] for k in ('bytes','sha256')}
def pairs(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate administrative key '+k)
  d[k]=v
 return d
def load(p,canonical=True):
 b=data(p);x=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
 if canonical:same(b.decode('ascii'),canon(x).decode('ascii'),'canonical admin JSON: '+str(p))
 return x
def pinned(row,parse=False):
 same(ref(row['path']),{k:row[k] for k in ('path','bytes','sha256')},'exact pinned bytes: '+row['path'])
 return load(row['path']) if parse else row
def identity_saved(row):
 pinned(row);p=Path(row['path']);same(str(p.resolve()),row['resolved_path'],'literal resolution: '+str(p));same(row['symlink_chain'],[],'source/evidence no link: '+str(p));same(state(p.lstat()),row['state'],'full saved identity: '+str(p))
def tree(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  st=p.lstat();n=str(p.relative_to(root))
  if stat.S_ISREG(st.st_mode):rows.append(dict(relative=n,kind='file',**pure(ref(p))))
  elif stat.S_ISDIR(st.st_mode):rows.append(dict(relative=n,kind='directory'))
  elif stat.S_ISLNK(st.st_mode):rows.append(dict(relative=n,kind='symlink',target=os.readlink(p)))
  else:raise AssertionError('special evidence member')
 return rows
try:
 # Exact original source and all preserved historical/source/baseline evidence.
 pre=load(D/'SOURCE_PRE.json');post=load(D/'SOURCE_POST.json');same(post,dict(identities=pre['identities'],unchanged=True),'whole 547 source/baseline PRE/POST')
 same(len(pre['identities']),547,'547 source/baseline files');same(len({r['path'] for r in pre['identities']}),547,'unique source domain')
 for row in pre['identities']:identity_saved(row)
 deps=load(Q/'DEPENDENCIES.source-only.json');same(len(deps['opaque_files']),442,'442 inherited dependencies')
 smap={r['path']:r for r in pre['identities']}
 for row in deps['opaque_files']:same({k:smap[row['path']][k] for k in ('path','bytes','sha256')},row,'source closure dependency '+row['path'])
 same(tree(S),deps['packet_namespace'],'entire 48-file RI130 namespace')
 # New card, prior accepted stage, exact current source and scope.
 card=load(O/'OPTIMIZED_ADMISSION.json');fields(card,'schema status phase sources source_review packet output environment_root bootstrap bootstrap_host_preflight host baseline_acceptance normal_acceptance profiles_acceptance guard_admission bounds genuine_outer_required','17-field optimized admission')
 bounds=dict(snapshot_seconds=180,profile_seconds=30,guard_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864,driver_soft_seconds=900,genuine_outer_timeout_seconds=960)
 env=dict(PATH='/usr/bin:/bin',LC_ALL='C',TZ='UTC',TMPDIR=str(B/'ri146-genuine-current-capture-heib6de2/environment/tmp'),OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
 same(card['schema'],'ri141-root-preparation-admission-v1','admission schema');same(card['status'],'AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION','admission scope');same(card['phase'],'profile_optimized','optimized phase only');same(card['bounds'],bounds,'unchanged limits');same(card['packet'],str(S),'original subject namespace');same(card['output'],str(P),'exclusive output root');same(card['genuine_outer_required'],True,'genuine outer required')
 same([card[k] for k in ['profiles_acceptance','guard_admission']],[None]*2,'no premature later phase admissions')
 same(card['sources'],{n:pure(ref(Q/n)) for n in ('prepare.py','runtime_metadata.py','DEPENDENCIES.source-only.json')},'whole current three-source map')
 source_review=pinned(card['source_review'],True);same(source_review['status'],'ACCEPT_UNCHANGED_SOURCE_FOR_ONE_OPTIMIZED_PROFILE','actual source-only adjudication')
 for k in ['normal_acceptance','normal_root_adjudication','baseline_acceptance','fresh_source_check','fresh_vendor_pre','genuine_vendor_pre','independent_source_review','prior_root_source_decision','source_handoff']:pinned(source_review[k])
 baseline=pinned(card['baseline_acceptance'],True);fields(baseline,'schema status stage sources packet environment_root completions genuine_outer independent_review scientific_execution','closed baseline acceptance')
 same(baseline['schema'],'ri133-root-preparation-stage-review-v1','baseline schema');same(baseline['status'],'ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE','baseline accepted');same(baseline['stage'],'baseline','baseline stage');same(baseline['scientific_execution'],False,'baseline non-scientific')
 for k in ('sources','packet','environment_root'):same(baseline[k],card[k],'baseline same '+k)
 same(list(baseline['completions']),['capture'],'exact capture predecessor');same(list(baseline['genuine_outer']),['capture'],'exact capture outer predecessor')
 old=pinned(baseline['completions']['capture'],True);old_outer=pinned(baseline['genuine_outer']['capture'],True);pinned(old_outer['raw_tool_receipt']);pinned(baseline['independent_review'])
 same(old_outer['completion'],baseline['completions']['capture'],'capture actual completion binding');same(old['first_error'],None,'capture no first error');same(old['independent_tail_errors'],[],'capture no tails');same(old['status'],'CAPTURED_FOR_INDEPENDENT_REVIEW','capture outcome');same(old_outer['exit_code'],0,'capture outer exit0')
 for row in old['artifacts'].values():pinned(row)
 old_namespace=pinned(old['artifacts']['namespace'],True);oldroot=Path(baseline['completions']['capture']['path']).parent
 oldrows=old_namespace['entries']+[dict(relative=n,kind='file',**pure(ref(oldroot/n))) for n in ('NAMESPACE.json','COMPLETE.json')]
 same(tree(oldroot),sorted(oldrows,key=lambda x:x['relative']),'whole previous accepted capture namespace retained')
 # Independently retained genuine normal predecessor and review before optimized.
 normal_accept=pinned(card['normal_acceptance'],True)
 fields(normal_accept,'schema status stage sources packet environment_root completions genuine_outer independent_review scientific_execution','closed accepted normal predecessor')
 same(normal_accept['schema'],'ri133-root-preparation-stage-review-v1','normal acceptance schema');same(normal_accept['status'],'ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE','normal accepted status');same(normal_accept['stage'],'normal','normal accepted stage');same(normal_accept['scientific_execution'],False,'normal scope')
 for key in ('sources','packet','environment_root'):same(normal_accept[key],card[key],'normal predecessor same '+key)
 same(list(normal_accept['completions']),['profile_normal'],'normal predecessor exact phase');same(list(normal_accept['genuine_outer']),['profile_normal'],'normal predecessor exact genuine phase')
 normal_complete=pinned(normal_accept['completions']['profile_normal'],True);normal_outer=pinned(normal_accept['genuine_outer']['profile_normal'],True)
 same(normal_outer['completion'],normal_accept['completions']['profile_normal'],'normal outer exact completion');same(normal_outer['command'],normal_complete['command'],'normal genuine command');same(normal_outer['environment'],normal_complete['environment'],'normal genuine environment');same(normal_outer['exit_code'],0,'normal genuine exit0');same(normal_outer['external_timeout_seconds'],960,'normal genuine outer bound');pinned(normal_outer['raw_tool_receipt'])
 same(normal_complete['sources'],card['sources'],'normal complete source map');same(normal_complete['phase'],'profile_normal','actual normal phase');same(normal_complete['first_error'],None,'normal no first error');same(normal_complete['independent_tail_errors'],[],'normal no tails');same(normal_complete['status'],'CAPTURED_FOR_INDEPENDENT_REVIEW','normal actual status')
 normal_review=pinned(normal_accept['independent_review'],True);same(normal_review['status'],'ACCEPT_BOUNDED_NORMAL_PROFILE_EVIDENCE','independent normal verdict')
 same(sorted(p.name for p in NR.iterdir()),normal_review['exact_namespace'],'preserved exact17 normal review namespace')
 for row in normal_review['files']:pinned(row)
 for row in normal_complete['artifacts'].values():pinned(row)
 ns=pinned(normal_complete['artifacts']['namespace'],True)
 same(ns['excluded_not_yet_written'],['NAMESPACE.json','COMPLETE.json'],'normal final exclusions preserved')
 saved_normal_rows=ns['entries']+[dict(relative=n,kind='file',**pure(ref(N/n))) for n in ['NAMESPACE.json','COMPLETE.json']]
 same(tree(N),sorted(saved_normal_rows,key=lambda x:x['relative']),'whole accepted normal operation namespace retained')
 normal_report=load(N/'PROFILE.stdout');normal_check=load(N/'CHECKS.json')['profile']
 normal_adjud=pinned(source_review['normal_root_adjudication'],True);same(normal_adjud['status'],'ACCEPT_GENUINE_NORMAL_RUNTIME_PROFILE','genuine normal root decision')
 same(normal_adjud['independent_review'],normal_accept['independent_review'],'normal review root selection');same(normal_adjud['genuine_outer'],normal_accept['genuine_outer']['profile_normal'],'normal root genuine identity')
 normal_card=pinned(normal_complete['admission'],True)
 ok(Path(card['normal_acceptance']['path']).stat().st_mtime_ns < (O/'OPTIMIZED_ADMISSION.json').stat().st_mtime_ns,'normal acceptance exists before separate optimized card')
 # Full snapshot identity bridge (administrative decode only).
 a=load(P/'PRE.stdout');z=load(P/'POST.stdout');same(data(P/'PRE.stdout'),data(P/'POST.stdout'),'complete snapshot byte equality')
 same(data(P/'PRE.stdout'),data(old['artifacts']['POST']['path']),'exact accepted baseline snapshot bytes')
 same(pure(ref(P/'PRE.stdout')),dict(bytes=7142026,sha256='ee672c5014d38656e19230bdd10c9831fabf71387e30248e600a8b6d2d8f378e'),'accepted whole snapshot pin')
 same(a['sources']['opaque_files'],deps['opaque_files'],'all442 captured source observations');same(a['sources']['packet_namespace'],deps['packet_namespace'],'captured source namespace')
 same(a['runtime_inventory'],pinned(deps['historical_runtime'],True),'whole historical runtime identity bridge')
 same(a['interpreter'],pinned(deps['historical_interpreter'],True),'authentic historical candidate binding')
 provenance=pinned(deps['historical_interpreter_provenance'],True);same([x for x in provenance['files'] if x['path']==deps['historical_interpreter']['path']],[deps['historical_interpreter']],'historical interpreter handoff identity')
 same(a['optional_namespaces'],dict(directories=pinned(deps['historical_optional_namespaces'],True)['directories']),'whole optional namespace actual contract')
 runtime={r['path']:r for r in a['runtime_inventory']['files']};selection={r['path']:r for r in a['selection']['files']}
 same(len(runtime),9923,'9923 saved runtime identities');same(sum(r['bytes'] for r in runtime.values()),258862951,'full saved runtime byte total');same(sorted(runtime),sorted(selection),'selection complete domain')
 runtime_post=load(D/'RUNTIME_POST_IDENTITIES.json');same(runtime_post['subject_execution'],False,'root runtime observation nonexecution');same(runtime_post['scientific_body_decode'],False,'root runtime opaque')
 same([x['path'] for x in runtime_post['identities']],sorted(runtime),'root post identity complete domain')
 for row in runtime_post['identities']:
  path=row['path'];same({k:row[k] for k in ('path','bytes','sha256')},runtime[path],'saved fresh root runtime hash '+path)
  same(row['resolved_path'],path,'saved runtime literal '+path);same(row['symlink_chain'],[],'saved runtime no alias '+path)
  same([row['state'][i] for i in (0,1,2,4,5,6)],[selection[path][k] for k in ('device','inode','mode','bytes','mtime_ns','ctime_ns')],'saved full current selection '+path)
 # Independently reconstruct every field of the profile's semantic result.
 report=load(P/'PROFILE.stdout');fields(report,'schema profile_before profile_after uname startup decimal hashlib modules scientific_targets_imported_or_executed boundary','closed ten-field profile')
 expected=dict(version='3.11.6 (main, Nov  2 2023, 04:39:43) [Clang 14.0.3 (clang-1403.0.22.14.1)]',implementation='cpython',version_info=[3,11,6,'final',0],executable=V+'/bin/python',prefix=V,exec_prefix=V,base_prefix='/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11',base_exec_prefix='/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11',path=[L.rsplit('/',1)[0]+'/python311.zip',L,L+'/lib-dynload',V+'/lib/python3.11/site-packages'],byteorder='little',isolated=1,dont_write_bytecode=1,optimize=1)
 same(report['schema'],'ri121-installed-runtime-profile-observation-v1','profile schema');same(report['profile_before'],expected,'full before optimized profile');same(report['profile_after'],expected,'full after optimized profile');same(report['uname'],card['host']['uname'],'profile same host')
 same(report['scientific_targets_imported_or_executed'],False,'no scientific entry');same(report['boundary'],'Installed-runtime observation under pinned supplier, cache-selection and host premises; no scientific qualification.','literal bounded claim')
 same(report['startup'],dict(enable_user_site=False,site_prefixes=[V],distutils_hook_loaded=True,sitecustomize_loaded=True,usercustomize_loaded=False),'all startup fields')
 dec=report['decimal'];fields(dec,'extension_loaded fallback_loaded decimal_class_is_fallback extension_import_error fraction_class_module','closed decimal fields')
 same({k:v for k,v in dec.items() if k!='extension_import_error'},dict(extension_loaded=False,fallback_loaded=True,decimal_class_is_fallback=True,fraction_class_module='fractions'),'all three decimal fallback premises and Fraction supplier')
 fields(dec['extension_import_error'],'type message','complete decimal exception');same(dec['extension_import_error']['type'],'ImportError','decimal error type')
 # Rebuild entire literal error rather than accept substring extraction.
 opts='/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib';actual='/opt/homebrew/Cellar/mpdecimal/4.0.1/lib/libmpdec.3.dylib';cryp='/System/Volumes/Preboot/Cryptexes/OS'
 ordered=[opts,cryp+opts,opts,'/usr/local/lib/libmpdec.3.dylib','/usr/lib/libmpdec.3.dylib',actual,cryp+actual,actual,'/usr/local/lib/libmpdec.3.dylib','/usr/lib/libmpdec.3.dylib']
 attempts=[dict(path=x,reason='no such file, not in dyld cache' if x=='/usr/lib/libmpdec.3.dylib' else 'no such file') for x in ordered]
 extension=L+'/lib-dynload/_decimal.cpython-311-darwin.so'
 literal='dlopen('+extension+', 0x0002): Library not loaded: '+opts+'\n  Referenced from: <0D7ED905-BC7D-37C9-9ECD-CAF5F3BE837D> '+extension+'\n  Reason: tried: '+', '.join("'"+x['path']+"' ("+x['reason']+")" for x in attempts)
 same(dec['extension_import_error']['message'],literal,'entire ordered ten-attempt error including all framing/repeats/reasons')
 domain=a['preobserved_dyld_routes'];same(domain['absent_paths'],sorted(set(ordered+['/opt/homebrew/lib/libmpdec.3.dylib'])),'all seven prospectively declared missing routes')
 same(domain['symlinks'],[dict(path='/opt/homebrew/opt/mpdecimal',target='../Cellar/mpdecimal/4.0.1')],'declared mpdecimal alias')
 for x in attempts:ok(x['path'] in domain['absent_paths'],'actual route preobserved '+x['path'])
 names=['blake2b','blake2s','md5','md5-sha1','ripemd160','sha1','sha224','sha256','sha384','sha3_224','sha3_256','sha3_384','sha3_512','sha512','sha512_224','sha512_256','shake_128','shake_256','sm3']
 empty='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
 same(report['hashlib'],dict(sha256_empty=empty,openssl_sha256_empty=empty,available_openssl_names=names),'complete observed hash usability and19 names')
 modules=report['modules'];ok(bool(modules),'nonempty module observation');ok(not {'white_kernel','white_path','white_controls','white_fixtures','kernel_controls','white_validator','validator_controls','qualify_white_only','_decimal','usercustomize'}.intersection(modules),'expected absent scientific/extension/user modules')
 ok({'__main__','_distutils_hack','sitecustomize','_pydecimal','decimal','fractions','hashlib','_hashlib'}.issubset(modules),'required loaded suppliers')
 descriptors=[];counts=collections.Counter();cache_absences=[];frozen=[];loaders=collections.Counter()
 for name,row in sorted(modules.items()):
  fields(row,'file cached origin loader_type','complete descriptor '+name);ok(type(row['loader_type']) is str,'loader type text '+name);loaders[row['loader_type']]+=1
  if row['origin']=='frozen':frozen.append(name)
  for field in ('file','cached','origin'):
   value=row[field];item=dict(module=name,field=field)
   if value is None or value in ('built-in','frozen'):item['value']=value;counts['sentinel']+=1
   elif name=='__main__':same([field,value],['file',str(S/'profile_observe.source-only.py')],'reviewed sole main descriptor');item['identity']=ref(value);counts['main']+=1
   elif value in runtime:
    ok(Path(value).is_absolute(),'absolute loaded descriptor '+value)
    item['binding']=dict(named_path=value,resolved_path=value,symlink_chain=[],target=pure(runtime[value]));counts['binding']+=1
   else:
    ok(field=='cached' and Path(value).is_absolute() and any(value.startswith(root+'/') for root in a['runtime_inventory']['roots']),'only missing in-domain cache alternative '+value)
    ok(value not in selection and not any(x['path']==value for x in a['runtime_inventory']['symlinks']),'cache absent complete roots '+value)
    item.update(path=value,absent_from_complete_inventory=True);counts['absent_cache']+=1;cache_absences.append(dict(module=name,path=value))
   descriptors.append(item)
  if row['loader_type']=='SourceFileLoader':same(row['file'],row['origin'],'SourceFileLoader file-origin '+name);ok(row['cached'].endswith('.cpython-311.opt-1.pyc'),'optimized cache suffix '+name)
  elif row['loader_type']=='ExtensionFileLoader':same(row['file'],row['origin'],'extension file-origin '+name);same(row['cached'],None,'extension no cached '+name)
  elif row['loader_type']=='type':ok(row['origin'] in ('frozen','built-in'),'built-in/frozen loader descriptor '+name);same(row['cached'],None,'builtin/frozen no cached '+name)
  else:same(name,'__main__','only NoneType main loader')
 reconstructed=dict(status='SAVED_PROFILE_FIELDS_RECONCILED_NOT_RUNTIME_ACCEPTANCE',expected_runtime=expected,all_descriptors=descriptors,ordered_actual_dyld_attempts=attempts,full_dyld_error=dec['extension_import_error'],preobserved_domain=domain,hash_algorithm_names=names,supplier_cache_and_stable_host_premises_retained=True,full_import_trace_claim=False,scientific_qualification=False)
 savedchecks=load(P/'CHECKS.json');same(savedchecks,dict(profile=reconstructed,post_metadata='PASS',source_and_admission_postcheck='PASS'),'whole independently rebuilt saved CHECKS object')
 # Exact both-mode relation plus independent normal whole descriptor reconstruction.
 adjusted=dict(expected);adjusted['optimize']=0
 same(normal_report['profile_before'],adjusted,'normal before exact adjusted runtime');same(normal_report['profile_after'],adjusted,'normal after exact adjusted runtime')
 for k in ('schema','uname','startup','decimal','hashlib','scientific_targets_imported_or_executed','boundary'):same(normal_report[k],report[k],'both observed nonmodule field '+k)
 same(normal_check['ordered_actual_dyld_attempts'],attempts,'both complete ordered dyld lists');same(normal_check['hash_algorithm_names'],names,'both algorithm-name lists')
 ndesc=[]
 for name,row in sorted(normal_report['modules'].items()):
  fields(row,'file cached origin loader_type','normal complete descriptor '+name)
  for field in ('file','cached','origin'):
   value=row[field];item=dict(module=name,field=field)
   if value is None or value in ('built-in','frozen'):item['value']=value
   elif name=='__main__':same([field,value],['file',str(S/'profile_observe.source-only.py')],'normal sole main');item['identity']=ref(value)
   elif value in runtime:item['binding']=dict(named_path=value,resolved_path=value,symlink_chain=[],target=pure(runtime[value]))
   else:
    ok(field=='cached' and any(value.startswith(root+'/') for root in a['runtime_inventory']['roots']) and value not in selection,'normal cache absence domain');item.update(path=value,absent_from_complete_inventory=True)
   ndesc.append(item)
 rebuilt_normal=dict(reconstructed);rebuilt_normal.update(expected_runtime=adjusted,all_descriptors=ndesc)
 same(normal_check,rebuilt_normal,'independent complete retained normal check reconstruction')
 same(rebuilt_normal,load(NR/'RECONSTRUCTED_PROFILE_CHECK.json'),'unchanged full accepted independent normal reconstruction')
 same(data(N/'PRE.stdout'),data(P/'PRE.stdout'),'normal to optimized complete baseline bytes');same(data(N/'POST.stdout'),data(P/'POST.stdout'),'normal to optimized post baseline bytes')
 diffs=[]
 def differences(left,right,path=''):
  if type(left) is dict and type(right) is dict:
   for k in sorted(set(left)|set(right)):
    if k not in left or k not in right:diffs.append(dict(field=path+'/'+k,normal=left.get(k),optimized=right.get(k)))
    else:differences(left[k],right[k],path+'/'+k)
  elif canon(left)!=canon(right):diffs.append(dict(field=path,normal=left,optimized=right))
 differences(normal_report,report)
 extras['mode_relation']=dict(schema='ri150-independent-saved-both-mode-relation-v1',status='PRESCRIBED_RELATION_PASSED',normal_report=ref(N/'PROFILE.stdout'),optimized_report=ref(P/'PROFILE.stdout'),normal_acceptance=card['normal_acceptance'],normal_root_adjudication=source_review['normal_root_adjudication'],adjusted_expected_runtime_equal=True,complete_ordered_dyld_attempts_equal=True,hash_algorithm_names_equal=True,whole_report_byte_equality_required=False,actual_complete_report_differences=diffs,normal_descriptors=ndesc,scientific_or_guard_credit=False)
 summary['mode_relation']=dict(report_difference_count=len(diffs),cache_descriptor_changes=sum(x['field'].endswith('/cached') for x in diffs),normal_report=ref(N/'PROFILE.stdout'),normal_acceptance=card['normal_acceptance'])
 extras['profile_reconstruction']=reconstructed
 summary['profile']=dict(modules=len(modules),descriptor_fields=len(descriptors),descriptor_counts=dict(counts),loader_counts=dict(loaders),absent_cache_records=cache_absences,frozen_names=frozen,ordered_dyld_attempts=len(attempts),unique_attempted_paths=len(set(ordered)),predeclared_absences=len(domain['absent_paths']),hash_algorithm_names=len(names),observer_pin=ref(S/'profile_observe.source-only.py'))
 # Every complete monitor attempt, sample, stream, command, ownership and final reap.
 complete=load(P/'COMPLETE.json');fields(complete,'schema phase status command environment admission sources artifacts first_error independent_tail_errors elapsed_seconds scientific_targets_executed actual_data_admitted full32_qualified ret_paused runtime_acceptance_created genuine_outer_created','17-field parent completion')
 same(complete['schema'],'ri133-preparation-completion-v1','parent schema');same(complete['phase'],'profile_optimized','parent phase');same(complete['status'],'CAPTURED_FOR_INDEPENDENT_REVIEW','parent saved status');same(complete['sources'],card['sources'],'parent source binding');same(complete['admission'],ref(O/'OPTIMIZED_ADMISSION.json'),'parent actual card');same(complete['environment'],env,'parent exact environment')
 command=[BOOT,'-I','-B',str(Q/'prepare.py'),'--admission',str(O/'OPTIMIZED_ADMISSION.json')];same(complete['command'],command,'parent exact direct command')
 same(complete['first_error'],None,'no parent first error');same(complete['independent_tail_errors'],[],'no independent tail error')
 for k in ['scientific_targets_executed','actual_data_admitted','full32_qualified','runtime_acceptance_created','genuine_outer_created']:same(complete[k],False,'no scope inflation '+k)
 same(complete['ret_paused'],True,'RET pause');ok(type(complete['elapsed_seconds']) in (int,float) and 0<complete['elapsed_seconds']<900,'parent saved soft interval')
 artifact_names={'PRE':'PRE.stdout','PRE_completion':'PRE.COMPLETION.json','PROFILE':'PROFILE.stdout','PROFILE_completion':'PROFILE.COMPLETION.json','POST':'POST.stdout','POST_completion':'POST.COMPLETION.json','checks':'CHECKS.json','namespace':'NAMESPACE.json'}
 same(sorted(complete['artifacts']),sorted(artifact_names),'exact eight artifact roles')
 for role,filename in artifact_names.items():same(complete['artifacts'][role],ref(P/filename),'artifact role binding '+role)
 same(load(P/'ATTEMPT.json'),dict(schema='ri133-preparation-attempt-v1',admission=ref(O/'OPTIMIZED_ADMISSION.json'),sources=card['sources'],phase='profile_optimized',environment=env,scientific_execution=False),'entire actual owned parent attempt')
 monitor=[];owners=[]
 for label,seconds in [('PRE',180),('PROFILE',30),('POST',180)]:
  child=load(P/(label+'.COMPLETION.json'));attempt=load(P/(label+'.ATTEMPT.json'))
  cmd=([V+'/bin/python','-I','-B','-O',str(S/'profile_observe.source-only.py')] if label=='PROFILE' else [BOOT,'-I','-B',str(Q/'prepare.py'),'--snapshot',str(O/'OPTIMIZED_ADMISSION.json')])
  fields(child,'command environment wall_seconds samples monitor_attempts peak_sampled_rss_kib stop_reason child_exit_code first_error tail_errors elapsed_seconds final_sample_to_reap_gap_seconds final_sample_gap_passed stdout stderr passed','complete child fields '+label)
  same(child['command'],cmd,'real child command '+label);same(child['environment'],env,'child exact env '+label);same(child['wall_seconds'],seconds,'child unchanged bound '+label)
  same([child[k] for k in ['first_error','stop_reason','child_exit_code','tail_errors','passed','final_sample_gap_passed']],[None,None,0,[],True,True],'child outcome fields '+label)
  fields(attempt,'command environment wall_seconds pid_owner scientific_target_entry','owned attempt fields '+label)
  same({k:v for k,v in attempt.items() if k!='pid_owner'},dict(command=cmd,environment=env,wall_seconds=seconds,scientific_target_entry=False),'whole nonscientific attempt '+label);ok(type(attempt['pid_owner']) is int and attempt['pid_owner']>0,'parent pid owner positive '+label);owners.append(attempt['pid_owner'])
  samples=child['samples'];raw=child['monitor_attempts'];ok(len(samples)>0 and len(raw)==len(samples),'all numeric actual ps attempts have samples '+label)
  prev=0.;residuals=[]
  for i,(s,t) in enumerate(zip(samples,raw)):
   fields(s,'elapsed_seconds rss_kib gap_seconds','sample fields '+label+str(i));fields(t,'elapsed_seconds returncode stdout stderr','raw attempt fields '+label+str(i))
   same(t['returncode'],0,'raw monitor rc '+label+str(i));same(t['stderr'],'','raw monitor stderr '+label+str(i));ok(type(t['stdout']) is str and t['stdout'].strip().isdigit(),'raw numeric stdout '+label+str(i))
   same([s['elapsed_seconds'],s['rss_kib']],[t['elapsed_seconds'],int(t['stdout'].strip())],'sample exact raw pair '+label+str(i))
   ok(type(s['rss_kib']) is int and 0<=s['rss_kib']<=524288,'raw RSS bound '+label+str(i));ok(type(s['elapsed_seconds']) in (float,int) and type(s['gap_seconds']) in (float,int) and prev<=s['elapsed_seconds']<=seconds and 0<=s['gap_seconds']<=.1,'actual exact time/gap bounds '+label+str(i))
   res=abs(s['elapsed_seconds']-prev-s['gap_seconds']);ok(res<1e-9,'source-specified arithmetic consistency '+label+str(i));residuals.append(res);prev=s['elapsed_seconds']
  same(child['peak_sampled_rss_kib'],max(s['rss_kib'] for s in samples),'peak recomputation '+label)
  same(child['final_sample_to_reap_gap_seconds'],child['elapsed_seconds']-prev,'complete final reap recomputation '+label)
  ok(prev<=child['elapsed_seconds']<=seconds and 0<=child['final_sample_to_reap_gap_seconds']<=.1,'final and wall bounds '+label)
  for stream in ['stdout','stderr']:same(child[stream],ref(P/(label+'.'+stream)),'full stream bytes '+label+stream);ok(child[stream]['bytes']<=67108864,'stream cap '+label+stream)
  same(child['stderr']['bytes'],0,'empty stderr '+label)
  monitor.append(dict(label=label,wall_seconds=seconds,elapsed_seconds=child['elapsed_seconds'],sample_count=len(samples),raw_attempt_count=len(raw),peak_sampled_rss_kib=child['peak_sampled_rss_kib'],maximum_sample_gap_seconds=max(s['gap_seconds'] for s in samples),final_sample_to_reap_gap_seconds=child['final_sample_to_reap_gap_seconds'],arithmetic_max_residual=max(residuals)))
 same(len(set(owners)),1,'same saved parent owner across three children')
 ok(sum(x['elapsed_seconds'] for x in monitor)<complete['elapsed_seconds'],'sequential child durations inside parent saved interval')
 summary['monitors']=monitor;summary['parent_elapsed_seconds']=complete['elapsed_seconds'];summary['saved_parent_pid']=owners[0]
 # Reconstruct every retained normal raw attempt/sample and final reap without replay.
 normal_monitor=[]
 for label in ('PRE','PROFILE','POST'):
  record=load(N/(label+'.COMPLETION.json'));record_attempt=load(N/(label+'.ATTEMPT.json'))
  same(record['environment'],env,'normal monitor unchanged environment '+label)
  same([record[k] for k in ('child_exit_code','first_error','stop_reason','tail_errors','passed')],[0,None,None,[],True],'normal entire monitor outcome '+label)
  cmd=[V+'/bin/python','-I','-B',str(S/'profile_observe.source-only.py')] if label=='PROFILE' else [BOOT,'-I','-B',str(Q/'prepare.py'),'--snapshot',normal_complete['admission']['path']]
  same(record['command'],cmd,'normal monitor exact command '+label);same(record_attempt['command'],cmd,'normal owned attempt exact command '+label);same(record_attempt['environment'],env,'normal owned environment '+label)
  limit=30 if label=='PROFILE' else 180;same(record['wall_seconds'],limit,'normal wall bound '+label);same(record_attempt['wall_seconds'],limit,'normal attempt bound '+label)
  ok(record_attempt['scientific_target_entry'] is False and type(record_attempt['pid_owner']) is int and record_attempt['pid_owner']>0,'normal nonscience owner '+label)
  same(len(record['samples']),len(record['monitor_attempts']),'normal full raw sample correspondence '+label);ok(bool(record['samples']),'normal samples nonempty '+label)
  previous=0
  for i,(sample,raw_sample) in enumerate(zip(record['samples'],record['monitor_attempts'])):
   fields(sample,'elapsed_seconds rss_kib gap_seconds','normal sample closed '+label+str(i));fields(raw_sample,'elapsed_seconds returncode stdout stderr','normal raw closed '+label+str(i))
   same(raw_sample['returncode'],0,'normal raw ps exit '+label+str(i));same(raw_sample['stderr'],'','normal raw stderr '+label+str(i));ok(raw_sample['stdout'].strip().isdigit(),'normal raw numeric '+label+str(i))
   same([sample['elapsed_seconds'],sample['rss_kib']],[raw_sample['elapsed_seconds'],int(raw_sample['stdout'].strip())],'normal raw exact data '+label+str(i))
   ok(type(sample['rss_kib']) is int and 0<=sample['rss_kib']<=524288 and previous<=sample['elapsed_seconds']<=limit and 0<=sample['gap_seconds']<=.1,'normal unchanged per-sample bounds '+label+str(i))
   ok(abs(sample['elapsed_seconds']-previous-sample['gap_seconds'])<1e-9,'normal saved gap arithmetic '+label+str(i));previous=sample['elapsed_seconds']
  same(record['peak_sampled_rss_kib'],max(x['rss_kib'] for x in record['samples']),'normal peak reconstruction '+label)
  same(record['final_sample_to_reap_gap_seconds'],record['elapsed_seconds']-previous,'normal final reap arithmetic '+label)
  ok(0<=record['elapsed_seconds']<=limit and 0<=record['final_sample_to_reap_gap_seconds']<=.1 and record['final_sample_gap_passed'] is True,'normal wall final constraints '+label)
  for stream in ('stdout','stderr'):same(record[stream],ref(N/(label+'.'+stream)),'normal full stream pin '+label+stream)
  same(record['stderr']['bytes'],0,'normal empty stderr '+label)
  normal_monitor.append(dict(label=label,sample_count=len(record['samples']),elapsed_seconds=record['elapsed_seconds'],peak_sampled_rss_kib=record['peak_sampled_rss_kib'],final_sample_to_reap_gap_seconds=record['final_sample_to_reap_gap_seconds']))
 summary['retained_normal_monitors']=normal_monitor
 # Exact namespace including two final self-exclusions.
 namespace=load(P/'NAMESPACE.json');fields(namespace,'schema root entries excluded_not_yet_written','namespace closed');same(namespace['root'],str(P),'namespace ownership');same(namespace['schema'],'ri133-retained-namespace-v1','namespace schema');same(namespace['excluded_not_yet_written'],['NAMESPACE.json','COMPLETE.json'],'two exact final exclusions')
 allrows=namespace['entries']+[dict(relative=n,kind='file',**pure(ref(P/n))) for n in ['NAMESPACE.json','COMPLETE.json']]
 same(tree(P),sorted(allrows,key=lambda x:x['relative']),'all16 output files and final exclusions');same(len(allrows),16,'16 exact output entries');ok(all(x['kind']=='file' for x in allrows),'all output regular files');ok(sum(x['bytes'] for x in allrows)<=536870912,'namespace aggregate cap')
 operation=load(D/'OPERATION_FINAL_IDENTITIES.json');same(tree(O),operation['entries'],'whole18 operation namespace');same(len(operation['entries']),18,'18 operation entries');same(operation['root'],str(O),'operation root')
 for row in operation['identities']:identity_saved(row)
 custody=load(D/'ADMISSION_CUSTODY.json');same(custody['genuine_operation_count'],1,'one operation declaration');identity_saved(custody['card']);identity_saved(custody['source_review']);same(custody['source_pre'],ref(D/'SOURCE_PRE.json'),'source before admission pin')
 # Genuine outer, session and literal tools are externally supplied origin evidence.
 outer=load(D/'GENUINE_OUTER.json');fields(outer,'schema status command environment exit_code completion raw_tool_receipt external_timeout_seconds','eight-field genuine outer')
 pinned(outer['raw_tool_receipt']);raw=load(outer['raw_tool_receipt']['path'],False);same(outer,dict(schema='ri133-root-genuine-outer-v1',status='ACTUAL_TOOL_COMPLETION',command=command,environment=env,exit_code=0,completion=ref(P/'COMPLETE.json'),raw_tool_receipt=ref(D/'GENUINE_TOOL_COMPLETE.json'),external_timeout_seconds=960),'entire genuine outer wrapper')
 same(raw['initial'],dict(chunk_id='ed392e',wall_time_seconds=1.003303958,session_id=91856,original_token_count=0,output=''),'actual initial tool result');same(raw['terminal'],dict(chunk_id='8b8828',wall_time_seconds=.000013708,exit_code=0,original_token_count=0,output=''),'actual terminal tool result')
 shell_prefix='exec /usr/bin/env -i '+' '.join(k+'='+v for k,v in env.items())+" /usr/bin/perl -e '$SIG{ALRM}=\"DEFAULT\"; alarm 960; exec @ARGV; die $!;' "
 same(raw['arguments'],dict(cmd=shell_prefix+' '.join(command),login=False,yield_time_ms=1000,max_output_tokens=1200),'full literal actual outer invocation');extras['genuine_initial_arguments']=raw['arguments']
 details=load(D/'GENUINE_TOOL_CALL_DETAILS.json',False)
 same(details,dict(schema='ri150-genuine-tool-call-details-v1',initial_workdir_parameter='omitted',actual_default_workdir='/Volumes/AI_DATA/development/det_8_framework-ret',initial=dict(chunk_id='ed392e',session_id=91856),terminal_arguments=dict(session_id=91856,chars='',max_output_tokens=1200,yield_time_ms=1000),terminal_chunk_id='8b8828',terminal_exit_code=0,existing_receipt_unchanged=True,rerun=False),'complete additive real call details and session correspondence')
 # Complete vendor PRE/POST and all saved module origins against full vendor namespace.
 vendor=load(D/'BOOTSTRAP_PRE.json');same(data(D/'BOOTSTRAP_PRE.json'),data(D/'BOOTSTRAP_POST.json'),'whole1690939 vendor PRE/POST byte equality');same(vendor['actual_environment'],env,'complete actual vendor environment');same(vendor['selected_interpreter_binding'],deps['selected_bootstrap_binding'],'full direct vendor authentic provenance');same(vendor['host'],card['host']['uname'],'vendor host unchanged');same(pinned(card['bootstrap_host_preflight'],True),vendor,'actual preflight card binding')
 selected=vendor['selected_interpreter_binding'];same(card['bootstrap'],dict(named_path=BOOT,resolved_path=BOOT,symlink_chain=[],target=pure(selected)),'card full direct bootstrap')
 pinned(vendor['collector']);pinned(vendor['metadata_helper']);same(pure(vendor['metadata_helper']),dict(bytes=3144,sha256='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'),'trusted metadata helper pin')
 fw=vendor['framework_namespace'];same(len(fw),2004,'entire saved vendor namespace');same(len({x['path'] for x in fw}),2004,'unique vendor names');vfiles={x['path']:x['identity'] for x in fw if x['kind']=='file'}
 same(sum(x['bytes'] for x in vfiles.values()),vendor['framework_file_bytes'],'saved vendor byte total');same(vendor['framework_file_bytes'],48024515,'retained vendor bytes')
 for name,bind in [(x['path'],x) for x in vendor['bindings']]:
  if bind['resolved_path'] in vfiles:same(pure(bind),pure(vfiles[bind['resolved_path']]),'vendor tool binding full namespace '+name)
 for mod in vendor['bootstrap_descriptor']['modules']:
  if 'identity' in mod:
   ident=mod['identity'];ok(ident['resolved_path'] in vfiles or ident['path'] in (str(D/'observe_bootstrap.py'),vendor['metadata_helper']['path']),'vendor module within supplier/reviewed collectors '+mod['name'])
   if ident['resolved_path'] in vfiles:same(pure(ident),pure(vfiles[ident['resolved_path']]),'complete saved vendor module pin '+mod['name'])
   else:identity_saved(ident)
 same(vendor['bootstrap_descriptor']['executable'],BOOT,'actual direct bootstrap executable');same([vendor['bootstrap_descriptor'][k] for k in ['isolated','dont_write_bytecode','optimize']],[1,1,0],'vendor actual flags')
 for phase,chunk in [('PRE','48324d'),('POST','a1d315')]:
  tool=load(D/('BOOTSTRAP_'+phase+'_TOOL.json'),False);same(tool['result']['chunk_id'],chunk,'actual supplier tool '+phase);same(tool['result']['exit_code'],0,'actual supplier tool success '+phase)
  wanted=shell_prefix.replace('alarm 960','alarm 240')+' '.join([BOOT,'-I','-B',str(D/'observe_bootstrap.py'),phase]);same(tool['command'],wanted,'literal supplier invocation '+phase);same(tool['arguments']['cmd'],wanted,'supplier argument command '+phase);same(tool['arguments']['login'],False,'supplier shell no login '+phase)
  ok(str(D/('BOOTSTRAP_'+phase+'.json')) in tool['result']['output'] and ref(D/('BOOTSTRAP_'+phase+'.json'))['sha256'] in tool['result']['output'],'supplier actual output file/hash linkage '+phase)
 # PRE/POST child bootstrap complete descriptors came from same supplier.
 boot=a['host_bootstrap']['bootstrap'];same(boot['named'],card['bootstrap'],'child named supplier');same(boot['actual'],card['bootstrap'],'child actual supplier');same(boot['executable'],BOOT,'child actual bootstrap descriptor');same([boot[k] for k in ('isolated','dont_write_bytecode','optimize')],[1,1,0],'snapshot bootstrap flags')
 for mod in boot['modules']:
  if 'binding' in mod:
   bi=mod['binding'];rp=bi['resolved_path'];ok(rp in vfiles or rp in (str(Q/'prepare.py'),str(Q/'runtime_metadata.py')),'saved child bootstrap file domain '+mod['name'])
   expect=pure(vfiles[rp]) if rp in vfiles else pure(ref(rp));same(bi['target'],expect,'child bootstrap complete module pin '+mod['name'])
 summary.update(source_files=547,inherited_dependencies=442,runtime_files=9923,runtime_bytes=258862951,output_files=16,operation_entries=18,operation_files=len(operation['identities']),vendor_entries=len(fw),vendor_files=len(vfiles),vendor_file_bytes=48024515,snapshot_bootstrap_modules=len(boot['modules']),root_vendor_modules=len(vendor['bootstrap_descriptor']['modules']),whole_snapshot=ref(P/'PRE.stdout'),optimized_report=ref(P/'PROFILE.stdout'),genuine_outer=ref(D/'GENUINE_OUTER.json'))
 # Supplementary root check is read after independent reconstruction, never substituted.
 rootcheck=load(D/'ROOT_PROFILE_CHECK.json');same(rootcheck['runtime_files'],9923,'root supplementary inventory count');same(rootcheck['parent_seconds'],summary['parent_elapsed_seconds'],'root supplementary parent interval')
 result=dict(schema='ri150-independent-saved-optimized-check-v1',status='PASS',summary=summary,predicates=checks,read_inputs=sorted(reads.values(),key=lambda x:x['path']),scope='Reviewer-owned administrative saved metadata reconstruction; no subject imports, runtime re-observation, scientific payload decode or new admission.')
 for name,value in [('RECONSTRUCTED_PROFILE_CHECK.json',extras['profile_reconstruction']),('SAVED_OPTIMIZED_CHECKS.json',result),('BOTH_MODE_RELATION.json',extras['mode_relation'])]:
  with (R/name).open('xb') as f:f.write(canon(value))
 print(json.dumps(dict(status='PASS',successful_administrative_predicates=len(checks),summary=summary),sort_keys=True))
except BaseException as exc:
 failure=dict(status='FAILED_REVIEWER_CHECK',error=dict(type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()),summary=summary,predicates=checks,read_inputs=sorted(reads.values(),key=lambda x:x['path']))
 failure_path=R/('FAILED_CHECK_%02d.json' % (len(list(R.glob('FAILED_CHECK_*.json')))+1))
 with failure_path.open('xb') as f:f.write(canon(failure))
 raise
