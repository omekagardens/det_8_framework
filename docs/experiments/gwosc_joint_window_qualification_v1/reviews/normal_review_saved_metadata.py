import hashlib, json, os
from pathlib import Path
E=Path('/Volumes/AI_DATA/development/det-review-evidence')
S=E/'ri121-synthetic-caller-repair-7ys8vsc3'
D=E/'ri121-root-runtime-qualification-jsf0o3_x'
R=Path(__file__).parent
def read(p): return json.loads(Path(p).read_bytes())
def identity(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p): return identity(Path(p).read_bytes())
def ref(p): return {'path':str(p),**pin(p)}
def canonical(j): return (json.dumps(j,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
checks=[]; bindings={}
def check(value,label):
    if not value: raise ValueError(label)
    checks.append(label)
def verify(row):
    path=row['path']; expected=row.get('pin',{k:row[k] for k in ('bytes','sha256') if k in row})
    actual=pin(path); check(actual==expected,'exact '+path); bindings[path]={'path':path,**actual}
f=read(S/'AUTHORIZED_FREEZE.json');t=read(S/'MANIFEST.source-only-template.json')
p=read(S/'controls/normal/receipt.json');w=read(S/'controls/normal/runtime.json');c=read(S/'controls/normal/CUSTODY.json')
a=read(S/'ADMIT_NORMAL.json');q=read(S/'controls/normal/RESULT.json');inv=read(D/'RUNTIME_INVENTORY.json')
domain=read(S/'REPORT_DOMAIN.source-only.json');history=read(S/'HISTORY_CLOSURE.source-only.json')
outer=read(D/'NORMAL_OUTER_TOOL.json');runtimead=read(D/'ROOT_RUNTIME_ADJUDICATION.json')
for key in f:
    if key not in ('schema','status','evidence','expected_runtime','runtime_inventory'): check(f[key]==t[key],'retained freeze '+key)
check(set(f)==set(t),'freeze exact keys')
check(f['evidence']['scientific_source_acceptance']==t['evidence']['scientific_source_acceptance'],'retained scientific acceptance')
for row in f['evidence'].values(): verify(row)
for row in f['helpers']: verify(row)
for row in f['sources']:
    for field in ('copy','original'): verify({'path':row[field],'pin':row['pin']})
for field in ('report_domain','history_closure','runtime_inventory'): verify(f[field])
check(len(history)==48,'48 history refs')
for row in history: verify(row)
sourcepins=read(S/'SOURCE_PINS.json');check(len(sourcepins['files'])==20,'20 source packet records plus manifests')
for row in sourcepins['files']: verify(row)
fp=pin(S/'AUTHORIZED_FREEZE.json');ap=pin(S/'ADMIT_NORMAL.json');cp=pin(S/'controls/normal/CUSTODY.json');qp=pin(S/'controls/normal/RESULT.json')
check(a['mode']=='normal' and a['normal_acceptance'] is None and a['freeze']==fp,'actual normal first admission')
check(a['command']==f['runs']['normal']['command'] and a['launcher_command']==f['runs']['normal']['launcher_command'],'admitted commands match')
for actor,j in [('parent',p),('worker',w)]:
    check(j['freeze']==fp and j['mode']=='normal' and j['phase']==f['phase'],actor+' mode freeze phase')
    check(j['prerequisites_passed'] is True and j['runtime_helper_state']=='captured' and j['runtime_postcheck_state']=='complete',actor+' complete gated runtime')
    check(j['source_before']==j['source_after']==p['source_before'],actor+' full source before after')
    check(j['acceptance_before']==j['acceptance_after']==p['acceptance_before'],actor+' full acceptance before after')
    check(j['acceptance_before']['history']==history and j['acceptance_before']['evidence']==f['evidence'],actor+' complete history evidence')
    check(j['mode_admission_before']==j['mode_admission_after']=={'normal_acceptance':None,'path':str(S/'ADMIT_NORMAL.json'),'pin':ap},actor+' exact mode admission before after')
check(p['runtime_before']==p['runtime_after']==w['runtime_bytes_before']==w['runtime_bytes_after'],'four complete runtime checks equal')
check(p['runtime_before']['inventory_pin']==pin(D/'RUNTIME_INVENTORY.json') and p['runtime_before']['runtime_files_count']==9923,'exact 9923 runtime binding')
check(p['runtime_before']['runtime_files_identity']==identity(canonical(inv['files'])),'whole saved runtime identity from all 9923 descriptors')
check(p['process_before']==p['process_after']==w['runtime_before']==w['runtime_after']==f['expected_runtime']==runtimead['expected_runtime'],'all four actual profiles match admitted normal')
check(w['exit_code']==0 and p['child_exit_code']==0 and p['success'] is True and p['stop_reason'] is None and w['error'] is None,'parent child success')
check(w['genuine_run_started'] is True and w['genuine_run_completed'] is True and w['full_validator_passed'] is True,'genuine run and complete independent validator')
captures={row['relative']:row['pin'] for row in f['sources']}
check(w['captured_sources_before']==w['captured_sources_after']==c['captured_sources']==captures,'three captured scientific sources stable')
check(c['freeze']==fp and c['report']=={'path':str(S/'controls/normal/RESULT.json'),**qp} and c['mode']=='normal' and c['inputs']==[],'custody full binding')
check(c['saved_result_validation']==w['saved_result_validation'] and c['scientific_validation']==w['scientific_validation'],'custody validation records')
check(w['scientific_validation']=={'bounds':3,'cases':9,'groups':12,'status':'all_fields_independently_match'},'complete scientific validator scope')
check(w['saved_result_validation']=={'historical_controls_reexecuted':False,'scientific_independent_reconstruction':True,'status':'all_saved_fields_match'},'saved audit not a historical control replay')
for k in ('stdout','stderr','custody','worker_receipt'): check(p['outputs'][k]==pin(f['runs']['normal'][k]),'exact output '+k)
check(p['verified_custody']['custody_pin']==cp and p['verified_custody']['report_pin']==qp,'parent verified custody pins')
check(w['operation']['result']==c['report'] and w['operation']['custody']=={'path':str(S/'controls/normal/CUSTODY.json'),**cp},'worker output pins')
check(read(S/'controls/normal/attempt.json')=={'command':f['runs']['normal']['command'],'freeze':fp,'mode':'normal','phase':f['phase']},'exact actual attempt')
check(outer['launch']['chunk_id']=='f388bf' and outer['launch']['session_id']==91595 and outer['completion']['chunk_id']=='cda7b7' and outer['completion']['exit_code']==0,'genuine initial and final outer transcription')
check(p['command']==f['runs']['normal']['command'] and p['environment']==f['environment'],'actual command and environment')
check(p['limits']==f['limits']=={'maximum_sample_gap_seconds':.1,'ps_timeout_seconds':.05,'rss_kib':524288,'target_poll_seconds':.025,'wall_seconds':180},'unchanged limits')
check(len(p['samples'])==len(p['monitor_attempts'])==97,'all 97 samples and raw attempts')
last=0
for i,(sample,attempt) in enumerate(zip(p['samples'],p['monitor_attempts'])):
    check(attempt['returncode']==0 and attempt['stderr']=='' and attempt['elapsed_seconds']==sample['elapsed_seconds'] and int(attempt['stdout'])==sample['rss_kib'],'raw monitor sample '+str(i))
    check(sample['gap_seconds']==sample['elapsed_seconds']-last and 0<sample['gap_seconds']<=.1 and 0<sample['rss_kib']<=524288,'sample gap rss '+str(i));last=sample['elapsed_seconds']
check(max(x['rss_kib'] for x in p['samples'])==p['peak_sampled_rss_kib']==54688,'actual peak RSS')
check(p['child_elapsed_seconds']==3.1491453340022417 and p['child_elapsed_seconds']<180,'actual elapsed below cap')
check(p['final_sample_to_reap_gap_seconds']==p['child_elapsed_seconds']-last and p['final_sample_gap_passed'] is True and p['final_sample_to_reap_gap_seconds']<=.1,'final sample to reap bound')
allowed={row['path']:{k:row[k] for k in ('bytes','sha256')} for row in inv['files']}
allowed.update({row['path']:row['pin'] for row in f['helpers']});allowed.update({row['copy']:row['pin'] for row in f['sources']})
module_rows={};modulesummary={}
for actor,j in [('parent',p),('worker',w)]:
    before=j['loaded_modules_before'];after=j['loaded_modules_after']
    check(all(after.get(k)==v for k,v in before.items()),actor+' no module origin changed or disappeared')
    modulesummary[actor]={'before_count':len(before),'after_count':len(after),'added_modules':sorted(set(after)-set(before))}
    for when in ('before','after'):
        for name,row in j['loaded_modules_'+when].items():
            check(row['path'] in allowed and {k:row[k] for k in ('bytes','sha256')}==allowed[row['path']],actor+' '+when+' loaded '+name)
            module_rows[row['path']]=row
for row in module_rows.values(): verify(row)
check(p['loaded_modules_before']==p['loaded_modules_after'],'parent origins identical')
check(canonical(q)==(S/'controls/normal/RESULT.json').read_bytes(),'whole report canonical body')
check({k:v for k,v in q.items() if k!='scientific_result'}==domain['qualification_envelope'],'entire qualification envelope exact')
science=q['scientific_result']
check({k:v for k,v in science.items() if k not in ('cases','bounds')}==domain['scientific_envelope'],'entire scientific envelope exact')
check([x['id'] for x in science['cases']]==domain['case_ids'] and [x['id'] for x in science['bounds']]==domain['bound_ids'],'exact nine case three bound inventories')
check(len(q['mutation_refusals'])==33 and len(q['parser_refusals'])==5 and len(q['psd_refusals'])==3,'33 mutation 5 parser 3 PSD controls')
for group in ('mutation_refusals','parser_refusals','psd_refusals'):
    for row in q[group]: check(row['expected']==row['primary']==row['validator'],'actual reported control agreement '+row['id'])
pre=read(D/'NORMAL_PRE_METADATA.json');post=read(D/'NORMAL_POST_METADATA.json')
check((D/'NORMAL_PRE_METADATA.json').read_bytes()==(D/'NORMAL_POST_METADATA.json').read_bytes()==(D/'PRE_SCIENCE_RUNTIME_METADATA.json').read_bytes(),'full external pre post metadata byte identical')
sidecarref=ref(D/'ACTUAL_DYLD_ROUTE_SIDECAR.json')
check(pre['observed_dyld_routes']==post['observed_dyld_routes']==sidecarref,'required nonnull exact actual dyld sidecar')
sidecar=read(sidecarref['path'])
for path in sidecar['absent_paths']: check(not os.path.lexists(path),'actual route absent '+path)
for row in sidecar['symlinks']: check(os.readlink(row['path'])==row['target'],'actual route symlink exact')
def walkrefs(value):
    if isinstance(value,dict):
        if 'path' in value and (('pin' in value and set(value['pin'])=={'bytes','sha256'}) or ('bytes' in value and 'sha256' in value)): verify(value)
        for child in value.values(): walkrefs(child)
    elif isinstance(value,list):
        for child in value: walkrefs(child)
walkrefs(runtimead['required_root_custody'])
for name in ('check_runtime_metadata.py','metadata.py','ACTUAL_DYLD_ROUTE_SIDECAR.json','NORMAL_OUTER_TOOL.json','NORMAL_PRE_METADATA.json','NORMAL_POST_METADATA.json','NORMAL_ROOT_PREFLIGHT.json','NORMAL_PREPARATION.json','ROOT_RUNTIME_ADJUDICATION.json','ROOT_SAVED_SCIENTIFIC_RECONSTRUCTION.json','review_saved_science.py','NORMAL_ROOT_SAVED_CUSTODY_CHECK.json'): bindings[str(D/name)]=ref(D/name)
for name in ('SOURCE_PINS.json','HANDOFF.json','AUTHORIZED_FREEZE.json','ADMIT_NORMAL.json','controls/normal/RESULT.json','controls/normal/receipt.json','controls/normal/runtime.json','controls/normal/CUSTODY.json','controls/normal/attempt.json','controls/normal/stderr'): bindings[str(S/name)]=ref(S/name)
check(not (S/'ADMIT_OPTIMIZED.json').exists(),'optimized not admitted during independent normal review')
result={'schema':'ri121-independent-normal-saved-metadata-check-v1','status':'ALL_SAVED_CUSTODY_METADATA_CHECKS_PASS','method':'Reviewer-owned JSON comparison and opaque hashing only; no target import, fixtures, science arithmetic, replay or admission. Root and child whole 9923-file scans not duplicated.','checks':checks,'bindings':list(bindings.values()),'modules':modulesummary,'unique_loaded_files':list(module_rows.values()),'sample_count':97,'peak_sampled_rss_kib':54688,'elapsed_seconds':p['child_elapsed_seconds'],'max_sample_gap_seconds':max(x['gap_seconds'] for x in p['samples']),'final_gap_seconds':p['final_sample_to_reap_gap_seconds'],'scientific_read_coverage':{'complete_cases':len(science['cases']),'case_field_counts_including_id':[len(x) for x in science['cases']],'bounds':len(science['bounds']),'controls':41,'recomputed':False},'reviewer_metadata_draft_correction':'An earlier unsaved metadata-only command stopped at the mistaken expectation len(sourcepins.files)+2==20; actual manifest has 20 records plus SOURCE_PINS/HANDOFF. Corrected before review acceptance, no target activity or output changes.'}
out=R/'INDEPENDENT_NORMAL_METADATA_CHECK.json';out.write_bytes(canonical(result))
print(json.dumps({'artifact':ref(out),'check_count':len(checks),'modules':modulesummary,'unique_loaded_files':len(module_rows)},indent=2))
