"""Fixed RI104 interval observation consumer; no import-time I/O or scientific import.

Source-only preparation. Actual execution requires the separate admitted caller.
Arithmetic uses exact denominator lifting and midpoint/radius contractions.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import io
import json
import math
import os
import re
import stat
import struct

BITS, FS, M, N, L, T, SAMPLES = 262144, 4096, 16384, 2769, 4096, 10961, 131072
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
ORDER = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
STARTS = {'left': (0, 8192, 16384, 24576, 32768, 40960, 49152),
          'right': (69632, 77824, 86016, 94208, 102400, 110592)}
DESIGN = {'bytes': 32152, 'sha256': 'cd7a585f0002f1aef4d16bb96884c0a745291d41b33e73ff466567cbff5f2478'}
DESIGN_ACCEPTANCE = {'bytes': 10268, 'sha256': '63b781b8a87c0ac86dfdf145ddf2b7073b71137eabd6c4778b5c8b10aabf8267'}
RI100_ACCEPTANCE = {'bytes': 7451, 'sha256': '499fddd1a5315fb8c14c39ae8d161ab11e12f53f8f640d814b1ed81e2f780d21'}
CAPTURE = {'bytes': 51891508, 'sha256': 'fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba'}
RI83 = {'bytes': 38952074, 'sha256': 'e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f'}
RI100 = {'bytes': 8844567, 'sha256': '37dc6865be52e6888bcf325022a18cef65e5b3dd8bf1ba2a9f287e1c12d929dc'}
METADATA = {'bytes': 31096, 'sha256': 'a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80'}
HDF5 = {'H1': {'bytes': 1040592, 'sha256': '6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6'},
        'L1': {'bytes': 1007420, 'sha256': '56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189'}}
MD5 = {'H1': '50441a42c13fc1f14e5c4ea5527f1515', 'L1': '361ae6a040a9fef7897b1e0124d5b0a1'}
ARTIFACT_NAMES = ('H1-left-mean.json', 'H1-raw.f64le', 'H1-right-mean.json',
                  'L1-left-mean.json', 'L1-raw.f64le', 'L1-right-mean.json')
GATES = ('admission:phase', 'admission:inputs', 'admission:metadata', 'admission:segments',
         'operator:complete', 'operator:constant_sum', 'scenario:H1:left', 'scenario:H1:right',
         'scenario:L1:left', 'scenario:L1:right', 'artifacts:complete', 'completion:stable')
COUNTS = {'windows': 26, 'raw': 208, 'short_long': 416, 'mean': 32, 'centered': 208,
          'scenarios': 4, 'artifacts': 6}
METHOD = {'design': DESIGN, 'N': N, 'L': L, 'T': T, 'M': M, 'fs': FS, 'samples': SAMPLES,
          'gps_origin': 1126259446, 'rows': list(ROWS), 'scenario_order': list(ORDER),
          'starts': {k: list(v) for k, v in STARTS.items()}, 'crop': 'first_T_of_each_M',
          'short_slice': [L, L + N], 'output_index': 'short_start_plus_selected_row',
          'preprocessing': 'none_exact_raw_binary64_values', 'arithmetic': 'exact_rational_intervals',
          'width_scale': ['1', format(10**12, 'x')], 'width_rule': 'width_le_input_max_over_10pow12_zero_exact',
          'centering': 'exact_coordinatewise_mean_per_detector_side', 'divisor': 'n_not_n_minus_one',
          'square': 'zero_lower_if_crosses_zero_else_min_endpoint_square',
          'units': 'nominal_strain_outputs_nominal_strain_squared_energies',
          'comparison': 'four_fixed_proxy_traces_no_empirical_magnitude_gate', 'integer_bit_limit': BITS}
LIMITATIONS = [
    'Finite exact long-minus-short processing sensitivity at eight fixed coordinates is not physical waveform error or a result for all2769 outputs.',
    'The same thirteen windows per detector are previously accessed development/calibration data; the empirical PSD comparison is not held-out validation.',
    'Side centering uses exact coordinatewise finite input means and divisor n; unknown population means and overlapping cross-window covariance prevent unbiased trace or chi-square claims.',
    'The four unchanged finite circulant empirical-PSD proxies are assumed models, not established detector-noise covariances or empirical acceptance bands.',
    'Coefficient enclosures and true A constant annihilation are inherited; midpoint rows are not projected and interval errors are not independent random variables.',
    'Nominal V2/C02, blank literal Yunits, clear L1 NO_CW_HW_INJ and unresolved calibration below10Hz remain; injection absence or negligible effect is not claimed.',
    'Deterministic width qualification is not a magnitude or physical-noise test; no calibration envelope, SNR, p-value, native forward map or geometry/gravity claim follows; RET stays paused.',
]


class ContextError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def need(ok, code, message):
    if not ok: raise ContextError(code, message)


def keys(v, names, code='SCHEMA'):
    need(type(v) is dict and all(type(k) is str for k in v) and set(v) == set(names), code, 'closed keys')


def seq(v, n, code='SCHEMA'):
    need(type(v) in (list, tuple) and len(v) == n, code, 'complete sequence')
    return v


def same(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) in (list, tuple): return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def equal(a, b, code, why): need(same(a, b), code, why)


def integer(v):
    need(type(v) is int, 'EXACT', 'plain integer')
    need(abs(v).bit_length() <= BITS, 'RESOURCE', 'integer ceiling')
    return v


def rational(v):
    need(type(v) is F, 'EXACT', 'exact Fraction')
    integer(v.numerator); integer(v.denominator)
    return v


def add(a, b): return rational(rational(a) + rational(b))
def mul(a, b): return rational(rational(a) * rational(b))
def divide(a, n):
    integer(n); need(n > 0, 'DOMAIN', 'positive divisor')
    return rational(rational(a) / n)


def total(v):
    result = F(0)
    for x in v: result = add(result, x)
    return result


def scalar(v):
    rational(v)
    return [format(v.numerator, 'x'), format(v.denominator, 'x')]


def unhex(v):
    need(type(v) is str, 'EXACT', 'hex string')
    need(len(v) <= (BITS + 3)//4 + 1, 'RESOURCE', 'hex ceiling')
    need(re.fullmatch(r'(?:0|-?[1-9a-f][0-9a-f]*)', v) is not None, 'EXACT', 'canonical hex')
    return integer(int(v, 16))


def unscalar(v):
    need(type(v) is list, 'EXACT', 'rational list'); seq(v, 2, 'EXACT')
    n, d = map(unhex, v)
    need(d > 0 and math.gcd(n, d) == 1, 'EXACT', 'reduced positive denominator')
    return rational(F(n, d))


def interval(v):
    seq(v, 2, 'INTERVAL'); lo, hi = map(rational, v)
    need(lo <= hi, 'INTERVAL', 'ordered endpoints')
    return [scalar(lo), scalar(hi)]


def uninterval(v):
    need(type(v) is list, 'INTERVAL', 'interval list'); seq(v, 2, 'INTERVAL')
    lo, hi = map(unscalar, v); need(lo <= hi, 'INTERVAL', 'ordered endpoints')
    return lo, hi


def canonical(v): return (json.dumps(v, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')
def compact(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')
def identity(b):
    need(type(b) is bytes, 'INPUT', 'immutable bytes')
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def cpin(v): return identity(canonical(v))


def pin(v):
    keys(v, ('bytes', 'sha256'), 'INPUT')
    need(type(v['bytes']) is int and v['bytes'] > 0, 'INPUT', 'pin length')
    need(type(v['sha256']) is str and re.fullmatch('[0-9a-f]{64}', v['sha256']) is not None, 'INPUT', 'pin digest')


def parse(b):
    need(type(b) is bytes, 'INPUT', 'JSON bytes')
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'SCHEMA', 'duplicate JSON key'); out[k] = v
        return out
    def bad(_): raise ContextError('EXACT', 'nonfinite JSON')
    try: return json.loads(b, object_pairs_hook=pairs, parse_constant=bad)
    except (UnicodeError, json.JSONDecodeError) as exc: raise ContextError('SCHEMA', 'invalid JSON') from exc


def state(s): return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def file_pin(path):
    p = Path(path); need(p.is_absolute() and p == p.resolve(), 'INPUT', 'literal absolute input')
    before = p.lstat(); need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'INPUT', 'regular single-link input')
    h, length = hashlib.sha256(), 0
    with p.open('rb') as f:
        equal(state(os.fstat(f.fileno())), state(before), 'INPUT', 'opened input changed')
        while block := f.read(1048576): h.update(block); length += len(block)
        equal(state(os.fstat(f.fileno())), state(before), 'INPUT', 'input changed during read')
    equal(state(p.lstat()), state(before), 'INPUT', 'path changed')
    need(length == before.st_size, 'INPUT', 'byte count')
    return {'bytes': length, 'sha256': h.hexdigest()}


class RowReader:
    """RI93 admitted framing pattern, with independent retained P/Q exposure."""
    def __init__(self, stream):
        self.stream, self.buffer, self.pos = stream, b'', 0
        self.digest, self.count = hashlib.sha256(), 0
    def refill(self):
        self.buffer, self.pos = self.stream.read(65536), 0
        self.digest.update(self.buffer); self.count += len(self.buffer)
        need(self.count <= 64*1024*1024, 'RESOURCE', 'capture byte ceiling')
    def take(self, n):
        out = bytearray()
        while len(out) < n:
            if self.pos == len(self.buffer):
                self.refill(); need(bool(self.buffer), 'INPUT', 'truncated capture')
            size = min(n-len(out), len(self.buffer)-self.pos)
            out += self.buffer[self.pos:self.pos+size]; self.pos += size
        return bytes(out)
    def row(self):
        need(self.take(1) == b'{', 'ROW', 'row start')
        chunks, length, depth, string, escape = [b'{'], 1, 1, False, False
        while depth:
            if self.pos == len(self.buffer):
                self.refill(); need(bool(self.buffer), 'INPUT', 'truncated row')
            start = self.pos
            while self.pos < len(self.buffer):
                c = self.buffer[self.pos]; self.pos += 1
                if string:
                    if escape: escape = False
                    elif c == 92: escape = True
                    elif c == 34: string = False
                elif c == 34: string = True
                elif c == 123: depth += 1
                elif c == 125:
                    depth -= 1
                    if depth == 0: break
            block = self.buffer[start:self.pos]; chunks.append(block); length += len(block)
            need(length <= 8*1024*1024, 'RESOURCE', 'row byte ceiling')
        return b''.join(chunks)
    def eof(self):
        if self.pos != len(self.buffer): return False
        self.refill(); return self.buffer == b''


def source_rows(path, expected):
    pin(expected); need(expected['bytes'] <= 64*1024*1024, 'RESOURCE', 'capture byte ceiling')
    equal(file_pin(path), expected, 'INPUT', 'capture identity before parse')
    before = Path(path).lstat()
    header = b'{"dimensions":'+compact({'N': N, 'L': L, 'T': T})+b',"row_order":'+compact(list(ROWS))+b',"rows":['
    with Path(path).open('rb') as f:
        equal(state(os.fstat(f.fileno())), state(before), 'INPUT', 'capture descriptor')
        reader = RowReader(f); equal(reader.take(len(header)), header, 'ROW', 'fixed capture header')
        for position, rowid in enumerate(ROWS):
            if position: equal(reader.take(1), b',', 'ROW', 'row delimiter')
            body = reader.row(); row = parse(body)
            equal(compact(row), body, 'CANONICAL', 'compact capture row')
            keys(row, ('row', 'short', 'long'), 'ROW'); equal(row['row'], rowid, 'ROW', 'row order')
            short, long = [], []
            for out, key, size in ((short, 'short', N), (long, 'long', T)):
                need(type(row[key]) is list, 'ROW', 'row array'); seq(row[key], size, 'ROW')
                for pair in row[key]: out.append(uninterval(pair))
            rowpin = identity(body); del row, body, out, pair
            yield {'row': rowid, 'short': short, 'long': long, 'source_row_pin': rowpin}
            del short, long
        footer = b'],"schema":"ri73-reconstructed-intervals-v1"}'
        equal(reader.take(len(footer)), footer, 'ROW', 'fixed capture footer')
        need(reader.eof(), 'ROW', 'extra capture bytes or row')
        equal({'bytes': reader.count, 'sha256': reader.digest.hexdigest()}, expected, 'INPUT', 'consumed capture identity')
        equal(state(os.fstat(f.fileno())), state(before), 'INPUT', 'capture descriptor after')
    equal(state(Path(path).lstat()), state(before), 'INPUT', 'capture path after')
    equal(file_pin(path), expected, 'INPUT', 'capture identity after')


def common(values):
    denominator = 1
    for x in values:
        rational(x); denominator = integer(math.lcm(denominator, x.denominator))
    return tuple(integer(x.numerator * (denominator // x.denominator)) for x in values), denominator


def lift_coeff(lo, hi):
    need(len(lo) == len(hi) and len(lo) > 0, 'DOMAIN', 'coefficient lengths')
    for a, b in zip(lo, hi): rational(a); rational(b); need(a <= b, 'INTERVAL', 'coefficient order')
    nums, den = common(tuple(lo) + tuple(hi)); size = len(lo)
    return nums[:size], nums[size:], den


def dot_prepared(lo, hi, den, nums, input_den, *, enforce_width=True):
    need(len(lo) == len(hi) == len(nums) and len(nums) > 0, 'DOMAIN', 'dot dimensions')
    center_num, radius_num = 0, 0
    for a, b, x in zip(lo, hi, nums):
        center_num = integer(center_num + integer(integer(a+b) * x))
        radius_num = integer(radius_num + integer(integer(b-a) * abs(x)))
    divisor = integer(integer(2*den) * input_den)
    center, radius = rational(F(center_num, divisor)), rational(F(radius_num, divisor))
    low, high = add(center, -radius), add(center, radius)
    width = mul(F(2), radius); peak = rational(F(max(map(abs, nums)), input_den))
    limit = divide(peak, 10**12)
    passed = width <= limit and (peak != 0 or (low == high == 0))
    if enforce_width: need(passed, 'WIDTH', 'fixed relative enclosure width')
    return {'interval': interval((low, high)), 'center': scalar(center), 'radius': scalar(radius),
            'width': scalar(width), 'input_max': scalar(peak), 'width_limit': scalar(limit), 'width_pass': passed}


def dot_box(lo, hi, v, *, enforce_width=True):
    need(type(enforce_width) is bool, 'DOMAIN', 'width mode bool')
    need(len(lo) == len(hi) == len(v) and len(v) in (1, 3, T), 'DOMAIN', 'fixed public dot domain')
    lo, hi, den = lift_coeff(lo, hi); nums, input_den = common(v)
    return dot_prepared(lo, hi, den, nums, input_den, enforce_width=enforce_width)


def signed_prepared(lo, hi, den, nums, input_den):
    need(len(lo) == len(hi) == len(nums), 'DOMAIN', 'endpoint dimensions')
    a, b = 0, 0
    for low, high, x in zip(lo, hi, nums):
        left, right = (low, high) if x >= 0 else (high, low)
        a = integer(a + integer(left*x)); b = integer(b + integer(right*x))
    divisor = integer(den*input_den)
    return interval((rational(F(a, divisor)), rational(F(b, divisor))))


def overlap(first, second, code):
    a, b = uninterval(first), uninterval(second)
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    need(lo <= hi, code, 'nonempty interval consistency')
    return interval((lo, hi))


def isum(values):
    lo, hi = F(0), F(0)
    for v in values:
        a, b = uninterval(v); lo, hi = add(lo, a), add(hi, b)
    return interval((lo, hi))


def idiv(value, n):
    a, b = uninterval(value)
    return interval((divide(a, n), divide(b, n)))


def square(value):
    lo, hi = uninterval(value); a, b = mul(lo, lo), mul(hi, hi)
    return interval((F(0) if lo <= 0 <= hi else min(a, b), max(a, b)))


def energy(raw_dots, mean_dot, centered_dots):
    need(len(raw_dots) == len(centered_dots) and len(raw_dots) in (2, 3, 6, 7), 'DOMAIN', 'fixed public energy domain')
    raw = [square(v['interval']) for v in raw_dots]
    centered = [square(v['interval']) for v in centered_dots]
    mean = square(mean_dot['interval']); u, v = idiv(isum(raw), len(raw)), idiv(isum(centered), len(centered))
    check = overlap(u, isum((v, mean)), 'ENERGY')
    return {'raw_squares': raw, 'mean_square': mean, 'centered_squares': centered,
            'U': u, 'M': mean, 'V': v, 'identity_intersection': check}


def raw_vector(body):
    need(type(body) is bytes and len(body) == SAMPLES*8, 'INPUT', 'complete raw f64le bytes')
    ratios, den = [], 1
    for (x,) in struct.iter_unpack('<d', body):
        need(math.isfinite(x), 'INPUT', 'nonfinite raw sample')
        a, b = x.as_integer_ratio(); integer(a); integer(b); ratios.append((a, b)); den = max(den, b)
    return tuple(integer(a*(den//b)) for a, b in ratios), integer(den)


def prepare_inputs(raw_bodies):
    keys(raw_bodies, ('H1', 'L1'), 'INPUT'); prepared = {}
    for detector in ('H1', 'L1'):
        nums, den = raw_vector(raw_bodies[detector])
        for side, starts in STARTS.items():
            vectors = [tuple(nums[s:s+T]) for s in starts]; count = len(starts)
            mean_nums = tuple(integer(sum(v[j] for v in vectors)) for j in range(T))
            mean_den = integer(count*den)
            centered = [tuple(integer(integer(count*x)-mean_nums[j]) for j, x in enumerate(v)) for v in vectors]
            prepared[detector+':'+side] = {'raw': vectors, 'raw_den': den,
                                          'mean': mean_nums, 'mean_den': mean_den,
                                          'centered': centered, 'centered_den': mean_den}
        del nums
    return prepared


def metadata_check(value):
    need(type(value) is dict and type(value.get('detectors')) is list and len(value['detectors']) == 2,
         'METADATA', 'full RI37 detector metadata')
    for index, detector in enumerate(('H1', 'L1')):
        entry = value['detectors'][index]
        need(type(entry) is dict, 'METADATA', 'detector metadata')
        for field, expected in (('data_quality', 127), ('hardware_injection_flags', 31 if detector == 'H1' else 23)):
            rec = entry.get(field)
            need(type(rec) is dict and type(rec.get('raw_bitfields')) is list, 'FLAGS', 'complete fixed flags')
            equal(rec['raw_bitfields'], [expected]*32, 'FLAGS', 'fixed literal flag masks')
    equal(cpin(value), METADATA, 'METADATA', 'complete accepted metadata')


def slice_record(start, end, metadata):
    need(type(start) is type(end) is int and 0 <= start < end <= SAMPLES, 'DOMAIN', 'slice indices')
    flags = list(range(start//FS, (end+FS-1)//FS))
    return {'start': start, 'end': end, 'gps_start_offset': scalar(F(start, FS)),
            'gps_end_offset': scalar(F(end, FS)), 'flag_rows': flags,
            'dq_masks': [metadata['data_quality']['raw_bitfields'][i] for i in flags],
            'injection_masks': [metadata['hardware_injection_flags']['raw_bitfields'][i] for i in flags]}


def projection_check(proj, phase, raw_bodies, capture_path):
    keys(proj, ('context', 'metadata', 'hdf5', 'capture', 'ri83', 'ri100', 'segments', 'traces'), 'INPUT')
    need(phase in ('fabricated_qualification', 'fixed_observed_application') and type(phase) is str, 'PHASE', 'fixed phase')
    actual = phase == 'fixed_observed_application'
    equal(proj['context'], 'accepted_fixed_observed_inputs' if actual else 'fabricated_inputs_not_observed', 'PHASE', 'projection context')
    metadata_check(proj['metadata']); keys(proj['hdf5'], ('H1', 'L1'), 'INPUT')
    for name, expected in (('capture', CAPTURE), ('ri83', RI83), ('ri100', RI100)):
        pin(proj[name])
        if actual: equal(proj[name], expected, 'INPUT', 'actual '+name+' pin')
        else: need(proj[name] != expected, 'PHASE', 'fabricated pin impersonates actual')
    for detector in ('H1', 'L1'):
        pin(proj['hdf5'][detector])
        if actual: equal(proj['hdf5'][detector], HDF5[detector], 'INPUT', 'actual HDF5 pin')
        else: need(proj['hdf5'][detector] != HDF5[detector], 'PHASE', 'fabricated HDF5 pin')
    equal(file_pin(capture_path), proj['capture'], 'INPUT', 'capture bytes')
    seq(proj['segments'], 26, 'INPUT'); expected_segments = []
    for name in ORDER:
        detector, side = name.split(':')
        for start in STARTS[side]:
            expected_segments.append({'id': name+':'+str(start), 'detector': detector, 'side': side,
                                      'start': start, 'end': start+M,
                                      'raw_sha256': hashlib.sha256(raw_bodies[detector][8*start:8*(start+M)]).hexdigest()})
    equal(proj['segments'], expected_segments, 'INPUT', 'all original M-segment hashes and indices')
    seq(proj['traces'], 4, 'TRACE')
    for name, record in zip(ORDER, proj['traces']):
        keys(record, ('id', 'interval', 'source_identity', 'model', 'units'), 'TRACE')
        equal(record['id'], name, 'TRACE', 'trace scenario order'); uninterval(record['interval']); pin(record['source_identity'])
        equal(record['model'], 'postulated_finite_circulant_from_empirical_psd' if actual else 'fabricated_trace_not_observed', 'TRACE', 'trace model')
        equal(record['units'], 'nominal_strain_squared_sum_of_eight_centered_coordinates', 'TRACE', 'trace units')


def provenance_check(value, phase, proj):
    keys(value, ('sources', 'input', 'acceptance', 'runtime'), 'PROVENANCE')
    keys(value['sources'], ('design', 'consumer', 'validator', 'qualifier', 'implementation', 'api'), 'PROVENANCE')
    for p in value['sources'].values(): pin(p)
    equal(value['sources']['design'], DESIGN, 'SOURCE', 'accepted design')
    equal(value['input'], cpin(proj), 'INPUT', 'complete projection binding')
    keys(value['acceptance'], ('design', 'ri100', 'qualification', 'custody'), 'PROVENANCE')
    equal(value['acceptance']['design'], DESIGN_ACCEPTANCE, 'PROVENANCE', 'design decision')
    equal(value['acceptance']['ri100'], RI100_ACCEPTANCE, 'PROVENANCE', 'prior result decision')
    for name in ('qualification', 'custody'):
        if phase == 'fabricated_qualification': need(value['acceptance'][name] is None, 'PHASE', 'fabricated admission claim')
        elif phase == 'fixed_observed_application': pin(value['acceptance'][name])
        else: raise ContextError('PHASE', 'fixed phase')
    keys(value['runtime'], ('fingerprint', 'inventory', 'interpreter'), 'PROVENANCE')
    for p in value['runtime'].values(): pin(p)


def write_artifact(directory, name, body, dtype, shape):
    need(name in ARTIFACT_NAMES, 'ARTIFACT', 'fixed artifact name')
    with (directory/name).open('xb') as f:
        f.write(body); f.flush(); os.fsync(f.fileno())
    return {'name': name, **identity(body), 'dtype': dtype, 'shape': shape}


def artifact_check(directory, records):
    equal(sorted(p.name for p in directory.iterdir()), list(ARTIFACT_NAMES), 'ARTIFACT', 'exclusive artifact inventory')
    equal([r['name'] for r in records], list(ARTIFACT_NAMES), 'ARTIFACT', 'artifact row order')
    for rec in records:
        keys(rec, ('name', 'bytes', 'sha256', 'dtype', 'shape'), 'ARTIFACT')
        p = directory/rec['name']; st = p.lstat()
        need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and not p.is_symlink(), 'ARTIFACT', 'regular exclusive artifact')
        equal(file_pin(p), {k: rec[k] for k in ('bytes', 'sha256')}, 'ARTIFACT', 'retained artifact bytes')


def build_result(raw_bodies, capture_path, projection, provenance, artifact_dir, *, phase='fabricated_qualification'):
    keys(raw_bodies, ('H1', 'L1'), 'INPUT')
    for body in raw_bodies.values(): need(type(body) is bytes and len(body) == SAMPLES*8, 'INPUT', 'complete raw bytes')
    projection_check(projection, phase, raw_bodies, capture_path); provenance_check(provenance, phase, projection)
    input_before, prov_before = cpin(projection), cpin(provenance)
    prepared = prepare_inputs(raw_bodies)
    directory = Path(artifact_dir)
    need(directory.is_absolute() and directory.parent == directory.parent.resolve(), 'ARTIFACT', 'literal artifact parent')
    need(not directory.exists() and not directory.is_symlink(), 'ARTIFACT', 'exclusive new artifact directory')
    directory.mkdir(mode=0o700); artifacts = []; scenarios = []
    for detector in ('H1', 'L1'):
        artifacts.append(write_artifact(directory, detector+'-raw.f64le', raw_bodies[detector], '<f8', [SAMPLES]))
    for index, name in enumerate(ORDER):
        detector, side = name.split(':'); pre = prepared[name]; metadata = projection['metadata']['detectors'][0 if detector == 'H1' else 1]
        filename = name.replace(':', '-')+'-mean.json'
        mean = {'schema': 'ri106-coordinatewise-mean-v1', 'id': name,
                'values': [scalar(rational(F(x, pre['mean_den']))) for x in pre['mean']]}
        artifacts.append(write_artifact(directory, filename, canonical(mean), 'reduced_hex_rational', [T])); del mean
        windows = []
        for start in STARTS[side]:
            windows.append({'start': start, 'slices': {'M': slice_record(start, start+M, metadata),
                            'T': slice_record(start, start+T, metadata),
                            'short': slice_record(start+L, start+L+N, metadata)},
                            'raw_sha256': hashlib.sha256(raw_bodies[detector][8*start:8*(start+M)]).hexdigest(), 'outputs': []})
        scenarios.append({'id': name, 'detector': detector, 'side': side, 'count': len(windows), 'windows': windows,
                          'mean': {'artifact': filename, 'outputs': []},
                          'centered': [{'start': start, 'outputs': []} for start in STARTS[side]],
                          'energy': {'components': []}, 'trace': projection['traces'][index]})
    operator_rows = []
    iterator = iter(source_rows(capture_path, projection['capture']))
    for expected_row in ROWS:
        try: source = next(iterator)
        except StopIteration as exc: raise ContextError('ROW', 'missing coefficient row') from exc
        equal(source['row'], expected_row, 'ROW', 'source row order')
        short, long = source['short'], source['long']
        sl, sh, sd = lift_coeff([v[0] for v in short], [v[1] for v in short])
        ql, qh, qd = lift_coeff([v[0] for v in long], [v[1] for v in long])
        den = integer(math.lcm(sd, qd)); slo = tuple(integer(x*(den//sd)) for x in sl); shi = tuple(integer(x*(den//sd)) for x in sh)
        qlo = tuple(integer(x*(den//qd)) for x in ql); qhi = tuple(integer(x*(den//qd)) for x in qh)
        alo = tuple(integer(qlo[j]-(shi[j-L] if L <= j < L+N else 0)) for j in range(T))
        ahi = tuple(integer(qhi[j]-(slo[j-L] if L <= j < L+N else 0)) for j in range(T))
        sums = (integer(sum(alo)), integer(sum(ahi)))
        need(sums[0] <= 0 <= sums[1], 'ROW', 'coefficient interval row sum misses constant annihilation')
        operator_rows.append({'row': expected_row, 'short_count': N, 'long_count': T, 'source_row_pin': source['source_row_pin'],
                              'a_midpoint_sum': scalar(rational(F(integer(sums[0]+sums[1]), integer(2*den)))),
                              'a_radius_sum': scalar(rational(F(integer(sums[1]-sums[0]), integer(2*den)))),
                              'a_row_sum_interval': interval((F(sums[0], den), F(sums[1], den))), 'contains_zero': True})
        del short, long, source, sl, sh, ql, qh
        for scen in scenarios:
            pre = prepared[scen['id']]; raw_dots, centered_dots = [], []
            for idx, nums in enumerate(pre['raw']):
                dot = {'row': expected_row, **dot_prepared(alo, ahi, den, nums, pre['raw_den'])}
                ps = signed_prepared(slo, shi, den, nums[L:L+N], pre['raw_den'])
                qs = signed_prepared(qlo, qhi, den, nums, pre['raw_den'])
                pl, ph = uninterval(ps); ql0, qh0 = uninterval(qs)
                inter = overlap(dot['interval'], interval((add(ql0, -ph), add(qh0, -pl))), 'DOT')
                scen['windows'][idx]['outputs'].append({'row': expected_row, 'short': ps, 'long': qs, 'delta': dot, 'route_intersection': inter})
                raw_dots.append(dot)
            md = {'row': expected_row, **dot_prepared(alo, ahi, den, pre['mean'], pre['mean_den'])}
            scen['mean']['outputs'].append(md)
            equal(unscalar(md['center']), divide(total(unscalar(x['center']) for x in raw_dots), len(raw_dots)), 'CENTER', 'exact mean linearity')
            overlap(md['interval'], idiv(isum(x['interval'] for x in raw_dots), len(raw_dots)), 'CENTER')
            for idx, nums in enumerate(pre['centered']):
                dot = {'row': expected_row, **dot_prepared(alo, ahi, den, nums, pre['centered_den'])}
                equal(unscalar(dot['center']), add(unscalar(raw_dots[idx]['center']), -unscalar(md['center'])), 'CENTER', 'exact centered linearity')
                scen['centered'][idx]['outputs'].append(dot); centered_dots.append(dot)
            zl, zh = uninterval(isum(x['interval'] for x in centered_dots)); need(zl <= 0 <= zh, 'CENTER', 'centered sum includes zero')
            scen['energy']['components'].append({'row': expected_row, **energy(raw_dots, md, centered_dots)})
        del alo, ahi, slo, shi, qlo, qhi
    absent = object(); need(next(iterator, absent) is absent, 'ROW', 'extra source row')
    for scen in scenarios:
        e = scen['energy']
        for name in ('U', 'M', 'V'): e[name] = isum(row[name] for row in e['components'])
        e['identity_intersection'] = overlap(e['U'], isum((e['V'], e['M'])), 'ENERGY')
    artifacts.sort(key=lambda r: r['name']); artifact_check(directory, artifacts)
    equal(cpin(projection), input_before, 'INPUT', 'projection mutation'); equal(cpin(provenance), prov_before, 'PROVENANCE', 'provenance mutation')
    return {'schema': 'ri104-observed-context-benchmark-v1', 'phase': phase, 'status': 'all_gates_passed', 'method': METHOD,
            'provenance': provenance, 'inputs': {'projection': projection, 'artifacts': artifacts},
            'operator': {'capture': projection['capture'], 'schema': 'ri73-reconstructed-intervals-v1',
                         'dimensions': {'N': N, 'L': L, 'T': T}, 'row_order': list(ROWS), 'rows': operator_rows,
                         'constant_annihilation': 'accepted_true_A_annihilation_midpoints_not_projected' if phase == 'fixed_observed_application' else 'fabricated_row_fixture_not_observed'},
            'scenarios': scenarios, 'checks': {'inventory': list(GATES), 'counts': {'total': 12, 'passed': 12, 'failed': 0},
                                             'results': [{'id': name, 'passed': True} for name in GATES]}, 'limitations': list(LIMITATIONS)}


def check_ri100_header(value):
    """Check only the fixed prior header; this does not admit a result body.

    The actual adapter calls this after whole-body identity and JSON decoding.
    Qualification may supply only source-known header metadata to this guard.
    """
    need(type(value) is dict and all(type(key) is str for key in value),
         'INPUT', 'actual prior header mapping')
    equal(value.get('schema'), 'ri98-mode-weighted-trace-v1', 'INPUT', 'accepted prior schema')
    equal(value.get('phase'), 'fixed_saved_application', 'PHASE', 'actual prior phase')
    equal(value.get('status'), 'all_declared_checks_passed', 'TRACE', 'accepted prior status')


def actual_projection(ri83_body, ri100_body, metadata):
    # Entry point only after complete fixed body admission. No module imports.
    equal(identity(ri83_body), RI83, 'INPUT', 'RI83 before parse'); equal(identity(ri100_body), RI100, 'INPUT', 'RI100 before parse')
    old, trace = parse(ri83_body), parse(ri100_body)
    need(old.get('schema') == 'ri78-off-event-spectra-v1', 'INPUT', 'accepted report schema')
    check_ri100_header(trace)
    segments, traces = [], []
    for entry in old['detectors']:
        detector = entry['detector']
        for side in entry['sides']:
            for segment in side['segments']:
                start = segment['start']
                segments.append({'id': detector+':'+side['side']+':'+str(start), 'detector': detector, 'side': side['side'],
                                 'start': start, 'end': segment['end'], 'raw_sha256': segment['raw_sha256']})
    for name, entry in zip(ORDER, trace['scenarios']):
        equal(entry['id'], name, 'TRACE', 'actual trace order')
        traces.append({'id': name, 'interval': entry['final'], 'source_identity': entry['source_identity'],
                       'model': 'postulated_finite_circulant_from_empirical_psd', 'units': 'nominal_strain_squared_sum_of_eight_centered_coordinates'})
    return {'context': 'accepted_fixed_observed_inputs', 'metadata': metadata, 'hdf5': HDF5,
            'capture': CAPTURE, 'ri83': RI83, 'ri100': RI100, 'segments': segments, 'traces': traces}


def run_observed(hdf_bodies, capture_path, ri83_body, ri100_body, metadata_body, provenance, artifact_dir, inspector):
    keys(hdf_bodies, ('H1', 'L1'), 'INPUT')
    for detector in ('H1', 'L1'):
        equal(identity(hdf_bodies[detector]), HDF5[detector], 'INPUT', 'whole HDF5 before any parse')
        equal(hashlib.md5(hdf_bodies[detector], usedforsecurity=False).hexdigest(), MD5[detector], 'INPUT', 'publisher MD5')
    capture_state = state(Path(capture_path).lstat())
    equal(file_pin(capture_path), CAPTURE, 'INPUT', 'capture before parse')
    equal(state(Path(capture_path).lstat()), capture_state, 'INPUT', 'initial capture state')
    provenance_before = cpin(provenance)
    for body, expected in ((ri83_body, RI83), (ri100_body, RI100), (metadata_body, METADATA)):
        equal(identity(body), expected, 'INPUT', 'complete predecessor before parse')
    metadata = parse(metadata_body); metadata_check(metadata)
    import h5py  # Lazy, only after admitted actual input branch; runtime pinned by caller.
    inspected = dict(metadata); inspected['detectors'] = []
    expected_files = {item['detector']: item for item in inspector.FILES}
    for detector in ('H1', 'L1'):
        inspected['detectors'].append(inspector._inspect(hdf_bodies[detector], expected_files[detector]))
    equal(inspected, metadata, 'METADATA', 'full actual RI37 inspector replay')
    raw = {}
    for detector in ('H1', 'L1'):
        with h5py.File(io.BytesIO(hdf_bodies[detector]), 'r') as handle:
            values = handle['/strain/Strain'][()]
            need(values.shape == (SAMPLES,) and values.dtype.kind == 'f' and values.dtype.itemsize == 8,
                 'INPUT', 'full binary64 HDF5 vector')
            raw[detector] = values.astype('<f8', copy=False).tobytes(order='C')
        del values
    projection = actual_projection(ri83_body, ri100_body, metadata)
    result = build_result(raw, capture_path, projection, provenance, artifact_dir, phase='fixed_observed_application')
    equal(file_pin(capture_path), CAPTURE, 'INPUT', 'whole actual branch capture identity')
    equal(state(Path(capture_path).lstat()), capture_state, 'INPUT', 'whole actual branch capture state')
    keys(hdf_bodies, ('H1', 'L1'), 'INPUT')
    for detector in ('H1', 'L1'):
        equal(identity(hdf_bodies[detector]), HDF5[detector], 'INPUT', 'actual HDF5 container stable')
    for body, expected in ((ri83_body, RI83), (ri100_body, RI100), (metadata_body, METADATA)):
        equal(identity(body), expected, 'INPUT', 'actual held body stable')
    equal(cpin(provenance), provenance_before, 'PROVENANCE', 'whole actual branch provenance stable')
    return result
