"""RI130 captured-source WHITE-only worker. UNEXECUTED; root admission required."""
import hashlib
import importlib.util
import os
from pathlib import Path
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
    K.same(sys.argv,[str(root/'worker.py'),str(path),mode],'worker argv')
    K.same(dict(os.environ),m['environment'],'worker controlled environment')
    K.need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==(mode=='optimized'),'worker isolation flags')
    return m,C,K,C.identity(freeze_body)


def execute(m,mode,C,K,freeze_pin):
    """One genuine stage invocation, with all eligible tail checks independent."""
    root=Path(m['root']);run=m['runs'][mode];started=time.monotonic()
    runtime=None;evidence=None;captured=None;admitted=False;mode_bound=False
    first=None;envelope=None
    receipt={'schema':'ri130-white-worker-v1','mode':mode,'phase':K.PHASE,'context':K.CONTEXT,
      'freeze':freeze_pin,'limits':m['limits'],'source_count':30,'actual_scientific_inputs':[],
      'entry':'qualify_white_only.run_white_qualification','entry_phase':'fabricated_qualification',
      'entry_invocations':0,'entry_returned':False,'target_load_witness':[],
      'before':{},'postchecks':{},'saved_custody':None,'namespace_after':None,'error':None,
      'status':'started','full32_qualified':False,'actual_data_admitted':False,'ret_paused':True}
    try:
        K.need(not Path(run['worker_receipt']).exists() and not Path(run['worker_receipt']).is_symlink(),'worker receipt already exists')
        K.need(not Path(run['custody']).exists() and not Path(run['custody']).is_symlink(),'worker custody already exists')
        K.need(not Path(run['stage']).exists() and not Path(run['stage']).is_symlink(),'stage must be absent')
        receipt['before']['sources']=C.verify_sources(m)
        receipt['before']['source_admission']=K.source_admission(m,C);admitted=True
        receipt['before']['mode_admission']=K.mode_admission(m,mode,C);mode_bound=True
        # Nothing below is loaded until every source/history/current-runtime
        # acceptance and this mode's external pre-custody record has passed.
        runtime=K.load_helper(m,'runtime_support.py',C)
        receipt['before']['runtime']=runtime.verify(m,C)
        receipt['before']['profile']=runtime.profile(m,mode,C)
        evidence=K.load_helper(m,'evidence.py',C)
        receipt['before']['loaded']=runtime.loaded_files(m,C)
        captured=K.capture_targets(m,C)
        receipt['captured_targets']={name:C.identity(body) for name,body in captured.items()}
        modules=K.load_targets(m,captured,C,receipt['target_load_witness'])
        receipt['loaded_after_capture']=runtime.loaded_files(m,C)
        bindings=K.stage_bindings(m,C)
        receipt['entry_invocations']=1
        envelope=modules['qualify_white_only'].run_white_qualification(
            run['stage'],bindings,modules['white_validator'],modules['validator_controls'],phase='fabricated_qualification')
        receipt['entry_returned']=True
        body=C.canonical(envelope)
        K.need(len(body)<=K.CAP,'complete caller envelope cap')
        sys.stdout.buffer.write(body);sys.stdout.buffer.flush();os.fsync(sys.stdout.fileno())
        receipt['envelope_pin']=C.identity(body)
        # Refusal envelopes remain exactly saved, never promoted to success.
        receipt['saved_custody']=evidence.inspect_success(envelope,run['stage'],bindings,C)
    except BaseException as exc:
        first=exc
    finally:
        actions=[('freeze',lambda:K.same_after(C.file_pin(root/'AUTHORIZED_FREEZE.json'),freeze_pin,'freeze')),
                 ('sources',lambda:K.same_after(C.verify_sources(m),receipt['before'].get('sources'),'sources'))]
        if admitted:actions.append(('source_admission',lambda:K.same_after(K.source_admission(m,C),receipt['before']['source_admission'],'source acceptance')))
        if mode_bound:actions.append(('mode_admission',lambda:K.same_after(K.mode_admission(m,mode,C),receipt['before']['mode_admission'],'mode acceptance')))
        if captured is not None:
            actions.append(('captured_targets',lambda:K.same_after({name:C.identity(body) for name,body in captured.items()},receipt['captured_targets'],'captured target buffers')))
        # Retained runtime handle only; never first-import a helper after an
        # earlier source/admission rejection (the repaired RI121 F01 boundary).
        if runtime is not None:
            actions.extend([('runtime',lambda:K.same_after(runtime.verify(m,C),receipt['before'].get('runtime'),'runtime')),
                            ('profile',lambda:K.same_after(runtime.profile(m,mode,C),receipt['before'].get('profile'),'profile')),
                            ('loaded',lambda:runtime.loaded_files(m,C))])
        if evidence is not None and Path(run['stage']).is_dir():
            actions.append(('namespace',lambda:evidence.tree_snapshot(run['stage'],C)))
        if envelope is not None and receipt['saved_custody'] is not None:
            actions.append(('saved_custody',lambda:K.same_after(evidence.inspect_success(envelope,run['stage'],K.stage_bindings(m,C),C),receipt['saved_custody'],'full saved custody')))
        receipt['postchecks'],first=K.attempt_all(actions,first)
        if 'namespace' in receipt['postchecks']:receipt['namespace_after']=receipt['postchecks']['namespace']
        receipt['elapsed_seconds']=time.monotonic()-started
        receipt['status']='completed' if first is None else 'refused_or_failed'
        receipt['error']=None if first is None else {'type':type(first).__name__,'message':str(first)[:2048]}
        # This worker record is evidence only. The supervisor and genuine outer
        # observer bind both it and this custody record after process completion.
        custody={'schema':'ri130-white-worker-custody-v1','mode':mode,'phase':K.PHASE,'freeze':freeze_pin,
          'status':receipt['status'],'error':receipt['error'],'entry_invocations':receipt['entry_invocations'],
          'entry_returned':receipt['entry_returned'],'envelope_pin':receipt.get('envelope_pin'),
          'saved_custody':receipt['saved_custody'],'namespace_after':receipt['namespace_after'],
          'full32_qualified':False,'actual_data_admitted':False}
        try:C.write_exclusive(run['custody'],custody);receipt['custody_pin']=C.file_pin(run['custody'])
        except BaseException as exc:
            receipt['custody_write_error']={'type':type(exc).__name__,'message':str(exc)[:2048]}
            if first is None:first=exc
            receipt['status']='refused_or_failed';receipt['error']={'type':type(first).__name__,'message':str(first)[:2048]}
        C.write_exclusive(run['worker_receipt'],receipt)
    return 0 if first is None else 1


def main():
    if len(sys.argv)!=3:raise ValueError('freeze and mode required')
    m,C,K,freeze=bootstrap(sys.argv[1],sys.argv[2])
    return execute(m,sys.argv[2],C,K,freeze)


if __name__=='__main__':raise SystemExit(main())
