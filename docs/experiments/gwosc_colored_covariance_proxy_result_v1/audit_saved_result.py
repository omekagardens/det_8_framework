"""Independent RI90 saved-result algebra auditor; no work at import.

Only stdlib exact arithmetic over frozen saved bodies. No producer/validator
imports, coefficient reconstruction, physical covariance claim or authorization.
"""
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import struct
import sys

# Closed metadata literals transcribed by AST only; no producer implementation.
CONTRACT = {'BITS': 262144,
 'CERT_CHECKS': ('G_symmetry',
                 'H_symmetry_nonnegative',
                 'positive_LDL',
                 'LDL_reconstruction',
                 'two_sided_inverse',
                 'delta_identity',
                 'gamma_identity',
                 'rho_identity',
                 'rho_mathematical',
                 'rho_accuracy'),
 'DESIGN_PIN': {'bytes': 32470, 'sha256': '2a00cac0017f0b749ed958efef4d623143c97e33ba36c60454a65ef9069dc04e'},
 'GATE_IDS': ('admission:metadata',
              'admission:certificate',
              'scenario:H1:left',
              'scenario:H1:right',
              'scenario:L1:left',
              'scenario:L1:right',
              'completion:algebra'),
 'INPUTS': (('H1',
             'H-H1_LOSC_4_V2-1126259446-32.hdf5',
             1040592,
             '50441a42c13fc1f14e5c4ea5527f1515',
             '6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6'),
            ('L1',
             'L-L1_LOSC_4_V2-1126259446-32.hdf5',
             1007420,
             '361ae6a040a9fef7897b1e0124d5b0a1',
             '56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189')),
 'LIMITATIONS': ['The four saved Welch PSDs are empirical finite statistics, not established physical noise '
                 'covariance.',
                 'Each finite four-second circulant covariance is an explicit separate proxy postulate with '
                 'long-lag wraparound.',
                 'Public prior-access development inputs are not blind or protected validation; off-event names '
                 'an exclusion only.',
                 'Nominal V2/C02 strain has blank literal Yunits; L1 NO_CW_HW_INJ is clear throughout all 32 '
                 'seconds.',
                 'No stationarity, signal-free interval, Gaussianity, detector independence or calibrated '
                 'covariance is established.',
                 'Loewner endpoints bound quadratic forms; only diagonal and trace pairs are scalar variance '
                 'intervals.',
                 'A zero non-DC lower eigenvalue need not make output covariance singular; unresolved ranks '
                 'remain unresolved.',
                 'Held RI73 operator proof is prior accepted evidence; no adjoint reconstruction or predecessor '
                 'rerun is claimed.',
                 'No colored covariance entries, inverse, whitening, residual score, SNR, p-value or chi-square '
                 'law is computed.',
                 'Calibration, mean/template, detector response, timing, noise-estimation uncertainty and a '
                 'native forward map remain open; RET stays paused.'],
 'RECOVERY_PIN': {'bytes': 16293, 'sha256': 'be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0'},
 'RI37_PIN': {'bytes': 31096, 'sha256': 'a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80'},
 'RI73_CERT_KEYS': ('mathematical_gate',
                    'accuracy_gate',
                    'rho_limit',
                    'G',
                    'H',
                    'delta',
                    'eta2',
                    'ldl',
                    'inverse',
                    'left_inverse_product',
                    'right_inverse_product',
                    'gamma',
                    'rho',
                    'status',
                    'rank',
                    'inverse_error_norm_bound',
                    'inverse_lower',
                    'inverse_upper'),
 'RI73_DEPENDENCIES': {'check60': {'bytes': 38088,
                                   'path': 'gwosc_context_operator_v2/check.py',
                                   'sha256': 'a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02'},
                       'coefficients': {'bytes': 7698,
                                        'path': 'gwosc_nominal_processing_v1/COEFFICIENTS.json',
                                        'sha256': '700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0'},
                       'design': {'bytes': 29545,
                                  'path': 'gwosc_noise_operator_covariance_v1/DESIGN.md',
                                  'sha256': '08e6e99d0f884e26b9b4a2422789431d6d6acf077dbb751dd73144b5c6409cd6'},
                       'engine': {'bytes': 30531,
                                  'path': 'gwosc_context_operator_v2/operator.py',
                                  'sha256': 'ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af'},
                       'failed_predecessor': {'bytes': 161816,
                                              'path': 'gwosc_context_operator_v1/QUALIFICATION_REPORT.json',
                                              'sha256': '7dfbc8cac7e631a9c3663bca2b288b134d6cea03f1d0ca14c8334746761a808a'},
                       'filtering': {'bytes': 8805,
                                     'path': 'gwosc_nominal_processing_v1/filtering.py',
                                     'sha256': '9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be'},
                       'noise_design': {'bytes': 24027,
                                        'path': 'gwosc_context_noise_v1/DESIGN.md',
                                        'sha256': '74581df2266277b5ff12c9d45d110baf191f99dfbc7db8ea4b3810affa914921'},
                       'oracle': {'bytes': 9484,
                                  'path': 'gwosc_context_operator_v1/oracle.py',
                                  'sha256': '37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651'},
                       'prior_design': {'bytes': 21702,
                                        'path': 'gwosc_context_sensitivity_v1/DESIGN.md',
                                        'sha256': 'e672cea6c5f06c5927b54b0021636793c14b01e8efe57aa8e719fd464a527e45'},
                       'prior_qualification': {'bytes': 107468,
                                               'path': 'gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json',
                                               'sha256': '2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3'},
                       'qualification60': {'bytes': 9413345,
                                           'path': 'gwosc_context_operator_v2/QUALIFICATION_REPORT.json',
                                           'sha256': '1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f'},
                       'recipe': {'bytes': 14014,
                                  'path': 'gwosc_nominal_display_v1/RECIPE.md',
                                  'sha256': '872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a'},
                       'reference': {'bytes': 7253,
                                     'path': 'gwosc_nominal_processing_v1/reference.py',
                                     'sha256': 'c8cffaac8bf0c1647a120ecb00ba1505ef69b60f80cda653d60b2a2f7e9da305'},
                       'window_design': {'bytes': 19255,
                                         'path': 'gwosc_observed_context_v1/DESIGN.md',
                                         'sha256': '636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2'}},
 'RI73_GATE_IDS': ('fixture:fir',
                   'fixture:cancellation',
                   'fixture:singleton',
                   'fixture:offdiagonal_small',
                   'fixture:offdiagonal_large',
                   'fixture:failed_gate',
                   'fixture:midpoint',
                   'fixture:rank_ambiguity',
                   'fixture:singular',
                   'fixture:output_law',
                   'refusal:float_endpoint',
                   'refusal:bool_endpoint',
                   'refusal:nonfinite_endpoint',
                   'refusal:reversed_interval',
                   'refusal:negative_radius',
                   'refusal:matrix_rows',
                   'refusal:bool_dimension',
                   'refusal:bool_row_dimension',
                   'refusal:matrix_columns',
                   'refusal:ragged_box',
                   'refusal:asymmetric_gram',
                   'refusal:asymmetric_error',
                   'refusal:negative_error',
                   'refusal:negative_pivot',
                   'refusal:wrong_ldl',
                   'refusal:wrong_inverse',
                   'refusal:wrong_delta',
                   'refusal:wrong_gamma',
                   'refusal:incorrect_rank',
                   'refusal:bool_rank',
                   'refusal:wrong_mp1',
                   'refusal:wrong_mp2',
                   'refusal:wrong_mp3',
                   'refusal:off_support',
                   'refusal:negative_rho',
                   'refusal:rho_at_one',
                   'refusal:negative_output_error',
                   'refusal:unqualified_cdf',
                   'refusal:cdf_series_domain',
                   'refusal:negative_cdf_argument',
                   'refusal:estimated_covariance',
                   'refusal:colored_covariance',
                   'refusal:fraction_numerator_cap',
                   'refusal:fraction_denominator_cap',
                   'refusal:operation_result_cap',
                   'refusal:hex_length',
                   'refusal:hex_plus',
                   'refusal:hex_negative_zero',
                   'refusal:hex_leading_zero',
                   'refusal:hex_denominator_zero',
                   'refusal:hex_unreduced',
                   'refusal:work_cap',
                   'refusal:work_bool',
                   'refusal:output_cap',
                   'refusal:duplicate_json',
                   'refusal:nonfinite_json',
                   'refusal:overflow_json',
                   'refusal:changed_snapshot',
                   'refusal:bool_pin',
                   'refusal:changed_runtime',
                   'refusal:changed_runtime_build',
                   'refusal:failed_receipt',
                   'refusal:incomplete_receipt',
                   'refusal:changed_receipt_engine',
                   'refusal:changed_arithmetic',
                   'refusal:wrong_padding',
                   'refusal:bool_padding',
                   'refusal:changed_manifest_coefficient',
                   'refusal:changed_manifest_stage_order',
                   'refusal:changed_manifest_padding',
                   'refusal:missing_rows',
                   'refusal:wrong_rows',
                   'refusal:wrong_snapshot_shape',
                   'refusal:missing_expected_summaries',
                   'integration:reconstruction',
                   'integration:gram',
                   'integration:mathematical',
                   'integration:accuracy',
                   'integration:cross',
                   'probe:zero',
                   'probe:constant',
                   'probe:0',
                   'probe:1',
                   'probe:27',
                   'probe:805',
                   'probe:1384',
                   'probe:2741',
                   'probe:2767',
                   'probe:2768',
                   'integration:law',
                   'integration:final_custody',
                   'completion:custody'),
 'RI73_PIN': {'bytes': 11180937, 'sha256': '3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe'},
 'RI73_SOURCE_PIN': {'bytes': 68018, 'sha256': '574f5f1b8900221a47bc30ea62e6bed378a8fd1c8b4aa904e0549ade8ceb2887'},
 'RI73_TOP_KEYS': ('schema_version',
                   'mode',
                   'status',
                   'full_integration_qualified',
                   'source_identity',
                   'dependencies',
                   'runtime',
                   'inherited_arithmetic_contract',
                   'resource_contract',
                   'model',
                   'dimensions',
                   'rows',
                   'sample_spacing',
                   'gate_inventory',
                   'gate_counts',
                   'gates',
                   'deterministic_fixture_admission_passed',
                   'sampling_performed',
                   'admitted_coefficient_design_requested',
                   'reconstructed_rows_admitted',
                   'exact_scalar_encoding',
                   'scope'),
 'RI78_PIN': {'bytes': 24390, 'sha256': '3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce'},
 'RI80_PIN': {'bytes': 63464716, 'sha256': 'f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d'},
 'RI83_LIMITATIONS': ['Known public development inputs with prior display and context access; not blind/protected '
                      'validation.',
                      'Nominal released V2/C02 strain; literal Yunits is empty; no extra calibration correction '
                      'or uncertainty band.',
                      'L1 NO_CW_HW_INJ is clear throughout; continuous-wave injection absence/effect is not '
                      'established.',
                      'Off-event names the fixed exclusion only; short overlapping sides have unequal seven/six '
                      'segment counts.',
                      'Finite descriptive spectra do not establish signal-free data, stationarity, Gaussianity or '
                      'detector independence.',
                      'Estimated spectra are not known covariance, unit-white covariance, whitening, a chi-square '
                      'law or significance.',
                      'Calibration/timing/mean-response/noise-estimation premises and a native forward map remain '
                      'separate prerequisites.',
                      'Retained bins below 10 Hz have no added calibrated physical interpretation; no RET work is '
                      'implied.'],
 'RI83_PIN': {'bytes': 38952074, 'sha256': 'e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f'},
 'ROWS': (0, 1, 27, 805, 1384, 2741, 2767, 2768),
 'RUNTIME_KEYS': ('versions',
                  'python_implementation',
                  'python_build',
                  'operating_system',
                  'os_release',
                  'os_version',
                  'machine',
                  'byte_order',
                  'hdf5_version',
                  'numpy_configuration'),
 'SCENARIOS': ('H1:left', 'H1:right', 'L1:left', 'L1:right'),
 'VERSIONS': {'h5py': '3.12.1', 'numpy': '2.1.3', 'python': '3.11.6', 'scipy': '1.14.1'}}

