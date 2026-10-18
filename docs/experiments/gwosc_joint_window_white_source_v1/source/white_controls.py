"""RI125 PRIMARY white controls, source only; never an independent validator.

No import-time I/O or automatic execution. A future qualified caller supplies a
new absent external directory. Every file here is a conspicuous fabricated
control artifact. No actual result/capture/PSD is opened or admitted. Metadata
guard candidates deliberately stop before any scientific historical detail.
"""
from pathlib import Path
import copy
import os
import white_path as P

W = P.W
CONTEXT = 'RI125_FABRICATED_ONLY_NOT_HISTORICAL'


def simple_gram():
    return W.encode({'G': [[W.F(2)]], 'H': [[W.F(0)]], 'delta': W.F(0),
        'inverse': [[W.F(1, 2)]], 'gamma': W.F(1, 2), 'rho': W.F(0)})


def structural_mutation():
    # Exactly WK38: earlier checks pass, final structural trace intersection fails.
    shift = W.encode({'orientation': 'earlier_tail_times_later_head_transpose',
        'center': [[W.F(3)]], 'error': [[W.F(0)]], 'direct': [[(W.F(3), W.F(3))]],
        'midpoint_polarization': [[W.F(3)]], 'trace_center': W.F(3), 'trace_error': W.F(0)})
    return W.derive_response(simple_gram(), shift, n=2)


def rejected_header_scaffold():
    """Metadata-only malformed candidate. Cannot pass reconstruction/Gram checks.

    Never serialized as a historical body or passed through run_white. The
    future qualifier mutates exactly one header/gate and verifies that earlier
    first refusal, so the deliberately empty reconstruction is never decoded.
    """
    return {'schema_version': 'ri73-unit-white-operator-covariance-v1',
        'mode': 'fixed_operator_covariance', 'status': 'fixed_operator_covariance_passed',
        'full_integration_qualified': True, 'source_identity': dict(P.FIXED['ri73_source']),
        'dependencies': {}, 'runtime': {}, 'inherited_arithmetic_contract': {},
        'resource_contract': {}, 'model': {'kind': 'known_synthetic_unit_white',
            'mean': 'zero', 'covariance': 'I_T', 'input_dimension': P.T, 'output_dimension': 8},
        'dimensions': {'N': P.N, 'L': P.L, 'T': P.T}, 'rows': list(P.ROWS),
        'sample_spacing': W.scalar(W.F(1, 4096)), 'gate_inventory': list(P.RI73_GATES),
        'gate_counts': {'total': 92, 'passed': 92, 'failed': 0},
        'gates': [{'id': x, 'passed': True, 'detail': {}} for x in P.RI73_GATES],
        'deterministic_fixture_admission_passed': True, 'sampling_performed': False,
        'admitted_coefficient_design_requested': True, 'reconstructed_rows_admitted': True,
        'exact_scalar_encoding': 'MALFORMED_CONTROL_ONLY', 'scope': {'context': CONTEXT}}


def metadata_request_scaffold(directory):
    """Unadmitted metadata shape, no admission artifact and no actual input read."""
    def reference(role, value=None):
        return {'path': str(directory / ('unused-' + role)),
                'pin': dict(value or {'bytes': 1, 'sha256': '0' * 64})}
    request = {'schema': 'ri125-white-request-v1', 'phase': 'fixed_saved_application',
        'inputs': {name: reference(name, P.FIXED[name]) for name in P.INPUT_ROLES},
        'sources': {name: reference(name, P.DESIGN if name == 'design' else None)
                    for name in P.SOURCE_ROLES},
        'design_acceptance': reference('design-acceptance', P.DESIGN_ACCEPTANCE),
        'qualification': reference('qualification'), 'custody': reference('custody'),
        'runtime': {name: reference(name) for name in P.RUNTIME_ROLES},
        'admission': reference('admission'), 'output': str(directory / 'unused-output.json')}
    request['sources']['primary']['path'] = str(Path(P.__file__).resolve())
    request['sources']['white_kernel']['path'] = str(Path(W.__file__).resolve())
    return request


def row_record(label):
    zero = [['0', '1'], ['0', '1']]
    return {'row': label, 'short': [copy.deepcopy(zero) for _ in range(P.N)],
            'long': [copy.deepcopy(zero) for _ in range(P.T)]}


