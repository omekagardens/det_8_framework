"""UNEXECUTED independent RI125 white controls.

Only the independently authored white_validator is imported. The future runner
creates visibly fabricated files in a caller-supplied absent external directory.
No primary module or actual scientific input is read. These are declarations,
not qualification evidence, until separately reviewed and actually executed.
"""
import copy
import io
import os
from pathlib import Path
import white_validator as V

CONTEXT = V.CONTEXT
# Normative first-refusal observations, not primary computed result dictionaries.
KERNEL_EXPECTED = (
 ('SHAPE','strip rows list'), ('DOMAIN','fixed primitive domain'), ('DOMAIN','fixed primitive domain'),
 ('SCHEMA','closed object keys'), ('ROW','row order'), ('SHAPE','exact list length'),
 ('SHAPE','exact list length'), ('EXACT','hex string required'), ('EXACT','canonical signed hex'),
 ('EXACT','canonical signed hex'), ('EXACT','reduced positive denominator'), ('EXACT','reduced positive denominator'),
 ('RESOURCE','integer text ceiling'), ('RESOURCE','integer bit ceiling'), ('INTERVAL','ordered endpoints'),
 ('ORIENTATION','directed shift label'), ('SCHEMA','closed object keys'), ('SHAPE','fixed matrix size'),
 ('BOUND','nonnegative shift radius'), ('POLARIZATION','saved polarization'), ('DIRECT','saved direct enclosure intersection'),
 ('TRACE','complete shift trace'), ('DOMAIN','fixed window count'), ('SCHEMA','closed object keys'),
 ('GRAM','both inverse products'), ('GRAM','symmetric Gram/inverse and nonnegative bound'), ('GRAM','both inverse products'),
 ('GRAM','both inverse products'), ('GRAM','delta row-sum bound'), ('GRAM','gamma inverse row-sum bound'),
 ('GRAM','unchanged inherited rho gate'), ('GRAM','unchanged inherited rho gate'),
 ('BOUND','nonnegative error, positive lower bound'), ('BOUND','nonnegative error, positive lower bound'),
 ('ZERO_DIVISOR','division by zero'), ('RESOURCE','integer bit ceiling'),
 ('GRAM','nonpositive inherited Gram pivot'), ('STRUCTURAL','trace structural interval intersection'))


