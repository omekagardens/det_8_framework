"""RI106 fixed fabricated qualification; source-only until separately admitted.

No actual input path is opened, no HDF5 module imported, and no observed entry
is called. Independent tiny oracle uses Fraction signed endpoint sums.
"""
from fractions import Fraction as F
from pathlib import Path
import copy
import hashlib
import json
import math
import os
import struct

ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
N, L, T, M, FS, SAMPLES = 2769, 4096, 10961, 16384, 4096, 131072
ORDER = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
STARTS = {'left': (0, 8192, 16384, 24576, 32768, 40960, 49152),
          'right': (69632, 77824, 86016, 94208, 102400, 110592)}
POSITIVE_IDS = ('Q1:full_index_domain', 'Q2:three_window_side', 'Q3:two_window_side',
                'Q4:zero', 'Q5:common_constant', 'Q6:negative_amplitude', 'Q7:double_amplitude',
                'Q8:all64_box_corners', 'Q9:shared_uncertain_coefficient',
                'Q10:full_production_zero_saved_validation', 'Q11:square_endpoint_cases')
ARTIFACT_NAMES = ('BOX_CORNERS.json', 'DEPENDENCY_CASE.json', 'INDEX_H1.f64le', 'INDEX_L1.f64le',
                  'INDEX_RECORDS.json', 'PROJECTION.json', 'RESULT.json', 'SYNTHETIC_CAPTURE.json', 'TINY_CASES.json',
                  'application/H1-left-mean.json', 'application/H1-raw.f64le', 'application/H1-right-mean.json',
                  'application/L1-left-mean.json', 'application/L1-raw.f64le', 'application/L1-right-mean.json')
PRIMARY_REFUSALS = (
 ('P:duplicate_json', 'SCHEMA'), ('P:nonfinite_json', 'EXACT'), ('P:noncanonical_hex', 'EXACT'),
 ('P:zero_denominator', 'EXACT'), ('P:unreduced_rational', 'EXACT'), ('P:integer_ceiling', 'RESOURCE'),
 ('P:crossed_interval', 'INTERVAL'), ('P:nonexact_dot_input', 'EXACT'), ('P:dot_dimensions', 'DOMAIN'),
 ('P:overwide_interval', 'WIDTH'), ('P:raw_length', 'INPUT'), ('P:raw_nonfinite', 'INPUT'),
 ('P:missing_flags', 'FLAGS'), ('P:false_L1_CW_flag', 'FLAGS'), ('P:changed_metadata', 'METADATA'),
 ('P:alternate_segment_start', 'INPUT'), ('P:raw_segment_hash', 'INPUT'), ('P:swapped_trace', 'TRACE'),
 ('P:crossed_trace', 'INTERVAL'), ('P:actual_phase_fabrication', 'PHASE'), ('P:extra_projection_field', 'INPUT'),
 ('P:changed_capture_pin', 'INPUT'), ('P:changed_source_design', 'SOURCE'), ('P:claimed_qualification', 'PHASE'),
 ('P:changed_projection_binding', 'INPUT'), ('P:extra_provenance_field', 'PROVENANCE'),
 ('P:missing_source_row', 'ROW'), ('P:wrong_row_order', 'ROW'), ('P:wrong_row_length', 'ROW'),
 ('P:duplicate_source_key', 'SCHEMA'), ('P:noncanonical_source_row', 'CANONICAL'),
 ('P:crossed_source_interval', 'INTERVAL'), ('P:extra_ninth_source_row', 'ROW'),
 ('P:missing_artifact_record', 'ARTIFACT'), ('P:changed_artifact_pin', 'ARTIFACT'),
 ('P:extra_artifact_record', 'ARTIFACT'), ('P:wrong_artifact_name', 'ARTIFACT'),
 ('P:unsupported_dot_size', 'DOMAIN'), ('P:unsupported_energy_count', 'DOMAIN'))
