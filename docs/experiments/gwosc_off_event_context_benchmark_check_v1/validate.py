"""Independent RI106 endpoint-sign saved-result validator (source preparation).

This module imports no producer and performs no import-time I/O.  HDF5 is
imported lazily only in the separately admitted actual-input path.  Arithmetic
uses signed interval endpoints, independently streamed retained coefficients,
and exact finite raw samples.  The author wrote the RI104 design and earlier
RI98 product validator, but did not author this RI106 primary or qualifier.
"""

from fractions import Fraction
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import stat
import struct


BITS = 262144
FS, M, N, L, T, LENGTH = 4096, 16384, 2769, 4096, 10961, 131072
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
ORDER = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
STARTS = {'left': (0, 8192, 16384, 24576, 32768, 40960, 49152),
          'right': (69632, 77824, 86016, 94208, 102400, 110592)}
SNAPSHOT_PIN = {'bytes': 51891508, 'sha256': 'fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba'}
RI83_PIN = {'bytes': 38952074, 'sha256': 'e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f'}
RI100_PIN = {'bytes': 8844567, 'sha256': '37dc6865be52e6888bcf325022a18cef65e5b3dd8bf1ba2a9f287e1c12d929dc'}
RI37_PIN = {'bytes': 31096, 'sha256': 'a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80'}
HDF_PINS = {
    'H1': {'bytes': 1040592, 'sha256': '6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6'},
    'L1': {'bytes': 1007420, 'sha256': '56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189'},
}
MD5S = {'H1': '50441a42c13fc1f14e5c4ea5527f1515', 'L1': '361ae6a040a9fef7897b1e0124d5b0a1'}
DESIGN_PIN = {'bytes': 32152, 'sha256': 'cd7a585f0002f1aef4d16bb96884c0a745291d41b33e73ff466567cbff5f2478'}
DESIGN_DECISION = {'bytes': 10268, 'sha256': '63b781b8a87c0ac86dfdf145ddf2b7073b71137eabd6c4778b5c8b10aabf8267'}
RI100_DECISION = {'bytes': 7451, 'sha256': '499fddd1a5315fb8c14c39ae8d161ab11e12f53f8f640d814b1ed81e2f780d21'}
PHASES = ('fabricated_qualification', 'fixed_observed_application')
TRACE_UNITS = 'nominal_strain_squared_sum_of_eight_centered_coordinates'
GATES = ('admission:phase', 'admission:inputs', 'admission:metadata', 'admission:segments',
         'operator:complete', 'operator:constant_sum', 'scenario:H1:left', 'scenario:H1:right',
         'scenario:L1:left', 'scenario:L1:right', 'artifacts:complete', 'completion:stable')
METHOD = {'design': DESIGN_PIN, 'N': N, 'L': L, 'T': T, 'M': M, 'fs': FS, 'samples': LENGTH,
          'gps_origin': 1126259446, 'rows': list(ROWS), 'scenario_order': list(ORDER),
          'starts': {k: list(v) for k, v in STARTS.items()}, 'crop': 'first_T_of_each_M',
          'short_slice': [L, L + N], 'output_index': 'short_start_plus_selected_row',
          'preprocessing': 'none_exact_raw_binary64_values', 'arithmetic': 'exact_rational_intervals',
          'width_scale': ['1', format(10**12, 'x')], 'width_rule': 'width_le_input_max_over_10pow12_zero_exact',
          'centering': 'exact_coordinatewise_mean_per_detector_side', 'divisor': 'n_not_n_minus_one',
          'square': 'zero_lower_if_crosses_zero_else_min_endpoint_square',
          'units': 'nominal_strain_outputs_nominal_strain_squared_energies',
          'comparison': 'four_fixed_proxy_traces_no_empirical_magnitude_gate', 'integer_bit_limit': BITS}
# Protocol vocabulary shared by specification only; no producer computation is
# imported or called to construct this validator's expected numerical records.
LIMITATIONS = [
    'Finite exact long-minus-short processing sensitivity at eight fixed coordinates is not physical waveform error or a result for all2769 outputs.',
    'The same thirteen windows per detector are previously accessed development/calibration data; the empirical PSD comparison is not held-out validation.',
    'Side centering uses exact coordinatewise finite input means and divisor n; unknown population means and overlapping cross-window covariance prevent unbiased trace or chi-square claims.',
    'The four unchanged finite circulant empirical-PSD proxies are assumed models, not established detector-noise covariances or empirical acceptance bands.',
    'Coefficient enclosures and true A constant annihilation are inherited; midpoint rows are not projected and interval errors are not independent random variables.',
    'Nominal V2/C02, blank literal Yunits, clear L1 NO_CW_HW_INJ and unresolved calibration below10Hz remain; injection absence or negligible effect is not claimed.',
    'Deterministic width qualification is not a magnitude or physical-noise test; no calibration envelope, SNR, p-value, native forward map or geometry/gravity claim follows; RET stays paused.',
]


class ValidationError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def require(condition, code, message):
    if not condition:
        raise ValidationError(code, message)


def fields(value, names, code='SCHEMA'):
    require(type(value) is dict and all(type(k) is str for k in value)
            and set(value) == set(names), code, 'closed object fields differ')


