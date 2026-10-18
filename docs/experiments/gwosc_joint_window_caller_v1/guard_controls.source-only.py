"""Nonscientific RI121 regression controls; separate root admission is mandatory.

Uses the exact packet main functions and runtime scanner. Small control objects,
source/mode/runtime acceptance functions and runtime observations are explicitly
substituted to isolate ordering. No science path is entered or copied. This is
not a production receipt or evidence for the candidate interpreter's closure.
"""
import argparse
import builtins
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch


def pin(path):
    body=Path(path).read_bytes()
    return {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}


def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def need(condition,message):
    if not condition: raise ValueError(message)


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec)
    # Intentional active-helper execution, only after root's separate guard card.
    builtins.exec(compile(Path(path).read_bytes(),str(path),'exec'),value.__dict__)
    return value


def replace_root(value,old,new):
    if type(value) is str:return value.replace(old,new)
    if type(value) is list:return [replace_root(x,old,new) for x in value]
    if type(value) is dict:return {k:replace_root(v,old,new) for k,v in value.items()}
    return value


def failure_case(packet,base,side,refusal,postfail=False):
    """Actual main and actual finally; fixture admissions/runtime stop before science."""
    root=Path(tempfile.mkdtemp(prefix=side+'-'+refusal+'-',dir=base))
    template=json.loads((packet/'MANIFEST.source-only-template.json').read_bytes())
    manifest=replace_root(template,str(packet),str(root))
    manifest['schema']='ri121-synthetic-qualification-freeze-v1'
    manifest['status']='authorized_synthetic_qualification'
    for name in ('control.py','launch.py','worker.py','runtime_support.py'):
        (root/name).write_bytes((packet/name).read_bytes())
    (root/'controls'/'normal').mkdir(parents=True)
    (root/'tmp').mkdir()
    freeze=root/'AUTHORIZED_FREEZE.json'
    freeze.write_bytes(canonical(manifest))
    control=module(packet/'control.py','ri121_fixture_control')
    launch=module(packet/'launch.py','ri121_fixture_launch')
    worker=module(packet/'worker.py','ri121_fixture_worker')
    main=launch if side=='parent' else worker
    main.__file__=str(root/('launch.py' if side=='parent' else 'worker.py'))
    counts={'runtime_helper_calls':0,'runtime_helper_first_entries':0,'science_entries':0,
            'runtime_verify':0,'runtime_profile':0,'loaded_files':0,'source_checks':0}
    cached=[False]
    expected='fixture_'+refusal
    def source_check(value):
        counts['source_checks']+=1
        if refusal=='source':raise ValueError(expected)
        return [{'fixture':'source-only-no-science-read'}]
    def source_admission(value,ctrl):
        if refusal in ('caller','runtime_acceptance'):raise ValueError(expected)
        return {'fixture':'source-mode-runtime-prerequisites'}
    def mode_admission(value,mode,ctrl):
        if refusal=='mode':raise ValueError(expected)
        return {'fixture':'normal-mode-admission'}
    def verify(value,ctrl):
        counts['runtime_verify']+=1
        if postfail and counts['runtime_verify']>1:raise ValueError('fixture_postcheck')
        return {'fixture':'runtime-bytes'}
    def profile(value,mode,ctrl):
        counts['runtime_profile']+=1
        return {'fixture':'profile'}
    def loaded(value,ctrl):
        counts['loaded_files']+=1
        if counts['loaded_files']==1:raise ValueError(expected)
        return {'fixture':{'path':'fixture-only'}}
    runtime=SimpleNamespace(verify=verify,profile=profile,loaded_files=loaded)
    def runtime_helper(value,ctrl):
        counts['runtime_helper_calls']+=1
        if not cached[0]:counts['runtime_helper_first_entries']+=1;cached[0]=True
        return runtime
    def fixture_exec(body,namespace):
        builtins.exec(body,namespace)
        namespace['verify_sources']=source_check
    def captured(name,path,body):
        if name=='ri121_worker_control':return control
        if name=='ri121_worker_admission':return launch
        counts['science_entries']+=1
        raise ValueError('fixture_unexpected_science_entry')
    control.verify_sources=source_check
    launch.source_admission=source_admission
    launch.mode_admission=mode_admission
    launch.runtime_helper=runtime_helper
    launch.exec=fixture_exec
    worker.load_captured=captured
    with patch.object(sys,'argv',[str(main.__file__),str(freeze),'normal']), patch.dict(os.environ,manifest['environment'],clear=True):
        code=main.main()
    receipt=Path(manifest['runs']['normal']['receipt' if side=='parent' else 'worker_receipt'])
    record=json.loads(receipt.read_bytes())
    checks={'failed_completion':code==1,'no_science_entry':counts['science_entries']==0,
            'original_failure_preserved':(record.get('error')==expected if side=='parent' else record.get('error',{}).get('message')==expected)}
    if refusal!='late':
        checks['no_runtime_helper_entry']=counts['runtime_helper_calls']==0
        checks['no_runtime_scan']=counts['runtime_verify']==0
        # The old packet lacks entry-state fields; semantic counters still decide.
        if 'runtime_helper_state' in record:
            checks['unentered_custody']=record['runtime_helper_state']=='not_entered' and record['runtime_postcheck_state']=='not_entered' and record['prerequisites_passed'] is False
            fields=('runtime_before','runtime_after','process_before','process_after','loaded_modules_before','loaded_modules_after') if side=='parent' else ('runtime_bytes_before','runtime_bytes_after','runtime_before','runtime_after','loaded_modules_before','loaded_modules_after')
            checks['unentered_fields_null']=all(record.get(key) is None for key in fields)
    else:
        checks['one_first_helper_entry']=counts['runtime_helper_first_entries']==1
        expected_tail_count=1 if postfail and side=='worker' else 2
        checks['later_failure_postchecked']=counts['runtime_verify']==2 and counts['runtime_profile']==expected_tail_count and counts['loaded_files']==expected_tail_count
        if postfail:
            checks['postcheck_failure_retained']=bool(record.get('postcheck_error'))
            if side=='parent':checks['original_stop_reason_preserved']=record.get('stop_reason')=='supervisor_ValueError'
    return {'id':side+'_'+refusal+('_postcheck' if postfail else ''),'fixture_root':str(root),'checks':checks,
            'pass':all(checks.values()),'counts':counts,'receipt':{'path':str(receipt),**pin(receipt)}}


