"""RI125 W01-W15 PRIMARY fabricated recipes and calls; unexecuted source.

No file I/O or fixture construction at import. These are fixed white-only
operands, not actual RI73 records. The independent validator receives only
canonical operand bytes and does not import this module or its expectations.
"""
import white_path as P

W, F = P.W, P.W.F
CONTEXT = 'RI125_FABRICATED_ONLY_NOT_HISTORICAL'
CASE_IDS = (
    'W01_single_white_two', 'W02_single_white_three', 'W03_oriented_two',
    'W04_negative_scale', 'W05_double_scale', 'W06_interval_mixed',
    'W07_interval_crosses_zero', 'W08_zero_shift', 'W09_production_boundary_sparse',
    'W10_usefulness_boundaries', 'W11_asymmetric_rational_radii',
    'W12_sparse_lifted_denominators', 'W13_full_response_below',
    'W14_full_response_equal', 'W15_full_response_above',
)
EXPECTED_IDS = ('fixed_operand_schema_and_recipe', 'complete_result_shape',
                'literal_case_anchor', 'full_directed_shift_consistency',
                'correct_gram_presence_and_inherited_gate',
                'correct_response_presence_and_new_gate')
BOUND_EXPECTED_IDS = ('fixed_bound_operand_recipe', 'complete_bound_result_shape',
                      'literal_predicate_results', 'fabricated_identity_only')


def need(ok, message):
    W.need(ok, 'FIXTURE', message)


def box(low, high=None):
    return W.interval(F(low), F(low if high is None else high))


def zeros(count):
    return [box(0) for _ in range(count)]


def diagonal(values):
    return [[v if i == j else F(0) for j in range(len(values))]
            for i, v in enumerate(values)]


def gram(g, inverse, *, h=None):
    size = len(g)
    if h is None:
        h = diagonal([F(0)] * size)
    delta = max(sum(row, F(0)) for row in h)
    gamma = max(sum((abs(x) for x in row), F(0)) for row in inverse)
    return W.encode({'G': g, 'H': h, 'delta': delta, 'inverse': inverse,
                     'gamma': gamma, 'rho': delta * gamma})


def scalar_gram():
    return gram([[F(2)]], [[F(1, 2)]])


def toy_strips(a):
    return [{'row': i, 'head': [box(row[0])], 'tail': [box(row[2])]}
            for i, row in enumerate(a)]


def complete_rows():
    return [{'row': label, 'short': zeros(P.N), 'long': zeros(P.T)} for label in P.ROWS]


def full_strips(rows):
    # Copy through the exact scalar/interval encoders, not aliased row slices.
    return [{'row': row['row'],
             'head': [W.interval(*W.uninterval(v)) for v in row['long'][:P.N]],
             'tail': [W.interval(*W.uninterval(v)) for v in row['long'][P.STRIDE:]]}
            for row in rows]