def sequence(value, count, code='SCHEMA'):
    require(type(value) in (list, tuple) and len(value) == count,
            code, 'complete ordered sequence required')
    return value


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) in (tuple, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def equal(actual, expected, code, message):
    require(same(actual, expected), code, message)


def integer(value):
    require(type(value) is int, 'EXACT', 'plain integer required')
    require(abs(value).bit_length() <= BITS, 'RESOURCE', 'integer bit ceiling')
    return value


def rational(value):
    require(type(value) is Fraction, 'EXACT', 'Fraction required')
    integer(value.numerator)
    integer(value.denominator)
    return value


def plus(a, b):
    return rational(rational(a) + rational(b))


def minus(a, b):
    return rational(rational(a) - rational(b))


def times(a, b):
    return rational(rational(a) * rational(b))


def divide(a, count):
    require(type(count) is int and count > 0, 'DOMAIN', 'positive plain divisor')
    return rational(rational(a) / count)


def total(values):
    result = Fraction(0)
    for value in values:
        result = plus(result, value)
    return result


def hex_integer(value):
    require(type(value) is str, 'EXACT', 'hexadecimal integer text required')
    require(len(value) <= (BITS + 3) // 4 + 1, 'RESOURCE', 'integer text ceiling')
    require(re.fullmatch(r'0|-?[1-9a-f][0-9a-f]*', value) is not None,
            'EXACT', 'canonical lowercase signed hexadecimal integer')
    return integer(int(value, 16))


def decode(value):
    require(type(value) is list and len(value) == 2, 'EXACT', 'rational pair required')
    a, b = (hex_integer(x) for x in value)
    require(b > 0 and math.gcd(a, b) == 1, 'EXACT', 'positive reduced denominator')
    return rational(Fraction(a, b))


def encoded(value):
    if type(value) is Fraction:
        value = rational(value)
        return [format(value.numerator, 'x'), format(value.denominator, 'x')]
    if type(value) in (tuple, list):
        return [encoded(x) for x in value]
    if type(value) is dict:
        return {k: encoded(v) for k, v in value.items()}
    return value


def interval(value, *, serialized=False):
    a, b = sequence(value, 2, 'INTERVAL')
    if serialized:
        a, b = decode(a), decode(b)
    else:
        a, b = rational(a), rational(b)
    require(a <= b, 'INTERVAL', 'ordered interval endpoints required')
    return a, b


def canonical(value):
    try:
        return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                           allow_nan=False) + '\n').encode('ascii')
    except (TypeError, ValueError, UnicodeError) as error:
        raise ValidationError('CANONICAL', 'canonical finite JSON required') from error


def identity(body):
    require(type(body) is bytes, 'INPUT', 'immutable complete bytes required')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def pin(record, code='PROVENANCE'):
    fields(record, ('bytes', 'sha256'), code)
    require(type(record['bytes']) is int and record['bytes'] > 0
            and type(record['sha256']) is str
            and re.fullmatch(r'[0-9a-f]{64}', record['sha256']) is not None,
            code, 'complete byte identity required')


def parse_json(body):
    require(type(body) is bytes, 'INPUT', 'JSON bytes required')
    def pairs(items):
        output = {}
        for name, value in items:
            require(name not in output, 'SCHEMA', 'duplicate JSON key')
            output[name] = value
        return output
    def reject(value):
        raise ValidationError('SCHEMA', 'nonfinite JSON token')
    try:
        return json.loads(body.decode('ascii'), object_pairs_hook=pairs, parse_constant=reject)
    except ValidationError:
        raise
    except (UnicodeError, ValueError, TypeError, OverflowError) as error:
        raise ValidationError('SCHEMA', 'invalid JSON body') from error


def endpoint_dot(coefficients, values):
    """Independent signed endpoint accumulation; no midpoint/radius oracle."""
    require(type(coefficients) in (tuple, list) and type(values) in (tuple, list)
            and len(coefficients) == len(values) and len(values) > 0,
            'DOMAIN', 'matching nonempty dot-product vectors required')
    endpoints = tuple(interval(coefficient) for coefficient in coefficients)
    lower, upper = zip(*endpoints)
    ld, li = lifted(lower)
    ud, ui = lifted(upper)
    vd, vi = lifted(values)
    return scaled_endpoint_dot((ld, li), (ud, ui), (vd, vi))