SOURCE_PINS = {
 'design': CONTRACT['DESIGN_PIN'],
 'consumer': {'bytes':39228,'sha256':'441d335ac06a54d69182a7da21e52f8cabac2ff9f2d5aca345fc35499843773a'},
 'validator': {'bytes':19544,'sha256':'16fb31be704e7bdec6b7cbf83e88c9500440113d2a7abaadb41eba4c11f46558'},
 'qualifier': {'bytes':51042,'sha256':'86d1f3ea54264d97e92dc20b44459420e15926a5a6b43617823c79115298da37'},
 'implementation': {'bytes':16470,'sha256':'f27ac481d857df3caeacd9c71341439a90fc5d41fe210c82619b36997fc29e8f'},
}

class AuditFailure(ValueError):
    pass


def need(condition, label):
    if not condition:
        raise AuditFailure(label)


def canonical_parts(value):
    for text in json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False).iterencode(value):
        yield text.encode('ascii')
    yield b'\n'


def object_pin(value):
    h, count = hashlib.sha256(), 0
    for chunk in canonical_parts(value):
        h.update(chunk); count += len(chunk)
    return {'bytes':count, 'sha256':h.hexdigest()}


def body_pin(body):
    need(type(body) is bytes, 'immutable body required')
    return {'bytes':len(body), 'sha256':hashlib.sha256(body).hexdigest()}