def kernel_call(index):
    fixture = V.expected_fixture(V.WHITE_CASES[2] if index == 25 else V.WHITE_CASES[0])
    strips, gram = copy.deepcopy(fixture['strips']), copy.deepcopy(fixture['gram'])
    shift = V.build_shift(strips,length=3,stride=2)
    if index <= 15:
        length, stride = 3, 2
        if index == 1: strips = tuple(strips)
        elif index == 2: length = True
        elif index == 3: strips = [copy.deepcopy(strips[0]) for _ in range(3)]
        elif index == 4: strips[0]['extra'] = None
        elif index == 5: strips[0]['row'] = True
        elif index == 6: strips[0]['head'] = []
        elif index == 7: strips[0]['head'][0][0] = True
        elif index == 8: strips[0]['head'][0][0][0] = True
        elif index == 9: strips[0]['head'][0][0][0] = ''
        elif index == 10: strips[0]['head'][0][0][0] = '01'
        elif index == 11: strips[0]['head'][0][0][1] = '0'
        elif index == 12: strips[0]['head'][0][0] = ['2','2']
        elif index == 13: strips[0]['head'][0][0][0] = '1' + '0'*65537
        elif index == 14: strips[0]['head'][0][0][0] = '1' + '0'*65536
        elif index == 15: strips[0]['head'][0] = [V.scalar(V.Q(2)),V.scalar(V.Q(1))]
        return V.build_shift(strips,length=length,stride=stride)
    if index == 33: return V.usefulness(V.ZERO,V.ZERO)
    if index == 34: return V.usefulness(V.Q(-1),V.ONE)
    if index == 35: return V.quotient(V.ONE,V.ZERO)
    if index == 36: return V.times(V.Q(1 << 262143),V.Q(4))
    n = 2
    if index == 16: shift['orientation'] = 'head_times_tail_transpose'
    elif index == 17: shift['extra'] = None
    elif index == 18: shift['center'] = []
    elif index == 19: shift['error'][0][0] = V.scalar(V.Q(-1))
    elif index == 20: shift['midpoint_polarization'][0][0] = V.scalar(V.ZERO)
    elif index == 21: shift['direct'][0][0] = V.interval(V.Q(3),V.Q(4))
    elif index == 22: shift['trace_center'] = V.scalar(V.ZERO)
    elif index == 23: n = True
    elif index == 24: gram['H_G'] = gram.pop('H')
    elif index == 25: gram['G'][0][1] = V.scalar(V.Q(2))
    elif index == 26: gram['H'][0][0] = V.scalar(V.Q(-1))
    elif index == 27: gram['inverse'][0][0] = V.scalar(V.ONE)
    elif index == 28: gram['G'][0][0] = V.scalar(V.ZERO)
    elif index == 29: gram['delta'] = V.scalar(V.ONE)
    elif index == 30: gram['gamma'] = V.scalar(V.ONE)
    elif index == 31: gram['rho'] = V.scalar(V.Q(1,10**12))
    elif index == 32:
        gram['H'][0][0] = gram['delta'] = V.scalar(V.Q(4,10**12))
        gram['rho'] = V.scalar(V.Q(2,10**12))
    elif index == 37:
        gram['G'][0][0] = V.scalar(V.Q(-2)); gram['inverse'][0][0] = V.scalar(V.Q(-1,2))
    elif index == 38:
        shift['center'][0][0] = V.scalar(V.Q(3))
        shift['midpoint_polarization'][0][0] = V.scalar(V.Q(3))
        shift['trace_center'] = V.scalar(V.Q(3)); shift['direct'][0][0] = V.interval(V.Q(3),V.Q(3))
    return V.make_response(gram,shift,n=n)


def metadata_header():
    """Incomplete guard candidate: no genuine coefficients/Gram or acceptance."""
    return {'schema_version':'ri73-unit-white-operator-covariance-v1','mode':'fixed_operator_covariance',
        'status':'fixed_operator_covariance_passed','full_integration_qualified':True,'source_identity':dict(V.FIXED['ri73_source']),
        'dependencies':{},'runtime':{},'inherited_arithmetic_contract':{},'resource_contract':{},
        'model':{'kind':'known_synthetic_unit_white','mean':'zero','covariance':'I_T','input_dimension':V.T,'output_dimension':8},
        'dimensions':{'N':V.N,'L':V.L,'T':V.T},'rows':list(V.ROW_IDS),'sample_spacing':V.scalar(V.Q(1,4096)),
        'gate_inventory':list(V.HISTORICAL_GATES),'gate_counts':{'total':92,'passed':92,'failed':0},
        'gates':[{'id':name,'passed':True,'detail':{}} for name in V.HISTORICAL_GATES],
        'deterministic_fixture_admission_passed':True,'sampling_performed':False,
        'admitted_coefficient_design_requested':True,'reconstructed_rows_admitted':True,
        'exact_scalar_encoding':'MALFORMED_CONTROL_ONLY','scope':{'context':CONTEXT}}


def metadata_request(directory):
    def ref(name,pin=None):
        return {'path':str(directory/('unused-'+name)),'pin':dict(pin or {'bytes':1,'sha256':'0'*64})}
    selection = {'primary':str(directory/'selected-primary-never-opened.py'),
                 'white_kernel':str(directory/'selected-kernel-never-opened.py'),
                 'validator':str(Path(V.__file__).resolve())}
    request = {'schema':'ri125-white-request-v1','phase':'fixed_saved_application',
        'inputs':{name:ref(name,V.FIXED[name]) for name in V.INPUT_NAMES},
        'sources':{name:ref(name,V.DESIGN if name=='design' else None) for name in V.SOURCE_NAMES},
        'design_acceptance':ref('design-acceptance',V.DESIGN_ACCEPTANCE),'qualification':ref('qualification'),
        'custody':ref('custody'),'admission':ref('admission'),
        'runtime':{name:ref(name) for name in V.RUNTIME_NAMES},'output':str(directory/'unused-output.json')}
    for name,value in selection.items(): request['sources'][name]['path'] = value
    return request, selection


