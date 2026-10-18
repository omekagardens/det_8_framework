import hashlib,json,os
from pathlib import Path
E=Path('/Volumes/AI_DATA/development/det-review-evidence');S=E/'ri121-synthetic-caller-repair-7ys8vsc3';D=E/'ri121-root-runtime-qualification-jsf0o3_x';R=Path(__file__).parent
N=E/'ri121-independent-normal-saved-_vk7vsiq'
def read(p):return json.loads(Path(p).read_bytes())
def pin(p):
    b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ref(p):return {'path':str(p),**pin(p)}
checks=[];bindings={}
def check(v,m):
    if not v:raise ValueError(m)
    checks.append(m)
def verify(row):
    path=row['path'];expected=row.get('pin',{k:row[k] for k in ('bytes','sha256') if k in row});actual=pin(path)
    check(expected==actual,'exact '+path);bindings[path]={'path':path,**actual}
n=read(S/'controls/normal/receipt.json');nw=read(S/'controls/normal/runtime.json');nc=read(S/'controls/normal/CUSTODY.json')
p=read(S/'controls/optimized/receipt.json');w=read(S/'controls/optimized/runtime.json');c=read(S/'controls/optimized/CUSTODY.json')
f=read(S/'AUTHORIZED_FREEZE.json');a=read(S/'ADMIT_OPTIMIZED.json');ra=read(D/'ROOT_NORMAL_ADJUDICATION.json');nr=read(N/'INDEPENDENT_NORMAL_SAVED_REVIEW.json');nm=read(N/'INDEPENDENT_NORMAL_METADATA_CHECK.json')
check(pin(N/'INDEPENDENT_NORMAL_SAVED_REVIEW.json')=={'bytes':15491,'sha256':'04fa87ef05e3640d87c6e0c990bc591032729c154340e4e37ff935d10675589d'},'accepted normal review retained')
check(pin(N/'INDEPENDENT_NORMAL_METADATA_CHECK.json')=={'bytes':105214,'sha256':'26843b959f47fb1f11aa08b2d7216e27a7170ed5a9d4df531ff6c2dc069fce11'},'normal full metadata evidence retained')
for row in nr['evidence']+nr['prior_independent_reviews']:verify(row)
for row in f['helpers']:verify(row)
for row in f['sources']:
    for field in ('original','copy'):verify({'path':row[field],'pin':row['pin']})
for row in f['evidence'].values():verify(row)
for row in ra.values():
    if isinstance(row,dict) and 'path' in row and 'sha256' in row:verify(row)
verify(a['normal_acceptance'])
check(a['normal_acceptance']==ref(D/'ROOT_NORMAL_ADJUDICATION.json'),'optimized binds exact accepted normal decision')
check(ra['status']=='ACCEPT_NORMAL_SYNTHETIC_EXECUTION_AND_CUSTODY' and ra['all41_controls_per_implementation'] is True and ra['complete_independent_saved_validation'] is True,'actual normal acceptance semantics')
check(ra['independent_custody_review']==ref(N/'INDEPENDENT_NORMAL_SAVED_REVIEW.json'),'normal root acceptance binds completed independent review')
check(set(a)==set(read(S/'ADMIT_NORMAL.json')) and a['schema']=='ri121-root-mode-admission-v1' and a['status']=='AUTHORIZED_SINGLE_SYNTHETIC_MODE','exact separate optimized admission schema')
check(a['mode']=='optimized' and a['phase']==f['phase'] and a['freeze']==pin(S/'AUTHORIZED_FREEZE.json') and a['caller_source_acceptance']==f['evidence']['caller_source_acceptance'],'optimized admission source freeze mode phase')
check(a['command']==f['runs']['optimized']['command'] and a['launcher_command']==f['runs']['optimized']['launcher_command'],'optimized exact admitted commands')
check(a['command'][1:4]==['-I','-B','-O'] and a['launcher_command'][1:4]==['-I','-B','-O'],'actual optimized isolated no cache writing flags')
pchanged={'child_elapsed_seconds','command','final_sample_to_reap_gap_seconds','mode','mode_admission_after','mode_admission_before','monitor_attempts','outputs','peak_sampled_rss_kib','process_after','process_before','samples','verified_custody'}
wchanged={'elapsed_seconds','mode','mode_admission_after','mode_admission_before','operation','runtime_after','runtime_before'}
for actor,current,normal,changed in [('parent',p,n,pchanged),('worker',w,nw,wchanged)]:
    check(set(current)==set(normal),actor+' identical full receipt schema')
    check({k for k in current if current[k]!=normal[k]}==changed,actor+' only reviewed cross-mode differences')
    for k in set(current)-changed:check(current[k]==normal[k],actor+' entire retained field '+k)
    check(current['mode']=='optimized',actor+' optimized mode')
    expectedad={'path':str(S/'ADMIT_OPTIMIZED.json'),'pin':pin(S/'ADMIT_OPTIMIZED.json'),'normal_acceptance':ref(D/'ROOT_NORMAL_ADJUDICATION.json')}
    check(current['mode_admission_before']==current['mode_admission_after']==expectedad,actor+' exact before after optimized admission')