def make_fixture(case_id):
    need(type(case_id) is str and case_id in CASE_IDS, 'fixed W01-W15 case id')
    full, g, n = None, None, []
    domain = {'r': 1, 'T': 3, 'd': 2}
    if case_id == CASE_IDS[9]:
        return {'schema': 'ri125-fabricated-bound-operands-v1', 'context': CONTEXT,
                'case_id': case_id, 'pairs': [W.encode({'delta': q, 'ell': F(1)})
                    for q in (F(1, 10**12)-F(1, 10**24), F(1, 10**12),
                              F(1, 10**12)+F(1, 10**24), F(1))]}
    if case_id in CASE_IDS[:2]:
        rows = toy_strips([[1, 0, -1]])
        g, n = scalar_gram(), [2 if case_id == CASE_IDS[0] else 3]
    elif case_id in CASE_IDS[2:5]:
        domain['r'] = 2
        scale = -1 if case_id == CASE_IDS[3] else (2 if case_id == CASE_IDS[4] else 1)
        rows = toy_strips([[scale, 0, -scale], [0, scale, -scale]])
        s2 = F(scale * scale)
        g = gram([[2*s2, s2], [s2, 2*s2]],
                 [[F(2, 3)/s2, F(-1, 3)/s2], [F(-1, 3)/s2, F(2, 3)/s2]])
        n = [2]
    elif case_id == CASE_IDS[5]:
        rows = [{'row': 0, 'head': [box(1, 2)], 'tail': [box(-2, -1)]}]
    elif case_id == CASE_IDS[6]:
        rows = [{'row': 0, 'head': [box(-1, 1)], 'tail': [box(-2, 2)]}]
    elif case_id == CASE_IDS[7]:
        rows = [{'row': 0, 'head': [box(0)], 'tail': [box(0)]}]
    elif case_id == CASE_IDS[8]:
        domain = {'r': 8, 'T': P.T, 'd': P.STRIDE}
        full = complete_rows()
        for index, values in ((0, {0: 1, 8192: 2, 3000: -3}),
                              (1, {2768: 3, 10960: -1, 3001: -2})):
            for coordinate, value in values.items():
                full[index]['long'][coordinate] = box(value)
        for i in range(2, 8):
            full[i]['long'][3000 + 2*i] = box(1)
            full[i]['long'][3001 + 2*i] = box(-1)
        rows = full_strips(full)
        g = gram(diagonal([F(14), F(14)] + [F(2)] * 6),
                 diagonal([F(1, 14), F(1, 14)] + [F(1, 2)] * 6))
        n = [7, 6]
    elif case_id == CASE_IDS[10]:
        domain['r'] = 2
        rows = [{'row': 0, 'head': [box(F(1, 3), F(2, 3))],
                 'tail': [box(F(-3, 7), F(-1, 7))]},
                {'row': 1, 'head': [box(F(-2, 5), F(1, 5))],
                 'tail': [box(F(2, 11))]}]
    elif case_id == CASE_IDS[11]:
        domain = {'r': 8, 'T': P.T, 'd': P.STRIDE}
        rows = [{'row': label, 'head': zeros(P.N), 'tail': zeros(P.N)} for label in P.ROWS]
        entries = (
            (0, 'head', 0, F(1, 3), F(2, 3)),
            (0, 'head', 2768, F(-1, 5), F(-1, 5)),
            (0, 'tail', 0, F(-3, 7), F(-1, 7)),
            (0, 'tail', 2768, F(2, 11), F(3, 11)),
            (1, 'head', 0, F(-2, 5), F(1, 5)),
            (1, 'head', 2768, F(1, 13), F(2, 17)),
            (1, 'tail', 0, F(2, 11), F(2, 11)),
            (1, 'tail', 2768, F(-1, 19), F(1, 23)),
            (2, 'head', 1, F(1, 13), F(1, 13)),
            (2, 'tail', 1, F(-1, 17), F(1, 19)),
        )
        for ordinal, strip, coordinate, low, high in entries:
            rows[ordinal][strip][coordinate] = box(low, high)
    else:
        domain = {'r': 8, 'T': P.T, 'd': P.STRIDE}
        q = F(1, 10**12) + (CASE_IDS.index(case_id) - 13) * F(1, 10**24)
        h = 12*q / (7 + 6*q)
        full = complete_rows()
        for i in range(8):
            full[i]['long'][3000 + 2*i] = box(1)
            full[i]['long'][3001 + 2*i] = box(-1)
        rows = full_strips(full)
        g = gram(diagonal([F(2)] * 8), diagonal([F(1, 2)] * 8),
                 h=diagonal([h] * 8))
        n = [7]
    return {'schema': 'ri125-fabricated-white-operands-v1', 'context': CONTEXT,
            'case_id': case_id, 'domain': domain, 'strips': rows, 'gram': g,
            'n_order': n, 'full_rows': full}


def parse_fixture(body):
    value = P.parse(body)
    need(type(value) is dict and value.get('context') == CONTEXT, 'fabricated fixture context')
    case_id = value.get('case_id')
    need(type(case_id) is str and case_id in CASE_IDS, 'fixed W01-W15 case id')
    # Reject additional fields, alternate recipes and disguised actual operands.
    P.equal(value, make_fixture(case_id), 'FIXTURE', 'complete fixed white-only operand recipe')
    P.equal(P.serial(value), body, 'CANONICAL', 'canonical complete fabricated operand')
    return value


def primary_fixture_bytes(body):
    operand = parse_fixture(body)
    case_id = operand['case_id']
    if case_id == CASE_IDS[9]:
        results = []
        for pair in operand['pairs']:
            delta, ell = W.unscalar(pair['delta']), W.unscalar(pair['ell'])
            eps, state = W.usefulness(delta, ell)
            results.append({'delta': pair['delta'], 'ell': pair['ell'],
                            'eps': W.scalar(eps), 'usefulness_state': state})
        return {'schema': 'ri125-fabricated-bound-result-v1',
                'phase': 'fabricated_qualification', 'context': CONTEXT,
                'case_id': case_id, 'results': results,
                'historical_acceptance': None, 'physical_claim': False}
    domain = operand['domain']
    shift = W.derive_shift(operand['strips'], length=domain['T'], stride=domain['d'])
    responses = [W.derive_response(operand['gram'], shift, n=n) for n in operand['n_order']]
    return {'schema': 'ri125-fabricated-white-primitive-v1',
            'phase': 'fabricated_qualification', 'context': CONTEXT,
            'case_id': case_id, 'domain': domain, 'gram': operand['gram'],
            'shift': shift, 'responses': responses,
            'historical_acceptance': None, 'physical_claim': False}