def empty_row(label):
    return {'row':label,'short':[V.interval(V.ZERO,V.ZERO) for _ in range(V.N)],
            'long':[V.interval(V.ZERO,V.ZERO) for _ in range(V.T)]}


def capture_encoding(rows,schema='ri125-fabricated-capture-v1'):
    return V.serialize({'dimensions':{'N':V.N,'L':V.L,'T':V.T},'row_order':list(V.ROW_IDS),'rows':rows,'schema':schema},True)


def declared_controls(directory):
    controls = []
    def add(identifier,code,message,fn): controls.append((identifier,code,message,fn))
    def file(name,body):
        path = directory/(name+'.fabricated')
        with path.open('xb') as stream:
            V.demand(stream.write(body)==len(body),'OUTPUT','complete fixture write')
        return {'path':str(path),'pin':V.content_pin(body)}
    def request_edit(edit):
        value, selection = metadata_request(directory); edit(value)
        return V.request_references(value,selection)
    def header_edit(edit):
        value = metadata_header(); edit(value)
        return V.historical_gram(value)
    def capture_edit(name,edit,complete=False):
        rows = [empty_row(i) for i in (V.ROW_IDS if complete else (0,))]
        reference = file(name,edit(rows))
        return list(V.stream_capture(reference,True))
    for number,(code,message) in enumerate(KERNEL_EXPECTED,1):
        add('WK%02d'%number,code,message,lambda number=number:kernel_call(number))
    add('WC01','PHASE','actual phase before body decoding',lambda:request_edit(lambda x:x.update(phase='fabricated_qualification')))
    add('WC02','SCHEMA','closed object keys',lambda:V.request_references({},{}))
    add('WC03','INPUT','externally frozen request bytes',lambda:V.validate_saved_white(b'{}',{'bytes':3,'sha256':'0'*64},{},b'{}',{'bytes':3,'sha256':'0'*64}))
    add('WC04','INPUT','fixed historical pin capture',lambda:request_edit(lambda x:x['inputs']['capture']['pin'].update(sha256='0'*64)))
    add('WC05','SOURCE','closed object keys',lambda:request_edit(lambda x:x['sources'].pop('validator')))
    add('WC06','SOURCE','loaded primary path',lambda:request_edit(lambda x:x['sources']['primary'].update(path=str(directory/'not-primary.py'))))
    add('WC07','SOURCE','loaded kernel path',lambda:request_edit(lambda x:x['sources']['white_kernel'].update(path=str(directory/'not-kernel.py'))))
    add('WC08','ADMISSION','exact root-bound card',lambda:V.primary_admission({},metadata_request(directory)[0]))
    add('WC09','INPUT','positive bounded pin length',lambda:V.validate_pin({'bytes':True,'sha256':'0'*64}))
    add('WC10','INPUT','lowercase sha256',lambda:V.validate_pin({'bytes':1,'sha256':'A'*64}))
    add('WC11','INPUT','literal absolute nonsymlink path',lambda:V.resolved_path('relative'))
    add('WC12','SCHEMA','duplicate JSON key',lambda:V.parse_json(b'{"v":1,"v":2}'))
    add('WC13','EXACT','decimal or nonfinite JSON token',lambda:V.parse_json(b'{"v":0.5}'))
    add('WC14','EXACT','decimal or nonfinite JSON token',lambda:V.parse_json(b'{"v":NaN}'))
    add('WC15','SCHEMA','invalid bounded JSON',lambda:V.parse_json(b'{'))
    add('WC16','RESOURCE','JSON integer text ceiling',lambda:V.parse_json(b'{"v":'+b'9'*65538+b'}'))
    def digest_mismatch():
        value = file('WC17',b'a'); value['pin'] = V.content_pin(b'b')
        return V.inspect_file(value)
    add('WC17','INPUT','whole body pin',digest_mismatch)
    def changed_file():
        value = file('WC18',b'a'); stamp = V.file_state(Path(value['path']).lstat())
        Path(value['path']).write_bytes(b'bb')
        return V.inspect_file(value,remember=stamp)
    add('WC18','CUSTODY','path state changed',changed_file)
    def symlink_input():
        value = file('WC19-seed',b'a'); link = directory/'WC19-link.fabricated'; link.symlink_to(value['path'])
        return V.inspect_file({'path':str(link),'pin':value['pin']})
    add('WC19','INPUT','literal absolute nonsymlink path',symlink_input)
    def hardlink_input():
        value = file('WC20-seed',b'a'); link = directory/'WC20-link.fabricated'; os.link(value['path'],link)
        return V.inspect_file({'path':str(link),'pin':value['pin']})
    add('WC20','INPUT','regular single-link source or input',hardlink_input)
    add('WC21','RI73','full inherited header mode',lambda:header_edit(lambda x:x.update(mode='fixtures_only')))
    add('WC22','RI73','full inherited header source_identity',lambda:header_edit(lambda x:x.update(source_identity={'bytes':1,'sha256':'0'*64})))
    add('WC23','RI73','full inherited header gate_inventory',lambda:header_edit(lambda x:x['gate_inventory'].reverse()))
    add('WC24','RI73','full inherited header gate_counts',lambda:header_edit(lambda x:x['gate_counts'].update(passed=91)))
    add('WC25','SHAPE','exact list length',lambda:header_edit(lambda x:x['gates'].pop()))
    add('WC26','RI73','literal 92-gate order',lambda:header_edit(lambda x:x['gates'][0].update(id='fixture:wrong')))
    for index in range(len(V.HISTORICAL_GATES)):
        add('WG%02d'%(index+1),'RI73','all inherited gates passed with details',
            lambda index=index:header_edit(lambda x:x['gates'][index].update(passed=False)))
    add('WC27','PHASE','actual capture forbidden in fabrication',lambda:list(V.stream_capture({'path':str(directory/'never-opened'),'pin':dict(V.FIXED['capture'])},True)))
    add('WC28','ROW','literal capture header',lambda:capture_edit('WC28',lambda rows:capture_encoding(rows).replace(b'"N":2769',b'"N":2768',1)))
    add('WC29','ROW','fixed row order',lambda:capture_edit('WC29',lambda rows:capture_encoding([{**rows[0],'row':True}])))
    add('WC30','ROW','closed object keys',lambda:capture_edit('WC30',lambda rows:capture_encoding([{**rows[0],'extra':None}])))
    add('WC31','SHAPE','exact list length',lambda:capture_edit('WC31',lambda rows:capture_encoding([{**rows[0],'short':[]}])))
    add('WC32','CANONICAL','compact row encoding',lambda:capture_edit('WC32',lambda rows:capture_encoding(rows).replace(b'"row":0',b'"row": 0',1)))
    add('WC33','SCHEMA','duplicate JSON key',lambda:capture_edit('WC33',lambda rows:capture_encoding(rows).replace(b'"row":0',b'"row":0,"row":0',1)))
    def bad_interval(rows):
        rows[0]['long'][0] = [['1','1'],['0','1']]
        return capture_encoding(rows)
    add('WC34','INTERVAL','ordered endpoints',lambda:capture_edit('WC34',bad_interval))
    def bad_scalar(rows):
        rows[0]['long'][0][0] = ['00','1']
        return capture_encoding(rows)
    add('WC35','EXACT','canonical signed hex',lambda:capture_edit('WC35',bad_scalar))
    add('WC36','ROW','row separator',lambda:capture_edit('WC36',capture_encoding))
    add('WC37','ROW','capture footer and ninth-row exhaustion',lambda:capture_edit('WC37',lambda rows:capture_encoding(rows+[empty_row(0)]),True))
    add('WC38','ROW','trailing capture bytes',lambda:capture_edit('WC38',lambda rows:capture_encoding(rows)+b'\n',True))
    add('WC39','ROW','capture footer and ninth-row exhaustion',lambda:capture_edit('WC39',lambda rows:capture_encoding(rows,'ri125-fabricated-capture-v0'),True))
    add('WC40','RESOURCE','capture row byte ceiling',lambda:V.CaptureReader(io.BytesIO(b'{"x":"'+b'x'*V.ROW_CAP)).object_body())
    add('WC41','BINDING','capture vector identity tied to accepted RI73 result',lambda:V.match_row(
        {'vectors':{'control':1},'row_identity':{'a_row_sum_interval':[]}},
        {'vector_identities':[{'control':2}],'constant_row_sum_intervals':[[]]},0))
    add('WC42','BINDING','complete row sum tied to accepted RI73 result',lambda:V.match_row(
        {'vectors':{},'row_identity':{'a_row_sum_interval':[0]}},
        {'vector_identities':[{}],'constant_row_sum_intervals':[[1]]},0))
    def occupied_output():
        value = file('WC43',b'preserve-me')
        return V.write_new_output(value['path'],{'context':CONTEXT})
    add('WC43','OUTPUT','output absent before exclusive open',occupied_output)
    add('WC44','RESOURCE','serialized byte ceiling',lambda:list(V.serialized_parts({'oversize':'x'*V.FILE_CAP})))
    add('WC45','PHASE','fabricated context',lambda:V.validate_fabricated_assembly({}, {}, 'W09_production_boundary_sparse','actual'))
    add('WC46','DOMAIN','fixed fabricated assembly case',lambda:V.validate_fabricated_assembly({}, {}, 'invented',CONTEXT))
    return controls,file