def capture_bytes(rows, *, schema='ri125-fabricated-capture-v1'):
    return P.serial({'dimensions': {'N': P.N, 'L': P.L, 'T': P.T},
        'row_order': list(P.ROWS), 'rows': rows, 'schema': schema}, compact=True)


def controls(directory):
    """Construct future isolated calls in literal order; do not call them here."""
    tasks = []
    def case(name, code, message, action):
        tasks.append((name, code, message, action))
    def file(name, body):
        p = directory / (name + '.fabricated')
        with p.open('xb') as stream:
            W.need(stream.write(body) == len(body), 'OUTPUT', 'complete fixture write')
        return {'path': str(p), 'pin': P.identity(body)}
    def request_change(action):
        request = metadata_request_scaffold(directory)
        action(request)
        return P.request_check(request)
    def header_change(action):
        value = rejected_header_scaffold()
        action(value)
        return P.ri73_operand(value)
    def capture_call(name, transform, *, complete=False):
        rows = [row_record(x) for x in (P.ROWS if complete else [0])]
        body = transform(rows)
        record = file(name, body)
        return list(P.capture_rows(record, fabricated=True))
    case('WK38', 'STRUCTURAL', 'trace structural interval intersection', structural_mutation)
    case('WC01', 'PHASE', 'actual phase before body decoding',
         lambda: request_change(lambda x: x.update(phase='fabricated_qualification')))
    case('WC02', 'SCHEMA', 'closed object keys', lambda: P.request_check({}))
    case('WC03', 'INPUT', 'externally frozen request bytes',
         lambda: P.run_white(b'{}', {'bytes': 3, 'sha256': '0' * 64}))
    # WC03 tests the returned refusal envelope, rather than an exception.
    case('WC04', 'INPUT', 'fixed historical pin capture',
         lambda: request_change(lambda x: x['inputs']['capture']['pin'].update(sha256='0' * 64)))
    case('WC05', 'SOURCE', 'closed object keys',
         lambda: request_change(lambda x: x['sources'].pop('validator')))
    case('WC06', 'SOURCE', 'loaded primary path',
         lambda: request_change(lambda x: x['sources']['primary'].update(path=str(directory / 'not-primary.py'))))
    case('WC07', 'SOURCE', 'loaded kernel path',
         lambda: request_change(lambda x: x['sources']['white_kernel'].update(path=str(directory / 'not-kernel.py'))))
    case('WC08', 'ADMISSION', 'exact root-bound card',
         lambda: P.admission_check({}, metadata_request_scaffold(directory)))
    case('WC09', 'INPUT', 'positive bounded pin length',
         lambda: P.pin({'bytes': True, 'sha256': '0' * 64}))
    case('WC10', 'INPUT', 'lowercase sha256',
         lambda: P.pin({'bytes': 1, 'sha256': 'A' * 64}))
    case('WC11', 'INPUT', 'literal absolute nonsymlink path', lambda: P.literal_path('relative'))
    case('WC12', 'SCHEMA', 'duplicate JSON key', lambda: P.parse(b'{"v":1,"v":2}'))
    case('WC13', 'EXACT', 'decimal or nonfinite JSON token', lambda: P.parse(b'{"v":0.5}'))
    case('WC14', 'EXACT', 'decimal or nonfinite JSON token', lambda: P.parse(b'{"v":NaN}'))
    case('WC15', 'SCHEMA', 'invalid bounded JSON', lambda: P.parse(b'{'))
    case('WC16', 'RESOURCE', 'JSON integer text ceiling',
         lambda: P.parse(b'{"v":' + b'9' * 65538 + b'}'))
    def wrong_file_pin():
        record = file('WC17', b'a')
        record['pin'] = P.identity(b'b')
        return P.read_bound(record)
    case('WC17', 'INPUT', 'whole body pin', wrong_file_pin)
    def changed_state():
        record = file('WC18', b'a')
        before = P.state(Path(record['path']).lstat())
        Path(record['path']).write_bytes(b'bb')
        return P.read_bound(record, before=before)
    case('WC18', 'CUSTODY', 'path state changed', changed_state)
    def symlink():
        record = file('WC19-seed', b'a')
        path = directory / 'WC19-link.fabricated'
        path.symlink_to(record['path'])
        return P.read_bound({'path': str(path), 'pin': record['pin']})
    case('WC19', 'INPUT', 'literal absolute nonsymlink path', symlink)
    def hardlink():
        record = file('WC20-seed', b'a')
        path = directory / 'WC20-link.fabricated'
        os.link(record['path'], path)
        return P.read_bound({'path': str(path), 'pin': record['pin']})
    case('WC20', 'INPUT', 'regular single-link source or input', hardlink)
    case('WC21', 'RI73', 'full inherited header mode',
         lambda: header_change(lambda x: x.update(mode='fixtures_only')))
    case('WC22', 'RI73', 'full inherited header source_identity',
         lambda: header_change(lambda x: x.update(source_identity={'bytes': 1, 'sha256': '0' * 64})))
    case('WC23', 'RI73', 'full inherited header gate_inventory',
         lambda: header_change(lambda x: x['gate_inventory'].reverse()))
    case('WC24', 'RI73', 'full inherited header gate_counts',
         lambda: header_change(lambda x: x['gate_counts'].update(passed=91)))
    case('WC25', 'SHAPE', 'exact list length', lambda: header_change(lambda x: x['gates'].pop()))
    case('WC26', 'RI73', 'literal 92-gate order',
         lambda: header_change(lambda x: x['gates'][0].update(id='fixture:wrong')))
    # Every historical gate bit is individually required, in the frozen order.
    for index, name in enumerate(P.RI73_GATES):
        case('WG%02d' % (index + 1), 'RI73', 'all inherited gates passed with details',
             lambda index=index: header_change(lambda x: x['gates'][index].update(passed=False)))
    case('WC27', 'PHASE', 'actual capture forbidden in fabrication',
         lambda: list(P.capture_rows({'path': str(directory / 'never-opened'),
                                     'pin': dict(P.FIXED['capture'])}, fabricated=True)))
    case('WC28', 'ROW', 'literal capture header',
         lambda: capture_call('WC28', lambda rows: capture_bytes(rows).replace(b'"N":2769', b'"N":2768', 1)))
    case('WC29', 'ROW', 'fixed row order',
         lambda: capture_call('WC29', lambda rows: capture_bytes([{**rows[0], 'row': True}])))
    case('WC30', 'ROW', 'closed object keys',
         lambda: capture_call('WC30', lambda rows: capture_bytes([{**rows[0], 'extra': None}])))
    case('WC31', 'SHAPE', 'exact list length',
         lambda: capture_call('WC31', lambda rows: capture_bytes([{**rows[0], 'short': []}])))
    case('WC32', 'CANONICAL', 'compact row encoding',
         lambda: capture_call('WC32', lambda rows: capture_bytes(rows).replace(b'"row":0', b'"row": 0', 1)))
    case('WC33', 'SCHEMA', 'duplicate JSON key',
         lambda: capture_call('WC33', lambda rows: capture_bytes(rows).replace(b'"row":0', b'"row":0,"row":0', 1)))
    def invalid_interval(rows):
        rows[0]['long'][0] = [['1', '1'], ['0', '1']]
        return capture_bytes(rows)
    case('WC34', 'INTERVAL', 'ordered endpoints', lambda: capture_call('WC34', invalid_interval))
    def invalid_scalar(rows):
        rows[0]['long'][0][0] = ['00', '1']
        return capture_bytes(rows)
    case('WC35', 'EXACT', 'canonical signed hex', lambda: capture_call('WC35', invalid_scalar))
    case('WC36', 'ROW', 'row separator', lambda: capture_call('WC36', capture_bytes))
    case('WC37', 'ROW', 'capture footer and ninth-row exhaustion',
         lambda: capture_call('WC37', lambda rows: capture_bytes(rows + [row_record(0)]), complete=True))
    case('WC38', 'ROW', 'trailing capture bytes',
         lambda: capture_call('WC38', lambda rows: capture_bytes(rows) + b'\n', complete=True))
    case('WC39', 'ROW', 'capture footer and ninth-row exhaustion',
         lambda: capture_call('WC39', lambda rows: capture_bytes(rows, schema='ri125-fabricated-capture-v0'), complete=True))
    def row_cap():
        import io
        return P.RowReader(io.BytesIO(b'{"x":"' + b'x' * P.ROW_LIMIT)).row()
    case('WC40', 'RESOURCE', 'capture row byte ceiling', row_cap)
    case('WC41', 'BINDING', 'capture vector identity tied to accepted RI73 result',
         lambda: P.bind_row({'vectors': {'control': 1}, 'row_identity': {'a_row_sum_interval': []}},
                           {'vector_identities': [{'control': 2}], 'constant_row_sum_intervals': [[]]}, 0))
    case('WC42', 'BINDING', 'complete row sum tied to accepted RI73 result',
         lambda: P.bind_row({'vectors': {}, 'row_identity': {'a_row_sum_interval': [0]}},
                           {'vector_identities': [{}], 'constant_row_sum_intervals': [[1]]}, 0))
    def existing_output():
        record = file('WC43', b'preserve-me')
        return P.write_exclusive(record['path'], {'context': CONTEXT})
    case('WC43', 'OUTPUT', 'output absent before exclusive open', existing_output)
    case('WC44', 'RESOURCE', 'serialized byte ceiling',
         lambda: list(P.json_chunks({'oversize': 'x' * P.LIMIT})))
    case('WC45', 'PHASE', 'fabricated context',
         lambda: P.fabricated_white({}, {}, case_id='W09_production_boundary_sparse', context='actual'))
    case('WC46', 'DOMAIN', 'fixed fabricated assembly case',
         lambda: P.fabricated_white({}, {}, case_id='invented', context=CONTEXT))
    return tasks, file


