"""Unexecuted RI98 fabricated qualification. No imports of either implementation.

The admitted caller supplies captured primary and independently authored
validator modules. No actual RI96 body or other observed operand is opened.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import os
import struct

M, FS, Q = 16384, 4096, 1 << 256
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
ORDER = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
ARTIFACTS = ('ANALYTIC_CASES.json', 'FABRICATED_PROJECTION.json', 'FABRICATED_RESULT.json')
REFUSALS = (
    ('primary:actual_body_pin', 'INPUT'), ('primary:duplicate_json_key', 'SCHEMA'),
    ('primary:nonfinite_json', 'EXACT'), ('primary:unreduced_rational', 'EXACT'),
    ('primary:negative_zero_integer', 'EXACT'), ('primary:excessive_integer', 'RESOURCE'),
    ('primary:unsupported_domain', 'DOMAIN'), ('primary:wrong_row_order', 'ROW'),
    ('primary:missing_row', 'ROW'), ('primary:extra_row', 'ROW'),
    ('primary:missing_mode', 'MODE'), ('primary:extra_mode', 'MODE'), ('primary:stale_mode_identity', 'MODE'),
    ('primary:reversed_rectangle', 'INTERVAL'), ('primary:nyquist_imaginary_excludes_zero', 'INTERVAL'),
    ('primary:negative_alpha', 'ALPHA'), ('primary:psd_float_shape', 'PSD'), ('primary:psd_wrong_size', 'PSD'),
    ('primary:psd_missing_bin', 'PSD'),
    ('primary:psd_dtype', 'PSD'), ('primary:psd_byte_identity', 'PSD'),
    ('primary:negative_psd', 'PSD'), ('primary:nonfinite_psd', 'PSD'),
    ('primary:duplicate_mode_index', 'MODE'), ('primary:reordered_modes', 'MODE'), ('primary:wrong_pair_weight', 'MODE'),
    ('primary:negative_mode_term', 'MODE'), ('primary:changed_tie_inventory', 'BAND'),
    ('primary:changed_band_spread', 'BAND'), ('primary:negative_band_margin', 'BAND'),
    ('primary:reversed_prior', 'ENVELOPE'), ('primary:empty_intersection', 'ENVELOPE'),
    ('primary:changed_design_pin', 'SOURCE'), ('primary:fabricated_actual_context', 'PHASE'),
    ('primary:claimed_fabricated_qualification', 'PHASE'), ('primary:claimed_fabricated_custody', 'PHASE'),
    ('primary:changed_projection_pin', 'INPUT'), ('primary:unknown_projection_field', 'INPUT'),
    ('primary:changed_scenario_order', 'PSD'),
    ('validator:extra_top_key', 'SCHEMA'), ('validator:phase_substitution', 'PHASE'),
    ('validator:source_pin', 'PROVENANCE'), ('validator:method_float_dimension', 'DOMAIN'),
    ('validator:limitations', 'SCHEMA'), ('validator:gate_count_boolean', 'SCHEMA'),
    ('validator:gate_result_integer', 'SCHEMA'), ('validator:projection_identity', 'INPUT'),
    ('validator:mode_center', 'RESULT'), ('validator:mode_tau', 'RESULT'),
    ('validator:mode_alpha', 'RESULT'), ('validator:missing_lambda_weight', 'RESULT'),
    ('validator:nyquist_imaginary_alpha', 'RESULT'), ('validator:alpha_in_tau', 'RESULT'),
    ('validator:negative_raw_clipped', 'RESULT'), ('validator:band_width_changed', 'RESULT'),
    ('validator:undefined_ratio_number', 'RESULT'), ('validator:changed_final', 'RESULT'),
    ('validator:changed_source_identity', 'RESULT'), ('validator:canonical_roundtrip_whitespace', 'CANONICAL'),
)


class QualificationError(ValueError):
    pass


def check(ok, message):
    if not ok:
        raise QualificationError(message)


def equal(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    if type(a) in (list, tuple): return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def enc(x):
    if type(x) is F: return [format(x.numerator, 'x'), format(x.denominator, 'x')]
    if type(x) in (list, tuple): return [enc(v) for v in x]
    if type(x) is dict: return {k: enc(v) for k, v in x.items()}
    return x


def parts(value):
    for p in json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False).iterencode(value):
        yield p.encode('ascii')
    yield b'\n'


def body(value):
    return b''.join(parts(value))


def pin_bytes(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def pin(value):
    h, n = hashlib.sha256(), 0
    for p in parts(value): h.update(p); n += len(p)
    return {'bytes': n, 'sha256': h.hexdigest()}


def clone(value):
    # Only compact tiny fixtures or metadata use this; never a full production copy.
    return json.loads(body(value))


def psd(eigenvalues, size):
    values = [x / (FS if k in (0, size//2) else FS//2) for k, x in enumerate(eigenvalues)]
    floats = [float(x) for x in values]
    check(all(F.from_float(x) == y for x, y in zip(floats, values)), 'fixture PSD is exactly binary64')
    raw = b''.join(struct.pack('<d', x) for x in floats)
    return {'dtype': '<f8', 'shape': [size//2+1], 'values_hex': [x.hex() for x in floats],
            'sha256': hashlib.sha256(raw).hexdigest()}


def make_rows(images, alphas, size):
    records = []
    names = ROWS if size == M else range(len(images))
    for name, image, alpha in zip(names, images, alphas):
        rectangles = []
        for x, y, tr, ti in image:
            endpoints = [(x-tr)*Q, (x+tr)*Q, (y-ti)*Q, (y+ti)*Q]
            check(all(z.denominator == 1 for z in endpoints), 'exact fixture Q256 grid')
            rectangles.append([format(z.numerator, 'x') for z in endpoints])
        records.append({'row': name, 'alpha': enc(alpha), 'midpoint_modes': rectangles,
                        'mode_identity': pin(rectangles)})
    return records


def held_scenario(images, alphas, eigenvalues, size, prior=None):
    """Independent fixture construction from explicit RI92 matrix inequalities.

    Analytic scalar anchors below remain the qualification oracle. This helper
    constructs an internally coherent inherited band premise for those cases;
    it does not certify a real predecessor or invoke the primary implementation.
    """
    dim = len(images)
    cm = [[F(0) for _ in range(dim)] for _ in range(dim)]
    cp = [[F(0) for _ in range(dim)] for _ in range(dim)]
    hm = [[F(0) for _ in range(dim)] for _ in range(dim)]
    hp = [[F(0) for _ in range(dim)] for _ in range(dim)]
    extrema = []
    for index in range(size.bit_length()-1):
        first, stop = 1 << index, min(1 << (index+1), size//2+1)
        lo, hi = min(eigenvalues[first:stop]), max(eigenvalues[first:stop])
        extrema.append(enc({'index': index, 'ell': lo, 'u': hi,
                            'minimum_indices': [k for k in range(first, stop) if eigenvalues[k] == lo],
                            'maximum_indices': [k for k in range(first, stop) if eigenvalues[k] == hi]}))
        for k in range(first, stop):
            weight = 1 if k == size//2 else 2
            for i in range(dim):
                xi, yi, tri, tii = images[i][k]
                eri, eii = tri + alphas[i], tii + alphas[i]
                if k == size//2: yi, eii = F(0), F(0)
                for j in range(dim):
                    xj, yj, trj, tij = images[j][k]
                    erj, eij = trj + alphas[j], tij + alphas[j]
                    if k == size//2: yj, eij = F(0), F(0)
                    center = weight * (xi*xj+yi*yj)
                    error = weight * (abs(xi)*erj+eri*abs(xj)+eri*erj+
                                      abs(yi)*eij+eii*abs(yj)+eii*eij)
                    cm[i][j] += lo*center; cp[i][j] += hi*center
                    hm[i][j] += lo*error; hp[i][j] += hi*error
    dm, dp = max(map(sum, hm)), max(map(sum, hp))
    trace = [sum(cm[i][i] for i in range(dim))-dim*dm,
             sum(cp[i][i] for i in range(dim))+dim*dp]
    return enc({'id': ORDER[0], 'source_record': psd(eigenvalues, size), 'band_extrema': extrema,
                'C_minus': cm, 'C_plus': cp, 'delta_minus': dm, 'delta_plus': dp,
                'trace': trace, 'prior_trace': trace if prior is None else prior})


def analytic_fixtures():
    z = (F(0), F(0), F(0), F(0))
    pair = [[z, (F(1,2), F(-1,2), F(0), F(0)), (F(1), F(0), F(0), F(0))],
            [z, (F(1,2), F(1,2), F(0), F(0)), (F(-1), F(0), F(0), F(0))]]
    result = []
    for name, eigen, target in [('Q1', [7,2,5], 14), ('Q2', [3,3,3], 12),
                                 ('Q3', [0,2,0], 4), ('Q4', [0,0,5], 10), ('Q5', [7,0,0], 0)]:
        result.append((name, 4, pair, [F(0), F(0)], list(map(F, eigen)), None,
                       {'center': F(target), 'error': F(0), 'raw': [F(target), F(target)]}))
    for name, tau in [('Q6', F(0)), ('Q7', F(1,4))]:
        # The complete midpoint image of (3/2,-3/2,0,0), not Nyquist alone.
        image = [[z, (F(3,4), F(-3,4), F(0), F(0)), (F(3,2), F(0), tau, F(0))]]
        expected = {'center': F(9), 'error': F(7) if tau == 0 else F(45,4),
                    'error_tau': F(0) if tau == 0 else F(13,4),
                    'error_alpha': F(7) if tau == 0 else F(8),
                    'raw': [F(2), F(16)] if tau == 0 else [F(-9,4), F(81,4)]}
        result.append((name, 4, image, [F(1,2)], [F(0), F(0), F(4)],
                       None if tau == 0 else [F(4), F(16)], expected))
    q8 = [[z, z, (F(1), F(0), F(0), F(0)), (F(1), F(0), F(0), F(0)), z]]
    result.append(('Q8', 8, q8, [F(0)], [F(0),F(0),F(1),F(3),F(0)], None,
                   {'center': F(8), 'error': F(0), 'raw': [F(8),F(8)], 'band_spread': F(8), 'band_margin': F(0)}))
    q9 = [[z,z,(F(1),F(0),F(1),F(0)),z,z] if i < 2 else [z,z,z,z,z] for i in range(8)]
    result.append(('Q9', 8, q9, [F(0)]*8, [F(0),F(0),F(1),F(1),F(0)], None,
                   {'center': F(4), 'error': F(12), 'raw': [F(-8),F(16)],
                    'ri96_raw_band': [F(-92),F(100)], 'band_spread': F(0), 'band_margin': F(192)}))
    image = [[z, (F(3,2), F(-3,2), F(0), F(0)), (F(3), F(0), F(1,2), F(0))]]
    result.append(('Q11', 4, image, [F(1)], [F(0),F(0),F(4)], [F(16),F(64)],
                   {'center': F(36), 'error': F(45), 'raw': [F(-9),F(81)], 'final': [F(16),F(64)]}))
    return result


def positive_cases(primary, validator):
    evidence, available = [], {}
    for name, size, images, alphas, eigen, prior, expected in analytic_fixtures():
        rows = make_rows(images, alphas, size)
        held = held_scenario(images, alphas, eigen, size, prior)
        terms = primary.derive_modes(rows, size=size)
        actual = primary.derive_scenario(held, terms, size=size, dimension=len(rows))
        independent = validator.validate_case(rows, held, terms, actual, size=size)
        check(independent == {'status':'all_fields_independently_match','rows':len(rows),
                              'modes':size//2,'scenarios':1}, name + ': independent product-form reconstruction')
        for field, wanted in expected.items():
            check(equal(actual[field], enc(wanted)), name + ': analytic ' + field)
        if name in ('Q1','Q2','Q3','Q4','Q5'):
            check(all(term['c'] == enc(F(2)) and term['h_tau'] == enc(F(0))
                      and term['h_alpha'] == enc(F(0)) for term in terms), name + ': pair powers')
        if name == 'Q1':
            changed = clone(held); changed['source_record'] = psd([F(13),F(2),F(5)], size)
            revised = primary.derive_scenario(changed, terms, size=size, dimension=2)
            check(all(equal(actual[k], revised[k]) for k in actual if k != 'source_identity'), 'Q1: only DC input changes')
        if name == 'Q2':
            check(held['source_record']['values_hex'] == [float(F(3,FS)).hex(), float(F(6,FS)).hex(), float(F(3,FS)).hex()],
                  'Q2: white eigenvalue normalization')
        if name in ('Q5','Q8'):
            check(actual['ratios']['ri96_over_raw_width'] == {'value': None, 'undefined_reason':'zero_width_denominator'},
                  name + ': zero width ratio')
        if name == 'Q7':
            check(actual['final'] == enc([F(4),F(16)]) and
                  actual['ratios']['ri96_over_final_width'] == {'value':enc(F(1)), 'undefined_reason':None} and
                  actual['ratios']['raw_upper_over_lower'] == {'value':None,'undefined_reason':'nonpositive_lower_endpoint'},
                  'Q7: raw negative/intersection/undefined ratio')
            check(terms[1]['h_tau'] == enc(F(13,16)) and terms[1]['h_alpha'] == enc(F(2)), 'Q7: radius split')
        available[name] = {'size':size, 'rows':rows, 'held':held, 'terms':terms, 'actual':actual}
        evidence.append({'id':name,'size':size,'rows':rows,'held':held,'mode_terms':terms,
                         'result':actual,'analytic_expectations':enc(expected),'passed':True})
    old, doubled = available['Q7']['actual'], available['Q11']['actual']
    for field in ('center','error_tau','error_alpha','error','band_spread','band_margin','band_width'):
        x = F(int(old[field][0],16), int(old[field][1],16))
        check(doubled[field] == enc(4*x), 'Q11: exact scalar scaling ' + field)
    for field in ('raw','ri96_raw_band','ri96_prior','final'):
        check(doubled[field] == [enc(4*F(int(x[0],16),int(x[1],16))) for x in old[field]], 'Q11: interval scaling ' + field)
    check(doubled['ratios'] == old['ratios'], 'Q11: ratios/status unchanged')
    return evidence, available


def production_projection():
    # Q10 is arithmetic coverage only: a fake zero operator, no positive-Gram claim.
    modes = [['0','0','0','0'] for _ in range(M//2+1)]
    proofs = [{'row':row,'alpha':enc(F(0)), 'midpoint_modes':modes, 'mode_identity':pin(modes)} for row in ROWS]
    eigen = [F(1) if k in (0,M//2) else F(1,2) for k in range(M//2+1)]
    record = psd(eigen,M)
    extrema = []
    for b in range(14):
        first, stop = 1 << b, min(1 << (b+1),M//2+1)
        value = F(1) if b == 13 else F(1,2)
        extrema.append(enc({'index':b,'ell':value,'u':value,
                            'minimum_indices':list(range(first,stop)),'maximum_indices':list(range(first,stop))}))
    zero = [[enc(F(0)) for _ in ROWS] for _ in ROWS]
    scenarios = [{'id':name,'source_record':record,'band_extrema':extrema,'C_minus':zero,'C_plus':zero,
                  'delta_minus':enc(F(0)),'delta_plus':enc(F(0)), 'trace':enc([F(0),F(0)]),
                  'prior_trace':enc([F(0),F(0)])} for name in ORDER]
    return {'context':'fabricated_projection_not_observed',
            'held_identity':pin_bytes(b'RI98 synthetic zero projection tag; no predecessor execution\n'),
            'rows':list(ROWS),'row_proofs':proofs,'scenarios':scenarios,
            'held_provenance_identity':pin({'context':'fabricated_not_observed'}),
            'held_limitations':['Fabricated RI98 projection; no observed input or predecessor execution.']}


def refused(out, primary, validator, name, code, action):
    try: action()
    except (primary.TraceError, validator.ValidationError) as error:
        check(error.code == code, name + ': unintended refusal ' + error.code)
        out.append({'id':name,'expected_code':code,'code':error.code,'refused':True})
    else: raise QualificationError(name + ': missing refusal')


def mutate(value, path, replacement, action):
    parent = value
    for key in path[:-1]: parent = parent[key]
    old = parent[path[-1]]; parent[path[-1]] = replacement
    try: return action()
    finally: parent[path[-1]] = old


def controls(primary, validator, available, projection, provenance, report):
    out = []
    def test(name, action):
        code = dict(REFUSALS)[name]
        refused(out, primary, validator, name, code, action)
    test('primary:actual_body_pin', lambda:primary.project_saved(b'{}'))
    test('primary:duplicate_json_key', lambda:primary.parse_json(b'{"a":1,"a":2}'))
    test('primary:nonfinite_json', lambda:primary.parse_json(b'{"a":NaN}'))
    test('primary:unreduced_rational', lambda:primary.decode_scalar(['2','2']))
    test('primary:negative_zero_integer', lambda:primary.hex_integer('-0'))
    test('primary:excessive_integer', lambda:primary.hex_integer('1'+'0'*65536))
    test('primary:unsupported_domain', lambda:primary.derive_modes([],size=16))
    q = available['Q1']; rows = clone(q['rows'])
    test('primary:wrong_row_order',lambda:mutate(rows,[0,'row'],1,lambda:primary.derive_modes(rows,size=4)))
    for name, replacement in [('primary:missing_row',projection['row_proofs'][:-1]),
                              ('primary:extra_row',projection['row_proofs']+[None])]:
        test(name,lambda replacement=replacement:mutate(projection,['row_proofs'],replacement,
             lambda:primary.projection_check(projection,'fabricated_qualification')))
    test('primary:missing_mode',lambda:mutate(rows,[0,'midpoint_modes'],rows[0]['midpoint_modes'][:-1],lambda:primary.derive_modes(rows,size=4)))
    test('primary:extra_mode',lambda:mutate(rows,[0,'midpoint_modes'],rows[0]['midpoint_modes']+[None],lambda:primary.derive_modes(rows,size=4)))
    test('primary:stale_mode_identity',lambda:mutate(rows,[0,'mode_identity','sha256'],'0'*64,lambda:primary.derive_modes(rows,size=4)))
    for name, endpoint in [('primary:reversed_rectangle',['1','0','0','0']),
                           ('primary:nyquist_imaginary_excludes_zero',['0','0','1','2'])]:
        changed = clone(rows); changed[0]['midpoint_modes'][2] = endpoint
        changed[0]['mode_identity'] = pin(changed[0]['midpoint_modes'])
        test(name,lambda changed=changed:primary.derive_modes(changed,size=4))
    test('primary:negative_alpha',lambda:mutate(rows,[0,'alpha'],enc(F(-1)),lambda:primary.derive_modes(rows,size=4)))
    held, terms = clone(q['held']), clone(q['terms'])
    action=lambda:primary.derive_scenario(held,terms,size=4,dimension=2)
    for name,path,replacement in [
        ('primary:psd_float_shape',['source_record','shape'],[3.0]),
        ('primary:psd_wrong_size',['source_record','shape'],[4]),
        ('primary:psd_missing_bin',['source_record','values_hex'],held['source_record']['values_hex'][:-1]),
        ('primary:psd_dtype',['source_record','dtype'],'>f8'),
        ('primary:psd_byte_identity',['source_record','sha256'],'0'*64),
        ('primary:negative_psd',['source_record','values_hex',1],(-1.0).hex()),
        ('primary:nonfinite_psd',['source_record','values_hex',1],'inf'),
        ('primary:changed_tie_inventory',['band_extrema',0,'minimum_indices'],[]),
        ('primary:negative_band_margin',['delta_plus'],enc(F(-1))),
        ('primary:reversed_prior',['prior_trace'],enc([F(2),F(1)]))]:
        test(name,lambda path=path,replacement=replacement:mutate(held,path,replacement,action))
    for name,path,replacement in [
        ('primary:duplicate_mode_index',[1,'k'],1),('primary:wrong_pair_weight',[1,'pair_weight'],2),
        ('primary:negative_mode_term',[0,'h_tau'],enc(F(-1)))]:
        test(name,lambda path=path,replacement=replacement:mutate(terms,path,replacement,action))
    test('primary:reordered_modes',lambda:primary.derive_scenario(held,list(reversed(terms)),size=4,dimension=2))
    changed = clone(held); changed['C_plus'][0][0]=enc(F(15)); changed['trace']=enc([F(14),F(22)])
    test('primary:changed_band_spread',lambda:primary.derive_scenario(changed,terms,size=4,dimension=2))
    q8 = available['Q8']; changed=clone(q8['held']); changed['prior_trace']=enc([F(4),F(5)])
    test('primary:empty_intersection',lambda:primary.derive_scenario(changed,q8['terms'],size=8,dimension=1))
    for name,target,path,replacement in [
        ('primary:changed_design_pin',provenance,['sources','design','sha256'],'0'*64),
        ('primary:fabricated_actual_context',projection,['context'],'accepted_ri96_saved_output'),
        ('primary:claimed_fabricated_qualification',provenance,['acceptance','qualification'],pin_bytes(b'claimed')),
        ('primary:claimed_fabricated_custody',provenance,['acceptance','custody'],pin_bytes(b'claimed')),
        ('primary:changed_projection_pin',provenance,['input','sha256'],'0'*64)]:
        if target is projection:
            action=lambda:primary.projection_check(projection,'fabricated_qualification')
        else:
            action=lambda:primary.provenance_check(provenance,'fabricated_qualification',pin(projection))
        test(name,lambda target=target,path=path,replacement=replacement,action=action:mutate(target,path,replacement,action))
    projection['extra'] = None
    try:test('primary:unknown_projection_field',lambda:primary.projection_check(projection,'fabricated_qualification'))
    finally:del projection['extra']
    test('primary:changed_scenario_order',lambda:mutate(projection,['scenarios'],list(reversed(projection['scenarios'])),
         lambda:primary.projection_check(projection,'fabricated_qualification')))
    def vf():return validator.verify_result_fields(report,projection,provenance,expected_phase='fabricated_qualification')
    report['extra'] = None
    try:test('validator:extra_top_key',vf)
    finally:del report['extra']
    for name,path,replacement in [
        ('validator:phase_substitution',['phase'],'fixed_saved_application'),
        ('validator:source_pin',['provenance','sources','consumer','sha256'],'0'*64),
        ('validator:method_float_dimension',['method','M'],16384.0),
        ('validator:limitations',['limitations'],[]),
        ('validator:gate_count_boolean',['checks','counts','failed'],False),
        ('validator:gate_result_integer',['checks','results',0,'passed'],1),
        ('validator:projection_identity',['inherited_premises','projection_identity','sha256'],'0'*64)]:
        test(name,lambda path=path,replacement=replacement:mutate(report,path,replacement,vf))
    expected = clone(report['mode_terms'][0]); actual = clone(expected)
    for name,field in [('validator:mode_center','c'),('validator:mode_tau','h_tau'),('validator:mode_alpha','h_alpha')]:
        test(name,lambda name=name,field=field:mutate(actual,[field],enc(F(1)),lambda:validator.verify_mode_term(actual,expected)))
    q6,q7,q9 = available['Q6']['actual'],available['Q7']['actual'],available['Q9']['actual']
    cases = [
        ('validator:missing_lambda_weight',q6,['error'],F(7,4)),
        ('validator:nyquist_imaginary_alpha',q6,['error'],F(8)),
        ('validator:alpha_in_tau',q7,['error_tau'],F(45,4)),
        ('validator:negative_raw_clipped',q7,['raw',0],F(0)),
        ('validator:band_width_changed',q9,['band_width'],F(191)),
        ('validator:undefined_ratio_number',q7,['ratios','raw_upper_over_lower'],{'value':enc(F(0)),'undefined_reason':None}),
        ('validator:changed_final',q7,['final',1],F(17)),
        ('validator:changed_source_identity',q7,['source_identity','sha256'],'0'*64),
    ]
    for name,expected,path,replacement in cases:
        actual = clone(expected)
        test(name,lambda actual=actual,expected=expected,path=path,replacement=replacement:
             mutate(actual,path,enc(replacement),lambda:validator.verify_scenario(actual,expected)))
    return out


def write_artifact(root, name, value):
    target = root/name; h,n=hashlib.sha256(),0
    with target.open('xb') as stream:
        for p in parts(value): stream.write(p);h.update(p);n+=len(p)
        stream.flush();os.fsync(stream.fileno())
    return {'name':name,'bytes':n,'sha256':h.hexdigest()}


def run(primary, validator, provenance_template, artifact_dir):
    """One frozen fabricated campaign; caller owns captured source/runtime gate."""
    root=Path(artifact_dir)
    check(root.is_absolute() and root.resolve()==root and root.is_dir() and not root.is_symlink()
          and not list(root.iterdir()), 'exclusive empty regular artifact directory')
    evidence, cases = positive_cases(primary, validator)
    projection=production_projection(); provenance=clone(provenance_template)
    provenance['input']=pin(projection)
    check(provenance['acceptance']['qualification'] is None and provenance['acceptance']['custody'] is None,
          'fabricated campaign has no actual admission')
    projection_pin,provenance_pin=pin(projection),pin(provenance)
    report=primary.build_result(projection,provenance)
    check(len(report['mode_terms'])==8192 and all(x['c']==enc(F(0)) and x['h_tau']==enc(F(0)) and x['h_alpha']==enc(F(0))
                                               for x in report['mode_terms']), 'Q10: all full-shape zero mode terms')
    for scenario in report['scenarios']:
        check(all(scenario[k]==enc(F(0)) for k in ('center','error_tau','error_alpha','error','band_spread','band_margin','band_width')),
              'Q10: all four complete exact zero scenarios')
        check(scenario['raw']==enc([F(0),F(0)]) and scenario['final']==enc([F(0),F(0)]) and
              all(x['value'] is None for x in scenario['ratios'].values()), 'Q10: zero intervals and undefined ratios')
    verified=validator.validate_result(report,projection,provenance,expected_phase='fabricated_qualification')
    check(verified=={'status':'all_fields_independently_match','rows':8,'modes':8192,'scenarios':4}, 'full independent validation counts')
    refusals=controls(primary,validator,cases,projection,provenance,report)
    check(pin(projection)==projection_pin and pin(provenance)==provenance_pin, 'controls restored exact input/provenance')
    artifacts=[write_artifact(root,'FABRICATED_PROJECTION.json',projection),
               write_artifact(root,'FABRICATED_RESULT.json',report)]
    report_pin=pin(report); del report
    complete=(root/'FABRICATED_RESULT.json').read_bytes()
    loaded=validator.load_result(complete,projection,provenance,expected_phase='fabricated_qualification')
    check(pin(loaded)==report_pin and pin_bytes(complete)==report_pin, 'full canonical decoder roundtrip')
    refused(refusals,primary,validator,'validator:canonical_roundtrip_whitespace','CANONICAL',
            lambda:validator.load_result(complete+b' ',projection,provenance,expected_phase='fabricated_qualification'))
    del loaded,complete
    evidence.append({'id':'Q10','context':'fabricated_zero_production_shape_not_observed',
                     'rows':8,'input_modes_per_row':8193,'retained_mode_terms':8192,'scenarios':4,
                     'projection_identity':projection_pin,'result_identity':report_pin,'passed':True})
    evidence.sort(key=lambda x:int(x['id'][1:]))
    artifacts.append(write_artifact(root,'ANALYTIC_CASES.json',evidence));artifacts.sort(key=lambda x:x['name'])
    check(tuple(x['name'] for x in artifacts)==ARTIFACTS and set(p.name for p in root.iterdir())==set(ARTIFACTS),
          'exact retained artifact inventory')
    inventory=dict(REFUSALS)
    check(len(refusals)==len(REFUSALS) and len({x['id'] for x in refusals})==len(REFUSALS)
          and all(x['expected_code']==inventory[x['id']]==x['code'] and x['refused'] is True for x in refusals),
          'complete intended-reason inventory')
    refusals.sort(key=lambda x:[name for name,code in REFUSALS].index(x['id']))
    return {'schema':'ri98-fabricated-qualification-v1','phase':'fabricated_qualification',
            'status':'all_declared_checks_passed','provenance':provenance,
            'counts':{'analytic_cases':11,'production_rows':8,'production_modes':8192,'scenarios':4,
                      'refusals':len(REFUSALS),'artifacts':3},
            'positive_cases':[{'id':'Q'+str(i),'passed':True} for i in range(1,12)],
            'refusal_inventory':[{'id':name,'code':code} for name,code in REFUSALS],
            'refusals':refusals,'artifacts':artifacts,
            'scope':'Fabricated exact arithmetic and closed validators only; no actual RI96 values or new Fourier transform.',
            'limitations':['Analytic qualification is not execution or custody of observed input.',
                           'Prior transform/covariance validity remains inherited for the separately admitted actual path.',
                           'No numerical resource success is established until this frozen source is genuinely executed.']}
