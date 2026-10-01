"""UNEXECUTED RI244 administrative preparation proposal; never dispatches a subject.
Only root may separately approve/run this writer. Its candidate wrapper is not an
adapter admission. No ADMIT_PRE_MODE, DISPATCH, O or E file is created here.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import stat
import sys
import time

B = Path('/Volumes/AI_DATA/development/det-review-evidence')
D = B/'ri244-current-normal-premode-2kfsmiea'
O = B/'ri156-operation-ri244-premode-2kfsmiea'
E = B/'ri154-white-execution-proposed-42_uvw15'
W = Path(__file__).resolve().parent
V = '/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
CAP = 67108864
ENV = {'LC_ALL':'C','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','OMP_NUM_THREADS':'1',
       'OPENBLAS_NUM_THREADS':'1','PATH':'/usr/bin:/bin','TMPDIR':str(D/'tmp'),'TZ':'UTC',
       'VECLIB_MAXIMUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
BOUNDS = {'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,
          'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':CAP}
NAMES = {'PREPARATION_ATTEMPT.json','CUSTODY_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json',
         'BOOTSTRAP_PREFLIGHT.json','PRE_MODE_BOOTSTRAP.proposal.py','ADMISSION_CANDIDATE.json'}


def need(ok, message):
    if not ok:
        raise ValueError('RI244_PREPARATION: '+message)


def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')


def same(a, b, label):
    need(canonical(a)==canonical(b), label)


def state(path):
    s=Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def initial_body(path, expected_sha):
    p=Path(path)
    need(p.is_absolute() and p.resolve(strict=True)==p and not p.is_symlink(), 'literal initial path')
    before=state(p)
    need(stat.S_ISREG(before[2]) and 0<before[4]<=CAP, 'bounded initial regular file')
    def descriptor_state(f):
        s=os.fstat(f.fileno())
        return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        same(descriptor_state(f),before,'initial opened descriptor')
        opened=f.read(CAP+1)
        same(descriptor_state(f),before,'initial final descriptor')
    same(state(p),before,'initial state drift')
    need(len(opened)==before[4] and hashlib.sha256(opened).hexdigest()==expected_sha,'initial body pin')
    return opened


def parse(body):
    def pairs(rows):
        out={}
        for key,value in rows:
            need(key not in out,'duplicate administrative key')
            out[key]=value
        return out
    def bad(value):
        raise ValueError('nonfinite administrative token '+value)
    value=json.loads(body,object_pairs_hook=pairs,parse_constant=bad)
    need(canonical(value)==body,'canonical administrative framing')
    return value


def main():
    need((sys.flags.isolated,sys.flags.dont_write_bytecode,sys.flags.optimize)==(1,1,0),'normal isolated administrative writer')
    args=argparse.ArgumentParser()
    args.add_argument('--root-decision',required=True)
    args.add_argument('--root-decision-sha256',required=True)
    a=args.parse_args()
    # Only the explicitly authenticated administrative helper is loaded. Root
    # authenticates this full writer and its ordinary Python supplier beforehand.
    decision_raw=initial_body(a.root_decision,a.root_decision_sha256)
    decision=parse(decision_raw)
    same(sorted(decision),sorted(('schema','status','preparation_source','proposal_handoff','output',
         'host_transcript','root_attests_fresh_genuine_host_tool_origin','operational_authorization')),'closed root decision')
    same([decision['schema'],decision['status'],decision['output']],
         ['ri244-root-unissued-preparation-decision-v1','AUTHORIZE_ONE_ADMINISTRATIVE_PREPARATION_ONLY',str(D)],'preparation-only decision')
    need(decision['root_attests_fresh_genuine_host_tool_origin'] is True and
         decision['operational_authorization'] is False,'no operational authority')
    own=decision['preparation_source']
    same(own['path'],str(Path(__file__).resolve()),'root-selected writer')
    need(len(initial_body(own['path'],own['sha256']))==own['bytes'],'whole writer pin')
    hp=B/'ri122-root-execution-review-6whn_vky/metadata.py'
    helper=initial_body(hp,'d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7')
    need(len(helper)==3144,'helper size')
    spec=importlib.util.spec_from_file_location('ri244_administrative_metadata_only',hp)
    m=importlib.util.module_from_spec(spec)
    exec(compile(helper,str(hp),'exec'),m.__dict__)
    seen={}
    def fresh(row):
        need(type(row) is dict and {'path','bytes','sha256'}<=set(row),'identity shape')
        need(type(row['bytes']) is int and 0<=row['bytes']<=CAP,'opaque file cap')
        value=m.identity(row['path'])
        same({k:value[k] for k in row},row,'whole input identity '+row['path'])
        if value['path'] in seen:
            same(value,seen[value['path']],'repeated input stability')
        seen[value['path']]=value
        return value
    def ref(path):
        value=m.identity(path)
        return {k:value[k] for k in ('path','bytes','sha256')}
    def read(row):
        fresh(row)
        body=initial_body(row['path'],row['sha256'])
        need(len(body)==row['bytes'],'read size')
        return parse(body)
    def keep_refs(value):
        # Traverse only already-selected administrative objects; pointed-to
        # bodies remain opaque. There is no recursive arbitrary body decoding.
        if type(value) is dict:
            if {'path','bytes','sha256'}<=set(value):
                fresh({k:value[k] for k in ('path','bytes','sha256')})
            elif set(value)=={'path','pin'} and type(value['pin']) is dict:
                fresh({'path':value['path'],**value['pin']})
            else:
                for child in value.values():keep_refs(child)
        elif type(value) is list:
            for child in value:keep_refs(child)
    fresh(ref(hp));decision_ref=ref(a.root_decision);fresh(decision_ref)
    handoff=read(decision['proposal_handoff'])
    same(decision['proposal_handoff']['path'],str(W/'HANDOFF.json'),'literal proposal seal')
    same(sorted(p.name for p in W.iterdir()),handoff['namespace'],'whole proposal namespace')
    for row in handoff['files']:fresh(row)
    refs=read({'path':str(W/'REFERENCES.json'),'bytes':4500,
               'sha256':'e1043bed3183088b4718a6dbfd3ea563b93d8875075fb60a148f71294b3c0b70'})
    for row in refs.values():fresh(row)
    manifest=read(refs['source_manifest']);need(len(manifest['modules'])==11 and len(manifest['dependencies'])==567,'source closure counts')
    for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:fresh(row)
    same(manifest['bootstrap_provenance'] in manifest['dependencies'],True,'bootstrap provenance retained')
    binding=fresh(manifest['bootstrap_binding'])
    same([binding['path'],binding['resolved_path'],binding['symlink_chain']],[V,V,[]],'exact direct vendor')
    qual=read(refs['qualification']);same(qual['source_manifest'],refs['source_manifest'],'qualified complete source')
    same([qual['status'],qual['all_passed'],qual['scientific_execution'],len(qual['controls'])],
         ['ACCEPT_EXACT_INERT_ADAPTER_CONTROLS',True,False,106],'accepted original qualification')
    for key in ('report','genuine_outer','independent_review'):fresh(qual[key])
    accepted=read(refs['input_review']);same(accepted['status'],'ACCEPT_UNISSUED_RUNTIME13_REQUEST5_SOURCE_COMPATIBILITY','accepted input scope')
    same([accepted['request'],accepted['runtime']],[refs['request'],refs['runtime']],'exact accepted candidate refs')
    keep_refs(accepted)
    request=read(refs['request']);runtime=read(refs['runtime'])
    same(sorted(request),sorted(('freeze','mode','actual_runtime','baseline','copies')),'request5')
    need(len(runtime)==13,'runtime13');same(request['actual_runtime'],refs['runtime'],'runtime candidate body')
    same([runtime['mode'],runtime['phase'],request['mode']],['normal','pre','normal'],'normal pre-mode')
    keep_refs(request);keep_refs(runtime)  # Installed freeze is only opaquely hashed.
    same(runtime['freeze'],{k:request['freeze'][k] for k in ('bytes','sha256')},'different freeze shapes')
    same(runtime['copy_observation'],refs['copy_observation'],'accepted whole copy observation')
    same(runtime['genuine_collection_tools'],refs['collection'],'accepted root genuine collection')
    same(read(runtime['snapshot']),read(runtime['baseline']),'whole current/accepted metadata')
    same(read(runtime['vendor_before']),read(runtime['vendor_after']),'complete accepted supplier projections')
    same(read(runtime['observed_dyld_routes']),read(runtime['snapshot'])['preobserved_dyld_routes'],'whole dyld sidecar')
    runtime_acceptance=read(runtime['runtime_acceptance']);keep_refs(runtime_acceptance)
    profiles=read(runtime_acceptance['profile_review']);keep_refs(profiles)
    normal=read(profiles['completions']['profile_normal']);keep_refs(normal)
    same([normal['artifacts']['PRE'],normal['environment']],[request['baseline'],runtime['environment']],'authentic normal baseline/environment')
    collection=read(refs['collection']);keep_refs(collection)
    capture=read(refs['capture_review']);same(capture['status'],'ACCEPT_CURRENT_E_METADATA_CAPTURE_AND_EXACT_SUPPLIER_PROJECTION','capture acceptance');keep_refs(capture)
    oldroles=read(refs['old_roles']);need(len(oldroles['observed_identities'])==2811,'all retained custody identities')
    for row in oldroles['observed_identities']:fresh(row)
    frozen=read(refs['copy_observation']);same(frozen['source_states'],oldroles['source_states'],'all retained source roles')
    same({k:len(v) for k,v in frozen['source_states'].items()},{'copies':48,'history':124,'target_originals':30},'role counts')
    old_supplier=read(refs['old_supplier']);old_E=read(refs['old_E']);oldhost=read(refs['old_host'])
    host=read(decision['host_transcript'])
    same(sorted(host),['arguments','observation','result'],'complete genuine host transcription')
    same(host['arguments'],oldhost['arguments'],'unchanged benign genuine host command')
    need(host['result'].get('exit_code')==0 and host['result'].get('session_id') is None,'genuine host terminal')
    need(type(host['result'].get('chunk_id')) is str and host['result']['chunk_id']!=oldhost['result']['chunk_id'],'new root host receipt')
    observation=json.loads(host['result']['output'])
    same(observation,host['observation'],'exact raw host stdout reconstruction')
    same(observation,oldhost['observation'],'whole host unchanged')
    same(observation['uname'],list(os.uname()),'actual host uname')
    oldpre=read(refs['old_preflight']);keep_refs(oldpre)
    old_admission=read({'path':str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),
         'bytes':2114,'sha256':'ac86cac1f9973266d84b2a1ad1b9a34e9655d897153dc264d6b0805f437389cd'})
    static=read(oldpre['static_native_adjudication'])
    def namespace(rows):
        result=[]
        for row in rows:
            p=Path(row['path']);before=state(p)
            value={'path':str(p),'kind':row['kind'],'state':before}
            if row['kind']=='directory':
                need(stat.S_ISDIR(before[2]),'supplier directory');value['entries']=sorted(x.name for x in p.iterdir())
            else:
                need(row['kind']=='symlink' and p.is_symlink(),'supplier link');value['target']=os.readlink(p)
            same(state(p),before,'supplier read-window drift');same(value,row,'full supplier namespace')
            result.append(value)
        return result
    def supplier():
        same(observation['uname'],list(os.uname()),'fresh supplier host uname')
        value={'vendor':[fresh(row) for row in old_supplier['vendor']],
               'tools':[fresh(row) for row in old_supplier['tools']],
               'namespace':namespace(old_supplier['namespace']),'absent':old_supplier['absent'],
               'host':{'argv':observation['command'],'exit_code':observation['returncode'],
                       'stdout':observation['stdout'],'stderr':observation['stderr'],'uname':observation['uname']},
               'environment':ENV,'observed_at_unix_ns':time.time_ns()}
        for path in value['absent']:need(not os.path.lexists(path),'supplier absent route')
        same([len(value['vendor']),sum(x['bytes'] for x in value['vendor']),len(value['tools']),len(value['namespace']),len(value['absent'])],
             [1810,48024515,4,195,2],'full vendor domain')
        same({k:v for k,v in value.items() if k not in ('environment','observed_at_unix_ns')},
             {k:v for k,v in old_supplier.items() if k not in ('environment','observed_at_unix_ns')},'stable complete vendor scope')
        return value
    def etree():
        rows=[]
        for row in old_E:
            p=E/row['relative'];need(not p.is_symlink(),'E literal entry');before=state(p)
            value={'relative':row['relative'],'kind':row['kind'],'state':before}
            if row['kind']=='directory':
                need(p.is_dir(),'E directory');value['entries']=sorted(x.name for x in p.iterdir())
            else:
                need(row['kind']=='file','E kind');value['identity']=fresh(row['identity'])
            same(state(p),before,'E read-window drift');same(value,row,'all historical E states/member lists');rows.append(value)
        need(len(rows)==58 and sum(x['kind']=='file' for x in rows)==49,'E49/9')
        return rows
    def absent_authority():
        for p in (D/'ADMIT_PRE_MODE.json',D/'DISPATCH.json',O,E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json'):
            need(not os.path.lexists(p),'no active authority/operation '+str(p))
        for p in (E/'tmp',E/'runs/normal',E/'runs/optimized'):
            same(sorted(x.name for x in p.iterdir()),[],'E output remains empty')
        same(sorted(x.name for x in Path(refs['request']['path']).parent.iterdir()),
             ['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json'],'preserved RI241 namespace')
    before_supplier=supplier();before_E=etree();absent_authority()
    need(D.resolve(strict=True)==D and D.is_dir() and not D.is_symlink(),'literal existing root reservation')
    same(sorted(p.name for p in D.iterdir()),[],'empty root preparation reservation')
    # All state needed for independent tails exists BEFORE output ownership.
    first=None;artifacts={};tails={};tail_observations={};snapshot=list(seen.values())
    def err(exc):return {'type':type(exc).__name__,'message':str(exc)[:2048]}
    def emit(name,value,raw=False):
        body=value if raw else canonical(value)
        need(type(body) is bytes and 0<len(body)<=CAP,'prepared output cap')
        with (D/name).open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
        need((D/name).read_bytes()==body,'raw prepared readback')
        result=ref(D/name);artifacts[name]=result;return result
    (D/'tmp').mkdir(mode=0o700)  # Failure here is genuine preownership refusal.
    try:
        (D/'monitor').mkdir(mode=0o700)
        emit('PREPARATION_ATTEMPT.json',{'schema':'ri244-unissued-preparation-attempt-v1',
             'decision':decision_ref,'proposal':decision['proposal_handoff'],'no_retry':True,'operational_authorization':False})
        custody=emit('CUSTODY_BEFORE.json',{'schema':'ri244-complete-preparation-custody-v1','identities':snapshot,
             'source_states':frozen['source_states'],'historical_roles':refs['old_roles'],'source_manifest':refs['source_manifest'],
             'root_decision':decision_ref,'host_transcript':decision['host_transcript']})
        vendor=emit('SUPPLIER_BEFORE.json',before_supplier);e_ref=emit('E_BEFORE.json',before_E)
        pre=emit('BOOTSTRAP_PREFLIGHT.json',{'schema':'ri244-root-unissued-premode-preflight-v1',
             'status':'PREPARED_UNISSUED_PENDING_INDEPENDENT_ROOT_REVIEW','selected_interpreter_binding':binding,
             'source_observation':custody,'runtime_observation':vendor,'E_observation':e_ref,
             'genuine_host':decision['host_transcript'],'source_acceptance':refs['source_review'],
             'input_acceptance':refs['input_review'],'static_native_adjudication':oldpre['static_native_adjudication'],
             'platform_premises':static['platform_premises_accepted'],'operation_premises':oldpre['operation_premises'],
             'environment':ENV,'scientific_execution_authorized':False,'operational_authorization':False})
        # Exact predecessor capture/monitor logic; only literal operation values change.
        template=initial_body(refs['bootstrap_template']['path'],refs['bootstrap_template']['sha256']).decode('ascii')
        bootstrap=template.replace('# One root-admitted administrative adapters action; unchanged RI141 child monitor.',
             '# UNISSUED RI244 bootstrap proposal. Separate root admission/dispatch required.')
        bootstrap=bootstrap.replace(repr(old_admission['environment']),repr(ENV))
        bootstrap=bootstrap.replace('ri204_whole_unchanged_ri141_adapters_monitor','ri244_whole_unchanged_ri141_premode_monitor')
        bootstrap=bootstrap.replace(str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),str(D/'ADMIT_PRE_MODE.json'))
        bootstrap=bootstrap.replace(str(B/'ri204-root-adapters-f04k2tg9/monitor'),str(D/'monitor'))
        bootstrap=bootstrap.replace("'ADAPTERS', 180, expected_environment)","'PRE_MODE', 180, expected_environment)")
        need('ri204-root-adapters' not in bootstrap and repr(ENV) in bootstrap,'complete literal bootstrap adaptation')
        sealed_bootstrap=next(row for row in handoff['files'] if row['path']==str(W/'PRE_MODE_BOOTSTRAP.proposal.txt'))
        need(bootstrap.encode('ascii')==initial_body(sealed_bootstrap['path'],sealed_bootstrap['sha256']),'entire sealed bootstrap text')
        boot_ref=emit('PRE_MODE_BOOTSTRAP.proposal.py',bootstrap.encode('ascii'),raw=True)
        candidate={'schema':'ri156-root-adapter-admission-v1','status':'AUTHORIZE_ONE_BOUNDED_METADATA_ACTION',
             'action':'pre_mode','source_manifest':refs['source_manifest'],'source_review':refs['source_review'],
             'qualification':refs['qualification'],'request':refs['request'],'output':str(O),'environment':ENV,
             'bootstrap_preflight':pre,'bounds':BOUNDS,'genuine_outer_required':True}
        need(len(candidate)==12,'exact candidate field count')
        emit('ADMISSION_CANDIDATE.json',{'schema':'ri244-wrapped-unissued-admission-v1','status':'UNISSUED_NOT_OPERATIONAL_AUTHORITY',
             'candidate':candidate,'bootstrap_proposal':boot_ref,'root_input_acceptance':refs['input_review'],
             'future_admission_path':str(D/'ADMIT_PRE_MODE.json'),'operational_authorization':False})
    except BaseException as exc:
        first=err(exc)
    def input_tail():
        failures=[];values=[]
        for row in snapshot:
            try:values.append(fresh(row))
            except BaseException as exc:failures.append({'path':row['path'],**err(exc)})
        tail_observations['inputs']={'values':values,'errors':failures}
        need(not failures,'one or more retained input identities failed')
        return len(values)
    def supplier_tail():
        value=supplier();tail_observations['supplier']=value
        same({k:v for k,v in value.items() if k!='observed_at_unix_ns'},
             {k:v for k,v in before_supplier.items() if k!='observed_at_unix_ns'},'whole supplier post equality')
        return {'vendor':1810,'namespace':195,'tools':4,'absent':2}
    def output_tail():
        values={};failures=[]
        for name,row in artifacts.items():
            try:value=ref(D/name);values[name]=value;same(value,row,'prepared output stable')
            except BaseException as exc:failures.append({'name':name,**err(exc)})
        tail_observations['outputs']={'values':values,'errors':failures}
        need(not failures,'prepared output drift');return values
    def namespace_tail():
        names=sorted(p.name for p in D.iterdir());tail_observations['namespace']=names
        need(set(names)<=(NAMES|{'tmp','monitor'}),'unexpected owned preparation member')
        same(set(artifacts).issubset(set(names)),True,'all produced files retained')
        for name in ('tmp','monitor'):
            p=D/name
            if p.exists():
                need(p.is_dir() and not p.is_symlink(),'owned directory kind');same(sorted(x.name for x in p.iterdir()),[],'no monitor execution')
            elif first is None:need(False,'missing prepared directory '+name)
        if first is None:same(sorted(names),sorted(NAMES|{'tmp','monitor'}),'complete success namespace')
        return names
    # Each group is attempted regardless of earlier or primary failure.
    for name,check in [('inputs',input_tail),('supplier',supplier_tail),('E',etree),
                       ('authority_absences',absent_authority),('outputs',output_tail),('namespace',namespace_tail)]:
        try:tails[name]={'value':check(),'error':None}
        except BaseException as exc:
            error=err(exc);tails[name]={'value':None,'error':error}
            if first is None:first=error
    completion={'schema':'ri244-unissued-preparation-completion-v1',
         'status':'UNISSUED_PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW' if first is None else 'REFUSED_RETAIN_ALL_PARTIALS',
         'first_error':first,'independent_tails':tails,'tail_observations':tail_observations,'artifacts':dict(artifacts),
         'input_count':len(snapshot),'root_decision':decision_ref,'operational_authorization':False,
         'subject_executed':False,'installed_freeze_decoded':False,'E_written':False,'RET_paused':True}
    emit('PREPARATION_COMPLETE.json',completion)
    return 0 if first is None else 1


if __name__=='__main__':
    raise SystemExit(main())