expectedprofile=dict(f['expected_runtime'],optimize=1)
check(p['process_before']==p['process_after']==w['runtime_before']==w['runtime_after']==expectedprofile,'four actual profiles differ from normal only optimize')
check(p['runtime_before']==p['runtime_after']==w['runtime_bytes_before']==w['runtime_bytes_after']==n['runtime_before'],'all runtime closures exactly accepted normal')
check(p['command']==a['command'],'actual optimized child command')
for k in ('stdout','stderr','custody','worker_receipt'):check(p['outputs'][k]==pin(f['runs']['optimized'][k]),'optimized output '+k)
check(w['operation']=={'claim':f['claim'],'custody':ref(S/'controls/optimized/CUSTODY.json'),'result':ref(S/'controls/optimized/RESULT.json')},'complete worker operation')
expectedc=dict(nc,mode='optimized',report=ref(S/'controls/optimized/RESULT.json'))
check(c==expectedc,'whole optimized custody changes only mode and report path')
expectedvc=dict(n['verified_custody'],custody_pin=pin(S/'controls/optimized/CUSTODY.json'))
check(p['verified_custody']==expectedvc,'complete verified custody')
check(read(S/'controls/optimized/attempt.json')=={'mode':'optimized','phase':f['phase'],'freeze':pin(S/'AUTHORIZED_FREEZE.json'),'command':a['command']},'exact actual optimized attempt')
outer=read(D/'OPTIMIZED_OUTER_TOOL.json');check(outer['launch']['chunk_id']=='dd4ec5' and outer['launch']['session_id']==28093 and outer['completion']['chunk_id']=='f3a3c1' and outer['completion']['exit_code']==0,'genuine optimized initial and final outer transcription')
check(p['child_exit_code']==0 and w['exit_code']==0 and p['success'] is True and w['genuine_run_completed'] is True and w['full_validator_passed'] is True,'actual optimized run and full validator successful')
check(len(p['samples'])==len(p['monitor_attempts'])==97,'all optimized 97 raw attempts and samples')
last=0
for i,(sample,attempt) in enumerate(zip(p['samples'],p['monitor_attempts'])):
    check(set(attempt)=={'elapsed_seconds','returncode','stdout','stderr'} and attempt['returncode']==0 and attempt['stderr']=='' and attempt['stdout'].strip().isdigit() and int(attempt['stdout'])==sample['rss_kib'] and attempt['elapsed_seconds']==sample['elapsed_seconds'],'optimized raw sample '+str(i))
    check(set(sample)=={'elapsed_seconds','gap_seconds','rss_kib'} and sample['gap_seconds']==sample['elapsed_seconds']-last and 0<sample['gap_seconds']<=.1 and 0<=sample['rss_kib']<=524288,'optimized gap rss '+str(i));last=sample['elapsed_seconds']
check(p['peak_sampled_rss_kib']==max(s['rss_kib'] for s in p['samples'])==52864,'optimized actual peak RSS')
check(p['child_elapsed_seconds']==3.127368416000536 and 0<w['elapsed_seconds']<p['child_elapsed_seconds']<180,'actual optimized elapsed within fixed cap')
check(p['final_sample_gap_passed'] is True and p['final_sample_to_reap_gap_seconds']==p['child_elapsed_seconds']-last and 0<=p['final_sample_to_reap_gap_seconds']<=.1,'actual optimized final sample gap')
positives=[s for s in p['samples'] if s['rss_kib']>0]
check(len(positives)==96 and p['samples'][-1]['rss_kib']==0 and p['child_elapsed_seconds']-positives[-1]['elapsed_seconds']<.1,'terminal zero sample permitted with recent positive coverage')
normalbody=(S/'controls/normal/RESULT.json').read_bytes();optbody=(S/'controls/optimized/RESULT.json').read_bytes();check(normalbody==optbody,'entire 81253 byte report equality')
q=json.loads(optbody);domain=read(S/'REPORT_DOMAIN.source-only.json')
check({k:v for k,v in q.items() if k!='scientific_result'}==domain['qualification_envelope'],'all optimized control envelope fields exact')
check({k:v for k,v in q['scientific_result'].items() if k not in ('cases','bounds')}==domain['scientific_envelope'],'optimized scientific envelope exact')
for key in ('mutation_refusals','parser_refusals','psd_refusals'):
    for row in q[key]:check(row['primary']==row['validator']==row['expected'],'optimized reported actual control '+row['id'])
