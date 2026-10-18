"""RI121 captured-source synthetic worker; source only until root admission."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time


def load_captured(name, path, body):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None or name in sys.modules:
        raise ValueError('captured module unavailable')
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    exec(compile(body,str(path),'exec'),module.__dict__)
    return module


def main():
    if len(sys.argv)!=3 or sys.argv[2] not in ('normal','optimized'):
        raise ValueError('expected authorized manifest and one mode')
    freeze_path,mode=Path(sys.argv[1]),sys.argv[2]
    root=Path(__file__).resolve().parent
    if freeze_path!=root/'AUTHORIZED_FREEZE.json' or freeze_path!=freeze_path.resolve() or freeze_path.is_symlink():
        raise ValueError('unexpected authorization path')
    raw=freeze_path.read_bytes();manifest=json.loads(raw)
    item=next(x for x in manifest['helpers'] if x['path']==str(root/'control.py'))
    body=(root/'control.py').read_bytes()
    if {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}!=item['pin']:
        raise ValueError('control source differs before import')
    control=load_captured('ri121_worker_control',root/'control.py',body)
    manifest=control.parse_json(raw)
    control.require(manifest['schema']=='ri121-synthetic-qualification-freeze-v1' and
                    manifest['status']=='authorized_synthetic_qualification' and
                    manifest['phase']=='fabricated_joint_window_qualification' and
                    manifest['context']=='fixed_synthetic_joint_window_arithmetic_only','phase not authorized')
    control.require(raw==control.canonical(manifest) and manifest['root']==str(root),'noncanonical authorization/root')
    control.require(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and
                    sys.flags.optimize==(0 if mode=='normal' else 1),'interpreter flags differ')
    control.require(dict(os.environ)==manifest['environment'],'exact worker environment differs')
    control.require(os.getppid()>1,'supervisor absent')
    run=manifest['runs'][mode]
    record={'schema':'ri121-synthetic-worker-receipt-v1','phase':manifest['phase'],'mode':mode,
            'freeze':control.identity(raw),'source_before':None,'source_after':None,
            'runtime_before':None,'runtime_after':None,'runtime_bytes_before':None,'runtime_bytes_after':None,
            'acceptance_before':None,'acceptance_after':None,'mode_admission_before':None,'mode_admission_after':None,
            'loaded_modules_before':None,'loaded_modules_after':None,
            'captured_sources_before':None,'captured_sources_after':None,'saved_result_validation':None,
            'scientific_validation':None,'full_validator_passed':False,'genuine_run_started':False,
            'genuine_run_completed':False,'operation':None,'error':None,
            'prerequisites_passed':False,'runtime_helper_state':'not_entered','runtime_postcheck_state':'not_entered'}
    admission,captured,runtime=None,None,None
    code,started=1,time.monotonic()
    try:
        record['source_before']=control.verify_sources(manifest)
        gate=next(row for row in manifest['helpers'] if row['path']==str(root/'launch.py'))
        admission=load_captured('ri121_worker_admission',gate['path'],control.verified_body(gate['path'],gate['pin']))
        admission.admit_command(manifest,mode,control)
        record['mode_admission_before']=admission.mode_admission(manifest,mode,control)
        record['acceptance_before']=admission.source_admission(manifest,control)
        record['prerequisites_passed']=True
        record['runtime_helper_state']='loading'
        runtime=admission.runtime_helper(manifest,control)
        record['runtime_helper_state']='captured'
        record['runtime_bytes_before']=runtime.verify(manifest,control)
        record['runtime_before']=runtime.profile(manifest,mode,control)
        record['loaded_modules_before']=runtime.loaded_files(manifest,control)
        sources={row['relative']:row for row in manifest['sources']}
        names=('primary.py','validator.py','qualify.py')
        # All three exact whole bodies are captured before any science import.
        captured={name:control.verified_body(sources[name]['copy'],sources[name]['pin']) for name in names}
        record['captured_sources_before']={name:control.identity(body) for name,body in captured.items()}
        control.require(record['captured_sources_before']==admission.SCIENCE,'captured science identities differ')
        primary,validator,qualifier=[load_captured('ri121_science_'+name.removesuffix('.py'),sources[name]['copy'],captured[name]) for name in names]
        record['genuine_run_started']=True
        report=qualifier.run(primary,validator)
        record['genuine_run_completed']=True
        body=qualifier.canonical(report)
        sys.stdout.buffer.write(body);sys.stdout.buffer.flush();os.fsync(sys.stdout.buffer.fileno())
        result_pin=control.file_pin(run['stdout'])
        control.require(result_pin==control.identity(body),'serialized qualification changed')
        saved_body=control.verified_body(run['stdout'],result_pin)
        saved=qualifier.parse_report(saved_body)
        # The independently owned reference is newly enumerated by the caller;
        # no reference is taken from the retained scientific_result.
        reference=primary.build_result()
        validation=qualifier.audit(saved,primary,validator,reference)
        scientific_validation=validator.validate_result(saved['scientific_result'])
        control.require(admission.canonical_pin(validation)==admission.canonical_pin(admission.AUDIT_OK) and
                        admission.canonical_pin(scientific_validation)==admission.canonical_pin(admission.VALIDATION_OK),
                        'complete saved qualification/scientific validation differs')
        control.require(qualifier.canonical(saved)==saved_body and control.file_pin(run['stdout'])==result_pin,
                        'saved qualification changed during validation')
        record['saved_result_validation']=validation;record['scientific_validation']=scientific_validation
        record['full_validator_passed']=True
        custody={'schema':'ri121-synthetic-custody-v1','phase':manifest['phase'],'mode':mode,
                 'report':{'path':run['stdout'],**result_pin},'freeze':record['freeze'],
                 'captured_sources':record['captured_sources_before'],'saved_result_validation':validation,
                 'scientific_validation':scientific_validation,'full_validator_passed':True,
                 'genuine_run_completed':True,'inputs':[],'claim':manifest['claim']}
        control.write_exclusive(run['custody'],custody)
        record['operation']={'result':custody['report'],'custody':{'path':run['custody'],**control.file_pin(run['custody'])},'claim':custody['claim']}
        code=0
    except BaseException as exc:
        record['error']={'type':type(exc).__name__,'message':str(exc)}
        print('RI121 synthetic qualification refused: '+str(exc),file=sys.stderr)
    finally:
        try:
            if captured is not None:
                record['captured_sources_after']={name:control.identity(body) for name,body in captured.items()}
                control.require(record['captured_sources_after']==record['captured_sources_before'],'captured source bytes changed')
            record['source_after']=control.verify_sources(manifest)
            # No first import/scan from a failure tail: retain the admitted handle.
            if runtime is not None:
                record['runtime_postcheck_state']='entered'
                record['runtime_bytes_after']=runtime.verify(manifest,control)
                control.require(record['runtime_bytes_after']==record['runtime_bytes_before'],'runtime bytes changed')
                record['runtime_after']=runtime.profile(manifest,mode,control)
                control.require(record['runtime_after']==record['runtime_before'],'runtime profile changed')
                record['loaded_modules_after']=runtime.loaded_files(manifest,control)
                if record['loaded_modules_before'] is not None:
                    control.require(all(record['loaded_modules_after'].get(k)==v for k,v in record['loaded_modules_before'].items()),
                                    'previously loaded origin changed')
                record['runtime_postcheck_state']='complete'
            if record['acceptance_before'] is not None:
                record['acceptance_after']=admission.source_admission(manifest,control)
                control.require(record['acceptance_after']==record['acceptance_before'],'source acceptance changed')
            if record['mode_admission_before'] is not None:
                record['mode_admission_after']=admission.mode_admission(manifest,mode,control)
                control.require(record['mode_admission_after']==record['mode_admission_before'],'root mode admission changed')
        except BaseException as exc:
            record['postcheck_error']={'type':type(exc).__name__,'message':str(exc)};code=1
        if code == 0 and not (record['prerequisites_passed'] is True and record['runtime_helper_state']=='captured' and
                              record['runtime_postcheck_state']=='complete' and all(record[key] is not None for key in
                              ('source_before','source_after','acceptance_before','acceptance_after','mode_admission_before','mode_admission_after',
                               'runtime_bytes_before','runtime_bytes_after','runtime_before','runtime_after','loaded_modules_before','loaded_modules_after'))):
            record['postcheck_error']={'type':'ValueError','message':'successful worker omitted admitted runtime stages'};code=1
        record['elapsed_seconds']=time.monotonic()-started;record['exit_code']=code
        control.write_exclusive(run['worker_receipt'],record)
    return code


if __name__=='__main__':
    raise SystemExit(main())
