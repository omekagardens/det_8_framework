"""RI131 UNEXECUTED source: extra independent-validator boundary controls.

No target import, import-time I/O, science reconstruction, loader, patching,
active card or CLI. A separately reviewed root caller supplies the exact module.
Entry controls stop before any historical file can be opened. Deeper controls
call the exact unchanged boundary functions and disclose that restricted scope.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import types

CONTEXT = 'RI131_FABRICATED_GUARDS_NOT_HISTORICAL_NOT_ADMISSION'
PHASE = 'fabricated_validator_guard_qualification'
CAP = 67108864
TARGET_PIN = {'bytes': 56593, 'sha256': '59df09a5f2aac01034df3202fc27ae2500239564a8714fa4c616600e19e66def'}
FIXED_SOURCE_PINS = {
    'validator': TARGET_PIN,
    'validator_controls': {'bytes': 17909, 'sha256': '9a400bd03a2c456b2b3603354dab55f5c46be5155d1af7fc5788b7702e9aa7aa'},
    'validator_protocol': {'bytes': 14060, 'sha256': 'caefb53c7c2ac5e7898ffcea03cd5bdf5a29768fa4db9fd723fb9cc1d305a990'},
    'validator_handoff': {'bytes': 4821, 'sha256': 'a75a6d31acc4348ee80f13d6bc035a2e070f5a472ca84e417d1681cd9443a9f9'},
    'root_source_adjudication': {'bytes': 3908, 'sha256': '459885e5dc514ceb9e4c62d4810464e07d29515cf0e59744d9f12b1c1cfe6cda'},
    'nonauthor_review': {'bytes': 19331, 'sha256': 'ec88bb4a923c610d61694d82eae0dba970c66784389bb434a87c87ab7ee5a555'},
}
SOURCE_ROLES = ('validator', 'validator_controls', 'validator_protocol', 'validator_handoff',
                'root_source_adjudication', 'nonauthor_review', 'guard_source', 'guard_contract', 'guard_inventory')
INPUT_NAMES = ('capture', 'ri73_result', 'ri73_source', 'ri73_reconciliation', 'ri73_final_review', 'ri73_audit_freeze')
SCIENCE_SOURCE_NAMES = ('design', 'contract', 'primary', 'white_kernel', 'validator', 'qualifier',
                       'cases', 'kernel_refusals', 'white_refusals', 'fabricated_interfaces')
RUNTIME_NAMES = ('fingerprint', 'inventory', 'interpreter')
REGISTERED_ROLES = (tuple('input:' + x for x in INPUT_NAMES)
    + tuple('source:' + x for x in SCIENCE_SOURCE_NAMES)
    + ('design_acceptance', 'qualification', 'custody', 'admission')
    + tuple('runtime:' + x for x in RUNTIME_NAMES) + ('candidate', 'independent_output'))
LIMITS = {'seconds': 180, 'sampled_rss_kib': 524288, 'poll_ms': 25, 'max_gap_ms': 100,
          'ps_timeout_ms': 50, 'file_bytes': CAP, 'capture_row_bytes': 8388608,
          'completed_integer_bits': 262144}

ENTRY_EXPECTED = (
 ('EV01','INPUT','externally frozen request bytes'),
 ('EV02','SCHEMA','invalid bounded JSON'),
 ('EV03','SCHEMA','duplicate JSON key'),
 ('EV04','INPUT','positive bounded pin length'),
 ('EV05','INPUT','externally frozen validation binding'),
 ('EV06','SCHEMA','invalid bounded JSON'),
 ('EV07','SCHEMA','duplicate JSON key'),
 ('EV08','ADMISSION','closed object keys'),
 ('EV09','ADMISSION','closed object keys'),
 ('EV10','PHASE','actual phase before body decoding'),
 ('EV11','SOURCE','closed object keys'),
 ('EV12','SOURCE','closed object keys'),
 ('EV13','INPUT','fixed historical pin capture'),
 ('EV14','SOURCE','closed object keys'),
 ('EV15','INPUT','literal absolute nonsymlink path'),
 ('EV16','SOURCE','loaded primary path'),
 ('EV17','SOURCE','loaded kernel path'),
 ('EV18','SOURCE','loaded validator path'),
 ('EV19','SOURCE','loaded validator path'),
 ('EV20','BINDING','candidate is the primary exclusive output'),
 ('EV21','INPUT','positive bounded pin length'),
 ('EV22','OUTPUT','exclusive absent output'),
 ('EV23','INPUT','distinct validation input and output paths'),
 ('EV24','INPUT','distinct required file paths'),
)
# All these mutations reach the complete binding comparator at target line 994.
BINDING_MUTATIONS = (
 ('schema',), ('phase',), ('status',), ('primary_request','sha256'), ('candidate','pin','sha256'),
) + tuple(('sources', x, 'sha256') for x in SCIENCE_SOURCE_NAMES) + tuple(
 ('inputs', x, 'sha256') for x in INPUT_NAMES) + (
 ('qualification','sha256'), ('custody','sha256'),
) + tuple(('runtime', x, 'sha256') for x in RUNTIME_NAMES) + (
 ('history_and_runtime_adjudicated_by_root',), ('protected_validation',), ('ret_paused',),
 ('limits','seconds'), ('limits','sampled_rss_kib'), ('limits','poll_ms'),
 ('limits','max_gap_ms'), ('limits','ps_timeout_ms'),
 ('sources','__extra__'), ('runtime','__extra__'), ('inputs','__extra__'), ('qualification','bytes'),
)
COMPARATOR_EXPECTED = (
 ('CB01','INPUT','whole body pin'), ('CB02','CUSTODY','path state changed'),
 ('CB03','INPUT','literal absolute nonsymlink path'), ('CB04','INPUT','regular single-link source or input'),
 ('CB05','SCHEMA','duplicate JSON key'), ('CB06','EXACT','decimal or nonfinite JSON token'),
 ('CB07','EXACT','decimal or nonfinite JSON token'), ('CB08','SCHEMA','invalid bounded JSON'),
 ('CB09','CANONICAL','canonical actual candidate'), ('CB10','CANONICAL','canonical actual candidate'),
 ('CB11','COMPARISON','complete independently reconstructed white result'),
 ('CB12','COMPARISON','complete independently reconstructed white result'),
 ('CB13','COMPARISON','complete independently reconstructed white result'),
)

# Every named scientific/result field is covered using one symbolic row and one
# response. Lists/matrices are also mutated as complete values. Repeated actual
# rows, all cells and the full two-response actual candidate remain E2E-blocked.
FIELD_PATHS = (
 ('schema',), ('phase',), ('status',), ('method','model'),
 ('method','dimensions','r'), ('method','dimensions','N'), ('method','dimensions','L'),
 ('method','dimensions','T'), ('method','dimensions','M'), ('method','dimensions','d'),
 ('method','dimensions','raw_samples'), ('method','dimensions','fs'),
 ('method','rows'), ('method','n_order'), ('method','crop'), ('method','integer_bit_limit'),
 ('method','precision_limit'), ('method','centering'),
 ('provenance','sources'), ('provenance','inputs'), ('provenance','acceptance','design'),
 ('provenance','acceptance','qualification'), ('provenance','acceptance','custody'),
 ('provenance','acceptance','dependencies'), ('provenance','runtime'),
 ('operator','capture'), ('operator','ri73_result'), ('operator','ri73_gram_detail'), ('operator','shape'),
 ('operator','row_identities',0,'row'), ('operator','row_identities',0,'source_row_pin'),
 ('operator','row_identities',0,'short_count'), ('operator','row_identities',0,'long_count'),
 ('operator','row_identities',0,'head_pin'), ('operator','row_identities',0,'tail_pin'),
 ('operator','row_identities',0,'a_row_sum_interval'), ('operator','row_identities',0,'contains_zero'),
 ('operator','gram','G'), ('operator','gram','H'), ('operator','gram','delta'),
 ('operator','gram','inverse'), ('operator','gram','gamma'), ('operator','gram','rho'),
 ('operator','inherited_gate_inventory'), ('operator','inherited_gates_all_passed'),
 ('shift','orientation'), ('shift','center'), ('shift','error'), ('shift','direct'),
 ('shift','midpoint_polarization'), ('shift','trace_center'), ('shift','trace_error'),
 ('white_responses',0,'n'), ('white_responses',0,'a'), ('white_responses',0,'b'),
 ('white_responses',0,'center'), ('white_responses',0,'error'), ('white_responses',0,'entry_intervals'),
 ('white_responses',0,'trace_interval'), ('white_responses',0,'trace_from_g_c'),
 ('white_responses',0,'structural_trace_interval'), ('white_responses',0,'delta'),
 ('white_responses',0,'ell'), ('white_responses',0,'eps'),
 ('white_responses',0,'enclosure_state'), ('white_responses',0,'usefulness_state'),
 ('checks','inventory'), ('checks','counts','total'), ('checks','counts','passed'),
 ('checks','counts','failed'), ('checks','results',0,'id'), ('checks','results',0,'passed'), ('limitations',),
)
BLOCKED = (
 {'id':'E2E01','reason':'Full validate_saved_white traversal through fixed actual RI73 result and complete capture requires genuine prior primary execution, original historical custody and separate root admission.'},
 {'id':'E2E02','reason':'Mutated full actual candidate at the primary request output cannot be substituted into immutable accepted evidence or justified by a fabricated admission. Direct comparator controls are not this coverage.'},
 {'id':'E2E03','reason':'Whole-entry output-write interruption and source/runtime mutation during a genuine actual numerical reconstruction require a separately reviewed caller/fault boundary and authentic inputs. Direct writer/read-set controls are not this coverage.'},
 {'id':'E2E04','reason':'Capture-load-source identity, runtime closure, watchdog, genuine process completion and normal-before-optimized qualification belong to a separate reviewed root caller; this module launches nothing.'},
)


class GuardError(ValueError):
    pass


def require(ok, text):
    if not ok: raise GuardError(text)


def same(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys() == b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def identity(body):
    require(type(body) is bytes and len(body)<=CAP,'bounded opaque body')
    return {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}


def canonical(value):
    data=(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
    require(len(data)<=CAP,'bounded guard artifact')
    return data


def stamp(s):
    return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode,s.st_nlink)


def literal(value):
    require(type(value) is str,'literal path string')
    p=Path(value)
    require(p.is_absolute() and str(p)==value and p==p.resolve(),'absolute nonsymlink path')
    return p


def opaque(path, *, single=True):
    s=path.lstat()
    require(stat.S_ISREG(s.st_mode) and (not single or s.st_nlink==1) and 0<=s.st_size<=CAP,'bounded regular file')
    h=hashlib.sha256(); count=0
    with os.fdopen(os.open(path,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        require(stamp(os.fstat(f.fileno()))==stamp(s),'opened file identity')
        while True:
            chunk=f.read(65536)
            if not chunk: break
            count+=len(chunk); require(count<=CAP,'opaque byte bound'); h.update(chunk)
        require(stamp(os.fstat(f.fileno()))==stamp(s),'final descriptor identity')
    require(stamp(path.lstat())==stamp(s),'final path identity')
    return {'bytes':count,'sha256':h.hexdigest()},stamp(s)


def put(path, body):
    require(type(body) is bytes and len(body)<=CAP,'bounded write body')
    with os.fdopen(os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600),'wb') as f:
        require(f.write(body)==len(body),'complete guard write'); f.flush(); os.fsync(f.fileno())
    pin,_=opaque(path); require(same(pin,identity(body)),'complete saved guard bytes')
    return {'path':str(path),'pin':pin}


def captured_metadata(ref, initial):
    path=literal(ref['path']); before=path.lstat()
    require(stamp(before)==initial,'metadata source still at initial state')
    with os.fdopen(os.open(path,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        require(stamp(os.fstat(f.fileno()))==initial,'metadata descriptor identity')
        body=f.read(CAP+1)
        require(stamp(os.fstat(f.fileno()))==initial,'metadata final descriptor identity')
    require(stamp(path.lstat())==initial and same(identity(body),ref['pin']),'captured metadata complete identity')
    return json.loads(body)


def altered(value):
    if type(value) is bool: return not value
    if type(value) is int: return value+1
    if type(value) is str: return value+'__RI131_MUTATED__'
    if type(value) is list: return value+[{'ri131_extra':True}]
    if type(value) is dict: return {**value,'__ri131_extra__':True}
    if value is None: return False
    raise GuardError('fixed mutation type')


def set_altered(value, path):
    holder=value
    for key in path[:-1]: holder=holder[key]
    leaf=path[-1]
    holder[leaf]=True if leaf=='__extra__' else altered(holder[leaf])


def scaffold(V, directory):
    """UNADMITTED in-memory metadata. Referenced historical files do not exist.

    Literal historical pins are normative identifiers, not fabricated file pins.
    No body with those pins is created. This can never pass its first input read.
    """
    def ref(name,pin=None):
        return {'path':str(directory/('NEVER_OPEN_'+name)),
                'pin':dict(pin or {'bytes':1,'sha256':'0'*64})}
    selection={'primary':str(directory/'NEVER_OPEN_primary.py'),
               'white_kernel':str(directory/'NEVER_OPEN_kernel.py'),
               'validator':str(Path(V.__file__).resolve())}
    request={'schema':'ri125-white-request-v1','phase':'fixed_saved_application',
        'inputs':{x:ref(x,V.FIXED[x]) for x in INPUT_NAMES},
        'sources':{x:ref('source-'+x,V.DESIGN if x=='design' else None) for x in SCIENCE_SOURCE_NAMES},
        'design_acceptance':ref('design-acceptance',V.DESIGN_ACCEPTANCE),
        'qualification':ref('qualification'),'custody':ref('custody'),'admission':ref('admission'),
        'runtime':{x:ref('runtime-'+x) for x in RUNTIME_NAMES},
        'output':str(directory/'NEVER_OPEN_primary-output.json')}
    for key,path in selection.items(): request['sources'][key]['path']=path
    candidate={'path':request['output'],'pin':{'bytes':1,'sha256':'0'*64}}
    return request,selection,candidate


def binding_for(V, request, selection, candidate, request_pin, directory):
    # Never written as a standalone card; only a marked guard-envelope operand.
    return {'schema':'ri125-white-independent-validation-admission-v1',
        'phase':'fixed_saved_application','status':'ROOT_ADMITS_ONE_WHITE_VALIDATION',
        'primary_request':request_pin,'candidate':copy.deepcopy(candidate),
        'sources':{x:copy.deepcopy(request['sources'][x]['pin']) for x in SCIENCE_SOURCE_NAMES},
        'inputs':{x:copy.deepcopy(request['inputs'][x]['pin']) for x in INPUT_NAMES},
        'qualification':copy.deepcopy(request['qualification']['pin']),
        'custody':copy.deepcopy(request['custody']['pin']),
        'runtime':{x:copy.deepcopy(request['runtime'][x]['pin']) for x in RUNTIME_NAMES},
        'selection':copy.deepcopy(selection),'output':str(directory/'NEVER_CREATE_actual-validation.json'),
        'limits':dict(V.LIMITS),'history_and_runtime_adjudicated_by_root':True,
        'protected_validation':False,'ret_paused':True}


def entry_case(V, directory, identifier, binding_path=None):
    request,selection,candidate=scaffold(V,directory)
    if identifier=='EV10': request['phase']='fabricated_qualification'
    elif identifier=='EV11': request['sources'].pop('validator')
    elif identifier=='EV12': request['runtime'].pop('inventory')
    elif identifier=='EV13': request['inputs']['capture']['pin']['sha256']='0'*64
    elif identifier=='EV24': request['sources']['contract']['path']=request['sources']['cases']['path']
    # Construct binding from a complete BASE map so malformed role maps reach
    # target validation rather than failing in this control's setup.
    base_request,base_selection,base_candidate=scaffold(V,directory)
    raw=canonical(request); request_pin=identity(raw)
    binding=binding_for(V,base_request,base_selection,base_candidate,request_pin,directory)
    if identifier=='EV14': binding['selection'].pop('primary')
    elif identifier=='EV15': binding['selection']['primary']='relative'
    elif identifier=='EV16': binding['selection']['primary']=str(directory/'NEVER_OPEN_other-primary.py')
    elif identifier=='EV17': binding['selection']['white_kernel']=str(directory/'NEVER_OPEN_other-kernel.py')
    elif identifier=='EV18': binding['selection']['validator']=str(directory/'NEVER_OPEN_other-validator.py')
    elif identifier=='EV19':
        wrong=str(directory/'NEVER_OPEN_other-validator.py')
        request['sources']['validator']['path']=wrong; binding['selection']['validator']=wrong
        raw=canonical(request); request_pin=identity(raw); binding['primary_request']=request_pin
    elif identifier=='EV20': candidate['path']=str(directory/'NEVER_OPEN_other-candidate.json')
    elif identifier=='EV21': candidate['pin']['bytes']=True
    elif identifier=='EV22': put(Path(binding['output']),b'RI131_OWNED_OCCUPIED_OUTPUT\n')
    elif identifier=='EV23': binding['output']=request['inputs']['capture']['path']
    if identifier=='EV01': request_pin={'bytes':len(raw)+1,'sha256':'0'*64}
    elif identifier=='EV02': raw=b'{'; request_pin=identity(raw)
    elif identifier=='EV03': raw=b'{"a":1,"a":1}'; request_pin=identity(raw)
    if identifier=='EV08': binding.pop('status')
    elif identifier=='EV09': binding['extra']=None
    if binding_path is not None: set_altered(binding,binding_path)
    binding_body=canonical(binding); binding_pin=identity(binding_body)
    if identifier=='EV04': binding_pin['bytes']=True
    elif identifier=='EV05': binding_pin={'bytes':len(binding_body)+1,'sha256':'0'*64}
    elif identifier=='EV06': binding_body=b'{'; binding_pin=identity(binding_body)
    elif identifier=='EV07': binding_body=b'{"a":1,"a":1}'; binding_pin=identity(binding_body)
    operand={'schema':'ri131-unadmitted-entry-guard-operands-v1','context':CONTEXT,
        'never_an_admission':True,'request_ascii':raw.decode('ascii'),'request_pin':request_pin,
        'candidate_reference':candidate,'binding_ascii':binding_body.decode('ascii'),'binding_pin':binding_pin,
        'mutation_id':identifier,'mutation_path':list(binding_path) if binding_path is not None else None}
    put(directory/'OPERAND.fabricated.json',canonical(operand))
    result=V.validate_saved_white(raw,request_pin,candidate,binding_body,binding_pin)
    require(type(result) is dict and set(result)=={'result','output_pin','refusal','postchecks'},'complete entry envelope')
    require(result['result'] is None and result['output_pin'] is None and result['postchecks']==[],
            'entry guard stops before registration or scientific file access')
    refusal=result['refusal']
    require(type(refusal) is dict and set(refusal)=={'schema','status','phase','stage','code','message','scientific_disposition_emitted','postchecks'},'closed refused entry')
    require(refusal['schema']=='ri125-application-refusal-v1' and refusal['status']=='REFUSED'
        and refusal['phase']=='fixed_saved_application' and refusal['stage']=='white'
        and refusal['scientific_disposition_emitted'] is False and refusal['postchecks']==[], 'no scientific entry disposition')
    if identifier=='EV22':
        require(Path(binding['output']).read_bytes()==b'RI131_OWNED_OCCUPIED_OUTPUT\n','occupied output preserved')
    else: require(not os.path.lexists(binding.get('output','')),'no actual output created')
    for name in INPUT_NAMES: require(not os.path.lexists(base_request['inputs'][name]['path']),'no fabricated historical file created')
    prefix='Refusal: '+refusal['code']+': '
    require(type(refusal['message']) is str and refusal['message'].startswith(prefix),'exact entry refusal prefix')
    return refusal['code'],refusal['message'][len(prefix):],result


def symbolic_tree():
    """Shape-only, deliberately invalid as any historical/scientific candidate.

    The extra outer context and schema prevent this metadata from being confused
    with WHITE_COUPLING. Values are symbols, never Gram/response coefficients.
    """
    def symbol(label): return {'ri131_symbol':label}
    row={'row':'ROW_SYMBOL','source_row_pin':symbol('source-row'),'short_count':1,'long_count':1,
        'head_pin':symbol('head'),'tail_pin':symbol('tail'),'a_row_sum_interval':['LOW_SYMBOL','HIGH_SYMBOL'],
        'contains_zero':False}
    response={name:symbol(name) for name in ('a','b','center','error','entry_intervals','trace_interval',
        'trace_from_g_c','structural_trace_interval','delta','ell','eps')}
    response.update(n=1,enclosure_state='ENCLOSURE_SYMBOL',usefulness_state='USEFULNESS_SYMBOL')
    data={'schema':'SYMBOLIC_WHITE_NOT_RESULT','phase':'fabricated_symbolic_guard', 'status':'SYMBOLIC_ONLY',
        'method':{'model':'MODEL_SYMBOL','dimensions':{name:1 for name in ('r','N','L','T','M','d','raw_samples','fs')},
            'rows':['ROW_SYMBOL'],'n_order':[1],'crop':'CROP_SYMBOL','integer_bit_limit':1,
            'precision_limit':symbol('precision'),'centering':'CENTERING_SYMBOL'},
        'provenance':{'sources':symbol('sources'),'inputs':[symbol('input')],
            'acceptance':{'design':symbol('design'),'qualification':symbol('qualification'),
                'custody':symbol('custody'),'dependencies':[symbol('dependency')]},'runtime':symbol('runtime')},
        'operator':{'capture':symbol('capture'),'ri73_result':symbol('result'),'ri73_gram_detail':symbol('detail'),
            'shape':[1,1],'row_identities':[row],'gram':{name:symbol(name) for name in ('G','H','delta','inverse','gamma','rho')},
            'inherited_gate_inventory':['GATE_SYMBOL'],'inherited_gates_all_passed':False},
        'shift':{name:symbol(name) for name in ('orientation','center','error','direct','midpoint_polarization','trace_center','trace_error')},
        'white_responses':[response],'checks':{'inventory':['CHECK_SYMBOL'],'counts':{'total':1,'passed':0,'failed':1},
            'results':[{'id':'CHECK_SYMBOL','passed':False}]},'limitations':['SYMBOLIC_ONLY_NOT_SCIENCE']}
    return {'schema':'ri131-symbolic-field-tree-v1','context':CONTEXT,'data':data}


def candidate_boundary(V, directory, identifier):
    base={'schema':'ri131-minimal-metadata-v1','context':CONTEXT,'count':1,'flags':[False,True]}
    encoded=canonical(base)
    if identifier in ('CB01','CB02','CB03','CB04'):
        ref=put(directory/'CANDIDATE.fabricated.json',encoded)
        put(directory/'INITIAL_REFERENCE.fabricated.json',canonical({'context':CONTEXT,'reference':copy.deepcopy(ref),'original_ascii':encoded.decode('ascii')}))
        if identifier=='CB01': ref['pin']['sha256']='0'*64
        elif identifier=='CB02':
            _,before=V.inspect_file(ref)
            Path(ref['path']).write_bytes(b'RI131_CHANGED_OWNED_CANDIDATE\n')
            return V.inspect_file(ref,remember=before)
        elif identifier=='CB03':
            link=directory/'CANDIDATE_SYMLINK.fabricated'; link.symlink_to(ref['path']); ref['path']=str(link)
        elif identifier=='CB04': os.link(ref['path'],directory/'CANDIDATE_HARDLINK.fabricated')
        return V.inspect_file(ref)
    if identifier in ('CB05','CB06','CB07','CB08'):
        raw={'CB05':b'{"x":1,"x":1}','CB06':b'{"x":0.5}','CB07':b'{"x":NaN}','CB08':b'{'}[identifier]
        put(directory/'CANDIDATE.fabricated.json',raw)
        return V.parse_json(raw)
    if identifier in ('CB09','CB10'):
        raw=(encoded+b' ' if identifier=='CB09' else b'{"b":2,"a":1}')
        put(directory/'CANDIDATE.fabricated.json',raw)
        parsed=V.parse_json(raw)
        return V.match(V.serialize(parsed),raw,'CANONICAL','canonical actual candidate')
    changed=copy.deepcopy(base)
    if identifier=='CB11': changed['extra']=None
    elif identifier=='CB12': changed.pop('count')
    elif identifier=='CB13': changed['count']=True
    put(directory/'CANDIDATE.fabricated.json',canonical(changed))
    put(directory/'REFERENCE.fabricated.json',encoded)
    return V.match(changed,base,'COMPARISON','complete independently reconstructed white result')


def field_boundary(V, directory, path):
    reference=symbolic_tree(); candidate=copy.deepcopy(reference)
    set_altered(candidate['data'],path)
    put(directory/'REFERENCE.fabricated.json',canonical(reference))
    put(directory/'CANDIDATE.fabricated.json',canonical(candidate))
    put(directory/'MUTATION.fabricated.json',canonical({'schema':'ri131-symbolic-field-mutation-v1',
        'context':CONTEXT,'path':['data']+list(path),'whole_entry_coverage':False}))
    return V.match(candidate,reference,'COMPARISON','complete independently reconstructed white result')


def normalized_exception(V, action):
    try:
        returned=action()
    except V.Refusal as exc:
        return {'code':exc.code,'message':exc.message,'unexpected':False,'returned':None}
    except Exception as exc:
        return {'code':type(exc).__name__,'message':str(exc)[:1024],'unexpected':True,'returned':None}
    return {'code':None,'message':None,'unexpected':False,'returned':returned}


def writer_boundary(V, directory, identifier):
    value={'schema':'ri131-owned-writer-value-v1','context':CONTEXT,'actual_science':False}
    output=directory/'OUTPUT.fabricated.json'
    if identifier=='OW01':
        original=b'RI131_PRESERVE_EXISTING_OUTPUT\n'; put(output,original)
        observed=normalized_exception(V,lambda:V.write_new_output(str(output),value))
        require(output.read_bytes()==original,'exclusive refusal preserves occupied output')
        return observed
    if identifier=='OW02':
        original=b'RI131_PRESERVE_SYMLINK_TARGET\n'; target=directory/'LINK_TARGET.fabricated'; put(target,original)
        output.symlink_to(target)
        observed=normalized_exception(V,lambda:V.write_new_output(str(output),value))
        require(target.read_bytes()==original and output.is_symlink(),'symlink refusal preserves both objects')
        return observed
    if identifier=='OW03':
        result=V.write_new_output(str(output),value)
        require(same(result,identity(canonical(value))) and output.read_bytes()==canonical(value),'positive writer full bytes and pin')
        return {'code':None,'message':None,'unexpected':False,'returned':{'pin':result,'canonical_complete':True}}
    if identifier=='OW04':
        observed=normalized_exception(V,lambda:V.write_new_output(str(output),{'oversize':'x'*CAP}))
        require(output.is_file() and output.read_bytes()==b'{\n  "oversize": ','exact retained partial prefix')
        require(observed['returned'] is None,'partial file has no returned accepted pin')
        return observed
    raise GuardError('fixed writer boundary')


def tail_boundary(V, directory, changed_index, initial_failure):
    refs=[]; readset=V.ReadSet()
    for i,role in enumerate(REGISTERED_ROLES):
        ref=put(directory/(f'{i:02d}_ROLE.fabricated'),('RI131_METADATA_ROLE_'+role+'\n').encode('ascii'))
        refs.append(ref); readset.add(role,ref)
    changed=refs[changed_index]; earlier=None
    put(directory/'INITIAL_REFERENCES.fabricated.json',canonical({'schema':'ri131-owned-role-inputs-v1',
        'context':CONTEXT,'roles':list(REGISTERED_ROLES),'references':refs,'changed_index':changed_index,
        'body_recipe':'ASCII RI131_METADATA_ROLE_ + literal role + newline','initial_failure':initial_failure}))
    if initial_failure:
        Path(changed['path']).write_bytes(b'RI131_CHANGED_BEFORE_INITIAL_READ\n')
        observed=normalized_exception(V,readset.begin)
        require(observed['code']=='INPUT' and observed['message']=='whole body pin','intended initial read pin failure')
        earlier=V.Refusal('INPUT','whole body pin')
    else:
        readset.begin()
        Path(changed['path']).write_bytes(b'RI131_CHANGED_AFTER_INITIAL_READ\n')
        earlier=V.Refusal('COMPARISON','complete independently reconstructed white result')
    postchecks=readset.final()
    require(type(postchecks) is list and len(postchecks)==25,'every registered final check attempted')
    require([x['role'] for x in postchecks]==list(REGISTERED_ROLES),'exact final role order')
    for i,(ref,record) in enumerate(zip(refs,postchecks)):
        require(type(record) is dict and set(record)=={'role','pin','unchanged','error'},'closed postcheck record')
        passed=(i<changed_index if initial_failure else i!=changed_index)
        require(record['unchanged'] is passed,'all expected initial/final custody outcomes')
        if passed:
            require(same(record['pin'],ref['pin']) and record['error'] is None,'complete successful role identity')
        else:
            message=('whole body pin' if i==changed_index and initial_failure else
                     'initial custody incomplete' if initial_failure else 'path state changed')
            code='INPUT' if i==changed_index and initial_failure else 'CUSTODY'
            require(record['pin'] is None and record['error']=='Refusal: '+code+': '+message,
                    'exact failed role diagnostic')
    prior=V.finish_validation(earlier,{'ri131_apparent_result':True},None,postchecks)
    late=V.finish_validation(None,{'ri131_apparent_result':True},None,postchecks)
    # A completed output pin may survive a subsequent refusal only as evidence.
    # This is a directly tested tail contract, not an actual accepted output.
    retained_pin=refs[-1]['pin']
    prior_with_pin=V.finish_validation(earlier,{'ri131_apparent_result':True},retained_pin,postchecks)
    late_with_pin=V.finish_validation(None,{'ri131_apparent_result':True},retained_pin,postchecks)
    for envelope,code,message,pin in ((prior,earlier.code,earlier.message,None),
            (late,'CUSTODY','one or more final source/input postchecks failed',None),
            (prior_with_pin,earlier.code,earlier.message,retained_pin),
            (late_with_pin,'CUSTODY','one or more final source/input postchecks failed',retained_pin)):
        require(type(envelope) is dict and set(envelope)=={'result','output_pin','refusal','postchecks'},'closed tail envelope')
        require(envelope['result'] is None and same(envelope['output_pin'],pin) and same(envelope['postchecks'],postchecks),'no accepted tail result')
        refusal=envelope['refusal']
        require(type(refusal) is dict and set(refusal)=={'schema','status','phase','stage','code','message','scientific_disposition_emitted','postchecks'},'closed tail refusal')
        require(refusal['schema']=='ri125-application-refusal-v1' and refusal['status']=='REFUSED'
            and refusal['phase']=='fixed_saved_application' and refusal['stage']=='white'
            and refusal['code']==code and refusal['message']=='Refusal: '+code+': '+message
            and refusal['scientific_disposition_emitted'] is False and same(refusal['postchecks'],postchecks),'exact first and late error semantics')
    return {'changed_role':REGISTERED_ROLES[changed_index],'initial_references':refs,'initial_failure':initial_failure,
            'postchecks':postchecks,'earlier_failure_result':prior,'late_failure_result':late,
            'earlier_failure_with_retained_pin':prior_with_pin,'late_failure_with_retained_pin':late_with_pin,
            'whole_entry_coverage':False}


def declarations():
    result=[{'id':identifier,'mechanism':'unchanged_entry_metadata_refusal','expected_code':code,'expected_message':message,
             'mutation_path':None} for identifier,code,message in ENTRY_EXPECTED]
    result.extend({'id':f'EB{i:02d}','mechanism':'unchanged_entry_metadata_refusal',
        'expected_code':'ADMISSION','expected_message':'exact independent root-bound validation card',
        'mutation_path':list(path)} for i,path in enumerate(BINDING_MUTATIONS,1))
    result.extend({'id':identifier,'mechanism':'direct_candidate_boundary','expected_code':code,
        'expected_message':message,'mutation_path':None} for identifier,code,message in COMPARATOR_EXPECTED)
    result.extend({'id':f'CF{i:02d}','mechanism':'direct_symbolic_full_field_comparator',
        'expected_code':'COMPARISON','expected_message':'complete independently reconstructed white result',
        'mutation_path':['data']+list(path)} for i,path in enumerate(FIELD_PATHS,1))
    result.extend({'id':identifier,'mechanism':'direct_writer_boundary','expected_code':code,'expected_message':message,'mutation_path':None}
        for identifier,code,message in (('OW01','OUTPUT','output absent before exclusive open'),
            ('OW02','INPUT','literal absolute nonsymlink path'),('OW03',None,None),('OW04','RESOURCE','serialized byte ceiling')))
    for kind in ('TF','TB'):
        result.extend({'id':f'{kind}{i+1:02d}','mechanism':'direct_complete_readset_and_tail',
            'expected_code':None,'expected_message':None,'mutation_path':[role]} for i,role in enumerate(REGISTERED_ROLES))
    return result


def inventory_tree(root):
    records=[]; states={}
    def visit(path,depth):
        require(depth<=4 and len(records)<4096,'bounded owned evidence inventory')
        s=path.lstat(); name=str(path.relative_to(root))
        states[name]=list(stamp(s))
        if stat.S_ISDIR(s.st_mode):
            records.append({'name':name,'kind':'directory','pin':None,'target':None})
            with os.scandir(path) as entries: names=sorted(x.name for x in entries)
            for child in names: visit(path/child,depth+1)
        elif stat.S_ISLNK(s.st_mode):
            target=os.readlink(path);require(len(target)<=4096,'bounded link target')
            records.append({'name':name,'kind':'symlink','pin':None,'target':target})
        else:
            value,_=opaque(path,single=False)
            records.append({'name':name,'kind':'file','pin':value,'target':None})
        require(stamp(path.lstat())==stamp(s),'owned inventory entry stable')
    visit(root,0)
    return {'schema':'ri131-complete-owned-evidence-inventory-v1','records':records,'states':states}


def run_guard_controls(directory, validator, source_bindings, *, phase):
    """One future root-admitted finite guard attempt. No fallback or cleanup."""
    root=None; created=False; first=None; report=None; output_pin=None; records=[]; source_states=[]
    stable_files=[]; frozen_trees=[]; first_failed_id=None
    def retain(ref):
        pin,before=opaque(Path(ref['path']));require(same(pin,ref['pin']),'initial stable artifact pin')
        stable_files.append({'reference':ref,'initial':before})
        return ref
    try:
        require(phase==PHASE,'explicit RI131 fabricated guard phase')
        require(type(validator) is types.ModuleType,'root-loaded exact validator module')
        require(type(source_bindings) is dict and set(source_bindings)==set(SOURCE_ROLES),'closed guard source roles')
        require(same(source_bindings['validator']['pin'],TARGET_PIN),'unchanged accepted validator target')
        require(str(Path(validator.__file__).resolve())==source_bindings['validator']['path'],'loaded validator path')
        require(str(Path(__file__).resolve())==source_bindings['guard_source']['path'],'loaded guard source path')
        require(len({r['path'] for r in source_bindings.values()})==len(SOURCE_ROLES),'distinct source paths')
        for role in SOURCE_ROLES:
            ref=source_bindings[role];require(type(ref) is dict and set(ref)=={'path','pin'},'closed source reference')
            p=ref['pin'];require(type(p) is dict and set(p)=={'bytes','sha256'}
                and type(p['bytes']) is int and 0<p['bytes']<=CAP and type(p['sha256']) is str
                and len(p['sha256'])==64 and all(c in '0123456789abcdef' for c in p['sha256']),'positive exact source pin')
            if role in FIXED_SOURCE_PINS: require(same(p,FIXED_SOURCE_PINS[role]),'fixed source dependency '+role)
            path=literal(ref['path']); source_states.append({'role':role,'reference':ref,'initial':None})
        for row in source_states:
            observed,initial=opaque(Path(row['reference']['path']))
            require(same(observed,row['reference']['pin']),'whole source identity')
            row['initial']=initial
        root=literal(directory)
        require(root.parent.is_dir() and not os.path.lexists(root),'fresh absent guard output directory')
        require(not any(Path(r['path']).is_relative_to(root) for r in source_bindings.values()),'sources outside owned outputs')
        root.mkdir(mode=0o700);created=True
        expected_inventory={'schema':'ri131-source-control-inventory-v1','phase':'source_specification_only',
            'controls':declarations(),'blocked_end_to_end':list(BLOCKED)}
        inventory_state=next(row['initial'] for row in source_states if row['role']=='guard_inventory')
        supplied=captured_metadata(source_bindings['guard_inventory'],inventory_state)
        require(same(supplied,expected_inventory),'exact full declared control inventory')
        for decl in declarations():
            identifier=decl['id']; work=root/identifier;work.mkdir(mode=0o700)
            try:
                if identifier.startswith(('EV','EB')):
                    code,message,diagnostic=entry_case(validator,work,identifier,
                        tuple(decl['mutation_path']) if identifier.startswith('EB') else None)
                    observed={'code':code,'message':message,'unexpected':False,'returned':diagnostic}
                elif identifier.startswith('CB'):
                    observed=normalized_exception(validator,lambda:candidate_boundary(validator,work,identifier))
                elif identifier.startswith('CF'):
                    observed=normalized_exception(validator,lambda:field_boundary(validator,work,tuple(decl['mutation_path'][1:])))
                elif identifier.startswith('OW'):
                    observed=writer_boundary(validator,work,identifier)
                else:
                    index=int(identifier[2:])-1
                    detail=tail_boundary(validator,work,index,identifier.startswith('TB'))
                    observed={'code':None,'message':None,'unexpected':False,'returned':detail}
                passed=(observed['unexpected'] is False and observed['code']==decl['expected_code']
                        and observed['message']==decl['expected_message'])
            except Exception as exc:
                observed={'code':type(exc).__name__,'message':str(exc)[:1024],'unexpected':True,'returned':None};passed=False
            if not passed and first_failed_id is None:first_failed_id=identifier
            case={'schema':'ri131-validator-guard-case-v1','context':CONTEXT,'declaration':decl,
                  'observed':observed,'passed':passed,'actual_scientific_input_opened':False,
                  'actual_validation_admitted':False,'complete_actual_entry_qualified':False}
            saved=retain(put(work/'CASE_RESULT.fabricated.json',canonical(case)))
            tree=inventory_tree(work)
            frozen_trees.append({'id':identifier,'value':tree})
            tree_ref=retain(put(root/(identifier+'_TREE.fabricated.json'),canonical(tree)))
            records.append({'id':identifier,'passed':passed,'case_result':saved,'tree':tree_ref})
        count=sum(x['passed'] for x in records)
        report={'schema':'ri131-fabricated-validator-guards-v1','phase':PHASE,'context':CONTEXT,
            'status':'all_declared_boundary_controls_passed' if count==len(records) else 'boundary_control_failure',
            'source_bindings':source_bindings,'limits':dict(LIMITS),'controls':records,
            'counts':{'total':len(records),'passed':count,'failed':len(records)-count},
            'blocked_end_to_end':list(BLOCKED),'all_actual_guard_coverage_complete':False,
            'white15_qualification_satisfied':False,'full32_qualification_satisfied':False,
            'actual_validation_admitted':False,'physical_claim':False,'ret_paused':True}
        output_pin=retain(put(root/'GUARD_REPORT.fabricated.json',canonical(report)))['pin']
        require(count==len(records),'first failed declared boundary control: '+str(first_failed_id))
    except Exception as exc:
        first=exc
    postchecks=[]
    for row in source_states:
        try:
            value,current=opaque(Path(row['reference']['path']))
            require(row['initial'] is not None and current==row['initial'] and same(value,row['reference']['pin']),'final source custody')
            postchecks.append({'role':row['role'],'unchanged':True,'pin':value,'error':None})
        except Exception as exc:
            postchecks.append({'role':row['role'],'unchanged':False,'pin':None,'error':(type(exc).__name__+': '+str(exc))[:1024]})
            if first is None:first=exc
    artifact_postchecks=[]
    for row in stable_files:
        ref=row['reference']
        try:
            pin,current=opaque(Path(ref['path']))
            require(current==row['initial'] and same(pin,ref['pin']),'stable saved artifact custody')
            artifact_postchecks.append({'path':ref['path'],'unchanged':True,'pin':pin,'error':None})
        except Exception as exc:
            artifact_postchecks.append({'path':ref['path'],'unchanged':False,'pin':None,'error':(type(exc).__name__+': '+str(exc))[:1024]})
            if first is None:first=exc
    tree_postchecks=[]
    for tree in frozen_trees:
        try:
            require(same(inventory_tree(root/tree['id']),tree['value']),'complete case tree stable')
            tree_postchecks.append({'id':tree['id'],'unchanged':True,'error':None})
        except Exception as exc:
            tree_postchecks.append({'id':tree['id'],'unchanged':False,'error':(type(exc).__name__+': '+str(exc))[:1024]})
            if first is None:first=exc
    namespace={'inventory':None,'error':None}
    if created:
        try:
            namespace['inventory']=inventory_tree(root)
            # If the source completed its declared writes, every top-level
            # member must be accounted for. Failed partial attempts retain the
            # inventory without asserting a completed namespace shape.
            if first is None:
                expected_names={'GUARD_REPORT.fabricated.json'}
                expected_names.update(row['id'] for row in records)
                expected_names.update(row['id']+'_TREE.fabricated.json' for row in records)
                actual_names={row['name'] for row in namespace['inventory']['records']
                              if row['name']!='.' and '/' not in row['name']}
                require(actual_names==expected_names,'complete top-level guard namespace')
                indexed={row['name']:row for row in namespace['inventory']['records']}
                for item in stable_files:
                    ref=item['reference']; name=str(Path(ref['path']).relative_to(root))
                    require(indexed[name]['kind']=='file' and same(indexed[name]['pin'],ref['pin'])
                        and same(namespace['inventory']['states'][name],list(item['initial'])),
                        'final namespace confirms saved artifact identity')
        except Exception as exc:
            namespace['error']=(type(exc).__name__+': '+str(exc))[:1024]
            if first is None:first=exc
    return {'report':report if first is None else None,'output_pin':output_pin,'completed_case_records':records,
        'source_postchecks':postchecks,'artifact_postchecks':artifact_postchecks,'tree_postchecks':tree_postchecks,'namespace':namespace,
        'refusal':None if first is None else {'schema':'ri131-guard-attempt-refusal-v1','status':'REFUSED',
            'phase':PHASE,'message':(type(first).__name__+': '+str(first))[:1024],
            'actual_validation_admitted':False,'accepted_scientific_disposition':False}}
