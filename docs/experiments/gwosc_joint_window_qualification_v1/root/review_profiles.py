"""Check saved profile observations and pins; never executes candidate code."""
import importlib.util
from pathlib import Path
import os

D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m',D/'metadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
C=m.B/'ri121-runtime-candidate-rIMnamYh'
inventory=m.load(C/'RUNTIME_INVENTORY.candidate.json')
files={r['path']:r for r in inventory['files']}
admit=m.load(D/'PROFILE_ADMISSION.json')
reports={}
verified=[]
def need(value,message):
    if not value:raise ValueError(message)
for mode in ('normal','optimized'):
    prefix='PROFILE_'+mode.upper()
    outer=m.load(D/(prefix+'_OUTER_TOOL.json'))
    completion=m.load(D/(prefix+'_COMPLETION.json'))
    need(outer['exit_code']==0 and completion['returncode']==0 and completion['timeout'] is None,'actual completion')
    need(completion['command']==admit['runs'][mode]['command'] and completion['environment']==admit['environment'],'invocation')
    need(completion['admission']==m.ref(D/'PROFILE_ADMISSION.json'),'admission changed')
    m.verify(completion['stdout']['path'],completion['stdout']);m.verify(completion['stderr']['path'],completion['stderr'])
    need(completion['stderr']['bytes']==0,'stderr')
    value=m.load(D/(prefix+'.json'));reports[mode]=value
    need(value['profile_before']==value['profile_after'],'profile drift')
    profile=value['profile_after']
    need(profile['isolated']==profile['dont_write_bytecode']==1 and profile['optimize']==(mode=='optimized'),'flags')
    need(value['uname']==list(os.uname()),'host drift')
    need(value['decimal']['extension_loaded'] is False and value['decimal']['fallback_loaded'] is True and value['decimal']['decimal_class_is_fallback'] is True,'fallback')
    error=value['decimal']['extension_import_error']
    need(error['type']=='ImportError' and 'Library not loaded: /opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib' in error['message'],'missing decimal library')
    empty='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    need(value['hashlib']['sha256_empty']==value['hashlib']['openssl_sha256_empty']==empty,'hash usability')
    need(value['startup']=={'enable_user_site':False,'site_prefixes':[str(m.B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env')], 'distutils_hook_loaded':True,'sitecustomize_loaded':True,'usercustomize_loaded':False},'startup')
    observed=[]
    for name,row in value['modules'].items():
        for field in ('file','cached','origin'):
            path=row[field]
            if path in (None,'built-in','frozen'):
                continue
            p=Path(path)
            need(p.is_absolute(),'nonabsolute module descriptor')
            if name=='__main__':
                need(field=='file' and p==D/'runtime_profile_probe.py','unexpected main origin')
                observed.append({'module':name,'field':field,'identity':m.ref(p)});continue
            if not p.exists():
                need(field=='cached' and not p.is_symlink(),'missing noncache path')
                observed.append({'module':name,'field':field,'path':path,'absent':True});continue
            resolved=str(p.resolve(strict=True))
            need(resolved in files,'out-of-domain module: '+name)
            ident=m.verify(resolved,files[resolved])
            observed.append({'module':name,'field':field,'identity':{k:ident[k] for k in ('path','bytes','sha256')}})
    verified.append({'mode':mode,'report':m.ref(D/(prefix+'.json')),'outer':m.ref(D/(prefix+'_OUTER_TOOL.json')),'completion':m.ref(D/(prefix+'_COMPLETION.json')),'module_count':len(value['modules']),'descriptors':observed})
normal=reports['normal']['profile_after']; optimized=dict(reports['optimized']['profile_after']);optimized['optimize']=0
need(normal==optimized,'mode profiles differ')
need(normal['path']==[inventory['absent_paths'][0],inventory['roots'][0],inventory['roots'][0]+'/lib-dynload',inventory['roots'][1]],'unexpected path')
need(normal['version_info']==[3,11,6,'final',0] and normal['implementation']=='cpython' and normal['byteorder']=='little','interpreter version')
need(normal['executable']==m.load(C/'INTERPRETER_BINDING.candidate.json')['named_path'],'executable name')
extra_absences=[
 '/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib',
 '/opt/homebrew/Cellar/mpdecimal/4.0.1/lib/libmpdec.3.dylib',
 '/System/Volumes/Preboot/Cryptexes/OS/opt/homebrew/Cellar/mpdecimal/4.0.1/lib/libmpdec.3.dylib',
]
for name in extra_absences:
    need(name in reports['normal']['decimal']['extension_import_error']['message'] and name in reports['optimized']['decimal']['extension_import_error']['message'],'actual route missing')
    try:Path(name).lstat()
    except FileNotFoundError:continue
    raise ValueError('additional loader route exists')
link=Path('/opt/homebrew/opt/mpdecimal')
need(link.is_symlink() and os.readlink(link)=='../Cellar/mpdecimal/4.0.1','mpdecimal opt route')
print(m.save('ACTUAL_DYLD_ROUTE_SIDECAR.json',{'schema':'ri121-root-observed-decimal-route-sidecar-v1','absent_paths':extra_absences,'symlinks':[{'path':str(link),'target':os.readlink(link)}],'boundary':'Concrete observed failed loader search routes, separately root-checked before/after production; outside fixed v2 in-process guards. Stable trusted host premise retained.'}))
print(m.save('ROOT_SAVED_PROFILE_CHECK.json',{'status':'ALL_SAVED_PROFILE_GATES_PASS','profiles':verified,'expected_runtime':normal,'profile_before_after_equal':True,'normal_optimized_equal_except_optimize':True,'decimal_fallback_observed':True,'hash_algorithms_not_provider_identities':True,'trace_complete':False,'scientific_qualification':False,'pre_metadata':m.ref(D/'PRE_PROFILE_EXTENDED_METADATA.json'),'post_metadata':m.ref(D/'POST_PROFILE_METADATA.json'),'driver_reviewed_by_root':m.ref(D/'run_profile_probe.py')}))