def fields(value, names, label):
    need(type(value) is dict and set(value) == set(names), label + ': closed fields differ')


def exact(actual, expected, label):
    need(type(actual) is type(expected), label + ': type differs')
    if type(expected) is dict:
        need(actual.keys() == expected.keys(), label + ': fields differ')
        for key in expected: exact(actual[key], expected[key], label + '/' + key)
    elif type(expected) is list:
        need(len(actual) == len(expected), label + ': length differs')
        for i,(a,b) in enumerate(zip(actual,expected)): exact(a,b,label+'/'+str(i))
    else:
        need(actual == expected, label + ': value differs')


def valid_pin(pin, label):
    fields(pin, ('bytes','sha256'), label)
    need(type(pin['bytes']) is int and pin['bytes'] > 0 and type(pin['sha256']) is str and
         re.fullmatch('[0-9a-f]{64}', pin['sha256']) is not None, label + ': malformed identity')


def parse(body, scientific_result=False):
    def pairs(rows):
        out = {}
        for key,value in rows:
            need(key not in out, 'duplicate JSON key'); out[key] = value
        return out
    def invalid(text):
        raise AuditFailure('nonfinite JSON: ' + text)
    def decimal(text):
        need(not scientific_result, 'decimal literal in exact scientific result')
        value = float(text); need(math.isfinite(value), 'overflowing JSON number'); return value
    return json.loads(body.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=invalid, parse_float=decimal)


def bounded(value):
    need(type(value) is F and max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= CONTRACT['BITS'],
         '262144-bit exact-rational resource bound')
    return value


