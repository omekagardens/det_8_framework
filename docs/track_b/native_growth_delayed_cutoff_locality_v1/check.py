#!/usr/bin/env python3
"""RI-79: two-record exact coefficient corroboration for a delayed cutoff.

Only the held q4/q5 rows on A=(0,1,1,0), records 0 and 1, are evaluated;
the five-parent top mark is fixed to zero. RI-74 replays the byte-pinned
actual RI-63 strict prefix. RI-77 is read only as a pinned certificate.
K7 and a6 remain symbolic: no q6/q7 row, global M6, other core/record,
optimizer, larger inventory, subprocess, download or file write is used.
The sign result can be unresolved; no anticipated outcome is an assertion.
An internal 120-second alarm and explicit 512-MiB RSS checkpoints complement
the prospectively frozen external sampled watchdog, not an allocator cap.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from pathlib import Path
import json
import resource
import runpy
import signal
import sys
import time


PINS = {
    'ri74_checker': 'edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
    'ri77_certificate': 'b959c82edb9233b71647e7cf09534f607da10cb2f1cefeb6b86e2ed36eb297a0',
}
BASE = (0, 1, 1, 0)
TOP = BASE+(15,)
TWIN = BASE+(15, 15)
SYMBOLIC_TRIPLE = BASE+(15, 15, 15)
RECORDS = (0, 1)
MAX_SECONDS, MAX_BYTES = 120, 512*1024**2
START = None
PREFIX = None
DEPENDENCY_PATHS = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    require(START is None or time.monotonic()-START <= MAX_SECONDS,
            '120-second verification envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((peak if sys.platform == 'darwin' else peak*1024) <= MAX_BYTES,
            '512-MiB resident-memory envelope exceeded')
    if stage:
        print('RI79: '+stage, file=sys.stderr, flush=True)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON object key')
        result[key] = value
    return result


def load_json(text):
    def bad(value):
        raise RuntimeError('nonfinite JSON constant')
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=bad)


def check_pin(raw, expected):
    require(sha256(raw).hexdigest() == expected, 'accepted dependency byte pin mismatch')


def fraction(text):
    require(isinstance(text, str), 'noncanonical rational encoding')
    try:
        result = F(text)
    except (ValueError, ZeroDivisionError):
        raise RuntimeError('noncanonical rational encoding') from None
    require(str(result) == text, 'noncanonical rational encoding')
    return result


def bits(mask):
    return tuple(v for v in range(mask.bit_length()) if mask & (1 << v))


@cache
def ideals(order):
    require(order in (BASE, TOP), 'ideal enumeration outside declared held rows')
    return tuple(s for s in range(1 << len(order))
                 if all(order[v] & s == order[v] for v in bits(s)))


def check_domain(order, record):
    require(len(order) <= 5, 'future probability lookup forbidden')
    require(order in (BASE, TOP), 'held parent outside frozen allowlist')
    require(type(record) is int and 0 <= record < (1 << len(order)), 'record outside marked domain')
    require(order != TOP or not record & 16, 'five-parent top mark must remain zero')
    require(record in RECORDS, 'record outside frozen pair')


def verify_transport(base_record, full_record):
    require(type(base_record) is int and base_record in RECORDS
            and full_record == base_record and not full_record & 16,
            'held base-record transport or top-zero condition corrupted')


def verify_actual_prefix(report):
    require(report['problem_sha256'] == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
            and report['actual_probability_manifest_sha256'] == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
            and report['canonical_lex_stages'] == 69 and len(report['inherited_controls']) == 15,
            'accepted actual strict prefix identity mismatch')


def rebuild_prefix():
    global PREFIX, DEPENDENCY_PATHS
    directory = Path(__file__).resolve().parent.parent
    paths = {
        'ri74_checker': directory/'native_growth_plancherel_graft_v1'/'check.py',
        'ri63_checker': directory/'native_growth_expected_defect_completion_v1'/'check.py',
        'ri63_certificate': directory/'native_growth_expected_defect_completion_v1'/'CERTIFICATE.json',
        'ri41_certificate': directory/'native_growth_height_normalization_v1'/'CERTIFICATE.json',
        'ri77_certificate': directory/'native_growth_random_cutoff_locality_v1'/'CERTIFICATE.json',
    }
    for key, path in paths.items():
        check_pin(path.read_bytes(), PINS[key])
    DEPENDENCY_PATHS = paths
    retained = load_json(paths['ri77_certificate'].read_bytes())
    require(retained['schema'] == 'ri77-selected-core-locality-v1', 'accepted RI77 certificate schema mismatch')
    budget('accepted closure pinned; replaying unchanged actual canonical strict q5 proof')
    module = runpy.run_path(str(paths['ri74_checker']))
    PREFIX = module['prefix_row']
    wrapped = getattr(PREFIX, '__wrapped__', None)
    require(wrapped is not None and hasattr(wrapped, '__globals__'), 'cached prefix helper has no underlying function')
    require(wrapped.__globals__ is module['rebuild_prefix'].__globals__, 'prefix helper globals disagree')
    report = module['rebuild_prefix']()
    live = wrapped.__globals__
    require(live['HELPER'] is not None and len(live['Q5']) == 2961, 'actual strict q5 helper state not populated')
    verify_actual_prefix(report)
    require(retained['accepted_prefix'] == report, 'RI77 retained actual prefix disagrees')
    cores = [item for item in retained['selected']['cores'] if tuple(item['order']) == TWIN]
    require(len(cores) == 1, 'retained twin-top core missing or duplicated')
    pair = {item['record']: item for item in cores[0]['rows'] if item['record'] in RECORDS}
    require(set(pair) == set(RECORDS), 'retained RI77 record pair incomplete')
    budget('accepted prefix complete; evaluating only two held q4/q5 row pairs')
    return report, pair


def verify_row(order, row):
    require(set(row) == set(ideals(order)) and all(isinstance(q, F) and q > 0 for q in row.values())
            and sum(row.values(), F(0)) == 1, 'held row lost labeled ideals or strict normalization')


def held_row(order, record):
    check_domain(order, record)
    require(PREFIX is not None, 'accepted prefix not initialized')
    row = PREFIX(order, record)
    verify_row(order, row)
    return row


def verify_full_slot(top_row, v, full_precursor=31):
    require(full_precursor == 31 and v == top_row[31]
            and v == 1-sum((top_row[s] for s in ideals(BASE)), F(0)),
            'five-parent full slot confused with base-full precursor')


def verify_retained(record, U6, v, retained):
    require(retained['record'] == record and fraction(retained['total']) == U6
            and fraction(retained['independent_identity']['top_slot']) == v,
            'reconstructed row disagrees with retained RI77 witness')


def polynomial(U6, v, T3):
    return (F(3), -3*U6, 3*v, T3)


def verify_polynomial(coefficients, U6, v, T3):
    require(tuple(coefficients) == polynomial(U6, v, T3), 'symbolic triple-top multiplicity or coefficient corrupted')


def row_data(record, retained):
    verify_transport(record, record)
    q, p = held_row(BASE, record), held_row(TOP, record)
    v = p[31]
    verify_full_slot(p, v)
    terms = [(s, p[s]**2/q[s], p[s]**3/q[s]**2) for s in ideals(BASE)]
    U6 = sum((u for _, u, _ in terms), F(0))+2*v
    divergence = 1+sum(((q[s]-p[s])**2/q[s] for s in ideals(BASE)), F(0))
    require(U6 == divergence, 'independent twin-top square identity failed')
    T3 = sum((t for _, _, t in terms), F(0))
    verify_retained(record, U6, v, retained)
    coeff = polynomial(U6, v, T3)
    verify_polynomial(coeff, U6, v, T3)
    return dict(record=record, top_record=0,
                q4=[[s, str(q[s])] for s in ideals(BASE)],
                q5=[[s, str(p[s])] for s in ideals(TOP)],
                labeled_terms=[[s, str(u), str(t)] for s, u, t in terms],
                v=str(v), U6=str(U6), T3=str(T3),
                symbolic_U7_coefficients=[str(c) for c in coeff],
                retained_RI77_record=record)


def verify_selected_locality(rows):
    for field, full in (('q4', 15), ('q5', 31)):
        first, second = ({s: fraction(q) for s, q in row[field]} for row in rows)
        for part in first:
            if part != full and not part & 1:
                require(first[part] == second[part], 'held proper row reads changed record outside precursor')


def separation_data(rows):
    require([r['record'] for r in rows] == list(RECORDS), 'coefficient record ordering changed')
    U0, U1 = (fraction(r['U6']) for r in rows)
    v0, v1 = (fraction(r['v']) for r in rows)
    T0, T1 = (fraction(r['T3']) for r in rows)
    dU, dv, dT = U1-U0, v1-v0, T1-T0
    require(dU > 0, 'retained positive U6 difference changed')
    require(dv == 0, 'retained top-full difference is not zero')
    a_star = 1/(2*(1+max(U0, U1)))
    margin = 3*dU-a_star*a_star*dT if dT > 0 else 3*dU
    return dict(delta_U6=str(dU), delta_v=str(dv), delta_T3=str(dT), a_star=str(a_star),
                positive_delta_T3=dT > 0, certified_bracket_lower_bound=str(margin),
                disposition=('resolved_negative' if margin > 0 else 'unresolved_bound'),
                symbolic_difference='-a6*(3*delta_U6-a6^2*delta_T3)',
                scale_interval='0 < a6 <= a_star; a6 is not numerically selected',
                full_complement_scale='a7 is separate: b_r=1-a7*U7(r;a6)')


def verify_separation(claim, rows):
    require(claim == separation_data(rows), 'symbolic scale bound or sign disposition corrupted')


def verify_certificate(certificate, expected):
    require(isinstance(certificate, dict) and set(certificate) == set(expected)
            and certificate.get('schema') == expected['schema'], 'certificate schema mismatch')
    require(certificate['dependencies'] == PINS, 'certificate dependency identities changed')
    require(canonical(certificate) == canonical(expected), 'certificate finite witness mismatch')


def expect_rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name+': wrong rejection reason')
        return name
    raise RuntimeError(name+': malformed candidate accepted')


def controls(witness, retained):
    result = []
    def test(name, function, reason):
        result.append(expect_rejection(name, function, reason))
    test('future_q6_lookup', lambda: held_row(TWIN, 0), 'future probability lookup forbidden')
    test('symbolic_q7_lookup', lambda: held_row(SYMBOLIC_TRIPLE, 0), 'future probability lookup forbidden')
    test('other_parent', lambda: held_row((0, 1, 0, 0), 0), 'held parent outside frozen allowlist')
    test('other_base_record', lambda: held_row(BASE, 2), 'record outside frozen pair')
    test('record_out_of_range', lambda: held_row(BASE, 16), 'record outside marked domain')
    test('boolean_record', lambda: held_row(BASE, True), 'record outside marked domain')
    test('changed_top_record', lambda: held_row(TOP, 16), 'five-parent top mark must remain zero')
    test('corrupt_record_transport', lambda: verify_transport(1, 0), 'held base-record transport or top-zero condition corrupted')
    test('changed_dependency_pin', lambda: check_pin(b'changed', PINS['ri77_certificate']), 'accepted dependency byte pin mismatch')
    altered = dict(witness['accepted_prefix']); altered['actual_probability_manifest_sha256'] = '0'*64
    test('boundary_or_other_q5_substitution', lambda: verify_actual_prefix(altered), 'accepted actual strict prefix identity mismatch')
    p = held_row(TOP, 0)
    altered = dict(p); del altered[15]
    test('missing_labeled_base_ideal', lambda: verify_row(TOP, altered), 'held row lost labeled ideals or strict normalization')
    altered = dict(p); altered[31] = F(0)
    test('nonpositive_full_slot', lambda: verify_row(TOP, altered), 'held row lost labeled ideals or strict normalization')
    test('base_full_is_not_parent_full', lambda: verify_full_slot(p, p[15], 15),
         'five-parent full slot confused with base-full precursor')
    row = witness['rows'][0]
    U6, v, T3 = (fraction(row[k]) for k in ('U6', 'v', 'T3'))
    test('wrong_RI77_U6', lambda: verify_retained(0, U6+1, v, retained[0]),
         'reconstructed row disagrees with retained RI77 witness')
    wrong = list(polynomial(U6, v, T3)); wrong[1] = -2*U6
    test('missing_triple_top_multiplicity', lambda: verify_polynomial(wrong, U6, v, T3),
         'symbolic triple-top multiplicity or coefficient corrupted')
    wrong = list(polynomial(U6, v, T3)); wrong[3] += 1
    test('corrupt_cubic_coefficient', lambda: verify_polynomial(wrong, U6, v, T3),
         'symbolic triple-top multiplicity or coefficient corrupted')
    altered = load_json(canonical(witness['rows'])); altered[1]['q5'][0][1] = str(fraction(altered[1]['q5'][0][1])+1)
    test('empty_precursor_record_leak', lambda: verify_selected_locality(altered),
         'held proper row reads changed record outside precursor')
    altered = dict(witness['separation']); altered['a_star'] = str(2*fraction(altered['a_star']))
    test('invalid_scale_envelope', lambda: verify_separation(altered, witness['rows']), 'symbolic scale bound or sign disposition corrupted')
    altered = dict(witness['separation']); altered['disposition'] = 'forced_anticipated_outcome'
    test('forged_sign_disposition', lambda: verify_separation(altered, witness['rows']), 'symbolic scale bound or sign disposition corrupted')
    test('duplicate_json_key', lambda: load_json('{"x":0,"x":1}'), 'duplicate JSON object key')
    test('nonfinite_json', lambda: load_json('{"x":NaN}'), 'nonfinite JSON constant')
    test('noncanonical_fraction', lambda: fraction('2/2'), 'noncanonical rational encoding')
    altered = load_json(canonical(witness)); altered['schema'] = 'wrong'
    test('wrong_certificate_schema', lambda: verify_certificate(altered, witness), 'certificate schema mismatch')
    altered = load_json(canonical(witness)); altered['rows'][1]['T3'] = str(fraction(altered['rows'][1]['T3'])+1)
    test('changed_certificate_coefficient', lambda: verify_certificate(altered, witness), 'certificate finite witness mismatch')
    return result


def deadline(signum, frame):
    raise RuntimeError('120-second wall-time alarm expired')


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'unknown command arguments')
    START = time.monotonic()
    signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    source = Path(__file__).read_bytes()
    try:
        prefix, retained = rebuild_prefix()
        rows = [row_data(record, retained[record]) for record in RECORDS]
        verify_selected_locality(rows)
        separation = separation_data(rows)
        verify_separation(separation, rows)
        witness = dict(schema='ri79-delayed-cutoff-locality-v1', dependencies=PINS,
                       checker_sha256=sha256(source).hexdigest(), accepted_prefix=prefix,
                       finite_domain=dict(base_order=BASE, records=RECORDS, top_marks=0,
                                          held_parent_orders=(BASE, TOP), held_marked_rows=4,
                                          held_labeled_probability_slots=sum(len(row['q4'])+len(row['q5']) for row in rows),
                                          symbolic_K7=SYMBOLIC_TRIPLE,
                                          q6_or_q7_probabilities_computed=False, global_M6_computed=False,
                                          scale_selected=False, optimizer_calls=0),
                       rows=rows, separation=separation)
        negative = controls(witness, retained)
        for key, path in DEPENDENCY_PATHS.items():
            check_pin(path.read_bytes(), PINS[key])
        require(Path(__file__).read_bytes() == source, 'checker source changed during verification')
        budget('two-record exact coefficients and intended-reason controls complete')
        if sys.argv[1:] == ['--witness']:
            print(canonical(witness))
        else:
            saved = load_json(Path(__file__).with_name('CERTIFICATE.json').read_bytes())
            verify_certificate(saved, witness)
            print('accepted_prefix='+canonical(prefix))
            print('finite_domain='+canonical(witness['finite_domain']))
            print('coefficients='+canonical([{k: v for k, v in row.items() if k not in ('q4', 'q5', 'labeled_terms')} for row in rows]))
            print('separation='+canonical(separation))
            print('negative_controls='+canonical(negative))
            print('witness_sha256='+digest(witness))
            print('DONE: two-record symbolic scale-bound corroboration; no q6/q7 probabilities or adopted law')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
