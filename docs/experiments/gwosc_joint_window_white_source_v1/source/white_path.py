"""RI125 bounded white application source. UNEXECUTED, NOT SELF-ADMITTING.

The prospective caller must authenticate this source before importing it, bind
the request pin externally, and adjudicate its complete runtime/history custody.
The local checks authenticate operands and enforce the frozen interface; a JSON
card is not evidence that root permission or actual execution occurred.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import stat
import white_kernel as W

LIMIT = 64 * 1024 * 1024
ROW_LIMIT = 8 * 1024 * 1024
N, L, T, STRIDE = 2769, 4096, 10961, 8192
ROWS = list(W.ROWS)
SOURCE_ROLES = ('design', 'contract', 'primary', 'white_kernel', 'validator',
                'qualifier', 'cases', 'kernel_refusals', 'white_refusals',
                'fabricated_interfaces')
INPUT_ROLES = ('capture', 'ri73_result', 'ri73_source', 'ri73_reconciliation',
               'ri73_final_review', 'ri73_audit_freeze')
RUNTIME_ROLES = ('fingerprint', 'inventory', 'interpreter')
FIXED = {
    'capture': {'bytes': 51891508, 'sha256': 'fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba'},
    'ri73_result': {'bytes': 11180937, 'sha256': '3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe'},
    'ri73_source': {'bytes': 68018, 'sha256': '574f5f1b8900221a47bc30ea62e6bed378a8fd1c8b4aa904e0549ade8ceb2887'},
    'ri73_reconciliation': {'bytes': 2098, 'sha256': '5263ab139542d6591af03300ded7f2d7c9fba5fd3585347b4f7b4bfb7605f232'},
    'ri73_final_review': {'bytes': 5479, 'sha256': 'c4ac724cbde99d98b3b95f51fcf030a9ac00e48fd7aafa8998356e0f3a9eea1e'},
    'ri73_audit_freeze': {'bytes': 31442, 'sha256': 'a10dd521e72e6cecbc55a5c35720a4d6755daebc9f1d07ecd5553af220402581'},
}
DESIGN = {'bytes': 31586, 'sha256': '4e725c42d77097e66b5b5cf5c3cc014f97b2a42663b0ef0ee3f78d8b4161699b'}
DESIGN_ACCEPTANCE = {'bytes': 2948, 'sha256': '2963dbd483539f90ef52b744e93b52451265975cbd041ff2d59df26f0d94936a'}
# These literal source-derived names are historical evidence, not rerun controls.
RI73_GATES = (
    'fixture:fir', 'fixture:cancellation', 'fixture:singleton',
    'fixture:offdiagonal_small', 'fixture:offdiagonal_large', 'fixture:failed_gate',
    'fixture:midpoint', 'fixture:rank_ambiguity', 'fixture:singular', 'fixture:output_law',
    'refusal:float_endpoint', 'refusal:bool_endpoint', 'refusal:nonfinite_endpoint',
    'refusal:reversed_interval', 'refusal:negative_radius', 'refusal:matrix_rows',
    'refusal:bool_dimension', 'refusal:bool_row_dimension', 'refusal:matrix_columns',
    'refusal:ragged_box', 'refusal:asymmetric_gram', 'refusal:asymmetric_error',
    'refusal:negative_error', 'refusal:negative_pivot', 'refusal:wrong_ldl',
    'refusal:wrong_inverse', 'refusal:wrong_delta', 'refusal:wrong_gamma',
    'refusal:incorrect_rank', 'refusal:bool_rank', 'refusal:wrong_mp1',
    'refusal:wrong_mp2', 'refusal:wrong_mp3', 'refusal:off_support',
    'refusal:negative_rho', 'refusal:rho_at_one', 'refusal:negative_output_error',
    'refusal:unqualified_cdf', 'refusal:cdf_series_domain', 'refusal:negative_cdf_argument',
    'refusal:estimated_covariance', 'refusal:colored_covariance',
    'refusal:fraction_numerator_cap', 'refusal:fraction_denominator_cap',
    'refusal:operation_result_cap', 'refusal:hex_length', 'refusal:hex_plus',
    'refusal:hex_negative_zero', 'refusal:hex_leading_zero',
    'refusal:hex_denominator_zero', 'refusal:hex_unreduced', 'refusal:work_cap',
    'refusal:work_bool', 'refusal:output_cap', 'refusal:duplicate_json',
    'refusal:nonfinite_json', 'refusal:overflow_json', 'refusal:changed_snapshot',
    'refusal:bool_pin', 'refusal:changed_runtime', 'refusal:changed_runtime_build',
    'refusal:failed_receipt', 'refusal:incomplete_receipt',
    'refusal:changed_receipt_engine', 'refusal:changed_arithmetic',
    'refusal:wrong_padding', 'refusal:bool_padding',
    'refusal:changed_manifest_coefficient', 'refusal:changed_manifest_stage_order',
    'refusal:changed_manifest_padding', 'refusal:missing_rows', 'refusal:wrong_rows',
    'refusal:wrong_snapshot_shape', 'refusal:missing_expected_summaries',
    'integration:reconstruction', 'integration:gram', 'integration:mathematical',
    'integration:accuracy', 'integration:cross', 'probe:zero', 'probe:constant',
    'probe:0', 'probe:1', 'probe:27', 'probe:805', 'probe:1384', 'probe:2741',
    'probe:2767', 'probe:2768', 'integration:law', 'integration:final_custody',
    'completion:custody',
)
WHITE_GATES = ('admission:phase', 'admission:inputs', 'admission:source',
               'operator:gram', 'operator:capture', 'operator:rows',
               'shift:direct', 'shift:polarization', 'response:7', 'trace:7',
               'structural:7', 'accuracy:7', 'response:6', 'trace:6',
               'structural:6', 'accuracy:6', 'completion:stable')
LIMITATIONS = [
    'Conditional conventional moments of fixed operators and explicitly postulated joint laws only.',
    'Numerical enclosure and usefulness bounds are not statistical or physical model error.',
    'All four public development/calibration scenarios remain unchanged and are not protected validation.',
    'Shared-white amplitude and population mean are unresolved; sample centering does not establish zero population mean.',
    'Exact periodic repetition is a hypothetical completion, not established detector noise.',
    'Nominal V2/C02, blank Yunits, clear L1 NO_CW_HW_INJ, possible injection effects and below-10-Hz calibration remain unresolved.',
    'No significance, fitted model, calibrated measurement, native forward map or geometry/gravity result is established; RET remains paused.',
]


def need(ok, code, message):
    W.need(ok, code, message)


def closed(value, names, code='SCHEMA'):
    need(type(value) is dict and all(type(k) is str for k in value)
         and set(value) == set(names), code, 'closed object keys')


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def equal(a, b, code, message):
    need(same(a, b), code, message)


def pin(value):
    closed(value, ('bytes', 'sha256'), 'INPUT')
    need(type(value['bytes']) is int and 0 < value['bytes'] <= LIMIT,
         'INPUT', 'positive bounded pin length')
    need(type(value['sha256']) is str
         and re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None,
         'INPUT', 'lowercase sha256')


def identity(body):
    need(type(body) is bytes and len(body) <= LIMIT, 'RESOURCE', 'bounded immutable body')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def json_chunks(value, *, compact=False):
    encoder = json.JSONEncoder(sort_keys=True, ensure_ascii=True, allow_nan=False,
                               **({'separators': (',', ':')} if compact else {'indent': 2}))
    count = 0
    for text in encoder.iterencode(value):
        block = text.encode('ascii')
        count += len(block)
        need(count <= LIMIT, 'RESOURCE', 'serialized byte ceiling')
        yield block
    if not compact:
        need(count + 1 <= LIMIT, 'RESOURCE', 'terminal newline ceiling')
        yield b'\n'


def serial(value, *, compact=False):
    return b''.join(json_chunks(value, compact=compact))


def json_pin(value, *, compact=False):
    h, count = hashlib.sha256(), 0
    for block in json_chunks(value, compact=compact):
        h.update(block)
        count += len(block)
    return {'bytes': count, 'sha256': h.hexdigest()}


def parse(body):
    need(type(body) is bytes and len(body) <= LIMIT, 'RESOURCE', 'JSON byte ceiling')
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'SCHEMA', 'duplicate JSON key')
            out[key] = value
        return out
    def bad(_):
        raise W.ApplicationError('EXACT', 'decimal or nonfinite JSON token')
    def integer(text):
        need(len(text) <= 65537, 'RESOURCE', 'JSON integer text ceiling')
        return W.integer(int(text))
    try:
        return json.loads(body, object_pairs_hook=pairs, parse_float=bad,
                          parse_constant=bad, parse_int=integer)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise W.ApplicationError('SCHEMA', 'invalid bounded JSON') from exc


def state(s):
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns,
            s.st_mode, s.st_nlink)


def literal_path(value):
    need(type(value) is str, 'INPUT', 'path string')
    p = Path(value)
    need(p.is_absolute() and str(p) == value and p == p.resolve(),
         'INPUT', 'literal absolute nonsymlink path')
    return p


def file_ref(value):
    closed(value, ('path', 'pin'), 'INPUT')
    pin(value['pin'])
    return literal_path(value['path'])


def read_bound(record, *, keep=False, before=None):
    p = file_ref(record)
    initial = p.lstat()
    need(stat.S_ISREG(initial.st_mode) and initial.st_nlink == 1,
         'INPUT', 'regular single-link source or input')
    need(0 < initial.st_size <= LIMIT, 'RESOURCE', 'file byte ceiling')
    if before is not None:
        need(state(initial) == before, 'CUSTODY', 'path state changed')
    h, count, pieces = hashlib.sha256(), 0, []
    fd = os.open(str(p), os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        need(state(os.fstat(stream.fileno())) == state(initial), 'CUSTODY', 'opened file differs')
        while True:
            block = stream.read(65536)
            if not block:
                break
            count += len(block)
            need(count <= LIMIT, 'RESOURCE', 'stream byte ceiling')
            h.update(block)
            if keep:
                pieces.append(block)
        need(state(os.fstat(stream.fileno())) == state(initial), 'CUSTODY', 'descriptor changed')
    need(state(p.lstat()) == state(initial), 'CUSTODY', 'closed path changed')
    equal({'bytes': count, 'sha256': h.hexdigest()}, record['pin'], 'INPUT', 'whole body pin')
    need(count == initial.st_size, 'CUSTODY', 'complete file length')
    return (b''.join(pieces) if keep else None), state(initial)


class Ledger:
    """Register every valid reference before opening any; finish each independently."""
    def __init__(self):
        self.entries = []

    def register(self, role, record):
        file_ref(record)
        self.entries.append([role, record, None])

    def read_all(self):
        for row in self.entries:
            _, row[2] = read_bound(row[1])

    def finish(self):
        out = []
        for role, record, before in self.entries:
            try:
                observed, current = read_bound(record, before=before)
                need(before is not None, 'CUSTODY', 'initial custody incomplete')
                out.append({'role': role, 'pin': record['pin'], 'unchanged': True, 'error': None})
            except Exception as exc:
                out.append({'role': role, 'pin': None, 'unchanged': False,
                            'error': (type(exc).__name__ + ': ' + str(exc))[:1024]})
        return out


class RowReader:
    def __init__(self, stream):
        self.stream, self.buffer, self.pos = stream, b'', 0
        self.digest, self.count = hashlib.sha256(), 0

    def refill(self):
        self.buffer, self.pos = self.stream.read(65536), 0
        self.digest.update(self.buffer)
        self.count += len(self.buffer)
        need(self.count <= LIMIT, 'RESOURCE', 'capture byte ceiling')

    def take(self, count):
        answer = bytearray()
        while len(answer) < count:
            if self.pos == len(self.buffer):
                self.refill()
                need(bool(self.buffer), 'ROW', 'truncated capture')
            size = min(count - len(answer), len(self.buffer) - self.pos)
            answer.extend(self.buffer[self.pos:self.pos + size])
            self.pos += size
        return bytes(answer)

    def row(self):
        need(self.take(1) == b'{', 'ROW', 'row start')
        chunks, count, depth, string, escape = [b'{'], 1, 1, False, False
        while depth:
            if self.pos == len(self.buffer):
                self.refill()
                need(bool(self.buffer), 'ROW', 'truncated row')
            start = self.pos
            while self.pos < len(self.buffer):
                c = self.buffer[self.pos]
                self.pos += 1
                if string:
                    if escape:
                        escape = False
                    elif c == 92:
                        escape = True
                    elif c == 34:
                        string = False
                elif c == 34:
                    string = True
                elif c == 123:
                    depth += 1
                elif c == 125:
                    depth -= 1
                    if depth == 0:
                        break
            part = self.buffer[start:self.pos]
            count += len(part)
            need(count <= ROW_LIMIT, 'RESOURCE', 'capture row byte ceiling')
            chunks.append(part)
        return b''.join(chunks)

    def eof(self):
        if self.pos != len(self.buffer):
            return False
        self.refill()
        return not self.buffer


def array_identity(values, label, domain):
    value = {'schema': 'ri73-exact-array-v1', 'label': label,
             'domain': domain, 'values': values}
    return {'schema': value['schema'], 'label': label, 'domain': domain,
            **json_pin(value, compact=True)}


def capture_rows(record, *, fabricated=False):
    """Full eight-row stream, not a selected-strip parser. Explicit final exhaustion."""
    need(type(fabricated) is bool, 'PHASE', 'explicit capture phase')
    if fabricated:
        need(not same(record.get('pin'), FIXED['capture']), 'PHASE', 'actual capture forbidden in fabrication')
    _, before = read_bound(record)
    p = file_ref(record)
    schema = ('ri125-fabricated-capture-v1' if fabricated
              else 'ri73-reconstructed-intervals-v1')
    header = (b'{"dimensions":' + serial({'N': N, 'L': L, 'T': T}, compact=True)
              + b',"row_order":' + serial(ROWS, compact=True) + b',"rows":[')
    with os.fdopen(os.open(str(p), os.O_RDONLY | os.O_NOFOLLOW), 'rb') as stream:
        need(state(os.fstat(stream.fileno())) == before, 'CUSTODY', 'capture descriptor initial')
        reader = RowReader(stream)
        equal(reader.take(len(header)), header, 'ROW', 'literal capture header')
        for index, label in enumerate(ROWS):
            if index:
                equal(reader.take(1), b',', 'ROW', 'row separator')
            body = reader.row()
            row = parse(body)
            equal(serial(row, compact=True), body, 'CANONICAL', 'compact row encoding')
            closed(row, ('row', 'short', 'long'), 'ROW')
            equal(row['row'], label, 'ROW', 'fixed row order')
            head, tail, sums = [], [], {}
            for name, count in (('short', N), ('long', T)):
                values = W.sequence(row[name], count)
                low = high = W.F(0)
                for coordinate, box in enumerate(values):
                    a, b = W.uninterval(box)
                    low, high = W.add(low, a), W.add(high, b)
                    if name == 'long' and coordinate < N:
                        head.append(box)
                    if name == 'long' and coordinate >= STRIDE:
                        tail.append(box)
                sums[name] = (low, high)
            row_sum = (W.sub(sums['long'][0], sums['short'][1]),
                       W.sub(sums['long'][1], sums['short'][0]))
            need(row_sum[0] <= 0 <= row_sum[1], 'ROW', 'constant sum enclosure')
            vectors = {'row': label,
                       'short': array_identity(row['short'], 'short', {'length': N, 'row': label}),
                       'long': array_identity(row['long'], 'long', {'length': T, 'row': label, 'seed': L + label})}
            result = {'strip': {'row': label, 'head': head, 'tail': tail},
                      'vectors': vectors,
                      'row_identity': {'row': label, 'source_row_pin': identity(body),
                          'short_count': N, 'long_count': T,
                          'head_pin': json_pin(head), 'tail_pin': json_pin(tail),
                          'a_row_sum_interval': W.interval(*row_sum), 'contains_zero': True}}
            del row, values, box, body, head, tail, sums
            yield result
            del result
        footer = b'],"schema":' + serial(schema, compact=True) + b'}'
        equal(reader.take(len(footer)), footer, 'ROW', 'capture footer and ninth-row exhaustion')
        need(reader.eof(), 'ROW', 'trailing capture bytes')
        equal({'bytes': reader.count, 'sha256': reader.digest.hexdigest()}, record['pin'],
              'INPUT', 'complete consumed capture pin')
        need(state(os.fstat(stream.fileno())) == before, 'CUSTODY', 'capture descriptor final')
    read_bound(record, before=before)


def ri73_operand(report):
    closed(report, ('schema_version', 'mode', 'status', 'full_integration_qualified',
        'source_identity', 'dependencies', 'runtime', 'inherited_arithmetic_contract',
        'resource_contract', 'model', 'dimensions', 'rows', 'sample_spacing',
        'gate_inventory', 'gate_counts', 'gates', 'deterministic_fixture_admission_passed',
        'sampling_performed', 'admitted_coefficient_design_requested',
        'reconstructed_rows_admitted', 'exact_scalar_encoding', 'scope'), 'RI73')
    for key, expected in {
        'schema_version': 'ri73-unit-white-operator-covariance-v1',
        'mode': 'fixed_operator_covariance', 'status': 'fixed_operator_covariance_passed',
        'full_integration_qualified': True, 'source_identity': FIXED['ri73_source'],
        'dimensions': {'N': N, 'L': L, 'T': T}, 'rows': ROWS,
        'sample_spacing': W.scalar(W.F(1, 4096)),
        'model': {'kind': 'known_synthetic_unit_white', 'mean': 'zero', 'covariance': 'I_T',
                  'input_dimension': T, 'output_dimension': 8},
        'gate_inventory': list(RI73_GATES), 'gate_counts': {'total': 92, 'passed': 92, 'failed': 0},
        'deterministic_fixture_admission_passed': True, 'sampling_performed': False,
        'admitted_coefficient_design_requested': True, 'reconstructed_rows_admitted': True,
    }.items():
        equal(report[key], expected, 'RI73', 'full inherited header ' + key)
    details = {}
    for name, gate in zip(RI73_GATES, W.sequence(report['gates'], 92)):
        closed(gate, ('id', 'passed', 'detail'), 'RI73')
        equal(gate['id'], name, 'RI73', 'literal 92-gate order')
        need(gate['passed'] is True and type(gate['detail']) is dict,
             'RI73', 'all inherited gates passed with details')
        details[name] = gate['detail']
    reconstruction = details['integration:reconstruction']
    closed(reconstruction, ('adjoints_reconstructed', 'summaries_reconciled', 'row_state_identity',
        'row_summaries', 'vector_identities', 'A_identity', 'P_identity', 'Q_identity',
        'constant_row_sum_intervals', 'coefficient_arrays_stored_in_result'), 'RI73')
    equal(reconstruction['adjoints_reconstructed'], 16, 'RI73', 'all reconstructed adjoints')
    equal(reconstruction['summaries_reconciled'], 8, 'RI73', 'all row summaries')
    equal(reconstruction['coefficient_arrays_stored_in_result'], False, 'RI73', 'external complete capture')
    W.sequence(reconstruction['vector_identities'], 8)
    W.sequence(reconstruction['constant_row_sum_intervals'], 8)
    detail = details['integration:gram']
    closed(detail, ('certificate', 'M_identity', 'R_identity'), 'RI73')
    certificate = detail['certificate']
    closed(certificate, ('mathematical_gate', 'accuracy_gate', 'rho_limit', 'G', 'H', 'delta',
        'eta2', 'ldl', 'inverse', 'left_inverse_product', 'right_inverse_product',
        'gamma', 'rho', 'status', 'rank', 'inverse_error_norm_bound',
        'inverse_lower', 'inverse_upper'), 'RI73')
    for key, value in (('status', 'certified'), ('rank', 8), ('mathematical_gate', True),
                       ('accuracy_gate', True), ('rho_limit', W.scalar(W.F(1, 10**12)))):
        equal(certificate[key], value, 'RI73', 'accepted inherited certificate ' + key)
    for name, limit_key, limit in (('mathematical', 'strict_limit', W.F(1)),
                                   ('accuracy', 'inclusive_limit', W.F(1, 10**12))):
        equal(details['integration:' + name], {'status': 'certified',
            'acceptance': {'passed': True}, 'rho': certificate['rho'],
            limit_key: W.scalar(limit)}, 'RI73', 'inherited acceptance details')
    gram = {key: certificate[key] for key in W.GRAM_KEYS}
    W.inherited_gram(gram, 8)
    return gram, json_pin(detail), reconstruction


def assemble_white(record, gram, reconstruction, *, fabricated=False):
    strips, identities = [], []
    iterator = capture_rows(record, fabricated=fabricated)
    try:
        for i, label in enumerate(ROWS):
            try:
                item = next(iterator)
            except StopIteration as exc:
                raise W.ApplicationError('ROW', 'missing full row') from exc
            equal(item['strip']['row'], label, 'ROW', 'assembly row order')
            if not fabricated:
                bind_row(item, reconstruction, i)
            strips.append(item['strip'])
            identities.append(item['row_identity'])
        marker = object()
        need(next(iterator, marker) is marker, 'ROW', 'extra ninth row')
    finally:
        iterator.close()
    # A saved Shift is never accepted as an operand here.
    shift = W.derive_shift(strips, length=T, stride=STRIDE)
    responses = [W.derive_response(gram, shift, n=n) for n in (7, 6)]
    return identities, shift, responses


def bind_row(item, reconstruction, index):
    equal(item['vectors'], reconstruction['vector_identities'][index],
          'BINDING', 'capture vector identity tied to accepted RI73 result')
    equal(item['row_identity']['a_row_sum_interval'],
          reconstruction['constant_row_sum_intervals'][index],
          'BINDING', 'complete row sum tied to accepted RI73 result')


def checks(responses):
    accuracy = {'accuracy:' + str(row['n']): row['usefulness_state'] == 'usefulness_passed'
                for row in responses}
    rows = [{'id': name, 'passed': accuracy.get(name, True)} for name in WHITE_GATES]
    passed = sum(item['passed'] for item in rows)
    return {'inventory': list(WHITE_GATES),
            'counts': {'total': len(rows), 'passed': passed, 'failed': len(rows) - passed},
            'results': rows}


def request_check(request):
    closed(request, ('schema', 'phase', 'inputs', 'sources', 'design_acceptance',
                     'qualification', 'custody', 'runtime', 'admission', 'output'))
    equal(request['phase'], 'fixed_saved_application', 'PHASE', 'actual phase before body decoding')
    equal(request['schema'], 'ri125-white-request-v1', 'SCHEMA', 'white request schema')
    closed(request['inputs'], INPUT_ROLES, 'INPUT')
    closed(request['sources'], SOURCE_ROLES, 'SOURCE')
    closed(request['runtime'], RUNTIME_ROLES, 'SOURCE')
    for name in INPUT_ROLES:
        file_ref(request['inputs'][name])
        equal(request['inputs'][name]['pin'], FIXED[name], 'INPUT', 'fixed historical pin ' + name)
    for name in SOURCE_ROLES:
        file_ref(request['sources'][name])
    equal(request['sources']['design']['pin'], DESIGN, 'SOURCE', 'accepted RI123 design')
    for name in ('design_acceptance', 'qualification', 'custody', 'admission'):
        file_ref(request[name])
    equal(request['design_acceptance']['pin'], DESIGN_ACCEPTANCE, 'SOURCE', 'RI123 root acceptance')
    for name in RUNTIME_ROLES:
        file_ref(request['runtime'][name])
    equal(str(Path(__file__).resolve()), request['sources']['primary']['path'], 'SOURCE', 'loaded primary path')
    equal(str(Path(W.__file__).resolve()), request['sources']['white_kernel']['path'], 'SOURCE', 'loaded kernel path')
    output = literal_path(request['output'])
    need(output.parent.is_dir() and not os.path.lexists(output), 'OUTPUT', 'exclusive absent output')
    refs = [('input:' + name, request['inputs'][name]) for name in INPUT_ROLES]
    refs += [('source:' + name, request['sources'][name]) for name in SOURCE_ROLES]
    refs += [(name, request[name]) for name in ('design_acceptance', 'qualification', 'custody', 'admission')]
    refs += [('runtime:' + name, request['runtime'][name]) for name in RUNTIME_ROLES]
    need(len({r['path'] for _, r in refs}) == len(refs), 'INPUT', 'distinct required file paths')
    need(request['output'] not in {r['path'] for _, r in refs}, 'OUTPUT', 'output/input alias')
    return refs


def admission_check(card, request):
    # Root/caller must authenticate this exact card and its approval out of band.
    equal(card, {'schema': 'ri125-white-admission-v1', 'phase': 'fixed_saved_application',
        'status': 'ROOT_ADMITS_ONE_WHITE_RUN',
        'inputs': {k: v['pin'] for k, v in request['inputs'].items()},
        'sources': {k: v['pin'] for k, v in request['sources'].items()},
        'design_acceptance': request['design_acceptance']['pin'],
        'qualification': request['qualification']['pin'], 'custody': request['custody']['pin'],
        'runtime': {k: v['pin'] for k, v in request['runtime'].items()},
        'output': request['output'], 'limits': {'seconds': 180, 'sampled_rss_kib': 524288,
            'poll_ms': 25, 'max_gap_ms': 100, 'ps_timeout_ms': 50},
        'history_and_runtime_adjudicated_by_root': True, 'protected_validation': False,
        'physical_covariance_accepted': False, 'ret_paused': True}, 'ADMISSION', 'exact root-bound card')


def actual_result(request, gram, detail_pin, identities, shift, responses):
    return {'schema': 'ri125-white-coupling-v1', 'phase': 'fixed_saved_application',
        'status': ('enclosure_and_usefulness_passed' if all(x['usefulness_state'] == 'usefulness_passed'
                   for x in responses) else 'enclosure_valid_accuracy_failed'),
        'method': {'model': 'shared_raw_white_unit_response',
            'dimensions': {'r': 8, 'N': N, 'L': L, 'T': T, 'M': 16384, 'd': STRIDE,
                           'raw_samples': 131072, 'fs': 4096},
            'rows': ROWS, 'n_order': [7, 6], 'crop': 'first_T', 'integer_bit_limit': W.BITS,
            'precision_limit': W.scalar(W.F(1, 10**12)), 'centering': 'divisor_n_shared_samples'},
        'provenance': {'sources': {k: v['pin'] for k, v in request['sources'].items()},
            'inputs': [{'role': k, 'pin': request['inputs'][k]['pin']} for k in INPUT_ROLES],
            'acceptance': {'design': request['design_acceptance']['pin'],
                'qualification': request['qualification']['pin'], 'custody': request['custody']['pin'],
                'dependencies': [{'role': k, 'pin': request['inputs'][k]['pin']}
                    for k in ('ri73_reconciliation', 'ri73_final_review', 'ri73_audit_freeze')]
                    + [{'role': 'one_run_admission', 'pin': request['admission']['pin']}]},
            'runtime': {k: v['pin'] for k, v in request['runtime'].items()}},
        'operator': {'capture': request['inputs']['capture']['pin'],
            'ri73_result': request['inputs']['ri73_result']['pin'], 'ri73_gram_detail': detail_pin,
            'shape': [8, T], 'row_identities': identities, 'gram': gram,
            'inherited_gate_inventory': list(RI73_GATES), 'inherited_gates_all_passed': True},
        'shift': shift, 'white_responses': responses, 'checks': checks(responses),
        'limitations': list(LIMITATIONS)}


def write_exclusive(path, result):
    p = literal_path(path)
    before = state(p.parent.lstat())
    need(p.parent.is_dir() and not os.path.lexists(p), 'OUTPUT', 'output absent before exclusive open')
    fd = os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    h, size = hashlib.sha256(), 0
    with os.fdopen(fd, 'wb') as stream:
        for block in json_chunks(result):
            need(stream.write(block) == len(block), 'OUTPUT', 'complete output write')
            h.update(block)
            size += len(block)
        stream.flush()
        os.fsync(stream.fileno())
        final = state(os.fstat(stream.fileno()))
    need(state(p.lstat()) == final, 'CUSTODY', 'output descriptor/path binding')
    parent = p.parent.lstat()
    need((parent.st_dev, parent.st_ino) == before[:2], 'CUSTODY', 'output parent identity')
    result_pin = {'bytes': size, 'sha256': h.hexdigest()}
    read_bound({'path': path, 'pin': result_pin}, before=final)
    return result_pin


def run_white(request_body, expected_request_pin):
    """One caller-admitted attempt. Returns success or refusal plus all postchecks.

    On a later failure an exclusively created output remains unaccepted evidence;
    it is neither removed nor overwritten. Caller must reject success artifacts
    when this envelope is refused, incomplete or fails its own final custody.
    """
    ledger, first, result, output_pin = Ledger(), None, None, None
    try:
        pin(expected_request_pin)
        equal(identity(request_body), expected_request_pin, 'INPUT', 'externally frozen request bytes')
        request = parse(request_body)
        references = request_check(request)
        for role, record in references:
            ledger.register(role, record)
        ledger.read_all()
        body, _ = read_bound(request['admission'], keep=True)
        admission_check(parse(body), request)
        del body
        # Every whole source/input body pin was checked before scientific decode.
        body, _ = read_bound(request['inputs']['ri73_result'], keep=True)
        report = parse(body)
        gram, detail_pin, reconstruction = ri73_operand(report)
        del body, report
        identities, shift, responses = assemble_white(request['inputs']['capture'], gram, reconstruction)
        del reconstruction
        result = actual_result(request, gram, detail_pin, identities, shift, responses)
        output_pin = write_exclusive(request['output'], result)
        ledger.register('output', {'path': request['output'], 'pin': output_pin})
        _, ledger.entries[-1][2] = read_bound(ledger.entries[-1][1])
    except Exception as exc:
        first = exc
    return finish_attempt(first, result, output_pin, ledger.finish())


def finish_attempt(first, result, output_pin, postchecks):
    """Shared actual tail; pure record logic is separately controllable."""
    if first is None and not all(row['unchanged'] for row in postchecks):
        first = W.ApplicationError('CUSTODY', 'one or more final source/input postchecks failed')
    if first is not None:
        refusal = {'schema': 'ri125-application-refusal-v1', 'status': 'REFUSED',
            'phase': 'fixed_saved_application', 'stage': 'white',
            'code': first.code if isinstance(first, W.ApplicationError) else 'FAILURE',
            'message': (type(first).__name__ + ': ' + str(first))[:1024],
            'scientific_disposition_emitted': False, 'postchecks': postchecks}
        return {'result': None, 'output_pin': output_pin, 'refusal': refusal, 'postchecks': postchecks}
    return {'result': result, 'output_pin': output_pin, 'refusal': None, 'postchecks': postchecks}


def fabricated_white(capture, gram, *, case_id, context):
    """Separate fabricated-only assembly. Never calls request or actual entry."""
    equal(context, 'RI125_FABRICATED_ONLY_NOT_HISTORICAL', 'PHASE', 'fabricated context')
    need(type(case_id) is str and case_id in ('W09_production_boundary_sparse',
         'J01_four_rows_exact', 'J02_precision_inconclusive'), 'DOMAIN', 'fixed fabricated assembly case')
    W.inherited_gram(gram, 8)
    identities, shift, responses = assemble_white(capture, gram, None, fabricated=True)
    return {'schema': 'ri125-fabricated-white-assembly-v1', 'phase': 'fabricated_qualification',
            'case_id': case_id, 'context': context, 'capture': capture['pin'],
            'gram': gram, 'row_identities': identities, 'shift': shift,
            'white_responses': responses, 'historical_acceptance': None,
            'physical_claim': False}
