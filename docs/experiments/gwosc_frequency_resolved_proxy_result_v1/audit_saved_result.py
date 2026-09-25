"""Independent RI96 saved arithmetic and custody audit. Source-only until admission.

No target imports or transform. Exact interval-to-row and product-envelope
arithmetic is reconstructed independently. The already qualified recursive
transform/roots/powers validation is an explicit, checked execution premise.
The sole CLI accepts one root-bound descriptor with its byte count and SHA256.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math
import os
import re
import stat
import struct
import sys

F = Fraction
ROOT = Path('/Volumes/AI_DATA/development/det-review-evidence/ri96-execution/application-preparation-wvp1hizx')
PROSPECTIVE_PIN = {'bytes': 43585, 'sha256': 'd12228df7dcd73aefb1d3c72da55ca2ea6b5aa2f68754bc011281fc005a0fc46'}
ROWS = [0, 1, 27, 805, 1384, 2741, 2767, 2768]
SCENARIOS = ['H1:left', 'H1:right', 'L1:left', 'L1:right']
Q, M, N, L, T, D, BITS = 1 << 256, 16384, 2769, 4096, 10961, 8, 262144
DEN = 2 * Q
VALIDATION = {'status': 'all_fields_independently_match', 'rows': 8, 'modes': 65544, 'bands': 14, 'scenarios': 4}
LIMITS = {'wall_seconds': 180, 'rss_kib': 524288, 'target_poll_seconds': 0.025,
          'maximum_sample_gap_seconds': 0.1, 'ps_timeout_seconds': 0.05}
RESULT_KEYS = ('schema', 'phase', 'status', 'model', 'method', 'provenance', 'prior',
               'rows', 'row_proofs', 'twiddles', 'bands', 'midpoint_parseval', 'scenarios', 'gates', 'limitations')


class AuditFailure(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditFailure(message)


def closed(value, keys, where):
    require(type(value) is dict and set(value) == set(keys), where + ': closed object')
    return value


def vector(value, length, where):
    require(type(value) is list and len(value) == length, where + ': fixed list length')
    return value


def same(actual, expected, where):
    # Canonical bytes distinguish bool/int and int/float, which Python == does not.
    require(json_pin(actual) == json_pin(expected), where + ': exact encoded equality')


def checked_int(value):
    require(type(value) is int and abs(value).bit_length() <= BITS, 'bounded exact integer')
    return value


def fraction(value):
    require(type(value) is F, 'exact Fraction required')
    checked_int(value.numerator); checked_int(value.denominator)
    return value


def hx(value):
    require(type(value) is str and len(value) <= (BITS + 3) // 4 + 1 and
            re.fullmatch(r'(?:0|-?[1-9a-f][0-9a-f]*)', value) is not None, 'canonical bounded hexadecimal')
    return checked_int(int(value, 16))


def rational(value):
    a, b = map(hx, vector(value, 2, 'rational'))
    require(b > 0 and math.gcd(a, b) == 1, 'reduced positive-denominator rational')
    return fraction(F(a, b))


def encoded(value):
    if type(value) is F:
        fraction(value)
        return [format(value.numerator, 'x'), format(value.denominator, 'x')]
    if type(value) in (tuple, list):
        return [encoded(v) for v in value]
    if type(value) is dict:
        return {k: encoded(v) for k, v in value.items()}
    return value


def chunks(value):
    for text in json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False).iterencode(value):
        yield text.encode('ascii')
    yield b'\n'


def json_pin(value):
    digest, count = hashlib.sha256(), 0
    for body in chunks(value):
        digest.update(body); count += len(body)
    return {'bytes': count, 'sha256': digest.hexdigest()}


def byte_pin(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def decode(body, *, scientific=False):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def invalid(text):
        raise AuditFailure('nonfinite or forbidden decimal JSON token: ' + text)
    options = {'object_pairs_hook': pairs, 'parse_constant': invalid}
    if scientific:
        options['parse_float'] = invalid
    try:
        return json.loads(body.decode('ascii'), **options)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise AuditFailure('ASCII JSON decode failed') from exc


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def pin_shape(value):
    closed(value, ('bytes', 'sha256'), 'pin')
    require(type(value['bytes']) is int and 0 <= value['bytes'] <= 1 << 40 and
            type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None,
            'byte-count/SHA256 pin')
    return value


def metadata(st):
    return {'device': st.st_dev, 'inode': st.st_ino, 'size': st.st_size,
            'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns}


class Custody:
    def __init__(self):
        self.bindings = {}

    def file(self, path, expected=None):
        path = Path(path)
        require(path.is_absolute() and path == path.resolve(), 'absolute unsubstituted path: ' + str(path))
        before = path.lstat()
        require(stat.S_ISREG(before.st_mode), 'regular nonsymlink input: ' + str(path))
        digest, count = hashlib.sha256(), 0
        with path.open('rb') as stream:
            require(metadata(os.fstat(stream.fileno())) == metadata(before), 'open identity changed')
            while body := stream.read(1024 * 1024):
                digest.update(body); count += len(body)
            require(metadata(os.fstat(stream.fileno())) == metadata(before), 'opened input changed')
        require(metadata(path.lstat()) == metadata(before) and count == before.st_size, 'input changed during hash')
        actual = {'bytes': count, 'sha256': digest.hexdigest()}
        if expected is not None:
            require(actual == pin_shape(expected), 'input byte identity: ' + str(path))
        current = {'pin': actual, 'metadata': metadata(before)}
        if str(path) in self.bindings:
            require(self.bindings[str(path)] == current, 'input binding changed: ' + str(path))
        self.bindings[str(path)] = current
        return actual

    def record(self, row, *, scientific=False, canonical=True):
        closed(row, ('path', 'bytes', 'sha256'), 'bound input')
        expected = {k: row[k] for k in ('bytes', 'sha256')}
        self.file(row['path'], expected)
        body = Path(row['path']).read_bytes()
        require(byte_pin(body) == expected, 'read after hash identity')
        value = decode(body, scientific=scientific)
        if canonical:
            require(json_pin(value) == expected, 'canonical JSON byte identity')
        return value

    def final(self):
        for path, binding in list(self.bindings.items()):
            self.file(path, binding['pin'])
        return {'files': len(self.bindings), 'ordered_bindings_identity': json_pin(self.bindings),
                'all_bytes_and_dev_inode_size_mtime_ctime_unchanged': True}


def pathrow(path, pin):
    return {'path': str(path), **pin}


def identical_files(left, right):
    with Path(left).open('rb') as a, Path(right).open('rb') as b:
        while True:
            x, y = a.read(1024 * 1024), b.read(1024 * 1024)
            require(x == y, 'complete normal/optimized result bytes differ')
            if not x:
                return


def matrix(value):
    result = [[rational(x) for x in vector(row, D, 'matrix row')] for row in vector(value, D, 'matrix')]
    require(all(result[i][j] == result[j][i] for i in range(D) for j in range(D)), 'symmetric exact matrix')
    return result


def zero_matrix():
    return [[F(0) for _ in range(D)] for _ in range(D)]


def gram_positive(g):
    # Exact LDL^T recurrence using previously completed columns; no eigen solver.
    lower = [[F(int(i == j)) for j in range(D)] for i in range(D)]
    diagonal = []
    for k in range(D):
        pivot = fraction(g[k][k] - sum((lower[k][j] ** 2 * diagonal[j] for j in range(k)), F(0)))
        require(pivot > 0, 'positive held Gram LDL pivot')
        diagonal.append(pivot)
        for i in range(k + 1, D):
            lower[i][k] = fraction((g[i][k] - sum((lower[i][j] * lower[k][j] * diagonal[j] for j in range(k)), F(0))) / pivot)
    return json_pin(encoded(diagonal))


def snapshot_rows(path, expected, custody):
    """Independent delimiter-framed compact row reader, never a full capture tree.

    The delimiters cannot occur in an admitted row's canonical hex-only values.
    An early delimiter in malformed text fails JSON/closed/hex checks. Each raw
    row is parsed exactly once, independently of the producer brace scanner.
    """
    require(expected['bytes'] <= 64 * 1024 * 1024, 'snapshot cap')
    custody.file(path, expected)
    header = b'{"dimensions":{"L":4096,"N":2769,"T":10961},"row_order":[0,1,27,805,1384,2741,2767,2768],"rows":['
    footer = b'],"schema":"ri73-reconstructed-intervals-v1"}'
    digest, total, buffer = hashlib.sha256(), 0, b''
    with Path(path).open('rb') as stream:
        require(metadata(os.fstat(stream.fileno())) == custody.bindings[str(path)]['metadata'], 'snapshot descriptor binding')
        def refill():
            nonlocal buffer, total
            body = stream.read(256 * 1024)
            digest.update(body); total += len(body); buffer += body
            require(total <= 64 * 1024 * 1024, 'stream snapshot cap')
            return bool(body)
        while len(buffer) < len(header):
            require(refill(), 'truncated snapshot header')
        require(buffer[:len(header)] == header, 'snapshot fixed header')
        buffer = buffer[len(header):]
        for index, row_id in enumerate(ROWS):
            delimiter = b'}, {"long":'.replace(b' ', b'') if index < 7 else b'}],"schema":'
            while delimiter not in buffer:
                require(len(buffer) <= 8 * 1024 * 1024 and refill(), 'row cap or truncated row')
            stop = buffer.index(delimiter) + 1
            require(stop <= 8 * 1024 * 1024, 'row byte cap')
            body, buffer = buffer[:stop], buffer[stop:]
            value = decode(body, scientific=True)
            require(compact(value) == body, 'canonical compact snapshot row')
            closed(value, ('row', 'long', 'short'), 'snapshot row')
            require(type(value['row']) is int and value['row'] == row_id, 'fixed snapshot row order')
            long = vector(value['long'], T, 'long intervals')
            short = vector(value['short'], N, 'short intervals')
            # Decode the short intervals once; no source implementation imported.
            shorts = []
            for item in short:
                low, high = map(rational, vector(item, 2, 'short interval'))
                require(low <= high, 'ordered short coefficient')
                shorts.append((low, high))
            mids, radii = [], []
            for j, item in enumerate(long):
                low, high = map(rational, vector(item, 2, 'long interval'))
                require(low <= high, 'ordered long coefficient')
                if L <= j < L + N:
                    sl, sh = shorts[j - L]
                    low, high = fraction(low - sh), fraction(high - sl)
                mids.append(fraction((low + high) / 2))
                radii.append(fraction((high - low) / 2))
            del value, body, long, short, shorts
            yield row_id, mids, radii
            if index < 7:
                require(buffer.startswith(b','), 'row comma')
                buffer = buffer[1:]
        while refill():
            require(len(buffer) <= len(footer), 'snapshot trailing data')
        require(buffer == footer and {'bytes': total, 'sha256': digest.hexdigest()} == expected, 'snapshot exact footer/hash')
        require(metadata(os.fstat(stream.fileno())) == custody.bindings[str(path)]['metadata'], 'snapshot parsed descriptor changed')
    custody.file(path, expected)


def rows_audit(report, snapshot, custody):
    records = vector(report['row_proofs'], D, 'row proofs')
    mode_rows, alphas, row_summary = [], [], []
    for index, (row_id, mids, radii) in enumerate(snapshot_rows(snapshot['path'], {k: snapshot[k] for k in ('bytes', 'sha256')}, custody)):
        record = closed(records[index], ('row', 'alpha', 'initial_q256', 'input_identity', 'midpoint_modes', 'mode_identity'), 'row proof')
        require(type(record['row']) is int and record['row'] == row_id, 'row proof order')
        alpha = fraction(sum(radii, F(0)) / 128)
        require(alpha >= 0 and rational(record['alpha']) == alpha, 'independent alpha sum')
        initial = vector(record['initial_q256'], T, 'initial quantization')
        for mid, pair in zip(mids, initial, strict=True):
            lo, hi = map(hx, vector(pair, 2, 'initial Q256 pair'))
            numerator = checked_int(mid.numerator * Q)
            require((lo, hi) == (numerator // mid.denominator, -((-numerator) // mid.denominator)), 'exact floor/ceiling midpoint quantization')
        require(record['input_identity'] == json_pin(initial), 'initial array identity')
        require(abs(sum(mids, F(0))) <= 128 * alpha, 'source constant-annihilation enclosure')
        saved_modes = vector(record['midpoint_modes'], M // 2 + 1, 'one-sided retained modes')
        require(record['mode_identity'] == json_pin(saved_modes), 'mode array identity')
        modes = []
        for k, item in enumerate(saved_modes):
            a, b, c, d = map(hx, vector(item, 4, 'Q256 complex rectangle'))
            require(a <= b and c <= d, 'ordered Fourier rectangle')
            if k in (0, M // 2):
                require(c <= 0 <= d, 'real endpoint imaginary zero')
            modes.append((a, b, c, d))
        a, b, c, d = modes[0]
        require(F(a, Q) - alpha <= 0 <= F(b, Q) + alpha and
                F(c, Q) - alpha <= 0 <= F(d, Q) + alpha, 'true DC compatible with saved enclosure')
        mode_rows.append(modes); alphas.append(alpha)
        row_summary.append({'row': row_id, 'initial_identity': json_pin(initial), 'mode_identity': json_pin(saved_modes),
                            'alpha': encoded(alpha), 'initial_coordinates_checked': T, 'rectangles_checked': M // 2 + 1})
    require(len(row_summary) == D, 'all source rows exhausted')
    return mode_rows, alphas, row_summary


def response_interval(modes, alphas, first, stop):
    """Independent product-of-magnitudes bound, with exact common denominators.

    For each real component, |xy-cd| <= (|c|+e)(|d|+f)-|cd|.
    This computes that product difference directly for each row pair and mode;
    it does not use the producer's h_tau + two linear sums + alpha-count route.
    The separate transform-only error sets coefficient alpha to zero. Nyquist
    and DC imaginary components AND their radii are identically zero.
    """
    cn = [[0] * D for _ in range(D)]
    hn = [[0] * D for _ in range(D)]
    tn = [[0] * D for _ in range(D)]
    denominators = [a.denominator for a in alphas]
    numerators = [a.numerator for a in alphas]
    for k in range(first, stop):
        endpoint = k in (0, M // 2)
        weight = 1 if endpoint else 2
        centers, absolute_products, expanded, transform_expanded = [], [], [], []
        for i in range(D):
            a, b, c, d = modes[i][k]
            x, tx = checked_int(a + b), checked_int(b - a)
            y, ty = (0, 0) if endpoint else (checked_int(c + d), checked_int(d - c))
            den, num = denominators[i], numerators[i]
            centers.append((x, y))
            absolute_products.append((checked_int(abs(x) * den), checked_int(abs(y) * den)))
            expanded.append((checked_int((abs(x) + tx) * den + DEN * num),
                             0 if endpoint else checked_int((abs(y) + ty) * den + DEN * num)))
            transform_expanded.append((checked_int(abs(x) + tx), checked_int(abs(y) + ty)))
        for i in range(D):
            x, y = centers[i]
            for j in range(i, D):
                u, v = centers[j]
                cn[i][j] = checked_int(cn[i][j] + weight * checked_int(x * u + y * v))
                full = sum(expanded[i][z] * expanded[j][z] - absolute_products[i][z] * absolute_products[j][z] for z in (0, 1))
                pure = sum(transform_expanded[i][z] * transform_expanded[j][z] - abs(centers[i][z] * centers[j][z]) for z in (0, 1))
                require(full >= 0 and pure >= 0, 'nonnegative independently expanded component bound')
                hn[i][j] = checked_int(hn[i][j] + weight * checked_int(full))
                tn[i][j] = checked_int(tn[i][j] + weight * checked_int(pure))
    c, h, ht = zero_matrix(), zero_matrix(), zero_matrix()
    for i in range(D):
        for j in range(i, D):
            c[i][j] = c[j][i] = fraction(F(cn[i][j], DEN * DEN))
            h[i][j] = h[j][i] = fraction(F(hn[i][j], DEN * DEN * denominators[i] * denominators[j]))
            ht[i][j] = ht[j][i] = fraction(F(tn[i][j], DEN * DEN))
    return c, h, ht


def add_matrices(matrices):
    return [[fraction(sum((a[i][j] for a in matrices), F(0))) for j in range(D)] for i in range(D)]


def band_audit(report, modes, alphas, gram):
    actual = vector(report['bands'], 14, 'bands')
    built, parseval_centers, parseval_errors = [], [], []
    for b in range(14):
        start = 1 << b
        stop = 2 * start if b < 13 else start + 1
        c, h, ht = response_interval(modes, alphas, start, stop)
        expect = {'index': b, 'first': start, 'last_exclusive': stop, 'C': encoded(c), 'H': encoded(h)}
        same(actual[b], expect, 'independent complete band ' + str(b))
        built.append((start, stop, c, h)); parseval_centers.append(c); parseval_errors.append(ht)
    dc, _, dc_tau = response_interval(modes, [F(0)] * D, 0, 1)
    parseval_centers.append(dc); parseval_errors.append(dc_tau)
    center, error = add_matrices(parseval_centers), add_matrices(parseval_errors)
    require(all(abs(center[i][j] - gram[i][j]) <= error[i][j] for i in range(D) for j in range(D)), 'independent midpoint Parseval includes G')
    same(report['midpoint_parseval'], {'center': encoded(center), 'error': encoded(error), 'contains_G': True}, 'full DC-inclusive midpoint Parseval')
    return built


def psd_values(record):
    closed(record, ('dtype', 'shape', 'values_hex', 'sha256'), 'PSD record')
    same(record['shape'], [8193], 'PSD shape')
    require(record['dtype'] == '<f8', 'PSD binary64 little-endian dtype')
    digest, values = hashlib.sha256(), []
    for text in vector(record['values_hex'], 8193, 'PSD hex values'):
        require(type(text) is str and len(text) <= 32, 'PSD bounded hex')
        try:
            number = float.fromhex(text)
        except (ValueError, OverflowError) as exc:
            raise AuditFailure('PSD malformed binary64') from exc
        require(math.isfinite(number) and number >= 0 and number.hex() == text, 'PSD canonical nonnegative finite binary64')
        digest.update(struct.pack('<d', number)); values.append(fraction(F.from_float(number)))
    require(record['sha256'] == digest.hexdigest(), 'PSD complete decoded-byte hash')
    return values


def weighted_matrices(bands, weights, field):
    return [[fraction(sum((weights[b] * bands[b][field][i][j] for b in range(14)), F(0)))
             for j in range(D)] for i in range(D)]


def scenario_audit(actual, prior_scenario, gram, rho, bands):
    # Endpoints are fs*P; interior paired real modes are fs*P/2.
    source = prior_scenario['source_record']
    p = psd_values(source)
    eigen = [fraction(x * (4096 if k in (0, 8192) else 2048)) for k, x in enumerate(p)]
    extrema, minima, maxima = [], [], []
    for b, (start, stop, _, _) in enumerate(bands):
        lo, hi = min(eigen[start:stop]), max(eigen[start:stop])
        minima.append(lo); maxima.append(hi)
        extrema.append({'index': b, 'ell': encoded(lo), 'u': encoded(hi),
                        'minimum_indices': [k for k in range(start, stop) if eigen[k] == lo],
                        'maximum_indices': [k for k in range(start, stop) if eigen[k] == hi]})
    cm = weighted_matrices(bands, minima, 2); cp = weighted_matrices(bands, maxima, 2)
    hm = weighted_matrices(bands, minima, 3); hp = weighted_matrices(bands, maxima, 3)
    dm, dp = max(sum(row, F(0)) for row in hm), max(sum(row, F(0)) for row in hp)
    lower = [[fraction(cm[i][j] - (dm if i == j else 0)) for j in range(D)] for i in range(D)]
    upper = [[fraction(cp[i][j] + (dp if i == j else 0)) for j in range(D)] for i in range(D)]
    minimum, maximum = min(eigen[1:]), max(eigen[1:])
    gl = [[fraction(x * minimum * (1 - rho)) for x in row] for row in gram]
    gu = [[fraction(x * maximum * (1 + rho)) for x in row] for row in gram]
    diagonal = [[lower[i][i], upper[i][i]] for i in range(D)]
    trace = [sum(lower[i][i] for i in range(D)), sum(upper[i][i] for i in range(D))]
    intervals = [[max(lower[i][i], gl[i][i]), min(upper[i][i], gu[i][i])] for i in range(D)]
    trace_interval = [max(trace[0], sum(gl[i][i] for i in range(D))), min(trace[1], sum(gu[i][i] for i in range(D)))]
    require(all(lo <= hi for lo, hi in intervals + [trace_interval]), 'nonempty scalar intersections')
    intersection = {'diagonal': intervals, 'trace': trace_interval,
                    'diagonal_ratios': [hi / lo if lo > 0 else None for lo, hi in intervals],
                    'trace_ratio': trace_interval[1] / trace_interval[0] if trace_interval[0] > 0 else None}
    expect = encoded({'id': prior_scenario['id'], 'source_record': source, 'band_extrema': extrema,
                      'C_minus': cm, 'C_plus': cp, 'H_minus': hm, 'H_plus': hp,
                      'delta_minus': dm, 'delta_plus': dp, 'lower': lower, 'upper': upper,
                      'diagonal': diagonal, 'trace': trace, 'global_lower': gl, 'global_upper': gu,
                      'scalar_intersections': intersection})
    same(actual, expect, 'all scenario fields ' + prior_scenario['id'])
    return {'id': prior_scenario['id'], 'source_sha256': source['sha256'], 'eigenvalues_checked': 8193,
            'extrema_with_all_ties_checked': 14, 'scenario_identity': json_pin(expect),
            'scalar_intersections': encoded(intersection), 'band_trace': encoded(trace),
            'global_trace': encoded([sum(gl[i][i] for i in range(D)), sum(gu[i][i] for i in range(D))])}


def twiddle_structure(value):
    closed(value, ('precision_bits', 'size', 'stages'), 'inherited twiddle evidence')
    same([value['precision_bits'], value['size']], [256, 16384], 'twiddle fixed domain')
    for stage, exponent in zip(vector(value['stages'], 14, 'twiddle stages'), range(1, 15), strict=True):
        closed(stage, ('base', 'length', 'powers_identity'), 'twiddle stage')
        require(type(stage['length']) is int and stage['length'] == 1 << exponent, 'twiddle stage length')
        a, b, c, d = map(hx, vector(stage['base'], 4, 'twiddle base'))
        require(a <= b and c <= d, 'ordered twiddle rectangle')
        pin_shape(stage['powers_identity'])
    return {'identity': json_pin(value), 'root_and_power_reconstruction': 'inherited_completed_qualified_recursive_validator',
            'independent_here': 'closed_stage_domain_and_ordered_base_rectangles_only'}


def runtime_audit(freeze, custody):
    item = freeze['runtime_inventory']
    inventory = custody.record(pathrow(item['path'], item['pin']))
    interpreter = freeze['interpreter']
    # The exact pinned chain is checked at every recorded link as well as at the
    # final named-path resolution. The inventory separately closes support bytes.
    for link in interpreter['symlink_chain']:
        closed(link, ('path', 'target'), 'interpreter symlink')
        require(Path(link['path']).is_symlink() and os.readlink(link['path']) == link['target'], 'interpreter chain link')
    require(str(Path(interpreter['named_path']).resolve()) == interpreter['resolved_path'], 'interpreter final resolution')
    custody.file(interpreter['resolved_path'], interpreter['target'])
    actual_names = set(inventory['extra_files'])
    for root in inventory['roots']:
        path = Path(root)
        require(path.is_dir() and path == path.resolve(), 'runtime root')
        for parent, dirs, names in os.walk(path):
            require(all(not (Path(parent) / name).is_symlink() for name in dirs), 'runtime symlink directory')
            actual_names.update(str(Path(parent) / name) for name in names)
    files = inventory['files']
    require(type(files) is list and len(files) == 3925 and
            [row['path'] for row in files] == sorted(actual_names), 'full runtime membership including pycs')
    total = 0
    for row in files:
        closed(row, ('path', 'bytes', 'sha256'), 'runtime file')
        custody.file(row['path'], {k: row[k] for k in ('bytes', 'sha256')}); total += row['bytes']
    require(total == 152961716, 'fixed complete runtime bytes')
    expected = {'interpreter': interpreter, 'runtime_files_count': len(files),
                'runtime_files_identity': json_pin(files), 'inventory_pin': item['pin']}
    return expected


def inputs_audit(freeze, custody):
    observed = []
    require([row['role'] for row in freeze['inputs']] == ['snapshot', 'ri90'], 'ordered two operands')
    for row in freeze['inputs']:
        closed(row, ('role', 'original', 'copy', 'pin'), 'operand identity')
        paths = []
        for field in ('original', 'copy'):
            custody.file(row[field], row['pin'])
            paths.append({'field': field, 'path': row[field], 'pin': row['pin'],
                          'metadata': custody.bindings[row[field]]['metadata']})
        observed.append({'role': row['role'], 'paths': paths})
    return observed


def closure_audit(freeze, custody):
    require(len(freeze['sources']) == 36 and len(freeze['helpers']) == 3, 'fixed source/helper counts')
    observed = []
    for row in freeze['sources']:
        closed(row, ('relative', 'original', 'copy', 'pin'), 'source row')
        require(row['copy'] == str(ROOT / 'experiments' / row['relative']), 'source copy placement')
        for field in ('original', 'copy'):
            custody.file(row[field], row['pin'])
            observed.append(pathrow(row[field], row['pin']))
    for row in freeze['helpers']:
        closed(row, ('path', 'pin'), 'helper row')
        custody.file(row['path'], row['pin']); observed.append(pathrow(row['path'], row['pin']))
    require(len(freeze['evidence']) == 13 and len(freeze['qualification_evidence']) == 13, 'held acceptance closure counts')
    for row in list(freeze['evidence'].values()) + freeze['qualification_evidence']:
        closed(row, ('path', 'bytes', 'sha256'), 'held acceptance record')
        custody.file(row['path'], {k: row[k] for k in ('bytes', 'sha256')})
    accepted = custody.record(freeze['evidence']['qualification_adjudication'])
    qualified = custody.record(freeze['evidence']['qualification_freeze'])
    require(accepted['schema'] == 'ri93-root-qualification-adjudication-v1' and
            accepted['status'] == 'accepted_fixed_fabricated_qualification' and
            accepted['complete_byte_equality'] is True and accepted['positive_checks'] == 11 and
            accepted['counts'] == qualified['expected_counts'] and
            accepted['authorized_freeze'] == freeze['evidence']['qualification_freeze'] and
            qualified['status'] == 'authorized_fabricated_qualification', 'genuine accepted qualification')
    same(qualified['expected_runtime'], freeze['expected_runtime'], 'inherited qualified runtime')
    same(qualified['interpreter'], freeze['interpreter'], 'inherited qualified interpreter')
    same(qualified['limits'], freeze['limits'], 'inherited fixed limits')
    same(accepted['evidence'], freeze['qualification_evidence'], 'all qualification evidence')
    qualification_reports = []
    for mode in ('normal', 'optimized'):
        require(type(accepted['actual_modes'][mode]['outer_exit']) is int and accepted['actual_modes'][mode]['outer_exit'] == 0,
                'actual qualification outer exit')
        receipt = custody.record(freeze['evidence']['qualification_' + mode + '_receipt'])
        require(receipt['schema'] == 'ri93-qualification-supervisor-receipt-v1' and receipt['mode'] == mode and
                receipt['success'] is True and receipt['stop_reason'] is None and
                type(receipt['child_exit_code']) is int and receipt['child_exit_code'] == 0,
                'genuine qualification mode success')
        require(receipt['freeze'] == {k: freeze['evidence']['qualification_freeze'][k] for k in ('bytes', 'sha256')},
                'qualification authorized freeze binding')
        run = qualified['runs'][mode]
        for name in ('stdout', 'stderr', 'worker_receipt', 'custody'):
            custody.file(run[name], receipt['outputs'][name])
        qualification_reports.append(run['stdout'])
        artifacts = receipt['verified_custody']['artifacts']
        require(len(artifacts) == 14, 'all genuine qualification artifacts')
        expected_artifacts = [{'name': x['name'], 'path': str(Path(run['artifact_dir']) / x['name']),
                               'bytes': x['bytes'], 'sha256': x['sha256']} for x in accepted['artifacts']]
        same(artifacts, expected_artifacts, 'accepted complete artifacts')
        for row in artifacts:
            custody.file(row['path'], {k: row[k] for k in ('bytes', 'sha256')})
    identical_files(*qualification_reports)
    inputs = inputs_audit(freeze, custody)
    acceptance = {'evidence': freeze['evidence'], 'qualification_evidence': freeze['qualification_evidence'],
                  'source_count': 36, 'inputs': inputs, 'provenance_template': freeze['provenance_template'],
                  'boundary': 'Held-capture frequency-band application of four postulated proxies; no physical noise adequacy or native prediction.'}
    return observed, acceptance


def finite_time(value):
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0, 'finite nonnegative elapsed metadata')
    return value


def monitor_audit(receipt):
    """Reconcile every raw ps observation against accepted sample arithmetic.

    Binary64 timestamp subtraction is compared with the conservative metadata
    bound 8 ulps of the two timestamps. This only handles subtraction rounding;
    the declared .1-second and 180-second gates are checked directly, unchanged.
    """
    attempts, samples = receipt['monitor_attempts'], receipt['samples']
    require(type(attempts) is list and attempts and type(samples) is list and samples, 'retained raw monitor evidence')
    live, previous_stamp = [], 0.0
    for index, item in enumerate(attempts):
        closed(item, ('elapsed_seconds', 'returncode', 'stdout', 'stderr'), 'successful raw ps attempt')
        stamp = finite_time(item['elapsed_seconds'])
        require(stamp >= previous_stamp and type(item['returncode']) is int and
                type(item['stdout']) is str and type(item['stderr']) is str, 'ordered raw ps values')
        previous_stamp = stamp
        raw = item['stdout'].strip()
        if item['returncode'] == 0 and raw.isdigit():
            live.append((stamp, int(raw)))
        else:
            require(index == len(attempts) - 1 and receipt['child_exit_code'] == 0,
                    'only final terminal ps observation may lack live RSS')
    require(len(samples) == len(live), 'all valid raw observations have one sample')
    previous, peak = 0.0, 0
    for sample, (stamp, rss) in zip(samples, live, strict=True):
        closed(sample, ('elapsed_seconds', 'rss_kib', 'gap_seconds'), 'monitor sample')
        require(sample['elapsed_seconds'] == stamp and type(sample['rss_kib']) is int and sample['rss_kib'] == rss,
                'sample equals raw ps')
        gap = finite_time(sample['gap_seconds'])
        rounding = 8 * max(math.ulp(float(stamp)), math.ulp(float(previous)))
        require(abs(gap - (stamp - previous)) <= rounding, 'sample gap agrees with timestamp subtraction')
        require(gap <= 0.1 and rss <= 524288, 'unchanged sample gap/RSS limits')
        previous, peak = stamp, max(peak, rss)
    elapsed = finite_time(receipt['child_elapsed_seconds'])
    final_gap = finite_time(receipt['final_sample_to_reap_gap_seconds'])
    require(elapsed <= 180 and previous <= elapsed and attempts[-1]['elapsed_seconds'] <= elapsed and
            final_gap == elapsed - previous and final_gap <= 0.1 and receipt['final_sample_gap_passed'] is True and
            type(receipt['peak_sampled_rss_kib']) is int and receipt['peak_sampled_rss_kib'] == peak,
            'terminal evidence and exact peak/final limits')
    return {'raw_attempts': len(attempts), 'live_samples': len(samples), 'peak_sampled_rss_kib': peak,
            'child_elapsed_seconds': elapsed, 'maximum_recorded_gap_seconds': max(x['gap_seconds'] for x in samples),
            'final_sample_to_reap_gap_seconds': final_gap,
            'scope': 'sampled sole worker RSS; no hard OS cap or process-group aggregate'}


def pointer(value, path):
    require(type(path) is list and path and all(type(k) in (str, int) for k in path), 'nonempty genuine completion field path')
    for key in path:
        value = value[key]
    return value


def mode_audit(mode, descriptor, freeze, source_records, runtime_records, acceptance, custody):
    specification = closed(descriptor['modes'][mode], ('result', 'receipt', 'worker_receipt', 'custody',
                           'attempt', 'outer_completion', 'outer_exit_pointer', 'outer_tool_pointer'), 'mode descriptor')
    run = freeze['runs'][mode]
    expected_paths = {'result': 'stdout', 'receipt': 'receipt', 'worker_receipt': 'worker_receipt',
                      'custody': 'custody', 'attempt': 'claim'}
    for field, name in expected_paths.items():
        require(specification[field]['path'] == run[name], 'actual mode output placement')
        custody.file(run[name], {k: specification[field][k] for k in ('bytes', 'sha256')})
    receipt = custody.record(specification['receipt'])
    worker = custody.record(specification['worker_receipt'])
    value = custody.record(specification['custody'])
    attempt = custody.record(specification['attempt'])
    completion = custody.record(specification['outer_completion'])
    exit_value = pointer(completion, specification['outer_exit_pointer'])
    tool_value = pointer(completion, specification['outer_tool_pointer'])
    require(type(exit_value) is int and exit_value == 0 and type(tool_value) is str and tool_value.strip(),
            'genuine separately retained outer completion zero/tool reference')
    freeze_pin = {k: descriptor['authorized_freeze'][k] for k in ('bytes', 'sha256')}
    same(attempt, {'freeze': freeze_pin, 'phase': 'fixed_saved_application', 'mode': mode, 'command': run['command']}, 'exclusive attempt record')
    for record, schema in ((receipt, 'ri96-application-supervisor-receipt-v1'), (worker, 'ri96-application-worker-receipt-v1')):
        require(record['schema'] == schema and record['phase'] == 'fixed_saved_application' and record['mode'] == mode and
                record['freeze'] == freeze_pin, 'actual mode identity')
    require(receipt['success'] is True and receipt['stop_reason'] is None and
            type(receipt['child_exit_code']) is int and receipt['child_exit_code'] == 0 and
            type(worker['exit_code']) is int and worker['exit_code'] == 0 and worker['error'] is None and
            not any(key in receipt for key in ('error', 'postcheck_error', 'termination_error')) and
            'postcheck_error' not in worker, 'complete parent and worker success')
    same(receipt['command'], run['command'], 'exact worker argv')
    same(receipt['environment'], freeze['environment'], 'exact environment')
    same(receipt['limits'], LIMITS, 'unchanged limits')
    for when in ('before', 'after'):
        same(receipt['source_' + when], source_records, 'parent complete source identity')
        same(worker['source_' + when], source_records, 'worker complete source identity')
        same(receipt['runtime_' + when], runtime_records, 'parent complete runtime inventory')
        same(worker['runtime_bytes_' + when], runtime_records, 'worker complete runtime inventory')
        same(worker['runtime_' + when], freeze['expected_runtime'], 'actual probed runtime fingerprint')
        same(receipt['acceptance_' + when], acceptance, 'parent full accepted premises')
        same(worker['acceptance_' + when], acceptance, 'worker full accepted premises')
        same(worker['inputs_' + when], acceptance['inputs'], 'worker operand bytes/stat identities')
        same(worker['captured_ri90_' + when], freeze['provenance_template']['inputs']['ri90'], 'captured immutable RI90 bytes')
    same(worker['saved_result_validation'], VALIDATION, 'genuine full independent validator completion counts')
    require(worker['full_validator_passed'] is True, 'validator genuinely completed')
    closed(receipt['outputs'], ('stdout', 'stderr', 'worker_receipt', 'custody'), 'complete mode outputs')
    for name in ('stdout', 'stderr', 'worker_receipt', 'custody'):
        custody.file(run[name], receipt['outputs'][name])
    require(receipt['outputs']['stderr'] == byte_pin(b''), 'empty successful stderr')
    result_pin = {k: specification['result'][k] for k in ('bytes', 'sha256')}
    require(receipt['outputs']['stdout'] == result_pin, 'full result identity')
    same(worker['operation'], {'result': pathrow(run['stdout'], result_pin),
                               'custody': pathrow(run['custody'], receipt['outputs']['custody']), 'claim': freeze['claim']}, 'worker exact returned custody')
    expect_custody = {'schema': 'ri96-application-custody-v1', 'phase': 'fixed_saved_application', 'mode': mode,
                      'context': freeze['context'], 'report': pathrow(run['stdout'], result_pin),
                      'provenance': freeze['provenance_template'], 'genuine_runtime_fingerprint': json_pin(freeze['expected_runtime']),
                      'inputs': acceptance['inputs'], 'captured_ri90': freeze['provenance_template']['inputs']['ri90'],
                      'saved_result_validation': VALIDATION, 'full_validator_passed': True, 'claim': freeze['claim']}
    same(value, expect_custody, 'complete scientific output custody')
    expect_verified = {'custody_pin': receipt['outputs']['custody'], 'report_pin': result_pin,
                       'provenance': freeze['provenance_template'], 'inputs': acceptance['inputs'],
                       'captured_ri90': freeze['provenance_template']['inputs']['ri90'],
                       'saved_result_validation': VALIDATION, 'full_validator_passed': True}
    same(receipt['verified_custody'], expect_verified, 'parent independent reopen custody')
    monitor = monitor_audit(receipt)
    return {'mode': mode, 'result': specification['result'], 'receipt': specification['receipt'],
            'outer_completion': specification['outer_completion'], 'outer_tool_reference': tool_value,
            'actual_outer_exit': 0, 'validation': VALIDATION, 'monitor': monitor}


def admission(descriptor, custody):
    closed(descriptor, ('schema', 'status', 'auditor', 'contract', 'authorized_freeze', 'root_admission',
                       'root_admission_status', 'modes'), 'audit descriptor')
    require(descriptor['schema'] == 'ri96-independent-saved-audit-input-v1' and
            descriptor['status'] == 'root_bound_completed_application_evidence' and
            descriptor['root_admission_status'] == 'accepted_actual_custody_pending_independent_saved_arithmetic',
            'concrete admitted saved-evidence descriptor required')
    require(descriptor['auditor']['path'] == str(Path(__file__).resolve()), 'captured auditor source binding')
    for field in ('auditor', 'contract'):
        row = closed(descriptor[field], ('path', 'bytes', 'sha256'), 'auditor/contract pin')
        custody.file(row['path'], {k: row[k] for k in ('bytes', 'sha256')})
    prospective = custody.record(pathrow(ROOT / 'PROSPECTIVE_FREEZE.json', PROSPECTIVE_PIN))
    require(descriptor['authorized_freeze']['path'] == str(ROOT / 'AUTHORIZED_FREEZE.json'), 'fixed application freeze path')
    freeze = custody.record(descriptor['authorized_freeze'])
    expected = dict(prospective); expected['status'] = 'authorized_fixed_saved_application'
    same(freeze, expected, 'only reviewed application authorization status differs')
    require(prospective['status'] == 'prospective_not_authorized' and freeze['schema'] == 'ri96-fixed-saved-application-freeze-v1' and
            freeze['root'] == str(ROOT) and freeze['phase'] == 'fixed_saved_application', 'fixed application phase/root')
    same(freeze['limits'], LIMITS, 'fixed resource envelope')
    closed(descriptor['modes'], ('normal', 'optimized'), 'both completed modes')
    root = custody.record(descriptor['root_admission'])
    # Root supplies this small bridge only after separately inspecting authentic
    # outer tool evidence and whole application custody. It is not final math
    # acceptance; the audit never creates or upgrades this record.
    closed(root, ('schema', 'status', 'authorized_freeze', 'modes', 'auditor', 'contract'), 'root custody bridge')
    require(root['schema'] == 'ri96-independent-audit-custody-admission-v1' and
            root['status'] == descriptor['root_admission_status'], 'root held-custody admission')
    for field in ('authorized_freeze', 'modes', 'auditor', 'contract'):
        same(root[field], descriptor[field], 'root bridge binding ' + field)
    sources, acceptance = closure_audit(freeze, custody)
    runtime = runtime_audit(freeze, custody)
    modes = [mode_audit(mode, descriptor, freeze, sources, runtime, acceptance, custody) for mode in ('normal', 'optimized')]
    left, right = (descriptor['modes'][m]['result'] for m in ('normal', 'optimized'))
    require({k: left[k] for k in ('bytes', 'sha256')} == {k: right[k] for k in ('bytes', 'sha256')}, 'full mode result identities equal')
    identical_files(left['path'], right['path'])
    return freeze, modes


def scientific_audit(report, ri90, snapshot, freeze, custody):
    closed(report, RESULT_KEYS, 'complete scientific result')
    require(report['schema'] == 'ri93-frequency-band-proxy-v1' and report['phase'] == 'fixed_saved_application' and
            report['status'] == 'all_gates_passed' and report['model'] == 'postulated_finite_circulant_from_empirical_psd',
            'fixed observed saved-result model/phase')
    same(report['method'], freeze['result_domain']['method'], 'unchanged numerical method')
    same(report['rows'], ROWS, 'fixed eight selected rows')
    same(report['provenance'], freeze['provenance_template'], 'all actual source/input/acceptance/runtime provenance')
    same(report['limitations'], freeze['result_domain']['limitations'], 'all ten limitations and physical claim boundary')
    gates = freeze['result_domain']['gates']
    same(report['gates'], {'inventory': gates, 'counts': {'total': 10, 'passed': 10, 'failed': 0},
                           'results': [{'id': name, 'passed': True} for name in gates]}, 'complete declared gate inventory')
    require(ri90['schema'] == 'ri86-colored-proxy-envelope-v1' and ri90['phase'] == 'fixed_saved_application' and
            ri90['status'] == 'all_gates_passed', 'accepted actual RI90 context')
    same(ri90['rows'], ROWS, 'held prior rows'); same(ri90['scenario_order'], SCENARIOS, 'held prior scenario order')
    prior = {'context': 'accepted_ri90_saved_output', 'G': ri90['certificate']['G'], 'rho': ri90['certificate']['rho'],
             'scenarios': [{'id': s['id'], 'source_record': s['source_record']} for s in ri90['scenarios']],
             'held_provenance': ri90['provenance'], 'held_limitations': ri90['limitations']}
    same(report['prior'], prior, 'complete accepted prior projection')
    gram, rho = matrix(prior['G']), rational(prior['rho'])
    require(0 <= rho <= F(1, 10**12), 'unchanged held accuracy premise')
    gram_pivots = gram_positive(gram)
    modes, alphas, row_evidence = rows_audit(report, snapshot, custody)
    twiddle = twiddle_structure(report['twiddles'])
    bands = band_audit(report, modes, alphas, gram)
    scenario_records = vector(report['scenarios'], 4, 'scenario list')
    require([s['id'] for s in prior['scenarios']] == SCENARIOS, 'four fixed independent proxy scenarios')
    scenarios = [scenario_audit(actual, held, gram, rho, bands)
                 for actual, held in zip(scenario_records, prior['scenarios'], strict=True)]
    return {'rows': row_evidence, 'gram_positive_LDL_pivots_identity': gram_pivots, 'twiddles': twiddle,
            'bands_identity': json_pin(report['bands']), 'midpoint_parseval_identity': json_pin(report['midpoint_parseval']),
            'scenarios': scenarios, 'all_independently_rebuilt_saved_arithmetic_fields_exactly_equal': True,
            'counts': {'source_rows': 8, 'source_intervals': 8 * (N + T), 'initial_coordinates': 8 * T,
                       'one_sided_rectangles_structurally_checked': 8 * 8193, 'band_C_entries': 14 * 64,
                       'band_H_entries': 14 * 64, 'parseval_center_entries': 64, 'parseval_error_entries': 64,
                       'PSD_bins': 4 * 8193, 'eigenvalues': 4 * 8193, 'band_extrema': 4 * 14,
                       'weighted_C_H_entries': 4 * 4 * 64, 'band_endpoint_entries': 4 * 2 * 64,
                       'global_endpoint_entries': 4 * 2 * 64, 'scenario_margins': 8,
                       'diagonal_interval_pairs': 32, 'trace_interval_pairs': 4,
                       'intersection_pairs_and_conditional_ratios': 36, 'limitations': 10},
            'independent_method': 'source-row midpoint/radius reconstruction and per-component product-of-magnitudes remainder; exact rational matrices',
            'inherited_not_recomputed': [
                'RI73 interval validity/adjoint reconstruction and its captured custody',
                'RI90 accepted Gram/rho certificate and empirical PSD scientific provenance',
                'The qualified recursive Q256 Fourier transform, root isolation, twiddle powers and mode enclosures, actually replayed by validate_saved in both RI96 modes',
                'The accepted constant-annihilation theorem and RI92 Loewner/Gram premises'],
            'claim_boundary': 'Conditional finite circulant proxy arithmetic only; no physical covariance adequacy, significance, native forward map or RET result'}


def main():
    require(len(sys.argv) == 4, 'usage: audit_saved_result.py DESCRIPTOR BYTES SHA256')
    require(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0,
            'one separately supervised normal -I -B audit invocation required')
    descriptor_path = Path(sys.argv[1])
    require(sys.argv[2].isdigit(), 'descriptor byte count')
    custody = Custody()
    descriptor_row = pathrow(descriptor_path, {'bytes': int(sys.argv[2]), 'sha256': sys.argv[3]})
    descriptor = custody.record(descriptor_row)
    freeze, mode_evidence = admission(descriptor, custody)
    # Both immutable scientific input identities and complete result/custody are
    # admitted before either operand's numerical body is decoded.
    inputs_audit(freeze, custody)
    ri90_input = freeze['inputs'][1]
    ri90 = custody.record(pathrow(ri90_input['copy'], ri90_input['pin']), scientific=True)
    report = custody.record(descriptor['modes']['normal']['result'], scientific=True)
    snapshot_input = freeze['inputs'][0]
    snapshot = pathrow(snapshot_input['copy'], snapshot_input['pin'])
    arithmetic = scientific_audit(report, ri90, snapshot, freeze, custody)
    full_result_pin = json_pin(report)
    require(full_result_pin == {k: descriptor['modes']['normal']['result'][k] for k in ('bytes', 'sha256')}, 'complete canonical saved result')
    del report, ri90
    final_bindings = custody.final()
    output = {'schema': 'ri96-independent-saved-arithmetic-audit-v1', 'status': 'all_declared_saved_arithmetic_and_custody_checks_passed',
              'descriptor': descriptor_row, 'application_freeze': descriptor['authorized_freeze'],
              'root_custody_premise': descriptor['root_admission'], 'auditor': descriptor['auditor'], 'contract': descriptor['contract'],
              'actual_modes': mode_evidence, 'normal_optimized_complete_byte_equality': True,
              'complete_saved_result_pin': full_result_pin, 'arithmetic': arithmetic, 'final_custody': final_bindings,
              'qualification_scope': 'Source-reviewed saved arithmetic consumer; no new claim of independent FFT derivation or fabricated-control qualification',
              'execution_scope': 'One actual audit invocation of both existing completed modes; output requires separate genuine audit supervisor/custody adjudication'}
    for body in chunks(output):
        sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