VALIDATOR_REFUSALS = (
 ('V:extra_top_field', 'SCHEMA'), ('V:wrong_phase', 'PHASE'), ('V:changed_design', 'SOURCE'),
 ('V:claimed_qualification', 'PHASE'), ('V:wrong_input_identity', 'INPUT'), ('V:relaxed_width_method', 'DOMAIN'),
 ('V:n_minus_one_method', 'DOMAIN'), ('V:scalar_temporal_centering', 'DOMAIN'), ('V:false_status', 'RESULT'),
 ('V:missing_gate', 'RESULT'), ('V:false_gate', 'RESULT'), ('V:float_gate_count', 'RESULT'),
 ('V:changed_limitations', 'SCHEMA'), ('V:wrong_signed_dot', 'DOT'), ('V:wrong_dot_scale', 'DOT'),
 ('V:wrong_square_lower', 'ENERGY'), ('V:wrong_energy_divisor', 'ENERGY'),
 ('V:missing_artifact_record', 'ARTIFACT'), ('V:changed_artifact_pin', 'ARTIFACT'),
 ('V:swapped_scenario_trace', 'TRACE'), ('V:wrong_scenario_count', 'DOMAIN'),
 ('V:duplicate_json', 'SCHEMA'), ('V:noncanonical_result', 'CANONICAL'),
 ('V:missing_source_row', 'ROW'), ('V:wrong_row_order', 'ROW'), ('V:wrong_row_length', 'ROW'),
 ('V:duplicate_source_key', 'SCHEMA'), ('V:noncanonical_source_row', 'CANONICAL'),
 ('V:crossed_source_interval', 'INTERVAL'), ('V:extra_ninth_source_row', 'SCHEMA'),
 ('V:unsupported_dot_size', 'DOMAIN'), ('V:unsupported_energy_count', 'DOMAIN'),
 ('V:missing_mean_file', 'ARTIFACT'), ('V:changed_artifact_body', 'ARTIFACT'),
 ('V:alternate_T_crop', 'DOMAIN'))
REFUSALS = PRIMARY_REFUSALS + VALIDATOR_REFUSALS
LIMITATIONS = [
 'All operands are fabricated; accepted public metadata supplies schema/flags only, not observed strain or actual predecessor execution.',
 'Wide box/dependency cases test exact primitive containment and deliberately do not pass the fixed full-path width gate.',
 'Qualification does not authorize observed HDF5/capture/report access or establish physical noise, calibration, independence or a native forward map.',
]


def check(ok, why):
    if not ok: raise ValueError('RI106 qualification: '+why)


