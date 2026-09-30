"""Unexecuted PRIMARY WK01-WK37 calls. WK38 is in unchanged white_controls.

This module does not provide an independent implementation or actual evidence.
Every mutation starts with freshly generated fixed W01/W03 operands and its
ordinary primary Shift. No actual data or historical acceptance is constructed.
"""
from pathlib import Path
import os
import white_fixtures as F

P, W = F.P, F.W
EXPECTED = (
    ('WK01', 'SHAPE', 'strip rows list'),
    ('WK02', 'DOMAIN', 'fixed primitive domain'),
    ('WK03', 'DOMAIN', 'fixed primitive domain'),
    ('WK04', 'SCHEMA', 'closed object keys'),
    ('WK05', 'ROW', 'row order'),
    ('WK06', 'SHAPE', 'exact list length'),
    ('WK07', 'SHAPE', 'exact list length'),
    ('WK08', 'EXACT', 'hex string required'),
    ('WK09', 'EXACT', 'canonical signed hex'),
    ('WK10', 'EXACT', 'canonical signed hex'),
    ('WK11', 'EXACT', 'reduced positive denominator'),
    ('WK12', 'EXACT', 'reduced positive denominator'),
    ('WK13', 'RESOURCE', 'integer text ceiling'),
    ('WK14', 'RESOURCE', 'integer bit ceiling'),
    ('WK15', 'INTERVAL', 'ordered endpoints'),
    ('WK16', 'ORIENTATION', 'directed shift label'),
    ('WK17', 'SCHEMA', 'closed object keys'),
    ('WK18', 'SHAPE', 'fixed matrix size'),
    ('WK19', 'BOUND', 'nonnegative shift radius'),
    ('WK20', 'POLARIZATION', 'saved polarization'),
    ('WK21', 'DIRECT', 'saved direct enclosure intersection'),
    ('WK22', 'TRACE', 'complete shift trace'),
    ('WK23', 'DOMAIN', 'fixed window count'),
    ('WK24', 'SCHEMA', 'closed object keys'),
    ('WK25', 'GRAM', 'both inverse products'),
    ('WK26', 'GRAM', 'symmetric Gram/inverse and nonnegative bound'),
    ('WK27', 'GRAM', 'both inverse products'),
    ('WK28', 'GRAM', 'both inverse products'),
    ('WK29', 'GRAM', 'delta row-sum bound'),
    ('WK30', 'GRAM', 'gamma inverse row-sum bound'),
    ('WK31', 'GRAM', 'unchanged inherited rho gate'),
    ('WK32', 'GRAM', 'unchanged inherited rho gate'),
    ('WK33', 'BOUND', 'nonnegative error, positive lower bound'),
    ('WK34', 'BOUND', 'nonnegative error, positive lower bound'),
    ('WK35', 'ZERO_DIVISOR', 'division by zero'),
    ('WK36', 'RESOURCE', 'integer bit ceiling'),
    ('WK37', 'GRAM', 'nonpositive inherited Gram pivot'),
)