def run_controls(directory):
    root = V.resolved_path(directory)
    V.demand(root.parent.is_dir() and not os.path.lexists(root),'OUTPUT','new control directory')
    root.mkdir(mode=0o700)
    declarations,file = declared_controls(root)
    records = []
    for identifier,expected_code,expected_message,action in declarations:
        actual_code, actual_message = None, None
        try:
            value = action()
            if identifier == 'WC03' and type(value) is dict and type(value.get('refusal')) is dict:
                actual_code = value['refusal']['code']
                actual_message = value['refusal']['message'].split(': ',2)[-1]
        except V.Refusal as exc:
            actual_code, actual_message = exc.code, exc.message
        except Exception as exc:
            actual_code, actual_message = type(exc).__name__, str(exc)[:1024]
        records.append({'id':identifier,'expected_code':expected_code,'expected_message':expected_message,
            'observed_code':actual_code,'observed_message':actual_message,
            'passed':actual_code==expected_code and actual_message==expected_message})
    first_ref, second_ref = file('WT01-a',b'a'), file('WT01-b',b'b')
    readset = V.ReadSet(); readset.add('first',first_ref); readset.add('second',second_ref); readset.begin()
    Path(first_ref['path']).write_bytes(b'changed')
    postchecks = readset.final()
    records.append({'id':'WT01','passed':len(postchecks)==2 and postchecks[0]['unchanged'] is False
        and postchecks[1]['unchanged'] is True,'postchecks':postchecks})
    first = V.finish_validation(V.Refusal('EXACT','first-error'),None,None,postchecks)
    records.append({'id':'WT02','passed':first['refusal']['code']=='EXACT' and first['result'] is None
        and first['postchecks']==postchecks,'refusal':first['refusal']})
    late = V.finish_validation(None,{'context':CONTEXT},None,postchecks)
    records.append({'id':'WT03','passed':late['refusal']['code']=='CUSTODY' and late['result'] is None
        and late['postchecks']==postchecks,'refusal':late['refusal']})
    passed = sum(1 for row in records if row['passed'])
    return {'schema':'ri125-independent-white-controls-v1','phase':'fabricated_qualification','context':CONTEXT,
        'actual_scientific_input_opened':False,'independent_validator_run':True,'controls':records,
        'counts':{'total':len(records),'passed':passed,'failed':len(records)-passed},
        'status':'all_declared_controls_passed' if passed==len(records) else 'control_failure'}