def canonical(x): return (json.dumps(x, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')
def compact(x): return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def scalar(x): return [format(x.numerator, 'x'), format(x.denominator, 'x')]
def enc_interval(x): return [scalar(x[0]), scalar(x[1])]
def dec(x): return F(int(x[0], 16), int(x[1], 16))
def dec_interval(x): return tuple(map(dec, x))


def write(path, body):
    with path.open('xb') as f: f.write(body); f.flush(); os.fsync(f.fileno())
    return pin(body)


def exact_dot(row, vector): return sum((a*x for a, x in zip(row, vector)), F(0))


def oracle_box(lo, hi, vector):
    lower = sum((min(a*x, b*x) for a, b, x in zip(lo, hi, vector)), F(0))
    upper = sum((max(a*x, b*x) for a, b, x in zip(lo, hi, vector)), F(0))
    return lower, upper


def oracle_square(box):
    lo, hi = box
    return (F(0) if lo <= 0 <= hi else min(lo*lo, hi*hi), max(lo*lo, hi*hi))


def oracle_side(rows, vectors):
    count = len(vectors); means = tuple(sum((v[j] for v in vectors), F(0))/count for j in range(len(vectors[0])))
    centered = [tuple(x-m for x, m in zip(v, means)) for v in vectors]
    outputs = [[exact_dot(row, v) for row in rows] for v in vectors]
    mean_outputs = [exact_dot(row, means) for row in rows]
    centered_outputs = [[exact_dot(row, v) for row in rows] for v in centered]
    u = [sum((v[i]*v[i] for v in outputs), F(0))/count for i in range(len(rows))]
    m = [x*x for x in mean_outputs]
    vv = [sum((v[i]*v[i] for v in centered_outputs), F(0))/count for i in range(len(rows))]
    check(all(u[i] == vv[i]+m[i] for i in range(len(rows))), 'independent finite energy identity')
    return means, centered, outputs, mean_outputs, centered_outputs, u, m, vv


def encoded_tree(v):
    if type(v) is F: return scalar(v)
    if type(v) in (tuple, list): return [encoded_tree(x) for x in v]
    if type(v) is dict: return {k: encoded_tree(x) for k, x in v.items()}
    return v


def check_tiny(primary, validator, rows, vectors, *, radius=F(0), enforce_width=True):
    means, centered, outputs, mean_outputs, centered_outputs, u, m, vv = oracle_side(rows, vectors)
    components = []
    for index, row in enumerate(rows):
        lo, hi = tuple(x-radius for x in row), tuple(x+radius for x in row)
        raw = [primary.dot_box(lo, hi, v, enforce_width=enforce_width) for v in vectors]
        mean = primary.dot_box(lo, hi, means, enforce_width=enforce_width)
        cent = [primary.dot_box(lo, hi, v, enforce_width=enforce_width) for v in centered]
        for record, v in [(mean, means)]+list(zip(raw, vectors))+list(zip(cent, centered)):
            expected = oracle_box(lo, hi, v)
            check(dec_interval(record['interval']) == expected, 'complete endpoint oracle equality')
            validator.verify_dot(record, lo, hi, v, enforce_width=enforce_width)
        e = primary.energy(raw, mean, cent); validator.verify_energy(e, raw, mean, cent)
        if radius == 0:
            for key, expected in (('U', u[index]), ('M', m[index]), ('V', vv[index])):
                check(dec_interval(e[key]) == (expected, expected), 'exact point energy anchor')
        components.append({'row_index': index, 'lo': list(lo), 'hi': list(hi), 'raw': raw, 'mean': mean, 'centered': cent, 'energy': e})
    return encoded_tree({'rows': rows, 'inputs': vectors, 'mean_input': means, 'centered_inputs': centered,
                         'exact_outputs': outputs, 'exact_mean_outputs': mean_outputs,
                         'exact_centered_outputs': centered_outputs, 'exact_U': u, 'exact_M': m, 'exact_V': vv,
                         'components': components, 'wide_primitive_only': not enforce_width})


def index_case(primary, metadata, directory):
    # All values are exactly represented binary64 labels; no observed values.
    bodies = {}
    for detector, sign in (('H1', 1), ('L1', -1)):
        values = [sign*j for j in range(SAMPLES)]
        for j in range(65536, 69632): values[j] = sign*(SAMPLES+j)
        for j in range(126976, SAMPLES): values[j] = sign*(2*SAMPLES+j)
        bodies[detector] = struct.pack('<'+str(SAMPLES)+'d', *values)
        write(directory/('INDEX_'+detector+'.f64le'), bodies[detector])
    prepared = primary.prepare_inputs(bodies)
    result = []
    for detector, metadata_index in (('H1', 0), ('L1', 1)):
        labels = struct.unpack('<'+str(SAMPLES)+'d', bodies[detector])
        for side, starts in STARTS.items():
            prepared_side = prepared[detector+':'+side]
            count = len(starts)
            sums = [sum(int(labels[s+j]) for s in starts) for j in range(T)]
            for j in range(T):
                check(prepared_side['mean'][j]*count == sums[j]*prepared_side['mean_den'], 'actual coordinatewise mean map')
            for position, start in enumerate(starts):
                nums = prepared_side['raw'][position]
                check(len(nums) == T, 'actual first-T extraction length')
                for j in range(T):
                    label = int(labels[start+j])
                    check(nums[j] == label*prepared_side['raw_den'], 'actual first-T extraction value')
                    check(prepared_side['centered'][position][j]*count == (count*label-sums[j])*prepared_side['centered_den'], 'actual centered input map')
                windows = {'M': (start, start+M), 'T': (start, start+T), 'short': (start+L, start+L+N)}
                slices = {}
                for kind, (a, b) in windows.items():
                    flags = list(range(a//FS, (b+FS-1)//FS))
                    expected = {'start': a, 'end': b, 'gps_start_offset': scalar(F(a, FS)),
                                'gps_end_offset': scalar(F(b, FS)), 'flag_rows': flags,
                                'dq_masks': [127]*len(flags), 'injection_masks': [31 if detector == 'H1' else 23]*len(flags)}
                    check(primary.slice_record(a, b, metadata['detectors'][metadata_index]) == expected, 'every slice/clock/flag field')
                    check(b <= start+M and a >= start, 'crop containment')
                    check(b <= 65536 if side == 'left' else 69632 <= a and b <= 126976, 'exclusion/tail sentinels')
                    slices[kind] = expected
                outputs = [start+L+i for i in ROWS]
                check(all(start+L <= i < start+L+N for i in outputs), 'selected output membership')
                result.append({'id': detector+':'+side+':'+str(start), 'slices': slices,
                               'output_indices': outputs, 'raw_sha256': hashlib.sha256(bodies[detector][8*start:8*(start+M)]).hexdigest()})
    check(len(result) == 26, 'all26 index windows')
    write(directory/'INDEX_RECORDS.json', canonical({'context': 'fabricated_index_labels', 'records': result,
         'M_overlap': 8192, 'T_overlap': 2769, 'short_centers_disjoint': True}))
    return {'windows': 26, 'slices': 78, 'selected_indices': 208, 'segment_hashes': 26}


def make_capture(directory):
    zero = [['0', '1'], ['0', '1']]
    rows = [{'row': i, 'short': [zero]*N, 'long': [zero]*T} for i in ROWS]
    value = {'dimensions': {'N': N, 'L': L, 'T': T}, 'row_order': list(ROWS), 'rows': rows, 'schema': 'ri73-reconstructed-intervals-v1'}
    body = compact(value); path = directory/'SYNTHETIC_CAPTURE.json'; write(path, body)
    return path, pin(body), value


def make_projection(primary, raw, capture_pin, metadata):
    segments = []
    for name in ORDER:
        detector, side = name.split(':')
        for start in STARTS[side]: segments.append({'id': name+':'+str(start), 'detector': detector, 'side': side,
             'start': start, 'end': start+M, 'raw_sha256': hashlib.sha256(raw[detector][8*start:8*(start+M)]).hexdigest()})
    return {'context': 'fabricated_inputs_not_observed', 'metadata': metadata,
            'hdf5': {d: pin(('fabricated_hdf5_not_observed:'+d).encode()) for d in ('H1', 'L1')},
            'capture': capture_pin, 'ri83': pin(b'fabricated_ri83_not_executed'), 'ri100': pin(b'fabricated_ri100_not_executed'),
            'segments': segments, 'traces': [{'id': name, 'interval': [['0', '1'], ['1', '1']],
                  'source_identity': pin(('fabricated_trace:'+name).encode()), 'model': 'fabricated_trace_not_observed',
                  'units': 'nominal_strain_squared_sum_of_eight_centered_coordinates'} for name in ORDER]}


def refuse(function, label, code, result):
    try: function()
    except Exception as exc:
        check(getattr(exc, 'code', None) == code, label+' intended first code')
        result.append({'id': label, 'expected_code': code, 'code': exc.code, 'passed': True})
    else: raise ValueError(label+' unexpectedly accepted')


def changed(obj, path, replacement):
    result = copy.deepcopy(obj); target = result
    for key in path[:-1]: target = target[key]
    target[path[-1]] = replacement
    return result


def primary_refusals(p, raw, capture_path, capture_value, projection, provenance, report, directory):
    zero = F(0); results = []
    simple = [
      lambda: p.parse(b'{"a":1,"a":2}'), lambda: p.parse(b'{"a":NaN}'), lambda: p.unscalar(['00', '1']),
      lambda: p.unscalar(['1', '0']), lambda: p.unscalar(['2', '2']), lambda: p.integer(1 << 262144),
      lambda: p.uninterval([['1', '1'], ['0', '1']]), lambda: p.dot_box([F(0)], [F(0)], [0.0]),
      lambda: p.dot_box([F(0)], [F(0)], [F(0), F(0)]), lambda: p.dot_box([F(-1)], [F(1)], [F(1)]),
      lambda: p.raw_vector(b'bad'), lambda: p.raw_vector(struct.pack('<d', float('inf'))+b'\0'*(8*SAMPLES-8)),
      lambda: p.metadata_check(changed(projection['metadata'], ['detectors', 1, 'hardware_injection_flags'], {})),
      lambda: p.metadata_check(changed(projection['metadata'], ['detectors', 1, 'hardware_injection_flags', 'raw_bitfields'], [31]*32)),
      lambda: p.metadata_check({**projection['metadata'], 'unexpected': True}),
    ]
    def proj(value): return lambda: p.projection_check(value, 'fabricated_qualification', raw, capture_path)
    simple += [proj(changed(projection, ['segments', 0, 'start'], 1)),
       proj(changed(projection, ['segments', 0, 'raw_sha256'], '0'*64)),
       proj(changed(projection, ['traces', 0, 'id'], 'H1:right')),
       proj(changed(projection, ['traces', 0, 'interval'], [['1', '1'], ['0', '1']])),
       lambda: p.projection_check(projection, 'fixed_observed_application', raw, capture_path),
       proj({**projection, 'extra': True}), proj(changed(projection, ['capture', 'sha256'], '0'*64))]
    def prov(value): return lambda: p.provenance_check(value, 'fabricated_qualification', projection)
    simple += [prov(changed(provenance, ['sources', 'design', 'sha256'], '0'*64)),
       prov(changed(provenance, ['acceptance', 'qualification'], pin(b'invented'))),
       prov(changed(provenance, ['input', 'sha256'], '0'*64)), prov({**provenance, 'extra': 0})]
    for (label, code), call in zip(PRIMARY_REFUSALS[:26], simple): refuse(call, label, code, results)
    check(len(simple) == 26, 'fixed primary scalar inventory')
    # Malformed capture bodies are retained individually and remain synthetic.
    negatives = directory/'negative-captures'; negatives.mkdir()
    row = capture_value['rows'][0]
    head = b'{"dimensions":'+compact(capture_value['dimensions'])+b',"row_order":'+compact(list(ROWS))+b',"rows":['
    tail = b'],"schema":"ri73-reconstructed-intervals-v1"}'
    first_wrong = changed(row, ['row'], 1)
    short_wrong = changed(row, ['short'], [])
    crossed = changed(row, ['long', 0], [['1', '1'], ['0', '1']])
    bodies = [head+tail, head+compact(first_wrong)+tail, head+compact(short_wrong)+tail,
              head+b'{"row":0,"row":0,"short":[],"long":[]}'+tail,
              head+canonical(row).rstrip(b'\n')+tail, head+compact(crossed)+tail,
              head+b','.join(compact(x) for x in capture_value['rows']+[row])+tail]
    for offset, body in enumerate(bodies):
        label, code = PRIMARY_REFUSALS[26+offset]; path = negatives/(label.replace(':', '-')+'.json'); write(path, body)
        def consume(path=path, expected=pin(body)):
            for _ in p.source_rows(path, expected): pass
        refuse(consume, label, code, results)
    records = report['inputs']['artifacts']; app = directory/'application'
    tail_calls = [lambda: p.artifact_check(app, records[:-1]),
                  lambda: p.artifact_check(app, changed(records, [0, 'sha256'], '0'*64)),
                  lambda: p.artifact_check(app, records+[records[0]]),
                  lambda: p.write_artifact(app, 'not-admitted.json', b'bad', 'bad', [1])]
    for (label, code), call in zip(PRIMARY_REFUSALS[33:37], tail_calls): refuse(call, label, code, results)
    zero_dot = p.dot_box([F(0)], [F(0)], [F(0)])
    domain_calls = [lambda: p.dot_box([F(0), F(0)], [F(0), F(0)], [F(0), F(0)]),
                    lambda: p.energy([zero_dot], zero_dot, [zero_dot])]
    for (label, code), call in zip(PRIMARY_REFUSALS[37:], domain_calls): refuse(call, label, code, results)
    check(len(results) == len(PRIMARY_REFUSALS), 'complete primary refusals')
    return results


def validator_refusals(v, report, raw, capture_path, projection, provenance, directory, tiny_component):
    results = []
    def fields(candidate, expected=provenance, phase='fabricated_qualification'):
        return lambda: v.verify_result_fields(candidate, projection, expected, phase)
    changes = [({**report, 'extra': None}, provenance, 'fabricated_qualification'),
       (report, provenance, 'fixed_observed_application'),
       (changed(report, ['provenance', 'sources', 'design', 'sha256'], '0'*64), provenance, 'fabricated_qualification'),
       (changed(report, ['provenance', 'acceptance', 'qualification'], pin(b'invented')), provenance, 'fabricated_qualification'),
       (changed(report, ['provenance', 'input', 'sha256'], '0'*64), provenance, 'fabricated_qualification'),
       (changed(report, ['method', 'width_scale'], ['1', '1']), provenance, 'fabricated_qualification'),
       (changed(report, ['method', 'divisor'], 'n_minus_one'), provenance, 'fabricated_qualification'),
       (changed(report, ['method', 'centering'], 'scalar_temporal_mean'), provenance, 'fabricated_qualification'),
       (changed(report, ['status'], 'success_unchecked'), provenance, 'fabricated_qualification'),
       (changed(report, ['checks', 'inventory'], report['checks']['inventory'][:-1]), provenance, 'fabricated_qualification'),
       (changed(report, ['checks', 'results', 0, 'passed'], False), provenance, 'fabricated_qualification'),
       (changed(report, ['checks', 'counts', 'total'], 12.0), provenance, 'fabricated_qualification'),
       (changed(report, ['limitations'], []), provenance, 'fabricated_qualification')]
    for (label, code), (candidate, expected, phase) in zip(VALIDATOR_REFUSALS[:13], changes):
        refuse(fields(candidate, expected, phase), label, code, results)
    # Exact one-coordinate point dot; no production recomputation for late mutation controls.
    point = {'interval': [['2', '1'], ['2', '1']], 'center': ['2', '1'], 'radius': ['0', '1'],
             'width': ['0', '1'], 'input_max': ['2', '1'], 'width_limit': ['1', format(5*10**11, 'x')], 'width_pass': True}
    point_negative = changed(point, ['interval'], [['-2', '1'], ['-2', '1']])
    primitive_calls = [lambda: v.verify_dot(point_negative, [F(1)], [F(1)], [F(2)]),
        lambda: v.verify_dot(changed(point, ['input_max'], ['1', '1']), [F(1)], [F(1)], [F(2)]),
        lambda: v.verify_square([['1', '1'], ['1', '1']], [['-1', '1'], ['1', '1']]),
        lambda: v.verify_energy(changed(tiny_component['energy'], ['U'],
                                [scalar(dec(x)*F(3,2)) for x in tiny_component['energy']['U']]),
                                tiny_component['raw'], tiny_component['mean'], tiny_component['centered'])]
    for (label, code), call in zip(VALIDATOR_REFUSALS[13:17], primitive_calls): refuse(call, label, code, results)
    expected_bodies = {record['name']: (directory/'application'/record['name']).read_bytes() for record in report['inputs']['artifacts']}
    artifact_calls = [lambda: v.verify_artifacts(directory/'application', report['inputs']['artifacts'][:-1], expected_bodies),
        lambda: v.verify_artifacts(directory/'application', changed(report['inputs']['artifacts'], [0, 'sha256'], '0'*64), expected_bodies),
        lambda: v.verify_scenario(changed(report['scenarios'][0], ['trace', 'id'], 'H1:right'), report['scenarios'][0]),
        lambda: v.verify_scenario(changed(report['scenarios'][0], ['count'], 6), report['scenarios'][0]),
        lambda: v.load_result(b'{"x":1,"x":2}\n'), lambda: v.load_result(b'{"x":1}\n')]
    for (label, code), call in zip(VALIDATOR_REFUSALS[17:23], artifact_calls): refuse(call, label, code, results)
    for (label, code), (primary_label, _) in zip(VALIDATOR_REFUSALS[23:30], PRIMARY_REFUSALS[26:33]):
        path = directory/'negative-captures'/(primary_label.replace(':', '-')+'.json')
        expected = pin(path.read_bytes())
        def consume(path=path, expected=expected):
            for _ in v.independent_rows(path, expected): pass
        refuse(consume, label, code, results)
    domain_calls = [lambda: v.verify_dot(point, [F(0), F(0)], [F(0), F(0)], [F(0), F(0)]),
                    lambda: v.verify_energy(tiny_component['energy'], [point], point, [point])]
    for (label, code), call in zip(VALIDATOR_REFUSALS[30:32], domain_calls): refuse(call, label, code, results)
    # These are isolated fabricated copies. Valid records and expected bodies
    # ensure refusal reaches physical membership/content guards, not pin fields.
    negative_root = directory/'negative-artifacts'; negative_root.mkdir(mode=0o700)
    mean_name = 'H1-left-mean.json'
    for offset, case in enumerate(('missing-mean-file', 'changed-file-body')):
        target = negative_root/case; target.mkdir(mode=0o700); retained = []
        for name, original in sorted(expected_bodies.items()):
            if case == 'missing-mean-file' and name == mean_name: continue
            body = original
            if case == 'changed-file-body' and name == mean_name:
                check(body.endswith(b'\n'), 'canonical mean terminal newline for byte mutation')
                body = body[:-1]+b' '
                check(len(body) == len(original) and body != original, 'same-size genuine changed mean body')
            retained.append({'name': name, **write(target/name, body)})
        label, code = VALIDATOR_REFUSALS[32+offset]
        refuse(lambda target=target: v.verify_artifacts(target, report['inputs']['artifacts'], expected_bodies),
               label, code, results)
        results[-1]['fixture'] = {'directory': 'negative-artifacts/'+case,
                                 'difference': 'absent_file' if case == 'missing-mean-file' else 'same_size_changed_bytes',
                                 'affected_name': mean_name, 'files': retained,
                                 'expected_inventory': copy.deepcopy(report['inputs']['artifacts']),
                                 'expected_bodies_source': 'unchanged_successful_application_artifacts'}
    # The centered-T alternative lies inside the same M segment but is not the
    # admitted first-T crop. Retain its internally consistent clock/flag rows.
    expected_scenario = report['scenarios'][0]
    crop_start = expected_scenario['windows'][0]['start']+(M-T)//2
    crop_end = crop_start+T
    crop_flags = list(range(crop_start//FS, (crop_end+FS-1)//FS))
    alternate_crop = {'start': crop_start, 'end': crop_end,
                      'gps_start_offset': scalar(F(crop_start, FS)),
                      'gps_end_offset': scalar(F(crop_end, FS)), 'flag_rows': crop_flags,
                      'dq_masks': [127]*len(crop_flags), 'injection_masks': [31]*len(crop_flags)}
    candidate = changed(expected_scenario, ['windows', 0, 'slices', 'T'], alternate_crop)
    label, code = VALIDATOR_REFUSALS[34]
    refuse(lambda: v.verify_scenario(candidate, expected_scenario), label, code, results)
    results[-1]['fixture'] = {'scenario': expected_scenario['id'], 'window_start': expected_scenario['windows'][0]['start'],
                             'expected_T_slice': expected_scenario['windows'][0]['slices']['T'],
                             'mutated_T_slice': alternate_crop}
    check(len(results) == len(VALIDATOR_REFUSALS), 'complete validator refusals')
    return results


def run(primary, validator, provenance_template, artifact_dir, metadata_body):
    directory = Path(artifact_dir)
    check(directory.is_absolute() and directory.parent == directory.parent.resolve() and not directory.exists(), 'fresh fixed output directory')
    directory.mkdir(mode=0o700)
    check(pin(metadata_body) == primary.METADATA, 'source-known metadata pin')
    metadata = primary.parse(metadata_body); primary.metadata_check(metadata)
    positive = []; summaries = index_case(primary, metadata, directory)
    positive.append({'id': POSITIVE_IDS[0], 'passed': True, 'counts': summaries})
    rows = ((F(1), F(-1), F(0)), (F(0), F(1), F(-1)))
    left = ((F(1), F(0), F(-1)), (F(0), F(1), F(-1)), (F(1), F(1), F(0)))
    right = ((F(-1), F(2), F(0)), (F(2), F(0), F(1)))
    variants = [left, right, tuple((F(0),)*3 for _ in range(3)), tuple((F(3),)*3 for _ in range(3)),
                tuple(tuple(-x for x in row) for row in left), tuple(tuple(2*x for x in row) for row in left)]
    tiny = []
    for index, vectors in enumerate(variants):
        case = check_tiny(primary, validator, rows, vectors); tiny.append(case)
        positive.append({'id': POSITIVE_IDS[index+1], 'passed': True, 'windows': len(vectors), 'rows': 2})
    # Independent hand-derived anchors, separate from the general tiny oracle.
    check(tiny[0]['exact_U'] == [scalar(F(2,3)), scalar(F(2))] and tiny[0]['exact_M'] == [scalar(F(0)), scalar(F(16,9))]
          and tiny[0]['exact_V'] == [scalar(F(2,3)), scalar(F(2,9))], 'three-window anchor')
    check(tiny[1]['exact_U'] == [scalar(F(13,2)), scalar(F(5,2))] and tiny[1]['exact_M'] == [scalar(F(1,4)), scalar(F(1,4))]
          and tiny[1]['exact_V'] == [scalar(F(25,4)), scalar(F(9,4))], 'two-window anchor')
    for index, factor in ((4, 1), (5, 4)):
        for name in ('exact_U', 'exact_M', 'exact_V'):
            check([dec(x) for x in tiny[index][name]] == [factor*dec(x) for x in tiny[0][name]], 'signed/double energy scaling')
    write(directory/'TINY_CASES.json', canonical({'context': 'fabricated_exact_tiny', 'cases': tiny}))
    wide = [check_tiny(primary, validator, rows, side, radius=F(1,16), enforce_width=False) for side in (left, right)]
    corners = []
    for mask in range(64):
        corner = tuple(tuple(rows[i][j] + (F(1,16) if mask & (1 << (3*i+j)) else -F(1,16)) for j in range(3)) for i in range(2))
        results = []
        for side_index, side in enumerate((left, right)):
            mean, centered, outputs, means, centered_outputs, u, m, vv = oracle_side(corner, side)
            for i in range(2):
                box = wide[side_index]['components'][i]
                for records, values in ((box['raw'], [x[i] for x in outputs]), (box['centered'], [x[i] for x in centered_outputs])):
                    for record, exact in zip(records, values):
                        a, b = dec_interval(record['interval']); check(a <= exact <= b, 'every corner output containment')
                a, b = dec_interval(box['mean']['interval']); check(a <= means[i] <= b, 'corner finite mean containment')
                for key, exact in (('U', u[i]), ('M', m[i]), ('V', vv[i])):
                    a, b = dec_interval(box['energy'][key]); check(a <= exact <= b, 'every corner energy containment')
            results.append(encoded_tree({'outputs': outputs, 'mean': means, 'centered': centered_outputs, 'U': u, 'M': m, 'V': vv}))
        corners.append({'mask': mask, 'matrix': encoded_tree(corner), 'sides': results})
    # The non-corner center matrix was evaluated in both point cases above.
    write(directory/'BOX_CORNERS.json', canonical({'context': 'wide_primitive_containment_only', 'boxes': wide,
                                                  'corners': corners, 'center_cases': tiny[:2]}))
    positive.append({'id': POSITIVE_IDS[7], 'passed': True, 'corners': 64, 'sides': 2, 'center_cases': 2})
    dependency = check_tiny(primary, validator, ((F(3,2),),), ((F(1),), (F(3),)), radius=F(1,2), enforce_width=False)
    component = dependency['components'][0]
    check([dec_interval(x['interval']) for x in component['centered']] == [(F(-2), F(-1)), (F(1), F(2))], 'dependency centered intervals')
    check(dec_interval(component['energy']['V']) == (F(1), F(4)), 'dependency energy interval')
    raw_boxes = [dec_interval(x['interval']) for x in component['raw']]
    mean_box = dec_interval(component['mean']['interval'])
    loose = [(a-mean_box[1], b-mean_box[0]) for a,b in raw_boxes]
    check(loose == [(F(-3), F(0)), (F(-1), F(4))], 'separate output subtraction reference')
    check(all((b-a) > (dec_interval(d['interval'])[1]-dec_interval(d['interval'])[0])
              for (a,b),d in zip(loose, component['centered'])), 'direct input centering is tighter in fixed dependency fixture')
    dependency['separate_output_subtraction'] = [enc_interval(x) for x in loose]
    write(directory/'DEPENDENCY_CASE.json', canonical(dependency))
    positive.append({'id': POSITIVE_IDS[8], 'passed': True, 'centered_intervals': [[['-2','1'],['-1','1']],[['1','1'],['2','1']]]})
    capture_path, capture_pin, capture_value = make_capture(directory)
    raw = {'H1': bytes(SAMPLES*8), 'L1': bytes(SAMPLES*8)}
    projection = make_projection(primary, raw, capture_pin, metadata)
    provenance = copy.deepcopy(provenance_template); provenance['input'] = pin(canonical(projection))
    write(directory/'PROJECTION.json', canonical(projection))
    report = primary.build_result(raw, capture_path, projection, provenance, directory/'application')
    report_pin = write(directory/'RESULT.json', canonical(report)); del report
    report = validator.load_result((directory/'RESULT.json').read_bytes())
    summary = validator.validate_result(report, raw, capture_path, projection, provenance, directory/'application', expected_phase='fabricated_qualification')
    expected_summary = {'status': 'all_fields_independently_match', 'windows': 26, 'raw': 208, 'short_long': 416,
                        'mean': 32, 'centered': 208, 'scenarios': 4, 'artifacts': 6}
    check(summary == expected_summary and all(type(summary[k]) is int for k in expected_summary if k != 'status'), 'complete independent full path')
    for scenario in report['scenarios']:
        for component in scenario['energy']['components']:
            check(all(dec_interval(component[k]) == (F(0), F(0)) for k in ('U','M','V')), 'full zero energies')
    positive.append({'id': POSITIVE_IDS[9], 'passed': True, 'full_validation': summary, 'result': report_pin})
    squares = []
    for lo, hi in ((F(-2), F(-1)), (F(1), F(3)), (F(-2), F(3)), (F(0), F(0)), (F(2), F(2))):
        box = enc_interval((lo, hi)); expected = enc_interval(oracle_square((lo, hi)))
        check(primary.square(box) == expected, 'independent square endpoints'); validator.verify_square(expected, box)
        squares.append({'input': box, 'square': expected})
    positive.append({'id': POSITIVE_IDS[10], 'passed': True, 'cases': squares})
    refusals = primary_refusals(primary, raw, capture_path, capture_value, projection, provenance, report, directory)
    refusals += validator_refusals(validator, report, raw, capture_path, projection, provenance, directory, tiny[0]['components'][0])
    check([(x['id'],x['expected_code']) for x in refusals] == list(REFUSALS), 'closed full refusal order')
    check([x['id'] for x in positive] == list(POSITIVE_IDS), 'closed positive order')
    # Seven retained malformed synthetic captures are also fixed evidence.
    expected_names = list(ARTIFACT_NAMES)+['negative-captures/'+label.replace(':','-')+'.json' for label,_ in PRIMARY_REFUSALS[26:33]]
    application_names = ('H1-left-mean.json', 'H1-raw.f64le', 'H1-right-mean.json',
                         'L1-left-mean.json', 'L1-raw.f64le', 'L1-right-mean.json')
    expected_names += ['negative-artifacts/missing-mean-file/'+name for name in application_names if name != 'H1-left-mean.json']
    expected_names += ['negative-artifacts/changed-file-body/'+name for name in application_names]
    artifacts = []
    for path in sorted(directory.rglob('*')):
        if path.is_dir(): continue
        check(path.is_file() and not path.is_symlink() and path.stat().st_nlink == 1, 'retained regular fixture file')
        artifacts.append({'name': path.relative_to(directory).as_posix(), **pin(path.read_bytes())})
    check([x['name'] for x in artifacts] == sorted(expected_names), 'whole retained fixture inventory')
    return {'schema': 'ri106-fabricated-qualification-v1', 'phase': 'fabricated_qualification',
            'status': 'all_fabricated_gates_passed', 'provenance': provenance,
            'scope': 'fixed_RI104_exact_interval_and_finite_centering_qualification_no_observed_execution',
            'counts': {'positive_groups': 11, 'primary_refusals': len(PRIMARY_REFUSALS),
                       'validator_refusals': len(VALIDATOR_REFUSALS), 'refusals': len(REFUSALS),
                       'box_corners': 64, 'application_artifacts': 6, 'retained_files': len(expected_names)},
            'positive': positive, 'refusal_inventory': [{'id': name, 'code': code} for name,code in REFUSALS],
            'refusals': refusals, 'artifacts': artifacts, 'limitations': list(LIMITATIONS)}