def run_controls(directory):
    """Future PRIMARY-only control execution; no independent-result claim."""
    root = P.literal_path(directory)
    W.need(root.parent.is_dir() and not os.path.lexists(root), 'OUTPUT', 'new control directory')
    root.mkdir(mode=0o700)
    tasks, file = controls(root)
    results = []
    for name, code, message, action in tasks:
        observed_code, observed_message = None, None
        try:
            value = action()
            if name == 'WC03' and type(value) is dict and type(value.get('refusal')) is dict:
                observed_code = value['refusal']['code']
                # run_white preserves exception class and its code in the message.
                observed_message = value['refusal']['message'].split(': ', 2)[-1]
        except W.ApplicationError as exc:
            observed_code = exc.code
            observed_message = str(exc).split(': ', 1)[-1]
        except Exception as exc:
            observed_code = type(exc).__name__
            observed_message = str(exc)[:1024]
        results.append({'id': name, 'expected_code': code, 'expected_message': message,
                        'observed_code': observed_code, 'observed_message': observed_message,
                        'passed': observed_code == code and observed_message == message})
    # Three positive tail controls exercise the exact actual tail functions.
    a, b = file('WT01-a', b'a'), file('WT01-b', b'b')
    ledger = P.Ledger()
    ledger.register('first', a)
    ledger.register('second', b)
    ledger.read_all()
    Path(a['path']).write_bytes(b'changed')
    postchecks = ledger.finish()
    results.append({'id': 'WT01', 'passed': len(postchecks) == 2
                    and postchecks[0]['unchanged'] is False
                    and postchecks[1]['unchanged'] is True, 'postchecks': postchecks})
    refused = P.finish_attempt(W.ApplicationError('EXACT', 'first-error'), None, None, postchecks)
    results.append({'id': 'WT02', 'passed': refused['refusal']['code'] == 'EXACT'
                    and refused['result'] is None and refused['postchecks'] == postchecks,
                    'refusal': refused['refusal']})
    late = P.finish_attempt(None, {'context': CONTEXT}, None, postchecks)
    results.append({'id': 'WT03', 'passed': late['refusal']['code'] == 'CUSTODY'
                    and late['result'] is None and late['postchecks'] == postchecks,
                    'refusal': late['refusal']})
    return {'schema': 'ri125-primary-white-controls-v1', 'phase': 'fabricated_qualification',
            'context': CONTEXT, 'actual_scientific_input_opened': False,
            'independent_validator_run': False, 'controls': results,
            'counts': {'total': len(results), 'passed': sum(x['passed'] for x in results),
                       'failed': sum(not x['passed'] for x in results)},
            'status': 'all_declared_controls_passed' if all(x['passed'] for x in results)
                      else 'control_failure'}
