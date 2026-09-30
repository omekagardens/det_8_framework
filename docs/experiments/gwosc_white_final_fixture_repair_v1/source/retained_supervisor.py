"""RI130 WHITE-only sole-child supervisor. UNEXECUTED, no admission at import."""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import time

CONTROL_PIN={'bytes':5171,'sha256':'d27acae5645ee42a1aca76bb053900c3af8edd09aa090eecc199b1c7a887af81'}


def bootstrap(freeze_name,mode):
    path=Path(freeze_name)
    if not (path.is_absolute() and str(path)==freeze_name and path==path.resolve() and path.name=='AUTHORIZED_FREEZE.json'):
        raise ValueError('literal authorized freeze path required')
    root=path.parent;control=root/'control.py'
    before=control.stat(follow_symlinks=False)
    if control.is_symlink() or not control.is_file():raise ValueError('regular bootstrap control required')
    body=control.read_bytes();after=control.stat(follow_symlinks=False)
    if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns):
        raise ValueError('bootstrap control moved')
    if {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}!=CONTROL_PIN:raise ValueError('bootstrap control pin')
    spec=importlib.util.spec_from_file_location('ri130_control',control)
    C=importlib.util.module_from_spec(spec);sys.modules[spec.name]=C
    exec(compile(body,str(control),'exec'),C.__dict__)
    freeze_pin=C.file_pin(path);C.require(0<freeze_pin['bytes']<=67108864,'bounded freeze body')
    freeze_body=C.verified_body(path,freeze_pin);m=C.parse_json(freeze_body)
    C.require(freeze_body==C.canonical(m),'canonical freeze required')
    C.require(m['schema']=='ri130-white-fabricated-freeze-v1' and m['phase']=='fabricated_white_qualification','WHITE-only bootstrap boundary')
    entry=next(x for x in m['helpers'] if x['path']==str(root/'caller_contract.py'))
    captured=C.verified_body(entry['path'],entry['pin'])
    spec=importlib.util.spec_from_file_location('ri130_caller_contract',entry['path'])
    K=importlib.util.module_from_spec(spec);sys.modules[spec.name]=K
    exec(compile(captured,entry['path'],'exec'),K.__dict__)
    K.validate_static(m,root,C)
    K.same(C.file_pin(path),C.identity(freeze_body),'freeze after bootstrap')
    K.need(mode in ('normal','optimized'),'worker mode')
    K.same(sys.argv,[str(root/'launch.py'),str(path),mode],'launcher argv')
    K.same(dict(os.environ),m['environment'],'launcher controlled environment')
    K.need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==(mode=='optimized'),'launcher isolation flags')
    return m,C,K,C.identity(freeze_body)