def expected_checks(operand, result):
    """Literal discriminatory anchors supplement full independent reconstruction.

    This is a primary test oracle, not the separately authored validator. It
    never supplies expected objects to that validator or replaces field equality.
    """
    case_id = operand['case_id']
    need(case_id in CASE_IDS, 'case expectation domain')
    P.equal(operand, make_fixture(case_id), 'FIXTURE', 'complete fixed white-only operand recipe')
    if case_id == CASE_IDS[9]:
        P.closed(result, ('schema', 'phase', 'context', 'case_id', 'results',
                          'historical_acceptance', 'physical_claim'), 'FIXTURE')
        P.equal(result['schema'], 'ri125-fabricated-bound-result-v1', 'FIXTURE', 'bound result schema')
        W.sequence(result['results'], 4)
        expected_states = ['usefulness_passed', 'usefulness_passed', 'accuracy_failed', 'accuracy_failed']
        for pair, row, state in zip(operand['pairs'], result['results'], expected_states):
            P.equal(row, {**pair, 'eps': pair['delta'], 'usefulness_state': state},
                    'FIXTURE', 'literal W10 predicate pair/result')
    else:
        P.closed(result, ('schema', 'phase', 'context', 'case_id', 'domain', 'gram',
                          'shift', 'responses', 'historical_acceptance', 'physical_claim'), 'FIXTURE')
        P.equal(result['schema'], 'ri125-fabricated-white-primitive-v1', 'FIXTURE', 'white result schema')
        P.equal(result['domain'], operand['domain'], 'FIXTURE', 'fixture domain')
        P.equal(result['gram'], operand['gram'], 'FIXTURE', 'complete fixture Gram copy')
        shift = result['shift']
        W.keys(shift, W.SHIFT_KEYS)
        size = operand['domain']['r']
        k, e = W.matrix(shift['center'], size), W.matrix(shift['error'], size)
        P.equal(shift['center'], shift['midpoint_polarization'], 'FIXTURE', 'all directed midpoint fields')
        for i in range(size):
            for j in range(size):
                low, high = W.uninterval(shift['direct'][i][j])
                need(e[i][j] >= 0 and max(low, k[i][j]-e[i][j]) <= min(high, k[i][j]+e[i][j]),
                     'complete primary/direct intersection')
        P.equal(shift['trace_center'], W.scalar(sum(k[i][i] for i in range(size))), 'FIXTURE', 'whole center trace')
        P.equal(shift['trace_error'], W.scalar(sum(e[i][i] for i in range(size))), 'FIXTURE', 'whole error trace')
        P.equal([v['n'] for v in result['responses']], operand['n_order'], 'FIXTURE', 'complete response order')
        if operand['gram'] is not None:
            rho = W.unscalar(operand['gram']['rho'])
            need(F(0) <= rho <= F(1, 10**12), 'unchanged inherited gate')
        for response in result['responses']:
            eps = W.unscalar(response['eps'])
            state = 'usefulness_passed' if eps <= F(1, 10**12) else 'accuracy_failed'
            P.equal(response['usefulness_state'], state, 'FIXTURE', 'unchanged inclusive new gate')
            P.equal(response['enclosure_state'], 'valid_conditional_enclosure', 'FIXTURE', 'valid enclosure retained')
        if case_id in CASE_IDS[:2]:
            n = 2 if case_id == CASE_IDS[0] else 3
            trace = F(3, 2) if n == 2 else F(16, 9)
            P.equal(result['responses'][0]['trace_interval'], box(trace), 'FIXTURE', 'literal scalar response')
            P.equal(shift['center'], W.encode([[F(-1)]]), 'FIXTURE', 'signed scalar overlap')
        elif case_id in CASE_IDS[2:5]:
            scale = F(4) if case_id == CASE_IDS[4] else F(1)
            P.equal(shift['center'], W.encode([[-scale, F(0)], [-scale, F(0)]]), 'FIXTURE', 'directed orientation')
            P.equal(result['responses'][0]['center'],
                    W.encode([[F(3, 2)*scale, F(3, 4)*scale], [F(3, 4)*scale, scale]]),
                    'FIXTURE', 'literal asymmetric-row response')
        elif case_id == CASE_IDS[5]:
            P.equal(shift['center'], W.encode([[F(-9, 4)]]), 'FIXTURE', 'W06 midpoint')
            P.equal(shift['error'], W.encode([[F(7, 4)]]), 'FIXTURE', 'W06 three errors')
            P.equal(shift['direct'], [[box(-4, -1)]], 'FIXTURE', 'W06 direct retains narrower box')
        elif case_id == CASE_IDS[6]:
            P.equal(shift['center'], W.encode([[F(0)]]), 'FIXTURE', 'W07 zero center')
            P.equal(shift['error'], W.encode([[F(2)]]), 'FIXTURE', 'W07 cross-radius term')
            P.equal(shift['direct'], [[box(-2, 2)]], 'FIXTURE', 'W07 all endpoint products')
        elif case_id == CASE_IDS[7]:
            P.equal(shift['center'], W.encode([[F(0)]]), 'FIXTURE', 'W08 zero center')
            P.equal(shift['error'], W.encode([[F(0)]]), 'FIXTURE', 'W08 zero radius')
            P.equal(shift['direct'], [[box(0)]], 'FIXTURE', 'W08 zero direct')
        elif case_id == CASE_IDS[8]:
            P.equal(shift['center'], W.encode(diagonal([F(2), F(-3)] + [F(0)]*6)),
                    'FIXTURE', 'W09 both support boundary coordinates')
            for response in result['responses']:
                n = response['n']
                q = F(40*(n-1), n) + F(2*(n-1), n*n)
                P.equal(response['trace_interval'], box(q), 'FIXTURE', 'W09 full trace')
                P.equal(response['eps'], W.scalar(F(0)), 'FIXTURE', 'W09 zero exact error')
        elif case_id == CASE_IDS[10]:
            P.equal(shift['center'], W.encode([[F(-1, 7), F(1, 35)], [F(1, 11), F(-1, 55)]]),
                    'FIXTURE', 'W11 all unequal-denominator centers')
            P.equal(shift['error'], W.encode([[F(1, 7), F(1, 7)], [F(1, 33), F(3, 55)]]),
                    'FIXTURE', 'W11 nonzero asymmetric directed errors')
            P.equal(shift['direct'], [[box(F(-2, 7), F(-1, 21)), box(F(-3, 35), F(6, 35))],
                                     [box(F(2, 33), F(4, 33)), box(F(-4, 55), F(2, 55))]],
                    'FIXTURE', 'W11 independent endpoint anchors')
        elif case_id == CASE_IDS[11]:
            need(e[0][1] > 0 and e[1][0] > 0 and e[0][1] != e[1][0], 'W12 asymmetric nonzero errors')
            P.equal(shift['center'][2][2], W.scalar(F(-1, 4199)), 'FIXTURE', 'W12 lifted rational center')
            P.equal(shift['error'][2][2], W.scalar(F(18, 4199)), 'FIXTURE', 'W12 mixed radii')
            P.equal(shift['direct'][2][2], box(F(-1, 221), F(1, 247)), 'FIXTURE', 'W12 distinct endpoints')
            need(all(k[i][j] == e[i][j] == 0 for i in range(3, 8) for j in range(8)), 'W12 all zero tail rows')
        else:
            q = F(1, 10**12) + (CASE_IDS.index(case_id)-13)*F(1, 10**24)
            response = result['responses'][0]
            P.equal(response['eps'], W.scalar(q), 'FIXTURE', 'full response at prescribed boundary')
            need(W.unscalar(operand['gram']['rho']) < F(1, 10**12), 'old gate strictly passes')
            P.equal(response['center'], W.encode(diagonal([F(12, 7)]*8)), 'FIXTURE', 'complete boundary center')
            P.equal(shift['center'], W.encode(diagonal([F(0)]*8)), 'FIXTURE', 'zero boundary overlap')
            P.equal(shift['error'], W.encode(diagonal([F(0)]*8)), 'FIXTURE', 'zero boundary overlap error')
    for field, expected in (('phase', 'fabricated_qualification'), ('context', CONTEXT),
                            ('case_id', case_id), ('historical_acceptance', None), ('physical_claim', False)):
        P.equal(result[field], expected, 'FIXTURE', 'closed fabricated result identity ' + field)
    names = BOUND_EXPECTED_IDS if case_id == CASE_IDS[9] else EXPECTED_IDS
    return {'inventory': list(names),
            'counts': {'total': len(names), 'passed': len(names), 'failed': 0},
            'results': [{'id': name, 'passed': True} for name in names]}
