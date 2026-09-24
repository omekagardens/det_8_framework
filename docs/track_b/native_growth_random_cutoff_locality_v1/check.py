#!/usr/bin/env python3
"""RI-77: exact selected-core record-locality witness, not a new growth law.

Read-only byte-pinned RI-74 reconstructs the accepted canonical strict q5.
The only new size-six potential rows are three declared cores, all 64 marks.
No global size-six normalization, q6 or q7 probabilities, optimizer, larger
order inventory, downloads, subprocesses or file writes are performed here.
The posterior numerical example is explicitly synthetic rational algebra.
The 120-second alarm and checkpointed 512-MiB RSS bound complement the
external prospective sampled watchdog; neither is an allocator hard cap.
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
}
CORES = ((0, 1, 0, 0, 15, 15), (0, 1, 1, 0, 15, 15), (0, 1, 3, 7, 15, 31))
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
        print('RI77: '+stage, file=sys.stderr, flush=True)


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


def bits(mask):
    return tuple(v for v in range(mask.bit_length()) if mask & (1 << v))


@cache
def validate(order):
    require(isinstance(order, tuple) and len(order) <= 6
            and all(type(p) is int and 0 <= p < (1 << v)
                    and all(order[u] & p == order[u] for u in bits(p))
                    for v, p in enumerate(order)), 'invalid bounded natural transitive order')


@cache
def ideals(order):
    validate(order)
    return tuple(s for s in range(1 << len(order))
                 if all(order[v] & s == order[v] for v in bits(s)))


def check_mark(order, record):
    require(type(record) is int and 0 <= record < (1 << len(order)),
            'record outside complete marked domain')


def induced(order, keep):
    vertices = bits(keep)
    return tuple(sum(1 << i for i, u in enumerate(vertices) if order[v] & (1 << u))
                 for v in vertices)


def transport(mask, keep):
    return sum(1 << i for i, v in enumerate(bits(keep)) if mask & (1 << v))


def verify_transport(original, keep, moved):
    require(moved == sum(((original >> v) & 1) << i for i, v in enumerate(bits(keep))),
            'record or precursor transport corrupted')


def maxima_mask(order):
    pasts = 0
    for past in order:
        pasts |= past
    return ((1 << len(order))-1) ^ pasts


def rebuild_prefix():
    global PREFIX, DEPENDENCY_PATHS
    directory = Path(__file__).resolve().parent.parent
    paths = {
        'ri74_checker': directory/'native_growth_plancherel_graft_v1'/'check.py',
        'ri63_checker': directory/'native_growth_expected_defect_completion_v1'/'check.py',
        'ri63_certificate': directory/'native_growth_expected_defect_completion_v1'/'CERTIFICATE.json',
        'ri41_certificate': directory/'native_growth_height_normalization_v1'/'CERTIFICATE.json',
    }
    for key, path in paths.items():
        check_pin(path.read_bytes(), PINS[key])
    DEPENDENCY_PATHS = paths
    budget('accepted closure pinned; replaying canonical strict parent-five proof')
    helper = runpy.run_path(str(paths['ri74_checker']))
    PREFIX = helper['prefix_row']
    wrapped = getattr(PREFIX, '__wrapped__', None)
    require(wrapped is not None and hasattr(wrapped, '__globals__'),
            'cached prefix helper has no underlying function')
    require(wrapped.__globals__ is helper['rebuild_prefix'].__globals__,
            'prefix helper functions have inconsistent global state')
    report = helper['rebuild_prefix']()
    # runpy's returned mapping need not be the live function global dictionary.
    live = wrapped.__globals__
    require(live['HELPER'] is not None and len(live['Q5']) == 2961,
            'actual strict q5 helper state was not populated')
    require(report['problem_sha256'] == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
            and report['actual_probability_manifest_sha256'] == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
            and report['canonical_lex_stages'] == 69 and len(report['inherited_controls']) == 15,
            'accepted canonical strict prefix report mismatch')
    budget('accepted prefix replay complete; no new parent-six inventory')
    return report


@cache
def prefix_row(order, record):
    require(len(order) <= 5, 'future probability lookup forbidden')
    validate(order)
    check_mark(order, record)
    require(PREFIX is not None, 'accepted prefix not initialized')
    result = PREFIX(order, record)
    require(set(result) == set(ideals(order)) and all(isinstance(q, F) and q > 0 for q in result.values())
            and sum(result.values(), F(0)) == 1, 'held prefix row lost strict normalization')
    return result


def potential(order, record, part):
    require(order in CORES, 'six-core is outside frozen allowlist')
    check_mark(order, record)
    require(part in ideals(order) and part != 63, 'new potential requires a proper ideal')
    remaining = maxima_mask(order) & ~part
    require(remaining != 0, 'proper ideal has no omitted maximum')
    value, factors = F(1), []
    deletion = remaining
    while deletion:
        keep = 63 ^ deletion
        smaller = induced(order, keep)
        moved_part = transport(part, keep)
        read_record = record if moved_part == (1 << len(smaller))-1 else record & part
        moved_record = transport(read_record, keep)
        verify_transport(part, keep, moved_part)
        verify_transport(read_record, keep, moved_record)
        q = prefix_row(smaller, moved_record)[moved_part]
        exponent = 1 if deletion.bit_count() % 2 else -1
        value = value*q if exponent == 1 else value/q
        factors.append([deletion, smaller, moved_part, moved_record, exponent, str(q)])
        deletion = (deletion-1) & remaining
    require(value > 0, 'deletion potential ceased to be positive')
    return value, factors


def verify_potential_row(order, row):
    require(set(row) == set(ideals(order))-{63}
            and all(isinstance(v, F) and v > 0 for v in row.values()),
            'proper-potential row lost labeled ideal coverage or positivity')


def verify_sum(row, total):
    require(sum(row.values(), F(0)) == total, 'proper-potential row sum mismatch')


def verify_local_rows(order, rows):
    for part in ideals(order):
        if part == 63:
            continue
        values = {}
        for record in range(64):
            key = record & part
            require(key not in values or values[key] == rows[record][part],
                    'proper potential read a record outside its precursor')
            values[key] = rows[record][part]


def verify_top_independence(totals):
    require(all(totals[r] == totals[r & 15] for r in range(64)),
            'twin-top potential sum read a top record')


def verify_chain(totals):
    require(all(v == 1 for v in totals), 'unique-maximum control sum is not one')


def twin_identity(order, record, total, row):
    base = order[:4]
    q = prefix_row(base, record & 15)
    p = prefix_row(base+(15,), record & 31)
    v = p[31]
    first = sum((p[s]*p[s]/q[s] for s in ideals(base)), F(0))+2*v
    second = 1+sum(((q[s]-p[s])**2/q[s] for s in ideals(base)), F(0))
    require(first == second == total and all(row[s] == p[s]*p[s]/q[s] for s in ideals(base))
            and row[31] == row[47] == v, 'independent twin-top identity failed')
    return dict(quadratic_sum=str(first), one_plus_divergence=str(second), top_slot=str(v),
                q_p_manifest_sha256=digest([[s, str(q[s]), str(p[s])] for s in ideals(base)]))


def selected_checks():
    result, all_factors = [], []
    total_slots = 0
    for index, order in enumerate(CORES):
        budget('checking declared core '+str(index+1)+' across all 64 records')
        rows, totals, entries = {}, [], []
        for record in range(64):
            row, row_factors = {}, []
            for part in ideals(order):
                if part == 63:
                    continue
                value, factors = potential(order, record, part)
                row[part] = value
                row_factors.append([part, factors])
                all_factors.append([index, record, part, factors])
            verify_potential_row(order, row)
            total = sum(row.values(), F(0))
            verify_sum(row, total)
            rows[record] = row
            totals.append(total)
            entry = dict(record=record, total=str(total),
                         proper_potentials=[[s, str(v)] for s, v in sorted(row.items())],
                         deletion_factors_sha256=digest(row_factors))
            if index < 2:
                entry['independent_identity'] = twin_identity(order, record, total, row)
            entries.append(entry)
            total_slots += len(row)
        verify_local_rows(order, rows)
        if index < 2:
            verify_top_independence(totals)
        else:
            verify_chain(totals)
        pair = next(([a, b] for a in range(64) for b in range(a+1, 64) if totals[a] != totals[b]), None)
        difference = None if pair is None else dict(records=pair, values=[str(totals[r]) for r in pair],
                                                   second_minus_first=str(totals[pair[1]]-totals[pair[0]]),
                                                   changed_record_bits=bits(pair[0] ^ pair[1]),
                                                   empty_precursor=0)
        result.append(dict(order=order, proper_ideals=len(rows[0]), marked_rows=64,
                           distinct_sums=len(set(totals)), first_differing_pair=difference,
                           disposition=('record_variation_witness' if pair is not None else 'bounded_no_variation'),
                           row_manifest_sha256=digest(entries), rows=entries))
    require(len(CORES) == 3, 'frozen core count changed')
    return dict(cores=result, selected_search_rows=128, chain_control_rows=64,
                total_proper_slots=total_slots,
                deletion_factor_evaluations=sum(len(item[3]) for item in all_factors),
                deletion_factor_manifest_sha256=digest(all_factors),
                overall_disposition=('locality_counterexample' if any(x['first_differing_pair'] is not None
                                                                     for x in result[:2]) else 'bounded_no_witness'))


def verify_posterior(b, d, data):
    require(0 < b < 1 and 0 < d < 1, 'synthetic posterior inputs outside positive unit interval')
    denominator = F(1, 2)+F(1, 2)*b
    numerator = F(1, 4)*b*d
    require(data == dict(numerator=str(numerator), denominator=str(denominator),
                         conditional=str(numerator/denominator))
            and numerator/denominator == b*d/(2*(1+b)), 'synthetic posterior tail-weight identity failed')


def posterior_check():
    b, d = F(2, 3), F(1, 5)
    data = dict(numerator='1/30', denominator='5/6', conditional='1/25')
    verify_posterior(b, d, data)
    return dict(kind='synthetic rational posterior algebra; not evaluated q6 or q7',
                b=str(b), d=str(d), w6='1/2', s7='1/2', w7='1/4', s8='1/4', **data)


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


def controls(witness):
    result = []
    def test(name, function, reason):
        result.append(expect_rejection(name, function, reason))
    test('unauthorized_six_core', lambda: potential((0,)*6, 0, 0), 'six-core is outside frozen allowlist')
    test('larger_core', lambda: potential(CORES[0]+(63,), 0, 0), 'six-core is outside frozen allowlist')
    test('q6_lookup', lambda: prefix_row(CORES[0], 0), 'future probability lookup forbidden')
    test('mark_out_of_range', lambda: potential(CORES[0], 64, 0), 'record outside complete marked domain')
    test('full_precursor', lambda: potential(CORES[0], 0, 63), 'new potential requires a proper ideal')
    test('nonideal_precursor', lambda: potential(CORES[0], 0, 2), 'new potential requires a proper ideal')
    test('changed_dependency_pin', lambda: check_pin(b'changed', PINS['ri74_checker']), 'accepted dependency byte pin mismatch')
    test('corrupt_record_transport', lambda: verify_transport(17, 47, 0), 'record or precursor transport corrupted')
    core = witness['selected']['cores'][0]
    rows = {r['record']: {s: F(v) for s, v in r['proper_potentials']} for r in core['rows']}
    altered = dict(rows[0]); del altered[47]
    test('merged_twin_top_ideals', lambda: verify_potential_row(CORES[0], altered),
         'proper-potential row lost labeled ideal coverage or positivity')
    test('corrupt_potential_sum', lambda: verify_sum(rows[0], F(core['rows'][0]['total'])+1),
         'proper-potential row sum mismatch')
    test('corrupt_twin_identity', lambda: twin_identity(CORES[0], 0, F(core['rows'][0]['total'])+1, rows[0]),
         'independent twin-top identity failed')
    altered_rows = {r: dict(row) for r, row in rows.items()}; altered_rows[1][0] += 1
    test('outside_empty_precursor_record', lambda: verify_local_rows(CORES[0], altered_rows),
         'proper potential read a record outside its precursor')
    totals = [F(r['total']) for r in core['rows']]; totals[16] += 1
    test('top_record_leak', lambda: verify_top_independence(totals), 'twin-top potential sum read a top record')
    test('corrupt_chain_sum', lambda: verify_chain([F(1)]*63+[F(2)]), 'unique-maximum control sum is not one')
    bad = dict(numerator='1/15', denominator='5/6', conditional='2/25')
    test('wrong_R7_bridge_in_numerator', lambda: verify_posterior(F(2, 3), F(1, 5), bad),
         'synthetic posterior tail-weight identity failed')
    test('duplicate_json_key', lambda: load_json('{"x":0,"x":1}'), 'duplicate JSON object key')
    test('nonfinite_json', lambda: load_json('{"x":NaN}'), 'nonfinite JSON constant')
    altered = load_json(canonical(witness)); altered['schema'] = 'wrong'
    test('wrong_certificate_schema', lambda: verify_certificate(altered, witness), 'certificate schema mismatch')
    altered = load_json(canonical(witness)); altered['selected']['total_proper_slots'] += 1
    test('changed_certificate_coverage', lambda: verify_certificate(altered, witness), 'certificate finite witness mismatch')
    altered = load_json(canonical(witness)); altered['selected']['overall_disposition'] = 'forged_disposition'
    test('forged_certificate_disposition', lambda: verify_certificate(altered, witness), 'certificate finite witness mismatch')
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
        prefix = rebuild_prefix()
        selected = selected_checks()
        witness = dict(schema='ri77-selected-core-locality-v1', dependencies=PINS,
                       checker_sha256=sha256(source).hexdigest(),
                       finite_domain=dict(new_six_cores=CORES, all_marks_per_core=64,
                                          prefix_parent_maximum=5, global_M6_computed=False,
                                          q6_or_q7_probabilities_computed=False, optimizer_calls=0,
                                          inherited_terminal_six_catalogue_is_prefix_verification=True),
                       accepted_prefix=prefix, selected=selected, posterior=posterior_check())
        negative = controls(witness)
        for key, path in DEPENDENCY_PATHS.items():
            check_pin(path.read_bytes(), PINS[key])
        require(Path(__file__).read_bytes() == source, 'checker source changed during verification')
        budget('selected exact rows and intended-reason controls complete')
        if sys.argv[1:] == ['--witness']:
            print(canonical(witness))
        else:
            saved = load_json(Path(__file__).with_name('CERTIFICATE.json').read_bytes())
            verify_certificate(saved, witness)
            print('accepted_prefix='+canonical(prefix))
            print('coverage='+canonical({k: v for k, v in selected.items() if k != 'cores'}))
            print('core_results='+canonical([{k: v for k, v in item.items() if k != 'rows'} for item in selected['cores']]))
            print('posterior='+canonical(witness['posterior']))
            print('negative_controls='+canonical(negative))
            print('witness_sha256='+digest(witness))
            print('DONE: bounded selected-core locality adjudication; no q6/q7 probability table or adopted law')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