def check_worker(m,mode,freeze_pin,before,C,K,E):
    run=m['runs'][mode]
    def saved(name):
        body=C.verified_body(run[name],K.bounded_file_pin(run[name],C));value=C.parse_json(body)
        K.same(body.decode('ascii'),C.canonical(value).decode('ascii'),'canonical worker output '+name)
        return value
    w=saved('worker_receipt');custody=saved('custody');envelope=saved('stdout')
    K.keys(w,('schema','mode','phase','context','freeze','limits','source_count','actual_scientific_inputs','entry','entry_phase',
       'entry_invocations','entry_returned','target_load_witness','before','postchecks','saved_custody','namespace_after','error',
       'status','full32_qualified','actual_data_admitted','ret_paused','captured_targets','loaded_after_capture','envelope_pin',
       'elapsed_seconds','custody_pin'),'complete successful worker receipt')
    K.same({k:w[k] for k in ('schema','mode','phase','context','freeze','limits','source_count','actual_scientific_inputs','entry',
       'entry_phase','entry_invocations','entry_returned','error','status','full32_qualified','actual_data_admitted','ret_paused')},
       {'schema':'ri130-white-worker-v1','mode':mode,'phase':K.PHASE,'context':K.CONTEXT,'freeze':freeze_pin,'limits':m['limits'],
       'source_count':30,'actual_scientific_inputs':[],'entry':'qualify_white_only.run_white_qualification',
       'entry_phase':'fabricated_qualification','entry_invocations':1,'entry_returned':True,'error':None,'status':'completed',
       'full32_qualified':False,'actual_data_admitted':False,'ret_paused':True},'genuine worker entry/completion boundary')
    K.need(type(w['elapsed_seconds']) in (int,float) and 0<=w['elapsed_seconds']<=180,'worker elapsed envelope')
    K.keys(w['before'],('sources','source_admission','mode_admission','runtime','profile','loaded'),'worker before fields')
    for name in ('sources','source_admission','mode_admission','runtime','profile'):
        K.same(w['before'][name],before[name],'parent/child before '+name)
    sources={x['relative']:x for x in m['sources']}
    captures={name:sources[relative]['pin'] for name,relative in K.MODULES}
    K.same(w['captured_targets'],captures,'all8 complete captured executable targets')
    K.same(w['target_load_witness'],[{'sequence':i,'module':name,'path':sources[relative]['copy'],
       'pin':sources[relative]['pin'],'state':'loaded'} for i,(name,relative) in enumerate(K.MODULES)],'entire ordered source-load witness')
    for loaded in (w['loaded_after_capture'],w['postchecks'].get('loaded',{}).get('value',{})):
        for name,relative in K.MODULES:
            K.same(loaded.get(name),{'path':sources[relative]['copy'],**sources[relative]['pin']},'all target module loaded origins')
    expected=('freeze','sources','source_admission','mode_admission','captured_targets','runtime','profile','loaded','namespace','saved_custody')
    K.keys(w['postchecks'],expected,'every eligible independent worker postcheck')
    for name,row in w['postchecks'].items():
        K.keys(row,('value','error'),'postcheck complete fields');K.need(row['error'] is None,'worker tail failure '+name)
    for name in ('sources','source_admission','mode_admission','runtime','profile'):
        K.same(w['postchecks'][name]['value'],w['before'][name],'worker before/after '+name)
    K.same(w['postchecks']['freeze']['value'],freeze_pin,'worker freeze custody')
    K.same(w['postchecks']['captured_targets']['value'],captures,'worker captured-buffer tail')
    K.same(w['envelope_pin'],C.file_pin(run['stdout']),'complete saved caller envelope')
    checked=E.inspect_success(envelope,run['stage'],K.stage_bindings(m,C),C)
    K.same(w['saved_custody'],checked,'entire saved stage evidence')
    K.same(w['postchecks']['saved_custody']['value'],checked,'complete stage postcheck')
    K.same(w['namespace_after'],w['postchecks']['namespace'],'retained complete namespace attempt')
    K.same(w['namespace_after']['value'],envelope['namespace']['inventory'],'complete saved namespace')
    K.same(w['custody_pin'],C.file_pin(run['custody']),'retained worker custody identity')
    K.same(custody,{'schema':'ri130-white-worker-custody-v1','mode':mode,'phase':K.PHASE,'freeze':freeze_pin,
       'status':'completed','error':None,'entry_invocations':1,'entry_returned':True,'envelope_pin':w['envelope_pin'],
       'saved_custody':checked,'namespace_after':w['namespace_after'],'full32_qualified':False,'actual_data_admitted':False},'whole worker custody envelope')
    K.same(C.file_pin(run['stderr']),C.identity(b''),'empty genuine child stderr')
    return {'worker':w,'envelope':envelope,'checked':checked}


