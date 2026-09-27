"""Root saved-custody checks, without importing a production helper or target."""
import sys
import importlib.util
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m',D/'metadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
S=m.B/'ri121-synthetic-caller-repair-7ys8vsc3'
mode=sys.argv[1];tag=mode.upper()
def need(v,s):
    if not v:raise ValueError(s)
def equal(a,b,s):need(m.canonical(a)==m.canonical(b),s)
f=m.load(S/'AUTHORIZED_FREEZE.json');run=f['runs'][mode]
rows={k:m.load(run[k])for k in ('stdout','receipt','worker_receipt','custody','claim')}
for k,v in rows.items():need(m.canonical(v)==Path(run[k]).read_bytes(),'canonical '+k)
r,w,c,result=rows['receipt'],rows['worker_receipt'],rows['custody'],rows['stdout']
need(r['success'] is True and r['stop_reason'] is None and type(r['child_exit_code'])is int and r['child_exit_code']==0,'parent success')
need(w['exit_code']==0 and w['error'] is None and w.get('postcheck_error') is None,'worker success')
need(w['genuine_run_started'] is w['genuine_run_completed'] is w['full_validator_passed'] is True,'genuine scientific run')
equal(r['command'],run['command'],'command');equal(r['environment'],f['environment'],'environment');equal(r['limits'],f['limits'],'limits')
equal(r['freeze'],m.pure(m.identity(S/'AUTHORIZED_FREEZE.json')),'freeze')
for x in (r,w):
    need(x['prerequisites_passed'] is True and x['runtime_helper_state']=='captured' and x['runtime_postcheck_state']=='complete','prerequisites')
    for stem in ('source','acceptance','mode_admission'):
        need(x[stem+'_before'] is not None,'missing stage');equal(x[stem+'_before'],x[stem+'_after'],'stage drift '+stem)
    need(all(x['loaded_modules_after'].get(k)==v for k,v in x['loaded_modules_before'].items()),'module origin drift')
    for row in x['loaded_modules_after'].values():m.verify(row['path'],row)
for stem in ('source','acceptance','mode_admission'):equal(r[stem+'_before'],w[stem+'_before'],'parent worker '+stem)
equal(r['runtime_before'],r['runtime_after'],'parent runtime');equal(w['runtime_bytes_before'],w['runtime_bytes_after'],'child runtime')
equal(r['runtime_before'],w['runtime_bytes_before'],'runtime crosscheck')
equal(r['process_before'],r['process_after'],'parent profile');equal(w['runtime_before'],w['runtime_after'],'worker profile');equal(r['process_before'],w['runtime_before'],'profile crosscheck')
for key in ('stdout','stderr','worker_receipt','custody'):equal(r['outputs'][key],m.pure(m.identity(run[key])),'output pin '+key)
need(Path(run['stderr']).read_bytes()==b'','stderr')
sciencepins={x['relative']:x['pin']for x in f['sources']}
equal(w['captured_sources_before'],sciencepins,'captured science');equal(w['captured_sources_before'],w['captured_sources_after'],'capture drift')
equal(c['captured_sources'],sciencepins,'custody captures')
equal(c['report'],m.ref(run['stdout']),'custody output')
equal(w['operation']['custody'],m.ref(run['custody']),'worker custody')
equal(w['operation']['result'],m.ref(run['stdout']),'worker output')
domain=m.load(S/'REPORT_DOMAIN.source-only.json')
equal({k:v for k,v in result.items()if k!='scientific_result'},domain['qualification_envelope'],'entire qualification envelope')
equal({k:v for k,v in result['scientific_result'].items()if k not in ('cases','bounds')},domain['scientific_envelope'],'entire scientific envelope')
equal([x['id']for x in result['scientific_result']['cases']],domain['case_ids'],'cases');equal([x['id']for x in result['scientific_result']['bounds']],domain['bound_ids'],'bounds')
need(len(r['samples'])>0,'no samples');last=0
for sample in r['samples']:
    need(sample['elapsed_seconds']>last and sample['gap_seconds']==sample['elapsed_seconds']-last,'sample timing')
    need(sample['gap_seconds']<=f['limits']['maximum_sample_gap_seconds'] and sample['rss_kib']<=f['limits']['rss_kib'],'sample limits');last=sample['elapsed_seconds']
for attempt in r['monitor_attempts']:
    need(attempt.get('returncode')==0 and attempt.get('stderr')=='' and attempt['stdout'].strip().isdigit(),'monitor completion requires review')
    need(any(sample['elapsed_seconds']==attempt['elapsed_seconds'] and sample['rss_kib']==int(attempt['stdout'])for sample in r['samples']),'raw monitor/sample mismatch')
need(len(r['samples'])==len(r['monitor_attempts']),'monitor completeness')
need(r['child_elapsed_seconds']<=180 and r['final_sample_to_reap_gap_seconds']<=.1 and r['final_sample_gap_passed'] is True,'final gap/wall')
need(r['peak_sampled_rss_kib']==max(x['rss_kib']for x in r['samples']),'peak RSS')
outer=m.load(D/(tag+'_OUTER_TOOL.json'));need(outer['completion']['exit_code']==0,'outer exit')
pre=m.load(D/(tag+'_PRE_METADATA.json'));post=m.load(D/(tag+'_POST_METADATA.json'));equal(pre,post,'root runtime custody drift')
equal(pre['observed_dyld_routes'],m.ref(D/'ACTUAL_DYLD_ROUTE_SIDECAR.json'),'mandatory sidecar')
for dep in m.load(D/'ROOT_RUNTIME_ADJUDICATION.json')['required_root_custody']:m.verify(dep['path'],dep)
if mode=='optimized':need(Path(run['stdout']).read_bytes()==Path(f['runs']['normal']['stdout']).read_bytes(),'entire mode equality')
print(m.save(tag+'_ROOT_SAVED_CUSTODY_CHECK.json',{'status':'ALL_SAVED_CUSTODY_GATES_PASS','mode':mode,'report':m.ref(run['stdout']),'receipt':m.ref(run['receipt']),'worker':m.ref(run['worker_receipt']),'custody':m.ref(run['custody']),'outer':m.ref(D/(tag+'_OUTER_TOOL.json')),'root_pre':m.ref(D/(tag+'_PRE_METADATA.json')),'root_post':m.ref(D/(tag+'_POST_METADATA.json')),'sidecar':m.ref(D/'ACTUAL_DYLD_ROUTE_SIDECAR.json'),'sample_count':len(r['samples']),'monitor_count':len(r['monitor_attempts']),'child_seconds':r['child_elapsed_seconds'],'peak_sampled_rss_kib':r['peak_sampled_rss_kib'],'maximum_gap':max(x['gap_seconds']for x in r['samples']),'final_gap':r['final_sample_to_reap_gap_seconds'],'all41_controls_per_implementation':True,'saved_controls_reexecuted':False,'actual_execution_evidence':'Exact captured qualifier.run sequence plus real monitored/reaped child and genuine outer exit; saved labels alone insufficient.'}))