def runtime_case(packet,base,kind):
    root=Path(tempfile.mkdtemp(prefix='runtime-'+kind+'-',dir=base))
    control=module(packet/'control.py','ri121_fixture_runtime_control')
    runtime=module(packet/'runtime_support.py','ri121_fixture_runtime')
    roots=[root/'stdlib',root/'venv_site',root/'system_site']
    for path in roots:path.mkdir()
    (roots[0]/'tiny.py').write_bytes(b'fixture only\n')
    config=root/'openssl.cnf';config.write_bytes(b'# isolated inactive configuration\n')
    lib=root/'libcrypto.fixture';lib.write_bytes(b'not an executable library\n')
    alias=root/'libcrypto.alias';alias.symlink_to(lib.name)
    absent=[str(root/('absent-'+str(i))) for i in range(8)]
    binding=control.binding(str(alias))
    runtime.ROOTS=[str(x) for x in roots];runtime.REQUIRED_FILES=[str(config)]
    runtime.ALLOWED_LINKS=[];runtime.ABSENT_PATHS=absent;runtime.REQUIRED_LOADER_BINDINGS=[binding]
    inventory={'schema':'ri121-complete-stdlib-runtime-inventory-v2','roots':runtime.ROOTS,
               'extra_files':sorted([str(config),str(lib)]),'files':[], 'symlinks':[],
               'absent_paths':absent,'loader_bindings':[binding],'scope':'isolated nonscientific regression fixture'}
    expected=None
    if kind=='absent_file':Path(absent[1]).write_bytes(b'appeared\n');expected='previously absent startup/import/loader path appeared'
    elif kind=='absent_dangling_link':Path(absent[1]).symlink_to('missing');expected='previously absent startup/import/loader path appeared'
    elif kind=='missing_loader':inventory['loader_bindings']=[];expected='mandatory loader binding omitted or changed'
    elif kind=='changed_loader_declaration':inventory['loader_bindings']=[{**binding,'resolved_path':str(root/'wrong')}];expected='mandatory loader binding omitted or changed'
    elif kind=='changed_loader_path':
        other=root/'other-lib';other.write_bytes(b'changed\n');alias.unlink();alias.symlink_to(other.name);expected='non-OS loader binding changed'
    elif kind=='missing_config':inventory['extra_files'].remove(str(config));expected='interpreter/framework/monitor/config runtime files omitted'
    observed=None;rows=None
    try:
        rows=runtime.scan(inventory,control)
        if kind=='positive':
            inventory['files']=rows
            ip=root/'fixture-inventory.json';ip.write_bytes(canonical(inventory))
            executable=root/'interpreter.fixture';executable.write_bytes(b'not executable\n')
            manifest={'runtime_inventory':{'path':str(ip),'pin':pin(ip)},'interpreter':control.binding(str(executable))}
            result=runtime.verify(manifest,control)
            need(result['runtime_files_count']==3,'fixture verify count differs')
    except BaseException as exc:observed={'type':type(exc).__name__,'message':str(exc)}
    passed=(observed is None and rows is not None) if expected is None else observed=={'type':'ValueError','message':expected}
    return {'id':'runtime_'+kind,'fixture_root':str(root),'pass':passed,'expected_failure':expected,'observed_failure':observed,
            'actual_scanner_and_verify_used':True,'substituted_domain_constants':['ROOTS','REQUIRED_FILES','ALLOWED_LINKS','ABSENT_PATHS','REQUIRED_LOADER_BINDINGS']}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--admission',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--scope',choices=('failure-tails','all'),default='all')
    args=parser.parse_args();packet=args.packet.resolve()
    admission=json.loads(args.admission.read_bytes())
    need(admission['status']=='AUTHORIZE_NONSCIENTIFIC_RI121_GUARD_CONTROLS_ONLY' and admission['packet']==str(packet) and
         admission['scope']==args.scope and admission['harness']==pin(__file__),'root guard-control admission differs')
    helpers={name:pin(packet/name) for name in ('control.py','launch.py','worker.py','runtime_support.py')}
    need(admission['helpers']==helpers,'root admitted helper pins differ')
    need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==0,'guard control interpreter flags differ')
    need(not args.output.exists(),'existing control report')
    base=Path(tempfile.mkdtemp(prefix='ri121-guard-fixtures-',dir=args.output.parent))
    rows=[]
    def attempt(label,fn):
        try:rows.append(fn())
        except BaseException as exc:rows.append({'id':label,'pass':False,'unexpected_control_error':{'type':type(exc).__name__,'message':str(exc)}})
    for side in ('parent','worker'):
        for refusal in ('source','caller','runtime_acceptance','late'):
            attempt(side+'_'+refusal,lambda s=side,r=refusal:failure_case(packet,base,s,r))
        attempt(side+'_late_postcheck',lambda s=side:failure_case(packet,base,s,'late',True))
    attempt('worker_mode',lambda:failure_case(packet,base,'worker','mode'))
    if args.scope=='all':
        for kind in ('positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config'):
            attempt('runtime_'+kind,lambda k=kind:runtime_case(packet,base,k))
    after={name:pin(packet/name) for name in helpers}
    stable=after==helpers
    report={'schema':'ri121-nonscientific-guard-control-report-v1','scope':args.scope,'packet':str(packet),
            'helpers_before':helpers,'helpers_after':after,'helpers_unchanged':stable,'cases':rows,
            'passed':sum(row['pass'] for row in rows),'failed':sum(not row['pass'] for row in rows),
            'science_module_executed':False,'science_path_attempted':any(row.get('counts',{}).get('science_entries',0) for row in rows),
            'candidate_interpreter_invoked':False,'production_runtime_qualified':False,
            'fixture_root':str(base),'admission':{'path':str(args.admission),**pin(args.admission)},
            'claim':'Isolated non-scientific first-refusal/failure-tail and finite runtime-guard regression checks only.'}
    with args.output.open('xb') as stream:stream.write(canonical(report));stream.flush();os.fsync(stream.fileno())
    print(json.dumps({'report':str(args.output),'passed':report['passed'],'failed':report['failed'],'helpers_unchanged':stable}))
    return 0 if stable and report['failed']==0 else 1


if __name__=='__main__':raise SystemExit(main())