def launch(m,mode,C,K,freeze_pin):
    root=Path(m['root']);run=m['runs'][mode];runtime=None;monitor=None;evidence=None;child=None
    admitted=False;mode_bound=False;first=None;started=None;out=None;err=None
    record={'schema':'ri130-white-supervisor-v1','mode':mode,'phase':K.PHASE,'context':K.CONTEXT,
      'freeze':freeze_pin,'limits':m['limits'],'command':run['command'],'launcher_command':run['launcher_command'],
      'environment':m['environment'],'before':{},'postchecks':{},'monitor_attempts':[],'samples':[],
      'peak_sampled_rss_kib':0,'child_exit_code':None,'child_elapsed_seconds':None,'stop_reason':None,
      'status':'started','error':None,'worker_check':None,'mode_relation':None,'retained_outputs':{},
      'full32_qualified':False,'actual_data_admitted':False,'ret_paused':True}
    directory=Path(run['receipt']).parent
    # Root precreates only the empty mode directories and controlled tmp root.
    K.need(directory==directory.resolve() and directory.is_dir() and not any(directory.iterdir()),'fresh empty mode directory')
    K.need((root/'tmp').is_dir() and root/'tmp'==(root/'tmp').resolve(),'literal controlled tmp directory')
    try:
        record['before']['sources']=C.verify_sources(m)
        record['before']['source_admission']=K.source_admission(m,C);admitted=True
        record['before']['mode_admission']=K.mode_admission(m,mode,C);mode_bound=True
        runtime=K.load_helper(m,'runtime_support.py',C)
        record['before']['runtime']=runtime.verify(m,C)
        record['before']['profile']=runtime.profile(m,mode,C)
        monitor=K.load_helper(m,'monitor.py',C)
        evidence=K.load_helper(m,'evidence.py',C)
        record['before']['loaded']=runtime.loaded_files(m,C)
        C.write_exclusive(run['claim'],{'schema':'ri130-exclusive-white-attempt-v1','mode':mode,'phase':K.PHASE,
           'freeze':freeze_pin,'mode_admission':record['before']['mode_admission'],'no_retry_or_replacement':True})
        out=Path(run['stdout']).open('xb');err=Path(run['stderr']).open('xb')
        started=time.monotonic()
        child=subprocess.Popen(run['command'],stdin=subprocess.DEVNULL,stdout=out,stderr=err,
           cwd=str(root),env=m['environment'],start_new_session=True)
        record['child_pid']=child.pid
        monitor.supervise(child,record,started)
        K.need(record['stop_reason'] is None and record['child_exit_code']==0,'genuine monitored child did not complete')
    except BaseException as exc:first=exc
    finally:
        # This tail never loads a new helper. It reaps only our own Popen child
        # even after monitor exceptions, preserving the original first error.
        actions=[]
        if child is not None and record['child_exit_code'] is None:
            actions.append(('reap_owned',lambda:monitor.reap_owned(child,record,started)))
        if out is not None:actions.append(('close_stdout',lambda:out.close()))
        if err is not None:actions.append(('close_stderr',lambda:err.close()))
        close_records,first=K.attempt_all(actions,first);record['ownership_tail']=close_records
        actions=[('freeze',lambda:K.same_after(C.file_pin(root/'AUTHORIZED_FREEZE.json'),freeze_pin,'freeze')),
                 ('sources',lambda:K.same_after(C.verify_sources(m),record['before'].get('sources'),'sources'))]
        if admitted:actions.append(('source_admission',lambda:K.same_after(K.source_admission(m,C),record['before']['source_admission'],'source acceptance')))
        if mode_bound:actions.append(('mode_admission',lambda:K.same_after(K.mode_admission(m,mode,C),record['before']['mode_admission'],'mode acceptance')))
        if runtime is not None:
            actions.extend([('runtime',lambda:K.same_after(runtime.verify(m,C),record['before'].get('runtime'),'runtime')),
                            ('profile',lambda:K.same_after(runtime.profile(m,mode,C),record['before'].get('profile'),'profile')),
                            ('loaded',lambda:runtime.loaded_files(m,C))])
        if evidence is not None and Path(run['stage']).is_dir():
            actions.append(('namespace',lambda:evidence.tree_snapshot(run['stage'],C)))
        record['postchecks'],first=K.attempt_all(actions,first)
        # Inspect every extant top-level output, including partial/refused output.
        output_actions=[(name,lambda name=name:C.file_pin(run[name])) for name in ('stdout','stderr','worker_receipt','custody','claim')]
        record['retained_outputs'],first=K.attempt_all(output_actions,first)
        if first is None:
            try:
                checked=check_worker(m,mode,freeze_pin,record['before'],C,K,evidence)
                record['worker_check']={'status':'complete_saved_worker_and_stage_match','worker_pin':C.file_pin(run['worker_receipt']),
                   'envelope_pin':C.file_pin(run['stdout']),'stage':checked['checked']}
                if mode=='optimized':
                    # The separate root normal acceptance was checked both before
                    # and after this child. Reinspect the complete normal envelope
                    # and compare every field under the closed path/pin relation.
                    normal=m['runs']['normal'];body=C.verified_body(normal['stdout'],K.bounded_file_pin(normal['stdout'],C))
                    normal_envelope=C.parse_json(body);K.same(body.decode('ascii'),C.canonical(normal_envelope).decode('ascii'),'normal canonical retained envelope')
                    record['mode_relation']=evidence.compare_modes(normal_envelope,checked['envelope'],normal['stage'],run['stage'],K.stage_bindings(m,C),C)
            except BaseException as exc:first=exc
        if evidence is not None:
            namespace_records,first=K.attempt_all([('mode_directory',lambda:evidence.tree_snapshot(directory,C))],first)
            record['pre_receipt_namespace']=namespace_records['mode_directory']
            if first is None:
                try:
                    observed=sorted(row['name'] for row in record['pre_receipt_namespace']['value']['records'] if row['name']!='.' and '/' not in row['name'])
                    expected=sorted(Path(run[name]).name for name in ('stdout','stderr','worker_receipt','custody','claim','stage'))
                    K.same(observed,expected,'complete caller namespace before exclusive supervisor receipt')
                except BaseException as exc:first=exc
        record['status']='completed_pending_external_custody_review' if first is None else 'refused_or_failed'
        record['error']=None if first is None else {'type':type(first).__name__,'message':str(first)[:2048]}
        C.write_exclusive(run['receipt'],record)
    return 0 if first is None else 1


def main():
    if len(sys.argv)!=3:raise ValueError('freeze and mode required')
    m,C,K,freeze=bootstrap(sys.argv[1],sys.argv[2])
    return launch(m,sys.argv[2],C,K,freeze)


if __name__=='__main__':raise SystemExit(main())