premeta=read(D/'OPTIMIZED_PRE_METADATA.json');postmeta=read(D/'OPTIMIZED_POST_METADATA.json')
check((D/'OPTIMIZED_PRE_METADATA.json').read_bytes()==(D/'OPTIMIZED_POST_METADATA.json').read_bytes()==(D/'NORMAL_PRE_METADATA.json').read_bytes()==(D/'NORMAL_POST_METADATA.json').read_bytes(),'entire four external metadata records equal')
check(premeta['observed_dyld_routes']==postmeta['observed_dyld_routes']==ref(D/'ACTUAL_DYLD_ROUTE_SIDECAR.json'),'optimized required nonnull exact sidecar')
for row in read(D/'ROOT_RUNTIME_ADJUDICATION.json')['required_root_custody']:verify(row)
for path in read(D/'ACTUAL_DYLD_ROUTE_SIDECAR.json')['absent_paths']:check(not os.path.lexists(path),'observed route remains absent '+path)
for row in read(D/'ACTUAL_DYLD_ROUTE_SIDECAR.json')['symlinks']:check(os.readlink(row['path'])==row['target'],'actual route link retained')
sequence=[N/'INDEPENDENT_NORMAL_SAVED_REVIEW.json',D/'ROOT_NORMAL_ADJUDICATION.json',S/'ADMIT_OPTIMIZED.json',S/'controls/optimized/attempt.json',S/'controls/optimized/runtime.json',S/'controls/optimized/receipt.json']
mtimes=[path.stat().st_mtime_ns for path in sequence];check(mtimes==sorted(mtimes),'saved filesystem timing corroborates review before admission before actual attempt completion')
for name in ('OPTIMIZED_PREPARATION.json','OPTIMIZED_ROOT_PREFLIGHT.json','OPTIMIZED_OUTER_TOOL.json','OPTIMIZED_PRE_METADATA.json','OPTIMIZED_POST_METADATA.json','OPTIMIZED_ROOT_SAVED_CUSTODY_CHECK.json','ROOT_NORMAL_ADJUDICATION.json'):bindings[str(D/name)]=ref(D/name)
for name in ('ADMIT_OPTIMIZED.json','controls/optimized/RESULT.json','controls/optimized/receipt.json','controls/optimized/runtime.json','controls/optimized/CUSTODY.json','controls/optimized/attempt.json','controls/optimized/stderr'):bindings[str(S/name)]=ref(S/name)
out={'schema':'ri121-independent-optimized-saved-metadata-check-v1','status':'ALL_OPTIMIZED_AND_CROSS_MODE_SAVED_CUSTODY_CHECKS_PASS','method':'Read-only saved JSON metadata, complete report byte equality, dependency hashing; no science replay or target import. Reuses accepted complete normal source/math/profile/closure review.','checks':checks,'bindings':list(bindings.values()),'sequence_mtimes':[{'path':str(path),'mtime_ns':stamp} for path,stamp in zip(sequence,mtimes)],'monitor':{'samples':97,'raw_attempts':97,'positive_samples':96,'terminal_zero_samples':1,'peak_sampled_rss_kib':52864,'elapsed_seconds':p['child_elapsed_seconds'],'max_sample_gap_seconds':max(s['gap_seconds'] for s in p['samples']),'final_gap_seconds':p['final_sample_to_reap_gap_seconds'],'last_positive_to_reap_seconds':p['child_elapsed_seconds']-positives[-1]['elapsed_seconds']},'loaded_modules':'All four entire maps exactly equal their already accepted normal counterparts: parent67/67 worker69/80; no new origins.'}
path=R/'INDEPENDENT_OPTIMIZED_METADATA_CHECK.json';path.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'artifact':ref(path),'checks':len(checks),'monitor':out['monitor']},indent=2))