def lifted(values):
    """Independent exact common denominator; no float conversion or rounding."""
    require(type(values) in (tuple, list) and len(values) > 0,
            'DOMAIN', 'nonempty exact vector required')
    denominator = 1
    for value in values:
        denominator = integer(math.lcm(denominator, rational(value).denominator))
    return denominator, tuple(integer(value.numerator * (denominator // value.denominator)) for value in values)


def scaled_endpoint_dot(lower, upper, vector):
    ld, li = lower
    ud, ui = upper
    vd, vi = vector
    require(len(li) == len(ui) == len(vi) and len(vi) > 0,
            'DOMAIN', 'matching endpoint integer vectors')
    # Two independent endpoint denominators are deliberately retained.  Four
    # signed integer sums keep the sign choice explicit, then combine exactly.
    lp = ln = up = un = 0
    for a, b, x in zip(li, ui, vi):
        if x == 0 or a == b == 0:
            continue
        if x >= 0:
            lp = integer(lp + integer(a * x))
            up = integer(up + integer(b * x))
        else:
            ln = integer(ln + integer(b * x))
            un = integer(un + integer(a * x))
    low = plus(rational(Fraction(lp, integer(ld * vd))), rational(Fraction(ln, integer(ud * vd))))
    high = plus(rational(Fraction(up, integer(ud * vd))), rational(Fraction(un, integer(ld * vd))))
    return low, high


def square(value):
    a, b = interval(value)
    aa, bb = times(a, a), times(b, b)
    return (Fraction(0) if a <= 0 <= b else min(aa, bb), max(aa, bb))


def interval_sum(values):
    low = high = Fraction(0)
    for value in values:
        a, b = interval(value)
        low, high = plus(low, a), plus(high, b)
    return low, high


def overlap(a, b):
    a, b = interval(a), interval(b)
    return max(a[0], b[0]) <= min(a[1], b[1])


def enforce_width(enclosure, scale):
    low, high = interval(enclosure)
    scale = rational(scale)
    require(scale >= 0, 'DOMAIN', 'nonnegative input scale required')
    require(minus(high, low) <= divide(scale, 10**12), 'WIDTH', 'fixed direct enclosure width exceeded')
    if scale == 0:
        require(low == high == 0, 'WIDTH', 'zero input requires exact zero enclosure')


def dot_record(enclosure, scale, *, enforce=True):
    require(type(enforce) is bool, 'DOMAIN', 'plain width enforcement flag')
    a, b = interval(enclosure)
    scale = rational(scale)
    require(scale >= 0, 'DOMAIN', 'nonnegative exact scale')
    width = minus(b, a)
    limit = divide(scale, 10**12)
    passed = width <= limit and (scale != 0 or a == b == 0)
    if enforce:
        enforce_width((a, b), scale)
    return encoded({'interval': (a, b), 'center': divide(plus(a, b), 2),
                    'radius': divide(width, 2), 'width': width, 'input_max': scale,
                    'width_limit': limit, 'width_pass': passed})


def verify_dot(record, lo, hi, values, *, enforce_width=True):
    require(type(lo) in (tuple, list) and type(hi) in (tuple, list)
            and type(values) in (tuple, list) and len(lo) == len(hi) == len(values)
            and len(values) in (1, 3, T), 'DOMAIN', 'fixed tiny or full dot domain')
    expected = dot_record(endpoint_dot(tuple(zip(lo, hi)), values),
                          max(abs(rational(value)) for value in values), enforce=enforce_width)
    verify_dot_record(record, expected)
    return expected


def verify_square(record, value):
    # The public protocol receives the serialized interval used by the actual
    # consumer. Internal square arithmetic still takes exact endpoint pairs.
    expected = encoded(square(interval(value, serialized=True)))
    equal(record, expected, 'ENERGY', 'independent square enclosure differs')
    return expected


def intersect(a, b, code='ENERGY'):
    a, b = interval(a), interval(b)
    result = max(a[0], b[0]), min(a[1], b[1])
    require(result[0] <= result[1], code, 'required interval intersection is empty')
    return result


def component_energy(raw_dots, mean_dot, centered_dots):
    require(type(raw_dots) in (tuple, list) and type(centered_dots) in (tuple, list)
            and len(raw_dots) == len(centered_dots) and len(raw_dots) in (2, 3, 6, 7),
            'DOMAIN', 'fixed tiny or full side count')
    def value(record):
        require(type(record) is dict and 'interval' in record, 'SCHEMA', 'dot interval required')
        return interval(record['interval'], serialized=True)
    raw_squares = tuple(square(value(x)) for x in raw_dots)
    centered_squares = tuple(square(value(x)) for x in centered_dots)
    mean_square = square(value(mean_dot))
    n = len(raw_dots)
    usum, vsum = interval_sum(raw_squares), interval_sum(centered_squares)
    u = tuple(divide(x, n) for x in usum)
    v = tuple(divide(x, n) for x in vsum)
    im = intersect(u, interval_sum((v, mean_square)))
    return encoded({'raw_squares': raw_squares, 'mean_square': mean_square,
                    'centered_squares': centered_squares, 'U': u, 'M': mean_square,
                    'V': v, 'identity_intersection': im})


def verify_energy(record, raw_dots, mean_dot, centered_dots):
    expected = component_energy(raw_dots, mean_dot, centered_dots)
    equal(record, expected, 'ENERGY', 'independent finite energy record differs')
    return expected


def exact_raw(body):
    require(type(body) is bytes and len(body) == LENGTH * 8, 'INPUT', 'complete little-endian float64 array')
    result = []
    for (value,) in struct.iter_unpack('<d', body):
        require(math.isfinite(value), 'INPUT', 'raw sample must be finite')
        result.append(rational(Fraction.from_float(value)))
    return tuple(result)


def state(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def regular_path(path, *, ceiling=None):
    require(isinstance(path, (str, Path)), 'INPUT', 'input path required')
    path = Path(path)
    try:
        require(path.is_absolute() and path.resolve(strict=True) == path,
                'INPUT', 'canonical absolute path required')
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and not path.is_symlink(), 'INPUT', 'regular nonsymlink file required')
        if ceiling is not None:
            require(info.st_size <= ceiling, 'RESOURCE', 'input file byte ceiling')
        return path, state(info)
    except OSError as error:
        raise ValidationError('INPUT', 'input path unavailable') from error


def open_identity(stream, ceiling=None):
    stream.seek(0)
    digest, count = hashlib.sha256(), 0
    while True:
        piece = stream.read(65536)
        if not piece:
            break
        count += len(piece)
        if ceiling is not None:
            require(count <= ceiling, 'RESOURCE', 'stream byte ceiling')
        digest.update(piece)
    return {'bytes': count, 'sha256': digest.hexdigest()}


class CaptureReader:
    """Independent closed compact capture grammar; byte-consumed identity."""
    def __init__(self, stream):
        self.stream = stream
        self.buffer = b''
        self.position = 0
        self.digest = hashlib.sha256()
        self.count = 0

    def available(self):
        if self.position == len(self.buffer):
            self.buffer = self.stream.read(65536)
            self.position = 0
            self.count += len(self.buffer)
            require(self.count <= 64 * 1024 * 1024, 'RESOURCE', 'capture byte ceiling')
            self.digest.update(self.buffer)
        return self.position < len(self.buffer)

    def byte(self):
        require(self.available(), 'INPUT', 'truncated coefficient capture')
        value = self.buffer[self.position]
        self.position += 1
        return value

    def expect(self, literal):
        for byte in literal:
            require(self.byte() == byte, 'SCHEMA', 'fixed capture grammar differs')

    def row(self):
        first = self.byte()
        require(first == ord('{'), 'ROW', 'coefficient row object required')
        parts, count = [b'{'], 1
        depth, quoted, escaped = 1, False, False
        while depth:
            require(self.available(), 'INPUT', 'truncated coefficient row')
            start = self.position
            while depth and self.position < len(self.buffer):
                value = self.buffer[self.position]
                self.position += 1
                if quoted:
                    if escaped:
                        escaped = False
                    elif value == 92:
                        escaped = True
                    elif value == 34:
                        quoted = False
                elif value == 34:
                    quoted = True
                elif value == 123:
                    depth += 1
                elif value == 125:
                    depth -= 1
            piece = self.buffer[start:self.position]
            parts.append(piece)
            count += len(piece)
            require(count <= 8 * 1024 * 1024, 'RESOURCE', 'capture row byte ceiling')
        body = b''.join(parts)
        row = parse_json(body)
        compact = json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')
        equal(body, compact, 'CANONICAL', 'capture row compact canonical bytes differ')
        return row, identity(body)


def independent_rows(path, expected_pin):
    """One retained short/long row at a time; caller must exhaust the iterator."""
    pin(expected_pin, 'INPUT')
    path, before = regular_path(path, ceiling=64 * 1024 * 1024)
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
        with os.fdopen(descriptor, 'rb') as stream:
            equal(state(os.fstat(stream.fileno())), before, 'INPUT', 'capture descriptor changed')
            equal(open_identity(stream, 64 * 1024 * 1024), expected_pin, 'INPUT', 'capture identity before decode')
            stream.seek(0)
            reader = CaptureReader(stream)
            reader.expect(b'{"dimensions":{"L":4096,"N":2769,"T":10961},"row_order":[0,1,27,805,1384,2741,2767,2768],"rows":[')
            for index, row_id in enumerate(ROWS):
                if index:
                    reader.expect(b',')
                row, row_pin = reader.row()
                fields(row, ('long', 'row', 'short'), 'ROW')
                equal(row['row'], row_id, 'ROW', 'coefficient row order differs')
                short = tuple(interval(x, serialized=True) for x in sequence(row['short'], N, 'ROW'))
                long = tuple(interval(x, serialized=True) for x in sequence(row['long'], T, 'ROW'))
                del row
                yield {'row': row_id, 'short': short, 'long': long, 'source_row_pin': row_pin}
                del short, long
            reader.expect(b'],"schema":"ri73-reconstructed-intervals-v1"}')
            require(not reader.available(), 'SCHEMA', 'capture trailing bytes')
            equal({'bytes': reader.count, 'sha256': reader.digest.hexdigest()}, expected_pin,
                  'INPUT', 'actually decoded capture byte identity differs')
            equal(state(os.fstat(stream.fileno())), before, 'INPUT', 'capture changed during decode')
            equal(open_identity(stream, 64 * 1024 * 1024), expected_pin, 'INPUT', 'capture identity after decode')
            equal(state(os.fstat(stream.fileno())), before, 'INPUT', 'capture changed during rehash')
        equal(state(path.lstat()), before, 'INPUT', 'capture pathname changed')
    except OSError as error:
        raise ValidationError('INPUT', 'capture I/O failed') from error


def verify_metadata(metadata):
    require(type(metadata) is dict and type(metadata.get('detectors')) is list
            and len(metadata['detectors']) == 2, 'METADATA', 'complete RI37 metadata pair')
    for detector, record in zip(('H1', 'L1'), metadata['detectors']):
        require(type(record) is dict and type(record.get('metadata')) is dict
                and record['metadata'].get('Detector') == detector,
                'METADATA', 'fixed detector metadata order')
        for key, mask in (('data_quality', 127), ('hardware_injection_flags', 31 if detector == 'H1' else 23)):
            require(type(record.get(key)) is dict and type(record[key].get('raw_bitfields')) is list,
                    'FLAGS', 'complete flag field required')
            equal(record[key]['raw_bitfields'], [mask] * 32, 'FLAGS', 'fixed flags including clear L1 CW bit')
    equal(identity(canonical(metadata)), RI37_PIN, 'METADATA', 'complete pinned RI37 metadata differs')


def verify_projection(projection, phase):
    require(type(phase) is str and phase in PHASES, 'PHASE', 'fixed phase required')
    fields(projection, ('context', 'metadata', 'hdf5', 'capture', 'ri83', 'ri100', 'segments', 'traces'), 'INPUT')
    actual = phase == 'fixed_observed_application'
    equal(projection['context'], 'accepted_fixed_observed_inputs' if actual else 'fabricated_inputs_not_observed',
          'PHASE', 'projection phase differs')
    verify_metadata(projection['metadata'])
    fields(projection['hdf5'], ('H1', 'L1'), 'INPUT')
    expected = dict(HDF_PINS, capture=SNAPSHOT_PIN, ri83=RI83_PIN, ri100=RI100_PIN)
    for key, value in list(projection['hdf5'].items()) + [(k, projection[k]) for k in ('capture', 'ri83', 'ri100')]:
        pin(value, 'INPUT')
        if actual:
            equal(value, expected[key], 'INPUT', 'fixed historical input pin differs')
        else:
            require(not same(value, expected[key]), 'PHASE', 'fabricated identity must not impersonate actual input')
    require(type(projection['segments']) is list and len(projection['segments']) == 26,
            'INPUT', 'complete segment projection')
    index = 0
    for scenario in ORDER:
        detector, side = scenario.split(':')
        for start in STARTS[side]:
            row = projection['segments'][index]
            fields(row, ('id', 'detector', 'side', 'start', 'end', 'raw_sha256'), 'INPUT')
            for key, value in {'id': scenario + ':' + str(start), 'detector': detector, 'side': side,
                               'start': start, 'end': start + M}.items():
                equal(row[key], value, 'INPUT', 'fixed segment metadata differs')
            require(type(row['raw_sha256']) is str and re.fullmatch(r'[0-9a-f]{64}', row['raw_sha256']) is not None,
                    'INPUT', 'complete raw segment hash')
            index += 1
    require(type(projection['traces']) is list and len(projection['traces']) == 4,
            'TRACE', 'four retained trace records required')
    for name, record in zip(ORDER, projection['traces']):
        fields(record, ('id', 'interval', 'source_identity', 'model', 'units'), 'TRACE')
        equal(record['id'], name, 'TRACE', 'trace scenario order differs')
        interval(record['interval'], serialized=True)
        pin(record['source_identity'], 'TRACE')
        equal(record['model'], 'postulated_finite_circulant_from_empirical_psd' if actual
              else 'fabricated_trace_not_observed', 'TRACE', 'trace model label differs')
        equal(record['units'], TRACE_UNITS, 'TRACE', 'trace units differ')


def verify_provenance(provenance, projection, phase, expected=None):
    fields(provenance, ('sources', 'input', 'acceptance', 'runtime'), 'PROVENANCE')
    fields(provenance['sources'], ('design', 'consumer', 'validator', 'qualifier', 'implementation', 'api'), 'PROVENANCE')
    for value in provenance['sources'].values():
        pin(value)
    equal(provenance['sources']['design'], DESIGN_PIN, 'SOURCE', 'accepted design differs')
    pin(provenance['input'])
    equal(provenance['input'], identity(canonical(projection)), 'INPUT', 'whole projection identity differs')
    fields(provenance['acceptance'], ('design', 'ri100', 'qualification', 'custody'), 'PROVENANCE')
    equal(provenance['acceptance']['design'], DESIGN_DECISION, 'PROVENANCE', 'design acceptance differs')
    equal(provenance['acceptance']['ri100'], RI100_DECISION, 'PROVENANCE', 'RI100 acceptance differs')
    for key in ('qualification', 'custody'):
        value = provenance['acceptance'][key]
        if phase == 'fabricated_qualification':
            require(value is None, 'PHASE', 'fabrication cannot claim future qualification or input custody')
        else:
            pin(value)
    fields(provenance['runtime'], ('fingerprint', 'inventory', 'interpreter'), 'PROVENANCE')
    for value in provenance['runtime'].values():
        pin(value)
    if expected is not None:
        equal(provenance, expected, 'PROVENANCE', 'caller-bound complete provenance differs')


def slice_record(start, end, metadata):
    require(type(start) is int and type(end) is int and 0 <= start < end <= LENGTH,
            'DOMAIN', 'fixed integer slice required')
    rows = list(range(start // FS, (end + FS - 1) // FS))
    return {'start': start, 'end': end,
            'gps_start_offset': encoded(Fraction(start, FS)), 'gps_end_offset': encoded(Fraction(end, FS)),
            'flag_rows': rows, 'dq_masks': [metadata['data_quality']['raw_bitfields'][j] for j in rows],
            'injection_masks': [metadata['hardware_injection_flags']['raw_bitfields'][j] for j in rows]}


def actual_projection(ri83_body, ri100_body, metadata):
    """Project exactly pinned accepted bodies, without rerunning their methods."""
    equal(identity(ri83_body), RI83_PIN, 'INPUT', 'RI83 body identity before decode')
    equal(identity(ri100_body), RI100_PIN, 'INPUT', 'RI100 body identity before decode')
    verify_metadata(metadata)
    spectra, traces = parse_json(ri83_body), parse_json(ri100_body)
    require(type(spectra) is dict and spectra.get('schema') == 'ri78-off-event-spectra-v1',
            'INPUT', 'accepted spectra schema')
    require(type(traces) is dict and traces.get('schema') == 'ri98-mode-weighted-trace-v1'
            and traces.get('phase') == 'fixed_saved_application' and traces.get('status') == 'all_gates_passed',
            'INPUT', 'accepted trace status')
    require(type(spectra.get('detectors')) is list and len(spectra['detectors']) == 2,
            'INPUT', 'accepted detector spectra inventory')
    segments = []
    for detector, record in zip(('H1', 'L1'), spectra['detectors']):
        require(type(record) is dict and record.get('detector') == detector
                and type(record.get('sides')) is list and len(record['sides']) == 2,
                'INPUT', 'accepted detector side inventory')
        for side, side_record in zip(('left', 'right'), record['sides']):
            require(type(side_record) is dict and side_record.get('side') == side
                    and type(side_record.get('segments')) is list
                    and len(side_record['segments']) == len(STARTS[side]), 'INPUT', 'accepted segment inventory')
            for start, row in zip(STARTS[side], side_record['segments']):
                require(type(row) is dict and row.get('start') == start and row.get('end') == start + M,
                        'INPUT', 'accepted segment boundaries')
                segments.append({'id': detector + ':' + side + ':' + str(start), 'detector': detector,
                                 'side': side, 'start': start, 'end': start + M, 'raw_sha256': row['raw_sha256']})
    require(type(traces.get('scenarios')) is list and len(traces['scenarios']) == 4,
            'TRACE', 'accepted four scenarios')
    retained = []
    for name, row in zip(ORDER, traces['scenarios']):
        require(type(row) is dict and row.get('id') == name and 'final' in row and 'source_identity' in row,
                'TRACE', 'accepted trace scenario fields')
        retained.append({'id': name, 'interval': row['final'], 'source_identity': row['source_identity'],
                         'model': 'postulated_finite_circulant_from_empirical_psd', 'units': TRACE_UNITS})
    projection = {'context': 'accepted_fixed_observed_inputs', 'metadata': metadata, 'hdf5': HDF_PINS,
                  'capture': SNAPSHOT_PIN, 'ri83': RI83_PIN, 'ri100': RI100_PIN,
                  'segments': segments, 'traces': retained}
    verify_projection(projection, 'fixed_observed_application')
    return projection


def scaled_magnitude(value):
    denominator, numerators = value
    return rational(Fraction(max(abs(x) for x in numerators), denominator))


def prepare_vectors(raw_bodies, projection):
    """Independently form exact finite means and vectors from raw byte arrays."""
    fields(raw_bodies, ('H1', 'L1'), 'INPUT')
    prepared, expected_artifacts, scenario_records = {}, {}, []
    segment_position = 0
    for detector, meta in zip(('H1', 'L1'), projection['metadata']['detectors']):
        body = raw_bodies[detector]
        values = exact_raw(body)
        expected_artifacts[detector + '-raw.f64le'] = body
        for side in ('left', 'right'):
            name = detector + ':' + side
            windows = tuple(values[start:start + T] for start in STARTS[side])
            mean = tuple(divide(total([window[j] for window in windows]), len(windows)) for j in range(T))
            centered = tuple(tuple(minus(window[j], mean[j]) for j in range(T)) for window in windows)
            mean_name = detector + '-' + side + '-mean.json'
            expected_artifacts[mean_name] = canonical({'schema': 'ri106-coordinatewise-mean-v1',
                                                       'id': name, 'values': encoded(mean)})
            # Keep only exact denominator/integer vectors for arithmetic.  The
            # original raw bodies and complete mean artifacts remain retained.
            prepared[name] = {'raw': tuple(lifted(w) for w in windows),
                              'short': tuple(lifted(w[L:L + N]) for w in windows),
                              'mean': lifted(mean), 'centered': tuple(lifted(w) for w in centered)}
            records = []
            for start in STARTS[side]:
                expected_segment = projection['segments'][segment_position]
                digest = hashlib.sha256(body[start * 8:(start + M) * 8]).hexdigest()
                equal(digest, expected_segment['raw_sha256'], 'INPUT', 'raw M-segment bytes differ')
                records.append({'start': start,
                                'slices': {'M': slice_record(start, start + M, meta),
                                           'T': slice_record(start, start + T, meta),
                                           'short': slice_record(start + L, start + L + N, meta)},
                                'raw_sha256': digest, 'outputs': []})
                segment_position += 1
            scenario_records.append({'id': name, 'detector': detector, 'side': side, 'count': len(windows),
                                     'windows': records, 'mean': {'artifact': mean_name, 'outputs': []},
                                     'centered': [{'start': s, 'outputs': []} for s in STARTS[side]],
                                     'energy': {'components': []},
                                     'trace': projection['traces'][len(scenario_records)]})
            del windows, centered, mean
        del values
    return prepared, expected_artifacts, scenario_records


def coefficient_rows(source):
    fields(source, ('row', 'short', 'long', 'source_row_pin'), 'ROW')
    pin(source['source_row_pin'], 'ROW')
    short = tuple(interval(v) for v in sequence(source['short'], N, 'ROW'))
    long = tuple(interval(v) for v in sequence(source['long'], T, 'ROW'))
    difference = []
    for j, (lo, hi) in enumerate(long):
        if L <= j < L + N:
            sl, sh = short[j - L]
            difference.append((minus(lo, sh), minus(hi, sl)))
        else:
            difference.append((lo, hi))
    def scale(pairs):
        low, high = zip(*pairs)
        return lifted(low), lifted(high)
    s, q, a = scale(short), scale(long), scale(difference)
    low_sum = rational(Fraction(integer(sum(a[0][1])), a[0][0]))
    high_sum = rational(Fraction(integer(sum(a[1][1])), a[1][0]))
    require(low_sum <= 0 <= high_sum, 'ROW', 'coefficient A row sum must enclose zero')
    record = encoded({'row': source['row'], 'short_count': N, 'long_count': T,
                      'source_row_pin': source['source_row_pin'],
                      'a_midpoint_sum': divide(plus(low_sum, high_sum), 2),
                      'a_radius_sum': divide(minus(high_sum, low_sum), 2),
                      'a_row_sum_interval': (low_sum, high_sum), 'contains_zero': True})
    return s, q, a, record


def derive_row(source, prepared, scenarios):
    s, q, a, operator_record = coefficient_rows(source)
    row_id = source['row']
    for scenario in scenarios:
        vectors = prepared[scenario['id']]
        raw_dots, centered_dots = [], []
        for window, raw, short in zip(scenario['windows'], vectors['raw'], vectors['short']):
            short_interval = scaled_endpoint_dot(s[0], s[1], short)
            long_interval = scaled_endpoint_dot(q[0], q[1], raw)
            delta_interval = scaled_endpoint_dot(a[0], a[1], raw)
            delta = dot_record(delta_interval, scaled_magnitude(raw))
            route = (minus(long_interval[0], short_interval[1]), minus(long_interval[1], short_interval[0]))
            common = intersect(delta_interval, route, 'DOT')
            raw_dots.append(delta)
            window['outputs'].append({'row': row_id, 'short': encoded(short_interval),
                                      'long': encoded(long_interval), 'delta': dict(delta, row=row_id),
                                      'route_intersection': encoded(common)})
        mean_interval = scaled_endpoint_dot(a[0], a[1], vectors['mean'])
        mean_dot = dot_record(mean_interval, scaled_magnitude(vectors['mean']))
        scenario['mean']['outputs'].append(dict(mean_dot, row=row_id))
        n = len(raw_dots)
        raw_mean_center = divide(total([decode(v['center']) for v in raw_dots]), n)
        require(raw_mean_center == decode(mean_dot['center']), 'CENTER', 'exact center mean linearity')
        average_interval = tuple(divide(v, n) for v in interval_sum([interval(d['interval'], serialized=True) for d in raw_dots]))
        require(overlap(mean_interval, average_interval), 'CENTER', 'direct mean/output mean intersection')
        for record, vector, raw_dot in zip(scenario['centered'], vectors['centered'], raw_dots):
            centered_interval = scaled_endpoint_dot(a[0], a[1], vector)
            centered = dot_record(centered_interval, scaled_magnitude(vector))
            require(decode(centered['center']) == minus(decode(raw_dot['center']), decode(mean_dot['center'])),
                    'CENTER', 'exact centered-input linearity')
            centered_dots.append(centered)
            record['outputs'].append(dict(centered, row=row_id))
        centered_sum = interval_sum([interval(v['interval'], serialized=True) for v in centered_dots])
        require(centered_sum[0] <= 0 <= centered_sum[1], 'CENTER', 'centered interval sum contains zero')
        energy = component_energy(raw_dots, mean_dot, centered_dots)
        scenario['energy']['components'].append(dict(energy, row=row_id))
    return operator_record


def finish_energies(scenarios):
    for scenario in scenarios:
        energy = scenario['energy']
        sums = {key: interval_sum([interval(component[key], serialized=True) for component in energy['components']])
                for key in ('U', 'M', 'V')}
        common = intersect(sums['U'], interval_sum((sums['V'], sums['M'])))
        energy.update(encoded(dict(sums, identity_intersection=common)))


def expected_artifact_inventory(bodies):
    names = ('H1-left-mean.json', 'H1-raw.f64le', 'H1-right-mean.json',
             'L1-left-mean.json', 'L1-raw.f64le', 'L1-right-mean.json')
    fields(bodies, names, 'ARTIFACT')
    return [dict(name=name, **identity(bodies[name]), dtype='<f8' if name.endswith('.f64le') else 'reduced_hex_rational',
                 shape=[LENGTH] if name.endswith('.f64le') else [T]) for name in names]


def verify_artifacts(directory, inventory, expected_bodies):
    """Exact membership, regular nlink-one nodes and every complete byte body."""
    expected_inventory = expected_artifact_inventory(expected_bodies)
    equal(inventory, expected_inventory, 'ARTIFACT', 'six complete artifact identities differ')
    require(isinstance(directory, (str, Path)), 'ARTIFACT', 'artifact directory path required')
    directory = Path(directory)
    try:
        require(directory.is_absolute() and directory.resolve(strict=True) == directory
                and stat.S_ISDIR(directory.lstat().st_mode) and not directory.is_symlink(),
                'ARTIFACT', 'canonical nonsymlink artifact directory')
        equal(sorted(p.name for p in directory.iterdir()), sorted(expected_bodies),
              'ARTIFACT', 'complete artifact directory membership differs')
        for name, expected in expected_bodies.items():
            path = directory / name
            before = path.lstat()
            require(stat.S_ISREG(before.st_mode) and not path.is_symlink() and before.st_nlink == 1,
                    'ARTIFACT', 'regular nonsymlink exclusive artifact required')
            require(before.st_size == len(expected), 'ARTIFACT', 'artifact byte count differs')
            descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
            with os.fdopen(descriptor, 'rb') as stream:
                equal(state(os.fstat(stream.fileno())), state(before), 'ARTIFACT', 'artifact changed at open')
                body = stream.read(len(expected) + 1)
                equal(body, expected, 'ARTIFACT', 'complete artifact byte values differ')
                equal(state(os.fstat(stream.fileno())), state(before), 'ARTIFACT', 'artifact changed during read')
            equal(state(path.lstat()), state(before), 'ARTIFACT', 'artifact path changed')
        equal(sorted(p.name for p in directory.iterdir()), sorted(expected_bodies),
              'ARTIFACT', 'artifact membership changed during verification')
    except OSError as error:
        raise ValidationError('ARTIFACT', 'artifact I/O failed') from error
    return expected_inventory


def verify_dot_record(record, expected):
    """Actual full-path guard, also available for bounded late mutations."""
    fields(record, ('interval', 'center', 'radius', 'width', 'input_max', 'width_limit', 'width_pass'), 'DOT')
    for key in ('width_limit', 'width_pass'):
        equal(record[key], expected[key], 'WIDTH', 'fixed width threshold or result differs')
    for key in ('interval', 'center', 'radius', 'width', 'input_max'):
        equal(record[key], expected[key], 'DOT', 'independent signed endpoint dot differs')


def verify_result_fields(report, projection, provenance, expected_phase):
    require(type(expected_phase) is str and expected_phase in PHASES, 'PHASE', 'supported exact phase required')
    fields(report, ('schema', 'phase', 'status', 'method', 'provenance', 'inputs', 'operator',
                    'scenarios', 'checks', 'limitations'))
    equal(report['schema'], 'ri104-observed-context-benchmark-v1', 'SCHEMA', 'result schema differs')
    equal(report['phase'], expected_phase, 'PHASE', 'result phase differs')
    equal(report['status'], 'all_gates_passed', 'RESULT', 'result status differs')
    equal(report['method'], METHOD, 'DOMAIN', 'complete fixed method differs')
    equal(report['limitations'], LIMITATIONS, 'SCHEMA', 'limitations differ')
    verify_projection(projection, expected_phase)
    verify_provenance(provenance, projection, expected_phase)
    verify_provenance(report['provenance'], projection, expected_phase, provenance)
    fields(report['inputs'], ('projection', 'artifacts'), 'INPUT')
    equal(report['inputs']['projection'], projection, 'INPUT', 'complete independent projection differs')
    expected_checks = {'inventory': list(GATES), 'counts': {'total': 12, 'passed': 12, 'failed': 0},
                       'results': [{'id': name, 'passed': True} for name in GATES]}
    equal(report['checks'], expected_checks, 'RESULT', 'complete gate inventory differs')
    require(type(report['scenarios']) is list and len(report['scenarios']) == 4,
            'SCHEMA', 'four complete result scenarios required')


def verify_operator(record, expected):
    fields(record, ('capture', 'schema', 'dimensions', 'row_order', 'rows', 'constant_annihilation'), 'ROW')
    equal(record, expected, 'ROW', 'complete independent operator record differs')


def verify_scenario(record, expected_scenario):
    """Full-path comparator. Expected arithmetic is separately reconstructed."""
    fields(record, ('id', 'detector', 'side', 'count', 'windows', 'mean', 'centered', 'energy', 'trace'))
    for key in ('id', 'detector', 'side', 'count'):
        equal(record[key], expected_scenario[key], 'DOMAIN', 'fixed scenario inventory differs')
    equal(record['trace'], expected_scenario['trace'], 'TRACE', 'unchanged proxy trace differs')
    require(type(record['windows']) is list and len(record['windows']) == len(expected_scenario['windows']),
            'DOMAIN', 'complete window inventory required')
    for given, expected in zip(record['windows'], expected_scenario['windows']):
        fields(given, ('start', 'slices', 'raw_sha256', 'outputs'))
        equal(given['start'], expected['start'], 'DOMAIN', 'window start differs')
        equal(given['slices'], expected['slices'], 'DOMAIN', 'complete slices/clock/flags differ')
        equal(given['raw_sha256'], expected['raw_sha256'], 'INPUT', 'raw segment identity differs')
        require(type(given['outputs']) is list and len(given['outputs']) == 8, 'ROW', 'eight raw outputs required')
        for actual_output, wanted_output in zip(given['outputs'], expected['outputs']):
            fields(actual_output, ('row', 'short', 'long', 'delta', 'route_intersection'), 'DOT')
            equal(actual_output['row'], wanted_output['row'], 'ROW', 'output row differs')
            for key in ('short', 'long', 'route_intersection'):
                equal(actual_output[key], wanted_output[key], 'DOT', 'independent P/Q/route interval differs')
            _verify_numbered_dot(actual_output['delta'], wanted_output['delta'])
    fields(record['mean'], ('artifact', 'outputs'), 'CENTER')
    equal(record['mean']['artifact'], expected_scenario['mean']['artifact'], 'CENTER', 'mean artifact differs')
    require(type(record['mean']['outputs']) is list and len(record['mean']['outputs']) == 8,
            'CENTER', 'eight mean outputs required')
    for given, expected in zip(record['mean']['outputs'], expected_scenario['mean']['outputs']):
        _verify_numbered_dot(given, expected)
    require(type(record['centered']) is list and len(record['centered']) == len(expected_scenario['centered']),
            'CENTER', 'complete centered-output inventory required')
    for given, expected in zip(record['centered'], expected_scenario['centered']):
        fields(given, ('start', 'outputs'), 'CENTER')
        equal(given['start'], expected['start'], 'CENTER', 'centered window start differs')
        require(type(given['outputs']) is list and len(given['outputs']) == 8, 'CENTER', 'eight centered outputs required')
        for actual_output, wanted_output in zip(given['outputs'], expected['outputs']):
            _verify_numbered_dot(actual_output, wanted_output)
    equal(record['energy'], expected_scenario['energy'], 'ENERGY', 'complete independent component/total energies differ')


def _verify_numbered_dot(record, expected):
    require(type(record) is dict and 'row' in record, 'ROW', 'numbered dot row required')
    equal(record['row'], expected['row'], 'ROW', 'numbered dot row differs')
    verify_dot_record({key: value for key, value in record.items() if key != 'row'},
                      {key: value for key, value in expected.items() if key != 'row'})


def capture_admission(path, expected_pin):
    pin(expected_pin, 'INPUT')
    path, before = regular_path(path, ceiling=64 * 1024 * 1024)
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
        with os.fdopen(descriptor, 'rb') as stream:
            equal(state(os.fstat(stream.fileno())), before, 'INPUT', 'capture changed at admission')
            equal(open_identity(stream, 64 * 1024 * 1024), expected_pin, 'INPUT', 'complete capture identity differs')
            equal(state(os.fstat(stream.fileno())), before, 'INPUT', 'capture changed during admission')
        equal(state(path.lstat()), before, 'INPUT', 'capture admission pathname changed')
    except OSError as error:
        raise ValidationError('INPUT', 'capture admission I/O failed') from error
    return path, before


def validate_result(report, raw_bodies, capture_path, projection, provenance, artifact_dir, *, expected_phase):
    """Full independent endpoint route; supplied raw bytes need external custody.

    Fabrication uses its explicitly declared source rows.  The actual wrapper
    below independently re-extracts both complete raw bodies from pinned HDF5.
    No success-token cache or producer iterator is accepted by this function.
    """
    verify_result_fields(report, projection, provenance, expected_phase)
    original_projection = identity(canonical(projection))
    original_provenance = identity(canonical(provenance))
    path, capture_state = capture_admission(capture_path, projection['capture'])
    fields(raw_bodies, ('H1', 'L1'), 'INPUT')
    original_raw = {key: identity(body) for key, body in raw_bodies.items()}
    prepared, expected_bodies, expected_scenarios = prepare_vectors(raw_bodies, projection)
    iterator = iter(independent_rows(path, projection['capture']))
    row_records = []
    for expected_row in ROWS:
        try:
            source = next(iterator)
        except StopIteration as error:
            raise ValidationError('ROW', 'missing independent coefficient row') from error
        require(type(source) is dict and type(source.get('row')) is int and source['row'] == expected_row,
                'ROW', 'complete ordered independent coefficient rows')
        row_records.append(derive_row(source, prepared, expected_scenarios))
        del source
    sentinel = object()
    require(next(iterator, sentinel) is sentinel, 'ROW', 'extra independent coefficient row')
    del prepared
    finish_energies(expected_scenarios)
    expected_operator = {'capture': projection['capture'], 'schema': 'ri73-reconstructed-intervals-v1',
                         'dimensions': {'N': N, 'L': L, 'T': T}, 'row_order': list(ROWS), 'rows': row_records,
                         'constant_annihilation': 'accepted_true_A_annihilation_midpoints_not_projected'
                         if expected_phase == 'fixed_observed_application' else 'fabricated_row_fixture_not_observed'}
    verify_operator(report['operator'], expected_operator)
    for record, expected in zip(report['scenarios'], expected_scenarios):
        verify_scenario(record, expected)
    verify_artifacts(artifact_dir, report['inputs']['artifacts'], expected_bodies)
    equal(identity(canonical(projection)), original_projection, 'INPUT', 'projection changed during validation')
    equal(identity(canonical(provenance)), original_provenance, 'PROVENANCE', 'provenance changed during validation')
    equal({key: identity(body) for key, body in raw_bodies.items()}, original_raw, 'INPUT', 'raw bodies changed during validation')
    _, after = capture_admission(path, projection['capture'])
    equal(after, capture_state, 'INPUT', 'capture source changed during validation')
    return {'status': 'all_fields_independently_match', 'windows': 26, 'raw': 208,
            'short_long': 416, 'mean': 32, 'centered': 208, 'scenarios': 4, 'artifacts': 6}


def load_result(body):
    report = parse_json(body)
    equal(body, canonical(report), 'CANONICAL', 'complete canonical result bytes required')
    return report


def validate_observed(report, hdf_bodies, capture_path, ri83_body, ri100_body,
                      metadata_body, provenance, artifact_dir, inspector):
    """All actual operand identities precede either HDF5/numerical body parse.

    The separately admitted captured inspector and complete runtime/source
    closure remain caller premises. This independently repeats full raw array
    extraction; no rounded RI83 array or producer-supplied raw artifact is used
    as an input oracle. No observer or target module is imported on fabrication.
    """
    fields(hdf_bodies, ('H1', 'L1'), 'INPUT')
    for name in ('H1', 'L1'):
        equal(identity(hdf_bodies[name]), HDF_PINS[name], 'INPUT', 'fixed complete HDF5 bytes differ')
        require(hashlib.md5(hdf_bodies[name], usedforsecurity=False).hexdigest() == MD5S[name],
                'INPUT', 'published MD5 identity differs')
    equal(identity(ri83_body), RI83_PIN, 'INPUT', 'complete RI83 identity before decode')
    equal(identity(ri100_body), RI100_PIN, 'INPUT', 'complete RI100 identity before decode')
    equal(identity(metadata_body), RI37_PIN, 'INPUT', 'complete RI37 identity before decode')
    path, before = capture_admission(capture_path, SNAPSHOT_PIN)
    # Only now may any HDF5/numerical-body parser be invoked.
    metadata = parse_json(metadata_body)
    verify_metadata(metadata)
    require(hasattr(inspector, 'FILES') and hasattr(inspector, '_inspect'), 'SOURCE', 'captured inspector API required')
    file_records = {entry['detector']: entry for entry in inspector.FILES}
    fields(file_records, ('H1', 'L1'), 'SOURCE')
    try:
        inspected = dict(metadata)
        inspected['detectors'] = [inspector._inspect(hdf_bodies[name], file_records[name]) for name in ('H1', 'L1')]
        equal(inspected, metadata, 'METADATA', 'complete independent inspector replay differs')
        import h5py
        raw_bodies = {}
        for name in ('H1', 'L1'):
            with h5py.File(io.BytesIO(hdf_bodies[name]), 'r') as handle:
                dataset = handle['/strain/Strain']
                require(dataset.shape == (LENGTH,) and dataset.dtype.name == 'float64', 'INPUT', 'fixed full strain dataset')
                values = dataset[()]
            body = values.astype('<f8', copy=False).tobytes(order='C')
            require(len(body) == LENGTH * 8, 'INPUT', 'full raw array extraction size')
            raw_bodies[name] = body
            del values, body
    except ValidationError:
        raise
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as error:
        raise ValidationError('INPUT', 'fixed observed extraction failed') from error
    projection = actual_projection(ri83_body, ri100_body, metadata)
    verdict = validate_result(report, raw_bodies, path, projection, provenance, artifact_dir,
                              expected_phase='fixed_observed_application')
    _, after = capture_admission(path, SNAPSHOT_PIN)
    equal(after, before, 'INPUT', 'actual capture changed across observed validation')
    # Bytes are immutable, but container substitution must still refuse.
    for name in ('H1', 'L1'):
        equal(identity(hdf_bodies[name]), HDF_PINS[name], 'INPUT', 'HDF5 body changed during validation')
    equal(identity(ri83_body), RI83_PIN, 'INPUT', 'RI83 body changed during validation')
    equal(identity(ri100_body), RI100_PIN, 'INPUT', 'RI100 body changed during validation')
    equal(identity(metadata_body), RI37_PIN, 'INPUT', 'metadata body changed during validation')
    return verdict
