"""RI93 fabricated qualification, unexecuted source until root freezes a caller.

Independent scalar radical oracle and analytic expectations; no ambient local
imports, real saved-input reads, hidden retry or predicate substitution.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import math
import struct

M, N, L, T, Q = 16384, 2769, 4096, 10961, 1 << 256
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
ORDER = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
PRODUCTION = ('zero', 'constant', 'alternating', 'quarter_cosine', 'quarter_sine', 'impulse_zero')
ARTIFACT_NAMES = ('TINY.json', 'ALGEBRA.json', 'SYNTHETIC_INTERVALS.json', 'PRIOR.json', 'SCHEMA_FIXTURE.json',
                  'BAD_HEADER.json', 'BAD_TRAILING.json', 'BAD_REVERSED.json',
                  'PRODUCTION_zero.json', 'PRODUCTION_constant.json', 'PRODUCTION_alternating.json',
                  'PRODUCTION_quarter_cosine.json', 'PRODUCTION_quarter_sine.json', 'PRODUCTION_impulse_zero.json')
REFUSALS = (
 ('p_bool_integer','EXACT'), ('p_large_integer','RESOURCE'), ('p_noncanonical_hex','EXACT'),
 ('p_unreduced_rational','EXACT'), ('p_negative_denominator','EXACT'), ('p_reversed_interval','INTERVAL'),
 ('p_negative_sqrt','INTERVAL'), ('p_wrong_transform_size','DOMAIN'), ('p_bool_transform_size','DOMAIN'),
 ('p_wrong_transform_length','DOMAIN'), ('p_float_transform_input','EXACT'),
 ('p_bad_row_shape','ROW'), ('p_negative_radius','INTERVAL'), ('p_nonzero_constant_box','DC'),
 ('p_wrong_matrix_domain','DOMAIN'), ('p_negative_alpha','ALPHA'), ('p_missing_mode','TRANSFORM'),
 ('p_negative_psd','PSD'), ('p_nonfinite_psd','PSD'), ('p_noncanonical_float','PSD'),
 ('p_psd_hash','PSD'), ('p_psd_dtype','PSD'), ('p_float_shape','PSD'), ('p_float_fs','DOMAIN'),
 ('p_missing_band','BAND'), ('p_changed_band','BAND'), ('p_negative_H','BAND'),
 ('p_bad_rho','GLOBAL'), ('p_nonpositive_gram','GLOBAL'), ('p_extra_none_row','ROW'),
 ('p_fake_actual_identity','PHASE'), ('p_fake_qualification_accepted','PHASE'),
 ('p_actual_body_before_path','INPUT'), ('p_snapshot_identity','INPUT'), ('p_snapshot_header','SCHEMA'),
 ('p_snapshot_trailing','SCHEMA'), ('p_snapshot_reversed','INTERVAL'),
 ('v_unknown_field','SCHEMA'), ('v_wrong_phase','PHASE'), ('v_wrong_status','SCHEMA'), ('v_wrong_model','SCHEMA'),
 ('v_changed_method','DOMAIN'), ('v_changed_crop','DOMAIN'), ('v_changed_normalization','DOMAIN'),
 ('v_changed_resource','DOMAIN'), ('v_changed_rows','ROW'), ('v_removed_limitations','SCHEMA'),
 ('v_changed_gates','SCHEMA'), ('v_changed_design','SOURCE'), ('v_fake_actual_identity','PHASE'),
 ('v_fake_qualification_accepted','PHASE'), ('v_changed_runtime','PROVENANCE'), ('v_changed_prior','GLOBAL'),
 ('v_row_alpha','ALPHA'), ('v_row_initial','TRANSFORM'), ('v_row_mode','TRANSFORM'),
 ('v_band_partition','BAND'), ('v_repeated_band','BAND'), ('v_band_center','BAND'), ('v_band_error','BAND'),
 ('v_parseval_true_A_confusion','PARSEVAL'), ('v_parseval_status','PARSEVAL'),
 ('v_scenario_source','PSD'), ('v_scenario_ties','ENVELOPE'), ('v_scenario_lower','ENVELOPE'),
 ('v_scenario_upper','ENVELOPE'), ('v_scenario_weighted_H','ENVELOPE'),
 ('v_scenario_delta','ENVELOPE'), ('v_scenario_global','GLOBAL'), ('v_scenario_intersection','ENVELOPE'),
 ('v_noncanonical_json','CANONICAL'), ('v_duplicate_json','SCHEMA'), ('v_actual_body_before_path','INPUT'),
 ('wrong_unweighted_H','ENVELOPE'), ('wrong_midpoint_DC_omission','PARSEVAL'),
 ('wrong_Nyquist_pair_weight','ENVELOPE'), ('wrong_interior_PSD_factor','ENVELOPE'),
)


class QualificationError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def need(ok, code, message):
    if not ok:
        raise QualificationError(code, message)


def rat(x):
    return [format(x.numerator, 'x'), format(x.denominator, 'x')]


def enc(value):
    if type(value) is F: return rat(value)
    if type(value) in (list, tuple): return [enc(x) for x in value]
    if type(value) is dict: return {k: enc(x) for k, x in value.items()}
    return value


def canonical_parts(value):
    for part in json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False).iterencode(value):
        yield part.encode('ascii')
    yield b'\n'


def ident(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def pin_object(value):
    h, count = hashlib.sha256(), 0
    for block in canonical_parts(enc(value)):
        h.update(block); count += len(block)
    return {'bytes': count, 'sha256': h.hexdigest()}


def psd_record(values):
    floats = [float(x) for x in values]
    return {'dtype': '<f8', 'shape': [len(floats)], 'values_hex': [x.hex() for x in floats],
            'sha256': hashlib.sha256(b''.join(struct.pack('<d', x) for x in floats)).hexdigest()}


def snapshot_row(position, reversed_interval=False):
    zero = [rat(F(0)), rat(F(0))]
    short = [zero for _ in range(N)]
    long = [zero for _ in range(T)]
    long[2 * position] = [rat(F(1)), rat(F(1))]
    long[2 * position + 1] = [rat(F(-1)), rat(F(-1))]
    if reversed_interval:
        long[0] = [rat(F(1)), rat(F(-1))]
    return {'long': long, 'row': ROWS[position], 'short': short}


def synthetic_rows():
    for position, row in enumerate(ROWS):
        m = [F(0)] * T; m[2 * position], m[2 * position + 1] = F(1), F(-1)
        yield {'row': row, 'midpoints': tuple(m), 'radii': (F(0),) * T}


def fabricate_prior():
    scenarios = []
    for name, variance in zip(ORDER, (1, 4, 1, 4), strict=True):
        values = [F(2 * variance, 4096)] * (M // 2 + 1)
        values[0] = values[-1] = F(variance, 4096)
        scenarios.append({'id': name, 'source_record': psd_record(values)})
    return {'context': 'fabricated_prior_not_observed',
            'G': [[rat(F(2 if i == j else 0)) for j in range(8)] for i in range(8)],
            'rho': rat(F(0)), 'scenarios': scenarios,
            'held_provenance': {'context': 'fabricated_not_observed'},
            'held_limitations': ['Fabricated prior for RI93 qualification; no observed values or predecessor execution.']}


def _sqrt_isolation(x, precision=384):
    """Independent high-precision rational isolator; no producer primitive calls."""
    unit = 1 << precision
    a = math.isqrt((x.numerator * unit * unit) // x.denominator)
    lower = F(a, unit)
    upper = lower if lower * lower == x else F(a + 1, unit)
    need(lower * lower <= x <= upper * upper, 'ORACLE', 'radical isolation')
    return lower, upper


def radical_basis():
    a, b = _sqrt_isolation(F(2))
    beta = (_sqrt_isolation(2 + a)[0], _sqrt_isolation(2 + b)[1])
    gamma = (_sqrt_isolation(2 - b)[0], _sqrt_isolation(2 - a)[1])
    return ((F(1), F(1)), (a, b), beta, gamma)


def angle_coefficients(index):
    """cos/sin(j*pi/8) as linear forms in 1,sqrt2,beta,gamma."""
    index %= 16
    quarter = (
        ((F(1),0,0,0),(0,0,0,0)),
        ((0,0,F(1,2),0),(0,0,0,F(1,2))),
        ((0,F(1,2),0,0),(0,F(1,2),0,0)),
        ((0,0,0,F(1,2)),(0,0,F(1,2),0)),
    )
    a, b = quarter[index % 4]; turn = index // 4
    if turn == 0: return a, b
    if turn == 1: return tuple(-x for x in b), a
    if turn == 2: return tuple(-x for x in a), tuple(-x for x in b)
    return b, tuple(-x for x in a)


def eval_form(coefficients, basis):
    lo = hi = F(0)
    for c, (a, b) in zip(coefficients, basis, strict=True):
        lo += c * (a if c >= 0 else b)
        hi += c * (b if c >= 0 else a)
    return lo, hi


def direct_scalar(values):
    n = len(values); need(n in (4, 16), 'ORACLE', 'fixed direct oracle domain')
    divisor = math.isqrt(n); basis = radical_basis(); modes, forms = [], []
    for k in range(n):
        real, imag = [F(0)] * 4, [F(0)] * 4
        for j, x in enumerate(values):
            cr, ci = angle_coefficients((16 // n) * k * j)
            for h in range(4):
                real[h] += x * cr[h] / divisor; imag[h] += x * ci[h] / divisor
        modes.append((*eval_form(real, basis), *eval_form(imag, basis)))
        forms.append((real, imag))
    return tuple(modes), forms


def compare_oracle(actual, exact_intervals):
    need(len(actual) == len(exact_intervals), 'ORACLE', 'oracle length')
    for rectangle, target in zip(actual, exact_intervals, strict=True):
        for offset in (0, 2):
            a, b = F(rectangle[offset], Q), F(rectangle[offset + 1], Q)
            lo, hi = target[offset], target[offset + 1]
            need(a <= lo <= hi <= b, 'ORACLE', 'certified FFT must contain independent radical oracle')


def tiny_checks(primary):
    cases = ((4, 'impulse_one', (F(0),F(1),F(0),F(0))),
             (4, 'first_difference', (F(1),F(-1),F(0),F(0))),
             (4, 'second_difference', (F(0),F(1),F(-1),F(0))),
             (16, 'impulse_one', tuple(F(int(j == 1)) for j in range(16))),
             (16, 'rational_ramp', tuple(F(j % 5 - 2, 8) for j in range(16))),
             (16, 'first_difference', (F(1),F(-1)) + (F(0),)*14))
    results = []
    for n, name, values in cases:
        expected, forms = direct_scalar(values)
        actual = primary.transform(values, n)
        compare_oracle(actual, expected)
        results.append({'id':str(n)+':'+name,'size':n,'input':enc(values),'independent_radical_forms':enc(forms),
                        'oracle_intervals':enc(expected),'actual_grid':[[format(x,'x') for x in r] for r in actual],
                        'all_components_contained':True})
    return {'context':'fabricated_direct_scalar_oracle','cases':results,'count':6}


def analytic_vector(name):
    if name == 'zero': return (F(0),)*M
    if name == 'constant': return (F(1),)*M
    if name == 'alternating': return tuple(F(1 if j%2 == 0 else -1) for j in range(M))
    if name == 'quarter_cosine': return tuple(F((1,0,-1,0)[j%4]) for j in range(M))
    if name == 'quarter_sine': return tuple(F((0,1,0,-1)[j%4]) for j in range(M))
    if name == 'impulse_zero': return (F(1),)+(F(0),)*(M-1)
    raise QualificationError('DOMAIN','unknown analytic fixture')


def analytic_expected(name, k):
    if name == 'zero': return F(0), F(0)
    if name == 'constant': return F(128 if k == 0 else 0), F(0)
    if name == 'alternating': return F(128 if k == M//2 else 0), F(0)
    if name == 'quarter_cosine': return F(64 if k in (M//4,3*M//4) else 0), F(0)
    if name == 'quarter_sine': return F(0), F(64 if k == M//4 else -64 if k == 3*M//4 else 0)
    return F(1,128), F(0)


def production_check(primary, name):
    actual = primary.transform(analytic_vector(name), M)
    for k, r in enumerate(actual):
        x, y = analytic_expected(name, k)
        need(F(r[0],Q) <= x <= F(r[1],Q) and F(r[2],Q) <= y <= F(r[3],Q),
             'ORACLE','production analytic mode differs')
    result={'context':'fabricated_production_analytic_transform','id':name,'size':M,'checked_modes':M,
            'expected_rule':name,'all_exact_analytic_values_enclosed':True,
            'actual_grid':[[format(x,'x') for x in r] for r in actual]}
    if name=='quarter_sine':
        doubled=primary.transform(tuple(2*x for x in analytic_vector(name)),M)
        total_base,total_double=[F(0),F(0)],[F(0),F(0)]
        response_matrices=[]
        for k,(base,twice) in enumerate(zip(actual,doubled,strict=True)):
            x,y=analytic_expected(name,k)
            need(F(twice[0],Q)<=2*x<=F(twice[1],Q) and F(twice[2],Q)<=2*y<=F(twice[3],Q),
                 'ORACLE','doubled production analytic mode differs')
            if k>M//2:continue
            weight=1 if k in (0,M//2) else 2
            expected_power=weight*(x*x+y*y)
            response={'index':k,'expected_base':rat(expected_power),'expected_doubled':rat(4*expected_power)}
            for rectangle,scale,accumulator in ((base,1,total_base),(twice,4,total_double)):
                a,b,c,d=rectangle
                center_real,width_real=F(a+b,2*Q),F(b-a,2*Q)
                center_imag,width_imag=F(c+d,2*Q),F(d-c,2*Q)
                if k in (0,M//2):
                    need(c<=0<=d,'ORACLE','analytic real endpoint enclosure')
                    center_imag=width_imag=F(0)
                center=weight*(center_real**2+center_imag**2)
                error=weight*(2*abs(center_real)*width_real+width_real**2+
                              2*abs(center_imag)*width_imag+width_imag**2)
                need(center-error<=scale*expected_power<=center+error,'ORACLE','production fourfold response enclosure')
                accumulator[0]+=center-error;accumulator[1]+=center+error
                response['base' if scale==1 else 'doubled']={'C':rat(center),'H':rat(error)}
            response_matrices.append(response)
        need(total_base[0]<=F(M,2)<=total_base[1] and
             total_double[0]<=F(2*M)<=total_double[1],'ORACLE','production response-energy scaling')
        result['doubled_input']={'factor':2,'checked_modes':M,'checked_one_sided_response_matrices':M//2+1,
             'actual_grid':[[format(x,'x') for x in r] for r in doubled],
             'response_matrices':response_matrices,
             'base_total_response_interval':enc(total_base),'doubled_total_response_interval':enc(total_double),
             'expected_base_total':rat(F(M,2)),'expected_doubled_total':rat(F(2*M)),
             'all_fourfold_analytic_response_powers_enclosed':True,
             'bitwise_width_scaling_asserted':False}
    return result


def decode_matrix(record):
    return [[F(int(a,16),int(b,16)) for a,b in row] for row in record]


def exact_transform4(row):
    need(len(row)==4,'ORACLE','size4 row')
    a,b,c,d=row
    return (( (a+b+c+d)/2,F(0)),((a-c)/2,(b-d)/2),((a-b+c-d)/2,F(0)),((a-c)/2,(d-b)/2))


def omega4(rows, spectrum):
    vectors=[exact_transform4(row) for row in rows]
    return [[sum((spectrum[k]*(vectors[i][k][0]*vectors[j][k][0]+vectors[i][k][1]*vectors[j][k][1])
                  for k in range(4)), F(0)) for j in range(len(rows))] for i in range(len(rows))]


def psd2(matrix):
    if len(matrix)==1:return matrix[0][0]>=0
    return matrix[0][0]>=0 and matrix[1][1]>=0 and matrix[0][0]*matrix[1][1]-matrix[0][1]**2>=0


def difference(a,b):
    return [[x-y for x,y in zip(ra,rb,strict=True)] for ra,rb in zip(a,b,strict=True)]


def algebra_checks(primary):
    rows=((F(1),F(-1),F(0)),(F(0),F(1),F(-1)))
    g=[[F(2),F(-1)],[F(-1),F(2)]]
    modes=[primary.transform(row+(F(0),),4)[:3] for row in rows]
    response=primary.band_matrices(modes,(F(0),F(0)),size=4)
    need(decode_matrix(response['bands'][0]['C'])==[[F(1),F(0)],[F(0),F(1)]], 'ORACLE','R1 exact')
    need(decode_matrix(response['bands'][1]['C'])==[[F(1),F(-1)],[F(-1),F(1)]], 'ORACLE','R2 exact')
    psd=psd_record((F(0),F(1),F(5,4)))
    out=primary.scenario_bounds(psd,g,F(0),response['bands'],size=4,fs=4)
    expected=[[F(7),F(-5)],[F(-5),F(7)]]
    need(decode_matrix(out['lower'])==expected==decode_matrix(out['upper']),'ORACLE','exact colored fixture')
    scaled_modes=[primary.transform(tuple(2*x for x in row)+(F(0),),4)[:3] for row in rows]
    scaled=primary.band_matrices(scaled_modes,(F(0),F(0)),size=4)
    for a,b in zip(response['bands'],scaled['bands'],strict=True):
        need(decode_matrix(b['C'])==[[4*x for x in row] for row in decode_matrix(a['C'])],'ORACLE','amplitude-squared scaling')
    # Independent coefficient box: corners need not annihilate constants; lambda_DC=0.
    radius=F(1,16); alpha=F(3,32); widen=Q//256
    inflated=[tuple((a-widen,b+widen,c-widen,d+widen) for a,b,c,d in row) for row in modes]
    box=primary.band_matrices(inflated,(alpha,alpha),size=4)
    # This independent box has no inherited tiny-rho Gram certificate.  Only
    # the band theorem applies to its corners; do not invoke global endpoints.
    weighted_center=[[F(0)]*2 for _ in range(2)]
    weighted_error=[[F(0)]*2 for _ in range(2)]
    for band,coefficient in zip(box['bands'],(F(2),F(5)),strict=True):
        c,h=decode_matrix(band['C']),decode_matrix(band['H'])
        for i in range(2):
            for j in range(2):
                weighted_center[i][j]+=coefficient*c[i][j]
                weighted_error[i][j]+=coefficient*h[i][j]
    delta=max(sum(row,F(0)) for row in weighted_error)
    lower=[[weighted_center[i][j]-(delta if i==j else 0) for j in range(2)] for i in range(2)]
    upper=[[weighted_center[i][j]+(delta if i==j else 0) for j in range(2)] for i in range(2)]
    boxed={'context':'band_enclosure_only_no_inherited_Gram_premise',
           'weights':enc((F(2),F(5))),'weighted_center':enc(weighted_center),
           'weighted_error':enc(weighted_error),'delta':rat(delta),'lower':enc(lower),'upper':enc(upper)}
    corner_records=[]
    for signs in itertools.product((-1,1),repeat=6):
        varied=tuple(tuple(rows[i][j]+radius*signs[3*i+j] for j in range(3))+(F(0),) for i in range(2))
        actual=omega4(varied,(F(0),F(2),F(5),F(2)))
        need(psd2(difference(actual,lower)) and psd2(difference(upper,actual)), 'ORACLE','corner Loewner containment')
        transforms=[exact_transform4(row) for row in varied]
        for b,k,w in ((box['bands'][0],1,2),(box['bands'][1],2,1)):
            center,error=decode_matrix(b['C']),decode_matrix(b['H'])
            for i in range(2):
                for j in range(2):
                    real=w*(transforms[i][k][0]*transforms[j][k][0]+transforms[i][k][1]*transforms[j][k][1])
                    need(abs(real-center[i][j])<=error[i][j],'ORACLE','corner entrywise error containment')
        corner_records.append({'signs':list(signs),'omega':enc(actual)})
    modes_correlated=[primary.transform((F(3,2),F(-3,2),F(0),F(0)),4)[:3]]
    correlated=primary.band_matrices(modes_correlated,(F(1,2),),size=4)
    C=decode_matrix(correlated['bands'][1]['C'])[0][0];H=decode_matrix(correlated['bands'][1]['H'])[0][0]
    need(C==F(9,4) and H==F(7,4) and 4*C+4*H==16 and 4*C+H==F(43,4), 'ORACLE','weighted-H witness')
    # Nonzero midpoint DC is essential in the independent Parseval comparison.
    offset=((F(1),F(0),F(0),F(0)),)
    offset_modes=[primary.transform(offset[0],4)[:3]]
    midpoint=primary.band_matrices(offset_modes,(F(1,2),),size=4)
    need(decode_matrix(midpoint['midpoint_parseval']['center'])==[[F(1)]], 'ORACLE','midpoint DC retained')
    non_dc=sum(decode_matrix(b['C'])[0][0] for b in midpoint['bands'])
    need(non_dc==F(3,4),'ORACLE','explicit wrong DC omission witness')
    spectral_cases=[]
    for label,eigen in (('white1',(1,1,1,1)),('white4',(4,4,4,4)),('zero',(0,0,0,0)),
                        ('dc_only',(9,0,0,0)),('interior_only',(0,2,0,2)),('nyquist_only',(0,0,5,0))):
        record=psd_record((F(eigen[0],4),F(eigen[1],2),F(eigen[2],4)))
        value=primary.scenario_bounds(record,g,F(0),response['bands'],size=4,fs=4)
        omega=omega4(tuple(row+(F(0),) for row in rows),tuple(map(F,eigen)))
        need(decode_matrix(value['lower'])==omega==decode_matrix(value['upper']),'ORACLE','exact singleton-band spectral fixture')
        spectral_cases.append({'id':label,'psd':record,'expected_omega':enc(omega),'result':value})
    return ({'context':'fabricated_exact_covariance_and_uncertainty','exact_rows':enc(rows),
             'response':response,'exact_colored':out,'expected_colored':enc(expected),'amplitude_scaled':scaled,
             'corner_response':box,'corner_result':boxed,'corner_count':64,'corners':corner_records,
             'correlated_response':correlated,'correct_weighted_upper':rat(F(16)),'wrong_unweighted_upper':rat(F(43,4)),
             'midpoint_DC_response':midpoint,'wrong_DC_omission':rat(F(3,4)),'spectral_cases':spectral_cases}, response, psd, g)


class Artifacts:
    def __init__(self, directory):
        self.root=Path(directory)
        need(self.root.is_absolute() and self.root==self.root.resolve() and self.root.is_dir()
             and not self.root.is_symlink() and not any(self.root.iterdir()), 'PATH','exclusive empty artifact directory')
        self.rows=[]
    def write(self,name,value,compact=False):
        need(name in ARTIFACT_NAMES and name not in {r['name'] for r in self.rows},'PATH','fixed unused artifact name')
        path=self.root/name;h=hashlib.sha256();count=0
        with path.open('xb') as stream:
            encoder=json.JSONEncoder(sort_keys=True,indent=None if compact else 2,
                                     separators=(',',':') if compact else None,ensure_ascii=True,allow_nan=False)
            for part in encoder.iterencode(value):
                b=part.encode('ascii');count+=len(b);need(count<=64*1024*1024,'RESOURCE','artifact byte ceiling');stream.write(b);h.update(b)
            if not compact:
                need(count+1<=64*1024*1024,'RESOURCE','artifact byte ceiling including newline')
                stream.write(b'\n');h.update(b'\n');count+=1
        row={'name':name,'bytes':count,'sha256':h.hexdigest()};self.rows.append(row);return path,row
    def write_bytes(self,name,body):
        need(name in ARTIFACT_NAMES and name not in {r['name'] for r in self.rows},'PATH','fixed unused byte artifact')
        need(len(body)<=64*1024*1024,'RESOURCE','artifact byte ceiling')
        path=self.root/name
        with path.open('xb') as stream:stream.write(body)
        row={'name':name,**ident(body)};self.rows.append(row);return path,row


def _mutate(container,path,value,work):
    target=container
    for key in path[:-1]:target=target[key]
    key=path[-1];old=target[key];target[key]=value
    try:return work()
    finally:target[key]=old


def run(primary,validator,provenance_template,artifact_dir):
    """Only caller-supplied captured modules; complete fabricated domain, one pass."""
    need(set(provenance_template)=={'sources','inputs','acceptance','runtime'} and provenance_template['inputs'] is None,
         'PROVENANCE','unexecuted synthetic-input template')
    artifacts=Artifacts(artifact_dir);cases=[]
    expected=dict(REFUSALS)
    def refuse(name,work):
        need(name in expected and name not in {x['id'] for x in cases},'INVENTORY','one declared refusal')
        try:work()
        except (primary.BandError,validator.ValidationError,QualificationError) as error:
            need(error.code==expected[name],'REASON','wrong intended code for '+name)
            cases.append({'id':name,'expected_code':expected[name],'code':error.code,'message':str(error),'passed':True})
        else:raise QualificationError('REFUSAL','negative control accepted: '+name)
    tiny=tiny_checks(primary);_,tiny_pin=artifacts.write('TINY.json',tiny);del tiny
    for name in PRODUCTION:
        value=production_check(primary,name);artifacts.write('PRODUCTION_'+name+'.json',value);del value
    algebra,small_bands,small_psd,small_g=algebra_checks(primary)
    _,algebra_pin=artifacts.write('ALGEBRA.json',algebra)
    bad_weight=F(43,4);actual_weight=F(16)
    refuse('wrong_unweighted_H',lambda:need(actual_weight<=bad_weight,'ENVELOPE','unweighted H misses exact correlated corner'))
    refuse('wrong_midpoint_DC_omission',lambda:need(F(1)==F(3,4),'PARSEVAL','omitting nonzero midpoint DC changes Gram'))
    refuse('wrong_Nyquist_pair_weight',lambda:need(2*5==5,'ENVELOPE','doubling singleton Nyquist changes covariance'))
    refuse('wrong_interior_PSD_factor',lambda:need(4*F(1)==2,'ENVELOPE','interior eigenvalue must use fs/2'))
    del algebra
    # Complete artificial capture has exactly the actual shape, with declared simple rows.
    snapshot={'dimensions':{'L':L,'N':N,'T':T},'row_order':list(ROWS),
              'rows':[snapshot_row(i) for i in range(8)],'schema':'ri73-reconstructed-intervals-v1'}
    capture_path,capture_pin=artifacts.write('SYNTHETIC_INTERVALS.json',snapshot,compact=True);del snapshot
    prior=fabricate_prior();_,prior_pin=artifacts.write('PRIOR.json',prior)
    provenance={**provenance_template,'inputs':{'snapshot':{k:capture_pin[k] for k in ('bytes','sha256')},
                 'ri90':{k:prior_pin[k] for k in ('bytes','sha256')},
                 'ri83':pin_object(prior['scenarios']),
                 'ri73':pin_object({'G':prior['G'],'rho':prior['rho'],'definition':'eight disjoint first differences'})}}
    # Both independent source readers must recover the exact declared fixture rows.
    for actual,known in zip(primary.source_rows(capture_path,provenance['inputs']['snapshot']),synthetic_rows(),strict=True):
        need(actual==known,'ORACLE','primary streamed synthetic capture')
    with capture_path.open('rb') as stream:
        for actual,known in zip(validator.SnapshotReader(stream,provenance['inputs']['snapshot']).rows(),synthetic_rows(),strict=True):
            need(actual==known,'ORACLE','independent streamed synthetic capture')
    report=primary.build_result(primary.source_rows(capture_path,provenance['inputs']['snapshot']),prior,provenance)
    fixture_path,fixture_pin=artifacts.write('SCHEMA_FIXTURE.json',report);del report
    body=fixture_path.read_bytes()
    with capture_path.open('rb') as stream:
        report=validator.load_result(body,validator.SnapshotReader(stream,provenance['inputs']['snapshot']).rows(),
                                     prior,provenance,expected_phase='fabricated_qualification')
    del body
    # Expected observed-shaped fixture has G=2I and exact white covariance 2*sigma² I.
    for scenario,variance in zip(report['scenarios'],(1,4,1,4),strict=True):
        intervals=[[F(int(x[0],16),int(x[1],16)) for x in pair] for pair in scenario['diagonal']]
        need(all(lo<=2*variance<=hi for lo,hi in intervals),'ORACLE','white fixture band endpoints contain exact output variance')
        need(scenario['scalar_intersections']['diagonal']==[[rat(F(2*variance)),rat(F(2*variance))]]*8,
             'ORACLE','white exact global scalar intersection')
    fixture_before=primary.canonical_pin(report)
    # All primitive negatives are tiny or fail before any transform.
    refuse('p_bool_integer',lambda:primary.integer(True))
    refuse('p_large_integer',lambda:primary.integer(1<<262144))
    refuse('p_noncanonical_hex',lambda:primary.decode_int('-0'))
    refuse('p_unreduced_rational',lambda:primary.decode_scalar(['2','2']))
    refuse('p_negative_denominator',lambda:primary.decode_scalar(['1','-1']))
    refuse('p_reversed_interval',lambda:primary.interval((1,0)))
    refuse('p_negative_sqrt',lambda:primary.sqrt_grid(F(-1)))
    refuse('p_wrong_transform_size',lambda:primary.transform((F(0),)*8,8))
    refuse('p_bool_transform_size',lambda:primary.transform((),True))
    refuse('p_wrong_transform_length',lambda:primary.transform((F(0),)*3,4))
    refuse('p_float_transform_input',lambda:primary.transform((0.0,)*4,4))
    refuse('p_bad_row_shape',lambda:primary.row_certificate(0,(F(0),),(F(0),),size=4))
    refuse('p_negative_radius',lambda:primary.row_certificate(0,(F(0),)*3,(F(-1),F(0),F(0)),size=4))
    refuse('p_nonzero_constant_box',lambda:primary.row_certificate(0,(F(1),)*3,(F(0),)*3,size=4))
    tiny_modes=[primary.transform((F(1),F(-1),F(0),F(0)),4)[:3]]
    refuse('p_wrong_matrix_domain',lambda:primary.band_matrices(tiny_modes,(F(0),),size=16))
    refuse('p_negative_alpha',lambda:primary.band_matrices(tiny_modes,(F(-1),),size=4))
    refuse('p_missing_mode',lambda:primary.band_matrices([tiny_modes[0][:-1]],(F(0),),size=4))
    def badpsd(key,value):return _mutate(small_psd,(key,),value,lambda:primary.decode_psd(small_psd,4))
    negative=psd_record((F(0),F(-1),F(0)))
    refuse('p_negative_psd',lambda:primary.decode_psd(negative,4))
    refuse('p_nonfinite_psd',lambda:badpsd('values_hex',['nan']+small_psd['values_hex'][1:]))
    refuse('p_noncanonical_float',lambda:badpsd('values_hex',['0x0p+0']+small_psd['values_hex'][1:]))
    refuse('p_psd_hash',lambda:badpsd('sha256','0'*64))
    refuse('p_psd_dtype',lambda:badpsd('dtype','>f8'))
    refuse('p_float_shape',lambda:badpsd('shape',[3.0]))
    refuse('p_float_fs',lambda:primary.scenario_bounds(small_psd,small_g,F(0),small_bands['bands'],size=4,fs=4.0))
    refuse('p_missing_band',lambda:primary.scenario_bounds(small_psd,small_g,F(0),small_bands['bands'][:1],size=4,fs=4))
    refuse('p_changed_band',lambda:_mutate(small_bands,('bands',0,'first'),2,lambda:primary.scenario_bounds(small_psd,small_g,F(0),small_bands['bands'],size=4,fs=4)))
    refuse('p_negative_H',lambda:_mutate(small_bands,('bands',0,'H',0,0),rat(F(-1)),lambda:primary.scenario_bounds(small_psd,small_g,F(0),small_bands['bands'],size=4,fs=4)))
    refuse('p_bad_rho',lambda:primary.scenario_bounds(small_psd,small_g,F(1,10**11),small_bands['bands'],size=4,fs=4))
    refuse('p_nonpositive_gram',lambda:primary.scenario_bounds(small_psd,[[F(0),F(0)],[F(0),F(0)]],F(0),small_bands['bands'],size=4,fs=4))
    refuse('p_extra_none_row',lambda:primary.require_exhausted(iter([None])))
    refuse('p_fake_actual_identity',lambda:_mutate(provenance,('inputs','ri90'),dict(primary.RI90_PIN),lambda:primary.validate_provenance(provenance,'fabricated_qualification')))
    refuse('p_fake_qualification_accepted',lambda:_mutate(provenance,('acceptance','qualification'),dict(primary.RI90_PIN),lambda:primary.validate_provenance(provenance,'fabricated_qualification')))
    refuse('p_actual_body_before_path',lambda:primary.run_saved(None,b'not an admitted report',provenance))
    refuse('p_snapshot_identity',lambda:next(primary.source_rows(capture_path,{'bytes':1,'sha256':'0'*64})))
    # Retain every wire-format negative as evidence, with each intended parser guard.
    original=capture_path.read_bytes()
    bad_header,ph=artifacts.write_bytes('BAD_HEADER.json',b' '+original)
    bad_trailing,pt=artifacts.write_bytes('BAD_TRAILING.json',original+b' ')
    del original
    broken={'dimensions':{'L':L,'N':N,'T':T},'row_order':list(ROWS),
            'rows':[snapshot_row(i,reversed_interval=(i==0)) for i in range(8)],'schema':'ri73-reconstructed-intervals-v1'}
    bad_reversed,pr=artifacts.write('BAD_REVERSED.json',broken,compact=True);del broken
    def consume_rows(path,row):
        for _ in primary.source_rows(path,{k:row[k] for k in ('bytes','sha256')}):pass
    refuse('p_snapshot_header',lambda:consume_rows(bad_header,ph))
    refuse('p_snapshot_trailing',lambda:consume_rows(bad_trailing,pt))
    refuse('p_snapshot_reversed',lambda:consume_rows(bad_reversed,pr))
    def validate_full():return validator.validate_result(report,(),prior,provenance,expected_phase='fabricated_qualification')
    # Every following full entry fails in a metadata guard before transform entry.
    extras=dict(report);extras['unexpected']=0
    refuse('v_unknown_field',lambda:validator.validate_result(extras,(),prior,provenance,expected_phase='fabricated_qualification'))
    mutations=(('v_wrong_phase',('phase',),'fixed_saved_application'),('v_wrong_status',('status',),'failed'),
               ('v_wrong_model',('model',),'physical_covariance'),
               ('v_changed_method',('method','precision_bits'),255),('v_changed_crop',('method','L'),4095),
               ('v_changed_normalization',('method','unitary_divisor'),64),
               ('v_changed_resource',('method','integer_bit_limit'),262145),
               ('v_changed_rows',('rows',),list(reversed(ROWS))),
               ('v_removed_limitations',('limitations',),[]),('v_changed_gates',('gates','counts','passed'),9),
               ('v_changed_design',('provenance','sources','design'),{'bytes':1,'sha256':'0'*64}),
               ('v_fake_actual_identity',('provenance','inputs','ri90'),dict(primary.RI90_PIN)),
               ('v_fake_qualification_accepted',('provenance','acceptance','qualification'),dict(primary.RI90_PIN)),
               ('v_changed_prior',('prior',),{**prior,'context':'changed'}))
    for name,path,value in mutations:refuse(name,lambda path=path,value=value:_mutate(report,path,value,validate_full))
    changed_runtime={**report['provenance'],'runtime':{**report['provenance']['runtime'],'fingerprint':{'bytes':1,'sha256':'1'*64}}}
    refuse('v_changed_runtime',lambda:_mutate(report,('provenance',),changed_runtime,validate_full))
    # Actual subrecord guards are called by validate_result; no patched predicates/caches.
    _,powers=validator.twiddle_evidence(M)
    source=next(synthetic_rows())
    first_rectangle=report['row_proofs'][0]['midpoint_modes'][1]
    need(int(first_rectangle[0],16)<int(first_rectangle[1],16),'ORACLE','nonzero rounded production width for shrink control')
    for name,path,value in (('v_row_alpha',('alpha',),rat(F(1))),('v_row_initial',('initial_q256',0),['0','0']),
                            ('v_row_mode',('midpoint_modes',1,1),first_rectangle[0])):
        refuse(name,lambda path=path,value=value:_mutate(report['row_proofs'][0],path,value,
                   lambda:validator.verify_row(report['row_proofs'][0],source,ROWS[0],powers)))
    del powers,source
    modes=[tuple(tuple(int(x,16) for x in r) for r in row['midpoint_modes']) for row in report['row_proofs']]
    alphas=[F(int(row['alpha'][0],16),int(row['alpha'][1],16)) for row in report['row_proofs']]
    g=decode_matrix(prior['G']);rho=F(0)
    need(decode_matrix(report['bands'][0]['H'])[0][0]>0,'ORACLE','nonzero error for underestimate control')
    for name,path,value in (('v_band_partition',('first',),2),('v_repeated_band',('index',),1),
                            ('v_band_center',('C',0,0),rat(F(-1))),('v_band_error',('H',0,0),rat(F(0)))):
        refuse(name,lambda path=path,value=value:_mutate(report['bands'][0],path,value,
                   lambda:validator.verify_band(report['bands'][0],modes,alphas,0)))
    refuse('v_parseval_true_A_confusion',lambda:_mutate(report['midpoint_parseval'],('center',0,0),rat(F(0)),
            lambda:validator.verify_parseval(report['midpoint_parseval'],modes,alphas,g)))
    refuse('v_parseval_status',lambda:_mutate(report['midpoint_parseval'],('contains_G',),False,
            lambda:validator.verify_parseval(report['midpoint_parseval'],modes,alphas,g)))
    computed_bands=[(decode_matrix(b['C']),decode_matrix(b['H'])) for b in report['bands']]
    scenario=report['scenarios'][0]
    def vscenario():return validator.verify_scenario(scenario,prior['scenarios'][0],computed_bands,g,rho)
    vm=(('v_scenario_source',('source_record',),{**scenario['source_record'],'sha256':'0'*64}),
        ('v_scenario_ties',('band_extrema',0,'minimum_indices'),[]),
        ('v_scenario_lower',('lower',0,0),rat(F(-1))),('v_scenario_upper',('upper',0,0),rat(F(-1))),
        ('v_scenario_weighted_H',('H_plus',0,0),rat(F(-1))),('v_scenario_delta',('delta_plus',),rat(F(-1))),
        ('v_scenario_global',('global_lower',0,0),rat(F(-1))),('v_scenario_intersection',('scalar_intersections','trace'),[rat(F(0)),rat(F(0))]))
    for name,path,value in vm:refuse(name,lambda path=path,value=value:_mutate(scenario,path,value,vscenario))
    refuse('v_noncanonical_json',lambda:validator.load_result(b' {} ',(),prior,provenance,expected_phase='fabricated_qualification'))
    refuse('v_duplicate_json',lambda:validator.load_result(b'{"a":1,"a":2}\n',(),prior,provenance,expected_phase='fabricated_qualification'))
    refuse('v_actual_body_before_path',lambda:validator.validate_saved(report,None,b'not an admitted report',provenance))
    need(primary.canonical_pin(report)==fixture_before=={k:fixture_pin[k] for k in ('bytes','sha256')},'CUSTODY','all reversible mutations restored full fixture bytes')
    need({c['id'] for c in cases}==set(expected) and len(cases)==len(REFUSALS),'INVENTORY','complete refusal inventory')
    byname={r['name']:r for r in artifacts.rows}
    need(set(byname)==set(ARTIFACT_NAMES) and {p.name for p in artifacts.root.iterdir()}==set(ARTIFACT_NAMES),'INVENTORY','complete retained artifact inventory')
    for row in artifacts.rows:
        need(ident((artifacts.root/row['name']).read_bytes())=={k:row[k] for k in ('bytes','sha256')},'CUSTODY','retained artifact bytes')
    return {'schema':'ri93-fabricated-qualification-v1','phase':'fabricated_qualification','status':'all_fabricated_gates_passed',
            'scope':'Fabricated mathematical and source-format qualification only; no actual interval/PSD values decoded.',
            'provenance':provenance,'counts':{'tiny_direct_cases':6,'production_analytic_cases':6,'production_modes_per_case':M,
                    'production_doubled_subcases':1,'production_scaling_response_matrices':M//2+1,
                    'coefficient_corners':64,'spectral_cases':6,'full_production_schema_fixtures':1,
                    'refusals':len(REFUSALS),'artifacts':len(ARTIFACT_NAMES)},
            'refusal_inventory':[{'id':name,'expected_code':code} for name,code in REFUSALS],
            'refusals':[next(c for c in cases if c['id']==name) for name,_ in REFUSALS],
            'artifacts':[byname[name] for name in ARTIFACT_NAMES],
            'positive_checks':{'independent_scalar_radical_oracle':True,'production_analytic_enclosures':True,
                'production_response_scaling':True,
                'coefficient_error_corners':True,'lambda_weighted_H':True,'midpoint_DC_preserved':True,
                'white_endpoint_mapping':True,'both_streamed_source_readers':True,'full_independent_result_validation':True,
                'canonical_result_roundtrip':True,'all_mutations_restored':True},
            'limitations':['No actual source-input numerical body was decoded; file operands above are exclusively generated fixtures.',
                           'Full genuine source/runtime custody is separately established by the frozen outer caller.',
                           'Qualification establishes neither physical noise adequacy nor a native forward map.']}


if __name__=='__main__':
    raise SystemExit('RI93 qualification requires captured modules and a separately authorized caller.')