def call(control):
    W.need(type(control) is str and control in [x[0] for x in EXPECTED],
           'CONTROL', 'fixed WK01-WK37 control')
    operand = F.make_fixture('W03_oriented_two' if control == 'WK25' else 'W01_single_white_two')
    rows, gram = operand['strips'], operand['gram']
    if control == 'WK01':
        return W.derive_shift(tuple(rows), length=3, stride=2)
    if control == 'WK02':
        return W.derive_shift(rows, length=True, stride=2)
    if control == 'WK03':
        return W.derive_shift(rows * 3, length=3, stride=2)
    if control == 'WK04':
        rows[0]['extra'] = None
    elif control == 'WK05':
        rows[0]['row'] = True
    elif control == 'WK06':
        rows[0]['head'] = []
    elif control == 'WK07':
        rows[0]['head'][0][0] = True
    elif control in ('WK08', 'WK09', 'WK10', 'WK13', 'WK14'):
        value = {'WK08': True, 'WK09': '', 'WK10': '01'}.get(control)
        if control == 'WK13':
            value = '1' + '0' * 65537
        if control == 'WK14':
            value = '1' + '0' * 65536
        rows[0]['head'][0][0][0] = value
    elif control == 'WK11':
        rows[0]['head'][0][0][1] = '0'
    elif control == 'WK12':
        rows[0]['head'][0][0] = ['2', '2']
    elif control == 'WK15':
        rows[0]['head'][0] = [W.scalar(W.F(2)), W.scalar(W.F(1))]
    if control in [x[0] for x in EXPECTED[:15]]:
        return W.derive_shift(rows, length=3, stride=2)
    shift = W.derive_shift(rows, length=3, stride=2)
    if control == 'WK16':
        shift['orientation'] = 'head_times_tail_transpose'
    elif control == 'WK17':
        shift['extra'] = None
    elif control == 'WK18':
        shift['center'] = []
    elif control == 'WK19':
        shift['error'][0][0] = W.scalar(W.F(-1))
    elif control == 'WK20':
        shift['midpoint_polarization'][0][0] = W.scalar(W.F(0))
    elif control == 'WK21':
        shift['direct'][0][0] = F.box(3, 4)
    elif control == 'WK22':
        shift['trace_center'] = W.scalar(W.F(0))
    elif control == 'WK23':
        return W.derive_response(gram, shift, n=True)
    elif control == 'WK24':
        gram['H_G'] = gram.pop('H')
    elif control == 'WK25':
        gram['G'][0][1] = W.scalar(W.F(2))
    elif control == 'WK26':
        gram['H'][0][0] = W.scalar(W.F(-1))
    elif control == 'WK27':
        gram['inverse'][0][0] = W.scalar(W.F(1))
    elif control == 'WK28':
        gram['G'][0][0] = W.scalar(W.F(0))
    elif control == 'WK29':
        gram['delta'] = W.scalar(W.F(1))
    elif control == 'WK30':
        gram['gamma'] = W.scalar(W.F(1))
    elif control == 'WK31':
        gram['rho'] = W.scalar(W.F(1, 10**12))
    elif control == 'WK32':
        gram['H'] = [[W.scalar(W.F(4, 10**12))]]
        gram['delta'] = W.scalar(W.F(4, 10**12))
        gram['rho'] = W.scalar(W.F(2, 10**12))
    elif control == 'WK33':
        return W.usefulness(W.F(0), W.F(0))
    elif control == 'WK34':
        return W.usefulness(W.F(-1), W.F(1))
    elif control == 'WK35':
        return W.div(W.F(1), W.F(0))
    elif control == 'WK36':
        return W.mul(W.F(2**262143), W.F(4))
    elif control == 'WK37':
        gram['G'] = [[W.scalar(W.F(-2))]]
        gram['inverse'] = [[W.scalar(W.F(-1, 2))]]
    return W.derive_response(gram, shift, n=2)


def run_controls(directory):
    root = P.literal_path(directory)
    W.need(root.parent.is_dir() and not os.path.lexists(root), 'OUTPUT', 'new kernel-control directory')
    root.mkdir(mode=0o700)
    results = []
    for name, expected_code, expected_message in EXPECTED:
        code = message = None
        try:
            call(name)
        except W.ApplicationError as exc:
            code, message = exc.code, str(exc).split(': ', 1)[-1]
        except Exception as exc:
            code, message = type(exc).__name__, str(exc)[:1024]
        results.append({'id': name, 'expected_code': expected_code,
            'expected_message': expected_message, 'observed_code': code,
            'observed_message': message, 'passed': code == expected_code and message == expected_message})
    return {'schema': 'ri125-primary-kernel-controls-v1', 'phase': 'fabricated_qualification',
        'context': F.CONTEXT, 'actual_scientific_input_opened': False,
        'independent_validator_run': False, 'controls': results,
        'counts': {'total': 37, 'passed': sum(x['passed'] for x in results),
                   'failed': sum(not x['passed'] for x in results)},
        'status': 'all_declared_controls_passed' if all(x['passed'] for x in results) else 'control_failure'}
