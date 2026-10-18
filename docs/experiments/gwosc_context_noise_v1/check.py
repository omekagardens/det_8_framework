"""RI68 exact covariance fixtures and fixed synthetic Gaussian diagnostics.

No observations, admitted coefficients or public-data inference are consumed.
--fixtures performs deterministic checks only and never constructs a PRNG.
The default study requires separate source review/freeze before execution.
All rational arithmetic results are limited to 32768 numerator/denominator bits.
The reused oracle sees only four tiny fixed basis problems; its inputs and
intermediate values in those problems have elementary bounds below 64 bits.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import re
import stat
import struct
import sys

BITS=32768
DIM=16
DEPENDENCIES={
    'design':{'path':'gwosc_context_noise_v1/DESIGN.md','bytes':24027,
              'sha256':'74581df2266277b5ff12c9d45d110baf191f99dfbc7db8ea4b3810affa914921'},
    'oracle':{'path':'gwosc_context_operator_v1/oracle.py','bytes':9484,
              'sha256':'37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651'},
    'runtime_receipt':{'path':'gwosc_observed_context_v1/QUALIFICATION_REPORT.json','bytes':33132,
              'sha256':'56aa06c442384bd6249875443930202e09e874b4318aa995a8b7bb6dec1dab1b'},
}
EXPECTED_VERSIONS={'python':'3.11.6','numpy':'2.1.3','scipy':'1.14.1','h5py':'3.12.1'}
MODEL_IDS=('G0','G1','G2','G3','G4')
ERRORS=(ValueError,TypeError,KeyError,OSError,ArithmeticError,RuntimeError,MemoryError)


def require(condition,message):
    if not condition: raise ValueError(message)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def encoded(value):
    if type(value) is F: return str(value)
    if isinstance(value,(list,tuple)): return [encoded(v) for v in value]
    if isinstance(value,dict): return {k:encoded(v) for k,v in value.items()}
    return value


def equal(actual,expected,label):
    require(canonical(encoded(actual))==canonical(encoded(expected)),label)


def identity(payload):
    require(type(payload) is bytes,'identity requires bytes')
    return {'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}


def verify_bytes(body,pin,label):
    require(type(pin) is dict and type(pin.get('bytes')) is int and 0<pin['bytes']<=1024*1024 and
            type(pin.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}',pin['sha256']),label+': invalid pin')
    equal(identity(body),{k:pin[k] for k in ('bytes','sha256')},label+': byte identity differs')
    return body


def bound_bytes(path,pin,label):
    try:
        info=path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size==pin['bytes'],label+': pinned regular file required')
        with path.open('rb') as stream: body=stream.read(pin['bytes']+1)
    except OSError as error: raise ValueError(label+': cannot read pinned file') from error
    return verify_bytes(body,pin,label)


def parse_json(body):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'duplicate JSON key');result[key]=value
        return result
    def invalid(value): raise ValueError('nonfinite JSON constant')
    return json.loads(body,object_pairs_hook=pairs,parse_constant=invalid)


def runtime():
    import h5py
    import numpy as np
    import scipy
    return {'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'h5py':h5py.__version__},
        'python_implementation':platform.python_implementation(),'python_build':sys.version,
        'operating_system':platform.system(),'os_release':platform.release(),'os_version':platform.version(),
        'machine':platform.machine(),'byte_order':sys.byteorder,'hdf5_version':h5py.version.hdf5_version,
        'numpy_configuration':np.show_config(mode='dicts')}


def validate_runtime_receipt(receipt,current):
    require(type(receipt) is dict and receipt.get('schema_version')=='ri64-consumer-qualification-v1' and
            receipt.get('status')=='all_consumer_gates_passed','runtime receipt status/schema differs')
    equal(receipt.get('gate_counts'),{'total':75,'passed':75,'failed':0},'runtime receipt incomplete')
    equal(current.get('versions'),EXPECTED_VERSIONS,'runtime package versions differ')
    equal(current,receipt.get('runtime'),'full qualified runtime differs')


def admission():
    base=Path(__file__).resolve().parent.parent
    sources={name:bound_bytes(base/pin['path'],pin,name) for name,pin in DEPENDENCIES.items()}
    # Every dependency snapshot is bound before metadata parsing or helper load.
    own=Path(__file__).read_bytes()
    receipt=parse_json(sources['runtime_receipt']);current=runtime()
    validate_runtime_receipt(receipt,current)
    path=base/DEPENDENCIES['oracle']['path']
    spec=importlib.util.spec_from_file_location('ri68_bound_exact_oracle',path)
    require(spec is not None and spec.loader is not None,'cannot specify exact oracle')
    oracle=importlib.util.module_from_spec(spec);sys.modules[spec.name]=oracle
    exec(compile(sources['oracle'],str(path),'exec'),oracle.__dict__)
    return {'base':base,'sources':sources,'own':own,'receipt':receipt,'runtime':current,'oracle':oracle}


def recheck(admitted):
    equal(identity(Path(__file__).read_bytes()),identity(admitted['own']),'checker source changed')
    for name,pin in DEPENDENCIES.items():
        require(bound_bytes(admitted['base']/pin['path'],pin,name)==admitted['sources'][name],name+': snapshot changed')
    validate_runtime_receipt(admitted['receipt'],runtime())


def rat(value):
    require(type(value) is F,'exact Fraction required')
    require(value.numerator.bit_length()<=BITS and value.denominator.bit_length()<=BITS,'Fraction resource limit')
    return value


def f(n,d=1):
    require(type(n) is int and type(d) is int,'integer Fraction components required')
    require(n.bit_length()<=BITS and d.bit_length()<=BITS,'Fraction resource limit')
    require(d!=0,'zero rational denominator')
    return rat(F(n,d))


def add(a,b): return rat(rat(a)+rat(b))
def sub(a,b): return rat(rat(a)-rat(b))
def mul(a,b): return rat(rat(a)*rat(b))
def div(a,b):
    rat(a);rat(b);require(b!=0,'zero rational divisor');return rat(a/b)
def neg(a):return rat(-rat(a))

def total(values):
    result=f(0)
    for value in values:result=add(result,value)
    return result


def vector(values,length=None):
    require(type(values) in (tuple,list) and 0<len(values)<=DIM and
            (length is None or len(values)==length),'vector dimensions differ')
    return tuple(rat(v) for v in values)


def matrix(rows):
    require(type(rows) in (tuple,list) and 0<len(rows)<=DIM,'matrix dimensions differ')
    result=tuple(vector(row) for row in rows)
    require(all(len(row)==len(result[0]) for row in result),'matrix is ragged')
    return result


def eye(n):
    require(type(n) is int and 1<=n<=DIM,'identity dimension differs')
    return tuple(tuple(f(int(i==j)) for j in range(n)) for i in range(n))


def zeros(n,m):
    require(type(n) is int and type(m) is int and 1<=n<=DIM and 1<=m<=DIM,'zero matrix dimensions differ')
    return tuple(tuple(f(0) for _ in range(m)) for _ in range(n))


def transpose(a):a=matrix(a);return tuple(zip(*a))

def mm(a,b):
    a,b=matrix(a),matrix(b);require(len(a[0])==len(b),'matrix product dimensions differ')
    bt=transpose(b)
    return tuple(tuple(total(mul(x,y) for x,y in zip(row,col,strict=True)) for col in bt) for row in a)


def mv(a,v):
    a=matrix(a);v=vector(v,len(a[0]))
    return tuple(total(mul(x,y) for x,y in zip(row,v,strict=True)) for row in a)


def scale(a,s):a=matrix(a);rat(s);return tuple(tuple(mul(v,s) for v in row) for row in a)

def matrix_add(a,b,subtract=False):
    a,b=matrix(a),matrix(b);require(len(a)==len(b) and len(a[0])==len(b[0]),'matrix sum dimensions differ')
    op=sub if subtract else add
    return tuple(tuple(op(x,y) for x,y in zip(ar,br,strict=True)) for ar,br in zip(a,b,strict=True))


def rank_exact(a):
    a=[list(row) for row in matrix(a)];n,m=len(a),len(a[0]);rank=0
    for col in range(m):
        pivot=next((i for i in range(rank,n) if a[i][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank];lead=a[rank][col]
        a[rank]=[div(v,lead) for v in a[rank]]
        for i in range(rank+1,n):
            factor=a[i][col]
            a[i]=[sub(x,mul(factor,y)) for x,y in zip(a[i],a[rank],strict=True)]
        rank+=1
        if rank==n:break
    return rank


def psd_rank(a):
    a=matrix(a);require(len(a)==len(a[0]),'covariance must be square')
    equal(a,transpose(a),'covariance must be symmetric')
    work=[list(row) for row in a];rank=0
    while work:
        require(all(work[i][i]>=0 for i in range(len(work))),'covariance is not PSD')
        pivot=next((i for i in range(len(work)) if work[i][i]>0),None)
        if pivot is None:
            require(all(v==0 for row in work for v in row),'covariance is not PSD');break
        work[0],work[pivot]=work[pivot],work[0]
        for row in work:row[0],row[pivot]=row[pivot],row[0]
        p=work[0][0]
        work=[[sub(work[i][j],div(mul(work[i][0],work[0][j]),p))
               for j in range(1,len(work))] for i in range(1,len(work))]
        rank+=1
    equal(rank,rank_exact(a),'PSD and elimination ranks disagree')
    return rank


def nullspace_basis(a):
    work=[list(row) for row in matrix(a)];n,m=len(work),len(work[0]);pivots=[]
    for col in range(m):
        row=len(pivots);pivot=next((i for i in range(row,n) if work[i][col]),None)
        if pivot is None:continue
        work[row],work[pivot]=work[pivot],work[row];lead=work[row][col]
        work[row]=[div(v,lead) for v in work[row]]
        for i in range(n):
            if i!=row:
                factor=work[i][col]
                work[i]=[sub(x,mul(factor,y)) for x,y in zip(work[i],work[row],strict=True)]
        pivots.append(col)
        if len(pivots)==n:break
    basis=[]
    for free in range(m):
        if free in pivots:continue
        v=[f(0)]*m;v[free]=f(1)
        for row,pivot in enumerate(pivots):v[pivot]=neg(work[row][free])
        basis.append(tuple(v))
    for v in basis:equal(mv(a,v),(f(0),)*n,'nullspace basis vector differs')
    if basis:equal(rank_exact(tuple(basis)),len(basis),'nullspace vectors are dependent')
    return tuple(basis)


def prepare_covariance(omega,pseudoinverse,expected_rank,covariance_kind='known'):
    require(covariance_kind=='known','estimated covariance has no fixed chi-square admission')
    omega,k=matrix(omega),matrix(pseudoinverse)
    require(len(omega)==len(omega[0])==len(k)==len(k[0]),'covariance/inverse dimensions differ')
    require(type(expected_rank) is int and 0<=expected_rank<=len(omega),'rank must be a bounded integer')
    equal(psd_rank(omega),expected_rank,'covariance rank differs')
    equal(mm(mm(omega,k),omega),omega,'Moore-Penrose O K O identity differs')
    equal(mm(mm(k,omega),k),k,'Moore-Penrose K O K identity differs')
    ok,ko=mm(omega,k),mm(k,omega)
    equal(transpose(ok),ok,'Moore-Penrose O K symmetry differs')
    equal(transpose(ko),ko,'Moore-Penrose K O symmetry differs')
    nullspace=nullspace_basis(omega)
    equal(len(nullspace),len(omega)-expected_rank,'nullspace dimension differs')
    return {'omega':omega,'pseudoinverse':k,'projector':ok,'rank':expected_rank,'nullspace_basis':nullspace}


def quadratic_on_support(residual,prepared):
    residual=vector(residual,len(prepared['omega']))
    equal(mv(prepared['projector'],residual),residual,'residual outside covariance support')
    require(all(total(mul(x,y) for x,y in zip(v,residual,strict=True))==0 for v in prepared['nullspace_basis']),
            'residual outside covariance support')
    q=total(mul(x,y) for x,y in zip(residual,mv(prepared['pseudoinverse'],residual),strict=True))
    require(q>=0,'negative covariance quadratic')
    return q


def exp_negative_bounds(x):
    x=rat(x);require(f(0)<x<f(130),'exponential argument outside fixed bound')
    term=f(1);s=term
    for k in range(1,129):term=div(mul(term,x),f(k));s=add(s,term)
    term129=div(mul(term,x),f(129))
    remainder=div(term129,sub(f(1),div(x,f(130))))
    return div(f(1),add(s,remainder)),div(f(1),s)


def probability_bounds(rank):
    require(type(rank) is int and rank in (2,8),'unsupported tail rank')
    lo,hi=exp_negative_bounds(f(rank));factor=f(1) if rank==2 else f(379,3)
    bounds=mul(lo,factor),mul(hi,factor)
    require(f(0)<bounds[0]<=bounds[1]<f(1),'invalid tail probability interval')
    require(sub(bounds[1],bounds[0])<=f(1,2**100),'probability oracle too wide')
    return bounds


def family_error_bound():
    margin=sub(f(1,64),f(1,2**100));require(margin>f(1,66),'null budget margin differs')
    x1=f(65536,4356);x2=mul(f(65536),mul(f(21,592),f(21,592)))
    b1,b2=exp_negative_bounds(x1),exp_negative_bounds(x2)
    upper=add(mul(f(6),b1[1]),b2[1]);require(upper<f(1,100000),'family error budget exceeded')
    return {'null_margin_lower_exact':str(f(1,66)),'null_exponent_exact':str(x1),
        'power_margin_exact':str(f(21,592)),'power_exponent_exact':str(x2),
        'null_exponential_interval':encoded(b1),'power_exponential_interval':encoded(b2),
        'family_upper_bound_exact':str(upper),'family_limit_exact':'1/100000',
        'meaning':'False-failure bound for the four correct ideal independent-trial Gaussian models; not a PRNG or detector-noise guarantee.'}


def covariance_from_factors(s,t):
    s,t=matrix(s),matrix(t);a=matrix_add(t,s,True)
    ss,tt,ts=mm(s,transpose(s)),mm(t,transpose(t)),mm(t,transpose(s))
    direct=mm(a,transpose(a));expanded=matrix_add(matrix_add(matrix_add(tt,ss),ts,True),transpose(ts),True)
    equal(direct,expanded,'shared covariance routes disagree')
    return {'short_factor':s,'context_factor':t,'difference_factor':a,'short_covariance':ss,
            'context_covariance':tt,'context_short_cross_covariance':ts,'covariance':direct}


def models():
    e=eye(8);z=zeros(8,8);s16=tuple((*r,*q) for r,q in zip(e,z,strict=True))
    t16=tuple((*q,*r) for r,q in zip(e,z,strict=True))
    corr=tuple((*r,*q) for r,q in zip(scale(e,f(3,5)),scale(e,f(4,5)),strict=True))
    d=tuple((f(int(i%2==0)),f(int(i%2==1))) for i in range(8));dd=mm(d,transpose(d))
    specifications=(('G0',e,e,zeros(8,8),zeros(8,8),0,256,8,2026092400,(f(0),)*8),
      ('G1',s16,t16,scale(e,f(2)),scale(e,f(1,2)),8,32768,16,2026092401,(f(0),)*8),
      ('G2',s16,corr,scale(e,f(4,5)),scale(e,f(5,4)),8,32768,16,2026092402,(f(0),)*8),
      ('G3',d,scale(d,f(2)),dd,scale(dd,f(1,16)),2,32768,2,2026092403,(f(0),)*8),
      ('G4',d,scale(d,f(2)),dd,scale(dd,f(1,16)),2,32768,2,2026092404,tuple(f(8 if i%2==0 else 0) for i in range(8))))
    result=[]
    for name,s,t,omega,k,rank,trials,columns,seed,shift in specifications:
        result.append({'id':name,'short_factor':s,'context_factor':t,'mean_shift':shift,
          'covariance':omega,'pseudoinverse':k,'rank':rank,'trials':trials,'latent_columns':columns,'seed':seed})
    return tuple(result)


def exact_refusal(work,reason):
    try:work()
    except ValueError as error:
        equal(str(error),reason,'refusal occurred for unintended reason')
        return {'refused':True,'reason':reason}
    raise ValueError('invalid request was accepted')


def matrix_rows(rows):
    return matrix(tuple(tuple(f(*v) if type(v) is tuple else f(v) for v in row) for row in rows))


def fir_fixture(oracle):
    f2=matrix_rows([[(7,4),(1,2)],[(3,4),(3,2)]])
    f4=matrix_rows([[(7,4),(1,2),0,0],[(1,2),(5,4),(1,2),0],
        [0,(1,2),(5,4),(1,2)],[0,0,(3,4),(3,2)]])
    stage=(((f(1),f(1,2),f(0),f(1),f(0),f(0)),),)
    for n,expected in ((2,f2),(4,f4)):
        actual=matrix(oracle.matrix_fraction(n,stage,(0,)));equal(actual,expected,'FIR oracle basis matrix differs')
    p=matrix_rows([[0,(7,4),(1,2),0],[0,(3,4),(3,2),0]])
    q=(f4[1],f4[2]);out=covariance_from_factors(p,q)
    expected={'difference_factor':matrix_rows([[(1,2),(-1,2),0,0],[0,(-1,4),(-1,4),(1,2)]]),
       'short_covariance':matrix_rows([[(53,16),(33,16)],[(33,16),(45,16)]]),
       'context_covariance':matrix_rows([[(33,16),(5,4)],[(5,4),(33,16)]]),
       'context_short_cross_covariance':matrix_rows([[(39,16),(27,16)],[(3,2),(9,4)]]),
       'covariance':matrix_rows([[(1,2),(1,8)],[(1,8),(3,8)]])}
    for key,val in expected.items():equal(out[key],val,'FIR '+key+' differs')
    inv=matrix_rows([[(24,11),(-8,11)],[(-8,11),(32,11)]])
    prepared=prepare_covariance(out['covariance'],inv,2)
    det=sub(mul(out['covariance'][0][0],out['covariance'][1][1]),mul(out['covariance'][0][1],out['covariance'][1][0]))
    equal(det,f(11,64),'FIR determinant differs')
    equal(quadratic_on_support((f(1),f(0)),prepared),f(24,11),'FIR unit residual score differs')
    impulse=mv(out['difference_factor'],(f(1),f(0),f(0),f(0)))
    equal(impulse,(f(1,2),f(0)),'FIR raw impulse differs')
    equal(quadratic_on_support(impulse,prepared),f(6,11),'FIR impulse score differs')
    wrong=matrix_add(out['short_covariance'],out['context_covariance'])
    equal(wrong,matrix_rows([[(43,8),(53,16)],[(53,16),(39,8)]]),'wrong FIR covariance expected value differs')
    refusal=exact_refusal(lambda:equal(wrong,out['covariance'],'shared-input covariance cross terms omitted'),
                          'shared-input covariance cross terms omitted')
    return {'F2':f2,'F4':f4,**out,'pseudoinverse':inv,'rank':2,'determinant':det,
            'unit_residual_q':f(24,11),'raw_impulse_output':impulse,'raw_impulse_q':f(6,11),
            'wrong_independence_covariance':wrong,'wrong_covariance_refusal':refusal,'basis_columns_checked':6}


def cancellation_fixture(oracle):
    stage=(((f(1),f(0),f(0),f(1),f(0),f(0)),),)
    for n in (2,4):equal(matrix(oracle.matrix_fraction(n,stage,(0,))),eye(n),'identity oracle basis differs')
    c=matrix_rows([[0,1,0,0],[0,0,1,0]]);out=covariance_from_factors(c,c)
    equal(out['covariance'],zeros(2,2),'cancellation covariance differs')
    prepared=prepare_covariance(out['covariance'],zeros(2,2),0)
    equal(quadratic_on_support((f(0),f(0)),prepared),f(0),'zero-rank score differs')
    refusal=exact_refusal(lambda:quadratic_on_support((f(0),f(1)),prepared),'residual outside covariance support')
    return {**out,'pseudoinverse':zeros(2,2),'rank':0,'q':f(0),'off_support':refusal,'basis_columns_checked':6}


def singular_fixture():
    omega=matrix_rows([[1,1],[1,1]]);k=scale(omega,f(1,4));prepared=prepare_covariance(omega,k,1)
    equal(quadratic_on_support((f(2),f(2)),prepared),f(4),'rank-one score differs')
    h=(f(1),f(-1));equal(mv(k,h),(f(0),f(0)),'null vector differs')
    refusal=exact_refusal(lambda:quadratic_on_support(h,prepared),'residual outside covariance support')
    return {'covariance':omega,'pseudoinverse':k,'rank':1,'projector':prepared['projector'],'nullspace_basis':prepared['nullspace_basis'],'q_at_2_2':f(4),
            'null_vector':h,'off_support':refusal}


def two_detector_fixture():
    factor=matrix_rows([[1,0],[(3,5),(4,5)]]);omega=mm(factor,transpose(factor))
    equal(omega,matrix_rows([[1,(3,5)],[(3,5),1]]),'detector cross covariance differs')
    k=matrix_rows([[(25,16),(-15,16)],[(-15,16),(25,16)]]);prepared=prepare_covariance(omega,k,2)
    det=sub(mul(omega[0][0],omega[1][1]),mul(omega[0][1],omega[1][0]));equal(det,f(16,25),'detector determinant differs')
    refusal=exact_refusal(lambda:equal(omega,eye(2),'detector cross covariance omitted'),'detector cross covariance omitted')
    return {'factor':factor,'covariance':omega,'pseudoinverse':k,'rank':prepared['rank'],'determinant':det,'wrong_independence':refusal}


def model_fixture(model):
    out=covariance_from_factors(model['short_factor'],model['context_factor'])
    equal(out['covariance'],model['covariance'],'model covariance differs')
    prepared=prepare_covariance(model['covariance'],model['pseudoinverse'],model['rank'])
    detail={**model,**out,'projector':prepared['projector'],'nullspace_basis':prepared['nullspace_basis'],
            'covariance_kind':'known','all_four_MP_identities':True}
    if model['id'] in ('G2','G3'):
        wrong=matrix_add(out['short_covariance'],out['context_covariance'])
        expected=scale(eye(8),f(2)) if model['id']=='G2' else scale(model['covariance'],f(5))
        equal(wrong,expected,'wrong surrogate covariance differs')
        detail['wrong_independence_covariance']=wrong
        detail['wrong_covariance_refusal']=exact_refusal(lambda:equal(wrong,model['covariance'],'shared-input covariance cross terms omitted'),
                                                        'shared-input covariance cross terms omitted')
    if model['id'] in ('G3','G4'):
        d=model['short_factor'];equal(mm(transpose(d),d),scale(eye(2),f(4)),'D transpose D differs')
        u=(f(3,2),f(-5,4));noise=mv(out['difference_factor'],u)
        y=tuple(add(n,h) for n,h in zip(noise,model['mean_shift'],strict=True))
        expected=add(mul(add(u[0],f(8) if model['id']=='G4' else f(0)),add(u[0],f(8) if model['id']=='G4' else f(0))),mul(u[1],u[1]))
        equal(quadratic_on_support(y,prepared),expected,'rank-two latent score differs')
        detail['fixed_latent']=u;detail['fixed_latent_q']=expected
    if model['id']=='G4':
        equal(quadratic_on_support(model['mean_shift'],prepared),f(64),'noncentrality differs')
        equal(sub(f(36,37),f(15,16)),f(21,592),'power margin differs')
        detail.update(noncentrality=f(64),power_lower=f(36,37),power_gate=f(15,16),power_margin=f(21,592))
    if model['id'] in ('G0','G3'):
        h=tuple(f(int(i==0)-(int(i==2) if model['id']=='G3' else 0)) for i in range(8))
        detail['off_support_shift']=h
        detail['off_support_refusal']=exact_refusal(lambda:quadratic_on_support(h,prepared),'residual outside covariance support')
    return detail


def refusal_inventory():
    return ('fraction_type','fraction_bool','fraction_nonfinite','fraction_resource','arithmetic_resource','zero_divisor',
      'matrix_empty','matrix_ragged','matrix_oversize','product_dimensions','covariance_nonsquare','covariance_asymmetric',
      'covariance_negative','covariance_zero_diagonal_indefinite','rank_wrong','rank_bool','inverse_wrong','inverse_second_identity','inverse_left_symmetry','inverse_right_symmetry','estimated_covariance',
      'residual_dimensions','support_violation','tail_rank','exponential_domain','source_changed','source_missing',
      'source_bad_pin','duplicate_json','nonfinite_json','receipt_failed','receipt_incomplete','runtime_changed','latent_nonfinite',
      'latent_wrong_shape','latent_wrong_dtype','latent_over_trials')


def refusal_case(name,admitted):
    e=eye(2);prepared=prepare_covariance(e,e,2)
    if name=='fraction_type':return exact_refusal(lambda:rat(1),'exact Fraction required')
    if name=='fraction_bool':return exact_refusal(lambda:rat(True),'exact Fraction required')
    if name=='fraction_nonfinite':return exact_refusal(lambda:rat(float('nan')),'exact Fraction required')
    if name=='fraction_resource':return exact_refusal(lambda:rat(F(1<<BITS)),'Fraction resource limit')
    if name=='arithmetic_resource':return exact_refusal(lambda:mul(f(1<<(BITS-1)),f(2)),'Fraction resource limit')
    if name=='zero_divisor':return exact_refusal(lambda:div(f(1),f(0)),'zero rational divisor')
    if name=='matrix_empty':return exact_refusal(lambda:matrix([]),'matrix dimensions differ')
    if name=='matrix_ragged':return exact_refusal(lambda:matrix([(f(1),),(f(0),f(1))]),'matrix is ragged')
    if name=='matrix_oversize':return exact_refusal(lambda:matrix([(f(0),)]*17),'matrix dimensions differ')
    if name=='product_dimensions':return exact_refusal(lambda:mm(e,((f(1),),)),'matrix product dimensions differ')
    if name=='covariance_nonsquare':return exact_refusal(lambda:psd_rank(((f(1),f(0)),)),'covariance must be square')
    if name=='covariance_asymmetric':return exact_refusal(lambda:psd_rank(matrix_rows([[1,1],[0,1]])),'covariance must be symmetric')
    if name=='covariance_negative':return exact_refusal(lambda:psd_rank(matrix_rows([[1,0],[0,-1]])),'covariance is not PSD')
    if name=='covariance_zero_diagonal_indefinite':return exact_refusal(lambda:psd_rank(matrix_rows([[0,1],[1,0]])),'covariance is not PSD')
    if name=='rank_wrong':return exact_refusal(lambda:prepare_covariance(e,e,1),'covariance rank differs')
    if name=='rank_bool':return exact_refusal(lambda:prepare_covariance(e,e,True),'rank must be a bounded integer')
    if name=='inverse_wrong':return exact_refusal(lambda:prepare_covariance(e,scale(e,f(2)),2),'Moore-Penrose O K O identity differs')
    if name=='inverse_second_identity':return exact_refusal(lambda:prepare_covariance(matrix_rows([[1,0],[0,0]]),eye(2),1),'Moore-Penrose K O K identity differs')
    if name=='inverse_left_symmetry':return exact_refusal(lambda:prepare_covariance(matrix_rows([[1,0],[0,0]]),matrix_rows([[1,1],[0,0]]),1),'Moore-Penrose O K symmetry differs')
    if name=='inverse_right_symmetry':return exact_refusal(lambda:prepare_covariance(matrix_rows([[1,0],[0,0]]),matrix_rows([[1,0],[1,0]]),1),'Moore-Penrose K O symmetry differs')
    if name=='estimated_covariance':return exact_refusal(lambda:prepare_covariance(e,e,2,'estimated'),'estimated covariance has no fixed chi-square admission')
    if name=='residual_dimensions':return exact_refusal(lambda:quadratic_on_support((f(1),),prepared),'vector dimensions differ')
    if name=='support_violation':return exact_refusal(lambda:quadratic_on_support((f(1),f(0)),prepare_covariance(zeros(2,2),zeros(2,2),0)),'residual outside covariance support')
    if name=='tail_rank':return exact_refusal(lambda:probability_bounds(1),'unsupported tail rank')
    if name=='exponential_domain':return exact_refusal(lambda:exp_negative_bounds(f(130)),'exponential argument outside fixed bound')
    if name=='source_changed':return exact_refusal(lambda:verify_bytes(b'abd',identity(b'abc'),'fixture'),'fixture: byte identity differs')
    if name=='source_missing':
        return exact_refusal(lambda:bound_bytes(admitted['base']/'ri68-intentionally-absent-file',identity(b'a'),'fixture'),'fixture: cannot read pinned file')
    if name=='source_bad_pin':return exact_refusal(lambda:verify_bytes(b'a',{'bytes':True,'sha256':'0'*64},'fixture'),'fixture: invalid pin')
    if name=='duplicate_json':return exact_refusal(lambda:parse_json(b'{"a":1,"a":2}'),'duplicate JSON key')
    if name=='nonfinite_json':return exact_refusal(lambda:parse_json(b'[NaN]'),'nonfinite JSON constant')
    if name in ('receipt_failed','receipt_incomplete','runtime_changed'):
        receipt=copy.deepcopy(admitted['receipt']);current=copy.deepcopy(admitted['runtime'])
        reason={'receipt_failed':'runtime receipt status/schema differs','receipt_incomplete':'runtime receipt incomplete',
                'runtime_changed':'full qualified runtime differs'}[name]
        if name=='receipt_failed':receipt['status']='failed'
        elif name=='receipt_incomplete':receipt['gate_counts']['failed']=False
        else:current['machine']='changed'
        return exact_refusal(lambda:validate_runtime_receipt(receipt,current),reason)
    if name.startswith('latent_'):
        import numpy as np
        values=np.zeros((1,8),dtype=np.float64);reason='latent draw shape/type differs'
        if name=='latent_nonfinite':values[0,0]=np.inf;reason='latent draw is nonfinite'
        elif name=='latent_wrong_shape':values=np.zeros((1,7),dtype=np.float64)
        elif name=='latent_wrong_dtype':values=values.astype(np.float32)
        elif name=='latent_over_trials':values=np.zeros((257,8),dtype=np.float64)
        return exact_refusal(lambda:validate_draws(values,models()[0],np),reason)
    raise ValueError('unknown refusal case')


def validate_draws(draws,model,np):
    require(type(draws) is np.ndarray and draws.dtype==np.dtype('float64') and draws.ndim==2 and
            0<draws.shape[0]<=model['trials'] and draws.shape[1]==model['latent_columns'] and draws.flags.c_contiguous,
            'latent draw shape/type differs')
    require(bool(np.isfinite(draws).all()),'latent draw is nonfinite')


class CanonicalStream:
    """SHA of one canonical JSON list, streamed without storing every score."""
    def __init__(self):self.hasher=hashlib.sha256();self.hasher.update(b'[');self.count=0;self.closed=False;self.bytes=1
    def append(self,value):
        require(not self.closed,'canonical stream closed')
        body=(b',' if self.count else b'')+canonical(value);self.hasher.update(body);self.bytes+=len(body);self.count+=1
    def finish(self):
        require(not self.closed,'canonical stream closed');self.hasher.update(b']');self.closed=True;self.bytes+=1
        return {'bytes':self.bytes,'sha256':self.hasher.hexdigest(),'records':self.count}


def reduce_draws(model,draws,np,global_stream=None):
    """May inspect artificial short batches; only study_gate admits full counts."""
    validate_draws(draws,model,np)
    prepared=prepare_covariance(model['covariance'],model['pseudoinverse'],model['rank'])
    s,t=model['short_factor'],model['context_factor'];a=matrix_add(t,s,True)
    score_stream=CanonicalStream();exceed=0;zero=0;support_alternatives=0;maximum=f(0);minimum=None
    for index,row in enumerate(draws):
        latent=tuple(rat(F.from_float(float(value))) for value in row)
        short,context=mv(s,latent),mv(t,latent)
        residual=tuple(add(sub(v,u),h) for u,v,h in zip(short,context,model['mean_shift'],strict=True))
        independent=tuple(add(v,h) for v,h in zip(mv(a,latent),model['mean_shift'],strict=True))
        equal(residual,independent,'sample shared-input maps disagree')
        q=quadratic_on_support(residual,prepared)
        if model['id']=='G0':equal(q,f(0),'cancellation sample score is nonzero')
        elif model['id'] in ('G3','G4'):
            shifted=add(latent[0],f(8) if model['id']=='G4' else f(0))
            equal(q,add(mul(shifted,shifted),mul(latent[1],latent[1])),'sample rank-two score differs')
        zero+=int(q==0);exceed+=int(q>f(2*model['rank']))
        maximum=max(maximum,q);minimum=q if minimum is None else min(minimum,q)
        alternative=None
        if model['id'] in ('G0','G3'):
            shift=tuple(f(int(i==0)-(int(i==2) if model['id']=='G3' else 0)) for i in range(8))
            shifted=tuple(add(v,h) for v,h in zip(residual,shift,strict=True))
            exact_refusal(lambda:quadratic_on_support(shifted,prepared),'residual outside covariance support')
            alternative=False;support_alternatives+=1
        item={'model':model['id'],'trial':index,'q':str(q),'in_support':True,'shifted_alternative_in_support':alternative}
        score_stream.append(item)
        if global_stream is not None:global_stream.append(item)
    payload=draws.astype('<f8',copy=False).tobytes(order='C')
    return {'actual_trials':len(draws),'exceedance_count':exceed,'threshold_exact':str(f(2*model['rank'])),
        'zero_score_count':zero,'minimum_score_exact':str(minimum),'maximum_score_exact':str(maximum),
        'support_checks':len(draws),'off_support_alternatives_refused':support_alternatives,
        'latent_identity':{'shape':list(draws.shape),'dtype':'little-endian binary64','order':'C',**identity(payload)},
        'score_support_identity':score_stream.finish()}


def study_gate(model,reduction):
    equal(reduction['actual_trials'],model['trials'],'study trial count differs')
    equal(reduction['support_checks'],model['trials'],'study support coverage differs')
    equal(reduction['off_support_alternatives_refused'],model['trials'] if model['id'] in ('G0','G3') else 0,
          'study off-support coverage differs')
    count=reduction['exceedance_count'];require(type(count) is int and 0<=count<=model['trials'],'invalid exceedance count')
    frequency=f(count,model['trials'])
    if model['id']=='G0':
        equal(reduction['zero_score_count'],model['trials'],'zero-covariance samples not exact zero')
        equal(count,0,'zero-covariance tail count differs')
        return {'kind':'exact_cancellation','passed':True}
    if model['id']=='G4':
        passed=frequency>=f(15,16)
        return {'kind':'shifted_alternative','frequency_exact':str(frequency),'lower_acceptance_exact':'15/16',
                'ideal_power_lower_exact':'36/37','passed':passed}
    bounds=probability_bounds(model['rank']);distance=max(abs(sub(frequency,bounds[0])),abs(sub(frequency,bounds[1])))
    return {'kind':'ideal_null_tail','frequency_exact':str(frequency),'probability_interval':encoded(bounds),
            'endpoint_distance_exact':str(distance),'limit_exact':'1/64','passed':distance<=f(1,64)}


def run_sampled_model(model,global_stream,progress):
    import numpy as np
    detail={'generator':'Generator(PCG64DXSM(SeedSequence(seed)))','seed':model['seed'],
            'call':{'method':'standard_normal','size':[model['trials'],model['latent_columns']],
                    'dtype':'np.float64','calls':1}}
    phase='generator_construction'
    try:
        generator=np.random.Generator(np.random.PCG64DXSM(np.random.SeedSequence(model['seed'])))
        progress['generator_constructed']=True
        detail['initial_generator_state']=copy.deepcopy(generator.bit_generator.state)
        phase='single_standard_normal_call';progress['draw_call_entered']=True
        draws=generator.standard_normal(size=(model['trials'],model['latent_columns']),dtype=np.float64)
        progress['draw_call_completed']=True
        detail['final_generator_state']=copy.deepcopy(generator.bit_generator.state)
        phase='validate_and_reduce_retained_draws'
        validate_draws(draws,model,np)
        detail['latent_identity']={'shape':list(draws.shape),'dtype':'little-endian binary64','order':'C',
            **identity(draws.astype('<f8',copy=False).tobytes(order='C'))}
        result=reduce_draws(model,draws,np,global_stream)
        progress['reduction_completed']=True
        equal(result['actual_trials'],model['trials'],'sampler returned incomplete trials')
        return {**detail,**result,'acceptance':study_gate(model,result)}
    except ERRORS as error:
        return {**detail,'phase':phase,'acceptance':{'passed':False,'error_type':type(error).__name__,'error':str(error)}}


def fixture_inventory():
    return ['fixture:fir','fixture:cancellation','fixture:rank_one','fixture:two_detector']+['model:'+n for n in MODEL_IDS]+\
        ['probability:rank2','probability:rank8','probability:family_budget']+['refusal:'+n for n in refusal_inventory()]


def record(gates,name,work):
    try:
        detail=work();passed=detail.get('acceptance',{}).get('passed',True) is True
        gates.append({'id':name,'passed':passed,'detail':encoded(detail)})
    except ERRORS as error:
        gates.append({'id':name,'passed':False,'detail':{'error_type':type(error).__name__,'error':str(error)}})


def run_checks(admitted,fixtures_only):
    declarations=models();equal(tuple(m['id'] for m in declarations),MODEL_IDS,'model order differs')
    model_manifest=encoded(declarations);manifest_identity=identity(canonical(model_manifest));gates=[]
    record(gates,'fixture:fir',lambda:fir_fixture(admitted['oracle']))
    record(gates,'fixture:cancellation',lambda:cancellation_fixture(admitted['oracle']))
    record(gates,'fixture:rank_one',singular_fixture);record(gates,'fixture:two_detector',two_detector_fixture)
    for model in declarations:record(gates,'model:'+model['id'],lambda m=model:model_fixture(m))
    for rank in (2,8):
        record(gates,'probability:rank'+str(rank),lambda r=rank:{'rank':r,'threshold':2*r,
            'probability_interval':probability_bounds(r),'series_degree':128,'summand_count':129,
            'remainder_first_degree':129,'width_limit':f(1,2**100)})
    record(gates,'probability:family_budget',family_error_bound)
    for name in refusal_inventory():record(gates,'refusal:'+name,lambda n=name:refusal_case(n,admitted))
    equal([g['id'] for g in gates],fixture_inventory(),'fixture inventory differs')
    recheck(admitted)
    study_ready=all(g['passed'] is True for g in gates)
    stream=CanonicalStream()
    progress={m['id']:{'generator_constructed':False,'draw_call_entered':False,'draw_call_completed':False,
                      'reduction_completed':False} for m in declarations}
    if not fixtures_only:
        for model in declarations:
            if study_ready:
                record(gates,'study:'+model['id'],lambda m=model:run_sampled_model(m,stream,progress[m['id']]))
            else:
                gates.append({'id':'study:'+model['id'],'passed':False,
                    'detail':{'not_run':True,'reason':'deterministic qualification failed; sampling was not authorized'}})
    final_stream=stream.finish()
    if not fixtures_only and all(g['passed'] is True for g in gates):
        equal(final_stream['records'],131328,'complete study score inventory differs')
        require(all(all(v is True for v in item.values()) for item in progress.values()),'complete study progress differs')
    equal(encoded(declarations),model_manifest,'model declarations changed')
    equal(encoded(models()),model_manifest,'frozen model reconstruction differs')
    recheck(admitted)
    failed=sum(g['passed'] is not True for g in gates)
    mode='fixtures_only' if fixtures_only else 'fixed_synthetic_study'
    status=('fixtures_only_passed' if fixtures_only else 'fixed_synthetic_study_passed') if failed==0 else mode+'_failed'
    return {'schema_version':'ri68-context-noise-v1','mode':mode,'status':status,
        'source_identity':identity(admitted['own']),'dependencies':{name:identity(body) for name,body in admitted['sources'].items()},
        'runtime':admitted['runtime'],'model_manifest':model_manifest,'model_manifest_identity':manifest_identity,
        'gate_inventory':fixture_inventory()+([] if fixtures_only else ['study:'+n for n in MODEL_IDS]),
        'gate_counts':{'total':len(gates),'passed':len(gates)-failed,'failed':failed},'gates':gates,
        'sampling_requested':not fixtures_only,'deterministic_admission_passed':study_ready,
        'sampling_progress':progress,
        'draw_calls_entered':sum(v['draw_call_entered'] is True for v in progress.values()),
        'draw_calls_completed':sum(v['draw_call_completed'] is True for v in progress.values()),
        'reductions_completed':sum(v['reduction_completed'] is True for v in progress.values()),
        'full_study_qualified':not fixtures_only and failed==0,
        'combined_score_support_identity':final_stream,
        'score_serialization':'canonical JSON list in G0..G4/trial order of model,trial,q,in_support,shifted_alternative_in_support; q is a Fraction string',
        'resource_contract':{'fraction_bits':BITS,'matrix_dimension':DIM,'trial_rows':131328,'one_worker':True,
            'external_seconds_per_execution':1800,'external_sampled_resident_byte_limit':2147483648,
            'watchdog_is_not_hard_allocator_cap':True},
        'scope':{'models':'Exact rational surrogates only; no admitted-A integration or observational file access.',
            'sampling':'Finite seeded binary64 PRNG diagnostics; ideal Gaussian probability budget is conditional, not an exact sampler or detector-noise guarantee.',
            'runtime_receipt':'RI64 receipt reused solely as pinned qualified runtime metadata; its75gates are not re-executed here.',
            'oracle':'Published exact DFI oracle reused only for the two lengths2/4 and fixed FIR/identity basis fixtures.',
            'inference':'No calibrated confidence, residual score on observed data, native forward map or physical gravity inference.'}}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures',action='store_true',help='Only deterministic exact fixtures; no PRNG construction or sampling.')
    args=parser.parse_args(argv);admitted=None
    try:
        admitted=admission();result=run_checks(admitted,args.fixtures)
        sys.stdout.buffer.write((json.dumps(result,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii'))
        return 0 if result['gate_counts']['failed']==0 else 1
    except ERRORS as error:
        result={'schema_version':'ri68-context-noise-failure-v1','status':'execution_refused',
            'mode':'fixtures_only' if args.fixtures else 'fixed_synthetic_study','full_study_qualified':False,
            'error_type':type(error).__name__,'error':str(error)}
        if admitted is not None:result['source_identity']=identity(admitted['own'])
        sys.stdout.buffer.write((json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('ascii'))
        print('RI68 refused: '+str(error),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