def plus(a,b): return bounded(bounded(a)+bounded(b))
def minus(a,b): return bounded(bounded(a)-bounded(b))
def times(a,b): return bounded(bounded(a)*bounded(b))
def divide(a,b):
    need(b != 0, 'zero divisor'); return bounded(bounded(a)/bounded(b))
def total(values):
    value=F(0)
    for x in values: value=plus(value,x)
    return value


def rational(pair):
    need(type(pair) is list and len(pair)==2, 'rational pair shape')
    patterns=('(?:0|-?[1-9a-f][0-9a-f]*)','[1-9a-f][0-9a-f]*')
    for i,text in enumerate(pair):
        need(type(text) is str and len(text) <= (CONTRACT['BITS']+3)//4+(i==0), 'rational text bound')
        need(re.fullmatch(patterns[i],text) is not None, 'canonical rational text')
    numerator,denominator=int(pair[0],16),int(pair[1],16)
    need(max(abs(numerator).bit_length(),denominator.bit_length()) <= CONTRACT['BITS'], 'parsed rational bound')
    value=bounded(F(numerator,denominator)); exact(pair,encode(value),'reduced rational'); return value


def encode(value):
    if type(value) is F:
        value=bounded(value); return [format(value.numerator,'x'),format(value.denominator,'x')]
    if type(value) in (list,tuple): return [encode(x) for x in value]
    if type(value) is dict: return {k:encode(v) for k,v in value.items()}
    return value


def matrix(value):
    need(type(value) is list and len(value)==8, 'eight matrix rows')
    out=[]
    for row in value:
        need(type(row) is list and len(row)==8, 'eight matrix columns')
        out.append([rational(x) for x in row])
    return out


def identity(): return [[F(int(i==j)) for j in range(8)] for i in range(8)]
def product(a,b): return [[total(times(a[i][k],b[k][j]) for k in range(8)) for j in range(8)] for i in range(8)]


def derive_ldl(g):
    # Independent exact Schur updates; retain a unit lower factor and pivots.
    schur=[row[:] for row in g]; lower=identity(); pivots=[]
    for k in range(8):
        pivot=schur[k][k]; need(pivot>0,'nonpositive independent LDL pivot'); pivots.append(pivot)
        for i in range(k+1,8): lower[i][k]=divide(schur[i][k],pivot)
        for i in range(k+1,8):
            for j in range(k+1,8):
                schur[i][j]=minus(schur[i][j],times(times(lower[i][k],pivot),lower[j][k]))
    return lower,pivots


def derive_inverse(g):
    # Eight-row exact Gauss-Jordan elimination, independent of the supplied V.
    rows=[g[i][:]+identity()[i] for i in range(8)]
    for k in range(8):
        pivot_row=next((i for i in range(k,8) if rows[i][k]!=0),None)
        need(pivot_row is not None,'singular held Gram')
        rows[k],rows[pivot_row]=rows[pivot_row],rows[k]
        pivot=rows[k][k]; rows[k]=[divide(x,pivot) for x in rows[k]]
        for i in range(8):
            if i != k:
                factor=rows[i][k]
                rows[i]=[minus(x,times(factor,y)) for x,y in zip(rows[i],rows[k])]
    exact(encode([row[:8] for row in rows]),encode(identity()),'independent elimination left half')
    return [row[8:] for row in rows]


def certificate(prior):
    fields(prior, CONTRACT['RI73_TOP_KEYS'], 'RI73 top')
    for key,value in {'schema_version':'ri73-unit-white-operator-covariance-v1','mode':'fixed_operator_covariance',
       'status':'fixed_operator_covariance_passed','full_integration_qualified':True,
       'deterministic_fixture_admission_passed':True,'sampling_performed':False,
       'admitted_coefficient_design_requested':True,'reconstructed_rows_admitted':True,
       'dimensions':{'N':2769,'L':4096,'T':10961},'rows':list(CONTRACT['ROWS']),
       'sample_spacing':encode(F(1,4096)),'source_identity':CONTRACT['RI73_SOURCE_PIN'],
       'dependencies':CONTRACT['RI73_DEPENDENCIES'],
       'model':{'kind':'known_synthetic_unit_white','mean':'zero','covariance':'I_T','input_dimension':10961,'output_dimension':8},
       'gate_inventory':list(CONTRACT['RI73_GATE_IDS']), 'gate_counts':{'total':92,'passed':92,'failed':0}}.items():
        exact(prior[key],value,'held prior '+key)
    fields(prior['runtime'],CONTRACT['RUNTIME_KEYS'],'held runtime')
    exact(prior['runtime']['versions'],CONTRACT['VERSIONS'],'held versions')
    exact(prior['runtime']['python_implementation'],'CPython','held implementation')
    exact(prior['runtime']['hdf5_version'],'1.12.2','held HDF5')
    need(type(prior['gates']) is list and len(prior['gates'])==92,'complete held gates')
    selected=None
    for gate,name in zip(prior['gates'],CONTRACT['RI73_GATE_IDS']):
        fields(gate,('id','passed','detail'),'held gate'); exact(gate['id'],name,'held ordered gate'); exact(gate['passed'],True,'held gate pass')
        need(type(gate['detail']) is dict,'held gate detail')
        if name=='integration:gram':
            fields(gate['detail'],('certificate','M_identity','R_identity'),'held Gram detail')
            selected=gate['detail']['certificate']
    need(selected is not None,'unique held certificate')
    fields(selected,CONTRACT['RI73_CERT_KEYS'],'held certificate')
    for key,value in {'mathematical_gate':True,'accuracy_gate':True,'rho_limit':encode(F(1,10**12)),
                      'status':'certified','rank':8}.items(): exact(selected[key],value,'held certificate '+key)
    g,h,v=(matrix(selected[name]) for name in ('G','H','inverse'))
    need(all(g[i][j]==g[j][i] and h[i][j]==h[j][i] for i in range(8) for j in range(8)),'G/H symmetry')
    need(all(x>=0 for row in h for x in row),'entrywise H nonnegativity')
    lower,pivots=derive_ldl(g); inverse=derive_inverse(g)
    reconstruction=[[total(times(times(lower[i][k],pivots[k]),lower[j][k]) for k in range(8)) for j in range(8)] for i in range(8)]
    exact(encode(reconstruction),encode(g),'independent LDL reconstruction')
    ldl={'lower':encode(lower),'pivots':encode(pivots),'reconstruction':encode(reconstruction)}
    exact(selected['ldl'],{'positive':True,**ldl},'complete held LDL')
    exact(encode(v),encode(inverse),'independently solved inverse')
    left,right=product(g,v),product(v,g)
    exact(encode(left),encode(identity()),'left inverse residual'); exact(encode(right),encode(identity()),'right inverse residual')
    exact(selected['left_inverse_product'],encode(left),'saved left inverse product')
    exact(selected['right_inverse_product'],encode(right),'saved right inverse product')
    delta=max(total(row) for row in h); gamma=max(total(bounded(abs(x)) for x in row) for row in v); rho=times(delta,gamma)
    for key,value in {'delta':delta,'gamma':gamma,'rho':rho}.items(): exact(selected[key],encode(value),'derived '+key)
    need(0<=rho<=F(1,10**12) and rho<1,'unchanged mathematical and usefulness rho gates')
    need(rational(selected['eta2'])>=0,'nonnegative held coefficient radius premise')
    exact(selected['inverse_error_norm_bound'],encode(divide(times(rho,gamma),minus(F(1),rho))),'held inverse-error algebra')
    for key,denominator in (('inverse_lower',plus(F(1),rho)),('inverse_upper',minus(F(1),rho))):
        exact(selected[key],encode([[divide(x,denominator) for x in row] for row in v]),'held inverse enclosure '+key)
    projected={'source_gate':'integration:gram','source_model':'known_synthetic_unit_white','G':encode(g),'H':encode(h),
               'V':encode(v),'ldl':ldl,'delta':encode(delta),'gamma':encode(gamma),'rho':encode(rho),'checks':list(CONTRACT['CERT_CHECKS'])}
    return projected,g,rho


def binary64(text):
    need(type(text) is str and len(text)<=32,'binary64 text shape')
    try: value=float.fromhex(text)
    except (ValueError,OverflowError) as exc: raise AuditFailure('invalid binary64') from exc
    need(math.isfinite(value) and value.hex()==text and value>=0,'canonical finite nonnegative binary64')
    return value,bounded(F.from_float(value))


def psd(record):
    fields(record,('dtype','shape','values_hex','sha256'),'PSD record'); exact(record['dtype'],'<f8','PSD dtype');exact(record['shape'],[8193],'PSD dimensions')
    need(type(record['values_hex']) is list and len(record['values_hex'])==8193,'all 8193 PSD bins')
    values=[]; digest=hashlib.sha256()
    for text in record['values_hex']:
        value,r= binary64(text);values.append(r);digest.update(struct.pack('<d',value))
    exact(record['sha256'],digest.hexdigest(),'complete PSD byte identity')
    return values


def side_contract(side):
    if side=='left': return {'interval':[0,65536],'starts':[0,8192,16384,24576,32768,40960,49152],
        'count':7,'used_interval':[0,65536],'unused_intervals':[]}
    need(side=='right','only two held sides')
    return {'interval':[69632,131072],'starts':[69632,77824,86016,94208,102400,110592],
        'count':6,'used_interval':[69632,126976],'unused_intervals':[[126976,131072]]}


def metadata_report(detectors):
    return {'schema_version':'gwosc-fixed-pair-qualification-v1','status':'identity_and_structure_verified',
      'event':'GW150914','strain_product_version':'V2','detectors':detectors,
      'interpretation_boundary':{
       'dimensionless_strain':'publisher interpretation; the literal strain Yunits attribute is empty',
       'C02_calibration':'external publisher release identification, not a literal calibration header',
       'calibration_uncertainty':'applicable artifact values, interpolation and correlations remain unqualified',
       'scientific_fit_readiness':'not established by identity, structure, finite samples or quality flags',
       'prior_access':'known public reference event; not blind evaluation data',
       'native_gravity_comparison':'no native forward law or DET-versus-GR inference supplied'}}


def retained_spectra(report):
    fields(report,('schema','method','inputs','frequency_hz','window','detectors','checks','limitations'),'RI83 top')
    exact(report['schema'],'ri78-off-event-spectra-v1','RI83 schema')
    method={'design_pin':CONTRACT['RI78_PIN'],'fs':4096,'segment_length':16384,'stride':8192,'nfft':16384,
      'exclusion':[65536,69632],'sides':{s:side_contract(s) for s in ('left','right')},'bins':8193,
      'endpoint_weights':[1,1],'interior_weight':2,'delta_f_hex':'0x1.0000000000000p-2',
      'detrend':'arithmetic_per_segment_mean_before_window','window':'periodic_hann_sym_false',
      'fft':'numpy_rfft_backward','scaling':'density_fs_times_actual_window_energy','average':'arithmetic_mean_periodograms',
      'asd':'sqrt_mean_psd','eps_hex':'0x1.0000000000000p-52','tau_hex':'0x1.0000000000000p-40','sqrt_relative_budget_hex':'0x1.0000000000000p-49'}
    exact(report['method'],method,'whole held spectral method');exact(report['limitations'],CONTRACT['RI83_LIMITATIONS'],'held spectral limitations')
    need(psd(report['frequency_hz'])==[F(k,4) for k in range(8193)],'every fixed frequency coordinate')
    need(type(report['inputs']) is list and len(report['inputs'])==2,'two original inputs');metadata=[]
    for row,known in zip(report['inputs'],CONTRACT['INPUTS']):
        detector,filename,size,md5,sha=known
        fields(row,('bytes','detector','filename','inspector_report_pin','md5','recovery_handoff_pin','ri37_detector','sha256','url'),'input context')
        for key,value in {'detector':detector,'filename':filename,'bytes':size,'md5':md5,'sha256':sha,
            'url':'https://gwosc.org/GW150914data/'+filename,'inspector_report_pin':CONTRACT['RI37_PIN'],
            'recovery_handoff_pin':CONTRACT['RECOVERY_PIN']}.items(): exact(row[key],value,'input '+key)
        metadata.append(row['ri37_detector'])
    exact(object_pin(metadata_report(metadata)),CONTRACT['RI37_PIN'],'complete held RI37 metadata')
    fields(report['checks'],('identity','detectors'),'RI83 checks')
    exact(report['checks']['identity'],{'inspector_report_pin':CONTRACT['RI37_PIN'],'recovery_handoff_pin':CONTRACT['RECOVERY_PIN'],
          'qualification_report_pin':CONTRACT['RI80_PIN'],'fixed_dimensions_indices_and_flags':True},'held identity checks')
    need(type(report['detectors']) is list and len(report['detectors'])==2,'two spectral detectors');out=[]
    for d,name in enumerate(('H1','L1')):
        detector=report['detectors'][d];fields(detector,('detector','sides'),'spectral detector');exact(detector['detector'],name,'detector order')
        need(type(detector['sides']) is list and len(detector['sides'])==2,'two held sides')
        for s,label in enumerate(('left','right')):
            side=detector['sides'][s];fields(side,('side','interval','starts','count','used_interval','unused_intervals','segments','mean_psd','asd','q','psd_unit','asd_unit'),'spectral side')
            exact(side['side'],label,'side order');spec=side_contract(label)
            for key,value in spec.items():exact(side[key],value,'held side '+key)
            exact(side['psd_unit'],'nominal_strain_squared_per_Hz','PSD unit');exact(side['asd_unit'],'nominal_strain_per_sqrt_Hz','ASD unit')
            need(type(side['segments']) is list and len(side['segments'])==spec['count'],'segment count')
            for segment,start in zip(side['segments'],spec['starts']):
                fields(segment,('start','end','gps_offset_numerators','gps_offset_denominator','flag_rows','dq_masks','injection_masks','mean','q','raw_sha256','demeaned_sha256','windowed_sha256','psd'),'segment')
                for key,value in {'start':start,'end':start+16384,'gps_offset_numerators':[start,start+16384],'gps_offset_denominator':4096,
                    'flag_rows':list(range(start//4096,(start+16384)//4096)),'dq_masks':[127]*4,'injection_masks':[(31,23)[d]]*4}.items():exact(segment[key],value,'segment context '+key)
            values=psd(side['mean_psd']);_,saved_q=binary64(side['q'])
            context={**spec,'psd_unit':side['psd_unit'],'asd_unit':side['asd_unit'],'prior_access':'known_public_development',
                     'Yunits':'','injection_mask':(31,23)[d],'dq_mask':127,'NO_CW_HW_INJ':d==0}
            source={'id':name+':'+label,'detector':name,'side':label,'source_pointer':f'/detectors/{d}/sides/{s}/mean_psd',
                    'source_record':side['mean_psd'],'saved_q_hex':side['q'],'context':context}
            out.append((source,values,saved_q))
    return out


def spectral_envelope(values,g,rho):
    # Endpoint modes have multiplicity one; paired interior modes have two.
    one_sided=[times(F(4096 if k in (0,8192) else 2048),p) for k,p in enumerate(values)]
    non_dc=one_sided[1:]; ell=min(non_dc); upper=max(non_dc)
    q=times(F(1,4),total(values))
    # Independent trace identity includes the duplicated interior modes and DC.
    full_trace=plus(plus(one_sided[0],one_sided[-1]),times(F(2),total(one_sided[1:-1])))
    need(divide(full_trace,F(16384))==q,'circulant trace/integrated PSD identity')
    positive=sum(x>0 for x in one_sided[1:-1]);rank_non_dc=2*positive+int(one_sided[-1]>0)
    rank_upper=min(8,rank_non_dc)
    status='positive_definite_rank8' if ell>0 else 'zero_rank0' if upper==0 else 'unresolved_by_envelope'
    low=times(ell,minus(F(1),rho));high=times(upper,plus(F(1),rho))
    lower=[[times(low,x) for x in row] for row in g];higher=[[times(high,x) for x in row] for row in g]
    return {'lambda_dc':one_sided[0],'lambda_nyquist':one_sided[-1],'non_dc_eigenvalues':non_dc,'q_proxy':q,
      'ell':ell,'u':upper,'minimum_indices':[i for i in range(1,8193) if one_sided[i]==ell],
      'maximum_indices':[i for i in range(1,8193) if one_sided[i]==upper],
      'positive_interior_count':positive,'zero_interior_count':8191-positive,'non_dc_rank':rank_non_dc,
      'spectral_rank':rank_non_dc+int(one_sided[0]>0),'rank_status':status,'rank_upper':rank_upper,'singularity_proved':rank_upper<8,
      'lower':lower,'upper':higher,'diagonal':[[lower[i][i],higher[i][i]] for i in range(8)],
      'trace':[total(lower[i][i] for i in range(8)),total(higher[i][i] for i in range(8))]}


def provenance(value):
    fields(value,('sources','inputs','acceptance','runtime'),'expected provenance')
    exact(value['sources'],SOURCE_PINS,'all fixed scientific source identities')
    exact(value['inputs'],{'ri83':CONTRACT['RI83_PIN'],'ri73':CONTRACT['RI73_PIN']},'fixed actual input identities')
    fields(value['acceptance'],('ri83','ri73','ri86','qualification'),'accepted predecessor identities')
    for key,pin in value['acceptance'].items():valid_pin(pin,'acceptance '+key)
    fields(value['runtime'],('inventory','fingerprint','interpreter'),'genuine runtime identities')
    for key,pin in value['runtime'].items():valid_pin(pin,'runtime '+key)


def audit_saved_result(result_body, ri83_body, ri73_body, result_identity, expected_provenance):
    valid_pin(result_identity,'frozen actual result')
    # All three byte identities precede every scientific JSON parse.
    for body,expected,label in ((result_body,result_identity,'RI90 result'),(ri83_body,CONTRACT['RI83_PIN'],'RI83'),(ri73_body,CONTRACT['RI73_PIN'],'RI73')):
        exact(body_pin(body),expected,label+' complete bytes')
    provenance(expected_provenance)
    actual=parse(result_body,True);saved83=parse(ri83_body);saved73=parse(ri73_body)
    exact(object_pin(actual),result_identity,'canonical exact result bytes')
    exact(object_pin(saved73['runtime']),expected_provenance['runtime']['fingerprint'],'held/genuine complete runtime fingerprint')
    projected,g,rho=certificate(saved73);sources=retained_spectra(saved83);scenarios=[];summaries=[]
    for source,values,saved_q in sources:
        derived=spectral_envelope(values,g,rho);difference=minus(derived['q_proxy'],saved_q)
        scenarios.append({**source,'q_difference':difference,'derived':derived})
        summaries.append({'id':source['id'],'source_psd_sha256':source['source_record']['sha256'],'bins_checked':8193,
          'non_dc_eigenvalues_checked':8192,'matrix_entries_checked':128,'ell':derived['ell'],'u':derived['u'],
          'minimum_indices':derived['minimum_indices'],'maximum_indices':derived['maximum_indices'],
          'q_proxy':derived['q_proxy'],'q_difference':difference,'spectral_rank':derived['spectral_rank'],
          'non_dc_rank':derived['non_dc_rank'],'rank_status':derived['rank_status'],'rank_upper':derived['rank_upper'],
          'singularity_proved':derived['singularity_proved'],'diagonal':derived['diagonal'],'trace':derived['trace']})
    expected=encode({'schema':'ri86-colored-proxy-envelope-v1','phase':'fixed_saved_application','status':'all_gates_passed',
      'model':'postulated_finite_circulant_from_empirical_psd','dimensions':{'M':16384,'N':2769,'L':4096,'T':10961,'output':8},
      'fs':F(4096),'df':F(1,4),'scenario_order':list(CONTRACT['SCENARIOS']),'rows':list(CONTRACT['ROWS']),
      'provenance':expected_provenance,'certificate':projected,'scenarios':scenarios,
      'gates':{'inventory':list(CONTRACT['GATE_IDS']),'counts':{'total':7,'passed':7,'failed':0},
               'results':[{'id':name,'passed':True} for name in CONTRACT['GATE_IDS']]},'limitations':CONTRACT['LIMITATIONS']})
    exact(actual,expected,'entire independently reconstructed output')
    for body,expected_pin in ((result_body,result_identity),(ri83_body,CONTRACT['RI83_PIN']),(ri73_body,CONTRACT['RI73_PIN'])):
        exact(body_pin(body),expected_pin,'immutable body remains fixed')
    return encode({'schema':'ri90-independent-saved-algebra-audit-v1','status':'all_saved_fields_independently_match',
      'input_identities':{'result':result_identity,'ri83':CONTRACT['RI83_PIN'],'ri73':CONTRACT['RI73_PIN']},
      'reconstructed_result_identity':object_pin(expected),'expected_provenance':expected_provenance,
      'certificate':{'projection_identity':object_pin(projected),'dimension':8,'positive_pivots':8,
        'independent_LDL_reconstruction':True,'independently_solved_inverse':True,'left_inverse_residual_zero':True,
        'right_inverse_residual_zero':True,'delta':rational(projected['delta']),'gamma':rational(projected['gamma']),
        'rho':rho,'fixed_rho_limit':F(1,10**12),'rho_accuracy_passed':True},'scenarios':summaries,
      'counts':{'scenarios':4,'source_psd_bins':32772,'non_dc_eigenvalues':32768,'matrix_endpoint_entries':512,
                'diagonal_endpoint_values':64,'trace_endpoint_values':8,'saved_q_differences':4},
      'premises':['Both published predecessor bodies are fixed by their accepted byte identities.',
        'Their acquisition, historical 92-gate operator proof, accepted qualification and original source/runtime custody are external accepted premises.',
        'Local exact checks prove only the projected numerical Gram/error/inverse certificate identities; coefficient reconstruction and the H enclosure are not rerun.',
        'DC exclusion uses the accepted held operator theorem A1=0; it is not inferred from estimated PSD data.',
        'Each finite circulant covariance is the declared separate proxy postulate. Empirical spectra are not established physical covariance.',
        'Root-frozen expected provenance and supervised invocation must be independently admitted; this auditor does not authorize itself.'],
      'limitations':CONTRACT['LIMITATIONS']})


def file_snapshot(path, expected):
    valid_pin(expected,'snapshot identity');path=Path(path)
    need(path.is_absolute() and path==path.resolve(),'literal nonsymlink absolute snapshot path')
    before=path.lstat();need(stat.S_ISREG(before.st_mode) and before.st_size==expected['bytes'],'snapshot regular/size')
    with path.open('rb') as stream:
        opened=os.fstat(stream.fileno());need((before.st_dev,before.st_ino)==(opened.st_dev,opened.st_ino),'snapshot inode changed')
        body=stream.read(expected['bytes']+1);after=os.fstat(stream.fileno())
    final=path.lstat();key=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mtime_ns)
    need(key(before)==key(after)==key(final),'snapshot changed during read');exact(body_pin(body),expected,'snapshot bytes')
    return body


def main():
    need(len(sys.argv)==4,'usage: audit_saved_result.py AUDIT_INPUT.json BYTES SHA256')
    need(sys.argv[2].isdigit() and str(int(sys.argv[2]))==sys.argv[2],'canonical descriptor byte count')
    descriptor_pin={'bytes':int(sys.argv[2]),'sha256':sys.argv[3]}
    body=file_snapshot(sys.argv[1],descriptor_pin);descriptor=parse(body)
    fields(descriptor,('schema','phase','files','expected_provenance','custody_premise'),'audit input descriptor')
    exact(descriptor['schema'],'ri90-independent-saved-audit-input-v1','audit input schema')
    exact(descriptor['phase'],'fixed_saved_application','audit input phase')
    exact(object_pin(descriptor),descriptor_pin,'canonical audit descriptor')
    fields(descriptor['files'],('result','ri83','ri73'),'three fixed snapshots')
    valid_pin(descriptor['custody_premise'],'root accepted caller custody premise')
    paths=[];snapshots={}
    for name,row in descriptor['files'].items():
        fields(row,('path','bytes','sha256'),'snapshot row');need(type(row['path']) is str,'snapshot path text')
        paths.append(row['path']);snapshots[name]=file_snapshot(row['path'],{k:row[k] for k in ('bytes','sha256')})
    need(len(set(paths))==3 and str(Path(sys.argv[1])) not in paths,'distinct descriptor and scientific paths')
    result_pin={k:descriptor['files']['result'][k] for k in ('bytes','sha256')}
    report=audit_saved_result(snapshots['result'],snapshots['ri83'],snapshots['ri73'],result_pin,descriptor['expected_provenance'])
    for name,row in descriptor['files'].items():file_snapshot(row['path'],{k:row[k] for k in ('bytes','sha256')})
    file_snapshot(sys.argv[1],descriptor_pin)
    report['audit_input_descriptor']=descriptor_pin;report['accepted_caller_custody_premise']=descriptor['custody_premise']
    for chunk in canonical_parts(report):sys.stdout.buffer.write(chunk)
    sys.stdout.buffer.flush();os.fsync(sys.stdout.buffer.fileno())
    return 0


if __name__=='__main__':
    raise SystemExit(main())
