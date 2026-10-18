"""Unexecuted RI125 WHITE-ONLY qualification orchestration source.

No CLI, import-time I/O, subprocess, dynamic loader or admission creator. Root
must review all sources, capture/load the exact modules and admit the bounded
fabricated caller before this function is called. It never admits actual data.
"""
from pathlib import Path
import hashlib
import os
import stat
import types
import white_fixtures as F
import kernel_controls as K
import white_controls as C

P, W = F.P, F.W
SOURCE_ROLES = ('white_kernel', 'white_path', 'wrapper_controls', 'white_contract',
    'cases', 'kernel_refusals', 'fabricated_interfaces', 'white_refusals_text',
    'white_source_handoff', 'white_root_disposition', 'fixtures', 'kernel_controls',
    'orchestrator', 'stage_contract', 'control_expectations', 'validator', 'validator_controls')
CONTROL_IDS = ([f'WK{i:02d}' for i in range(1, 39)]
    + [f'WC{i:02d}' for i in range(1, 27)] + [f'WG{i:02d}' for i in range(1, 93)]
    + [f'WC{i:02d}' for i in range(27, 47)] + ['WT01', 'WT02', 'WT03'])
LIMITS = {'seconds': 180, 'sampled_rss_kib': 524288, 'poll_ms': 25,
          'max_gap_ms': 100, 'ps_timeout_ms': 50, 'file_bytes': 67108864,
          'capture_row_bytes': 8388608, 'completed_integer_bits': 262144}
FIXED_SOURCES = {
    'white_kernel': {'bytes': 12790, 'sha256': 'b5ce9dd68fe89b09a83bf6e9520f798894b85866f4c48a8a2dfe7449ea0a915f'},
    'white_path': {'bytes': 32343, 'sha256': '32a084c003ecb0bb290ea3f85c3b4bcde4061e5cf62aa7b0b9f3ead19470618b'},
    'wrapper_controls': {'bytes': 15910, 'sha256': '5055fb4aec16563680b2941d445da8273e99799d8fbf567fb7affe368f28e6a2'},
    'white_contract': {'bytes': 26409, 'sha256': 'abd8aeb6e74a46194bb38f9abc8c02e6be5bcff83318f8df1d27334fa317f2bd'},
    'cases': {'bytes': 12011, 'sha256': 'fbcabc6b49f5ffb741688293a0dab894e7dc3b2fd761c6f123fbdcacf2ee3eef'},
    'kernel_refusals': {'bytes': 4802, 'sha256': '85651a0ead42ec2edf18bfdd049efd49c20cb09fb25bc2be1e4ba561b9b9f208'},
    'fabricated_interfaces': {'bytes': 8758, 'sha256': '2e1db0380e13791448c957453a823c1d2d20874b8af80dc01ddb8c09b4927f4e'},
    'white_refusals_text': {'bytes': 7426, 'sha256': 'dbc6a3a400b22973379c632cea3924413e36bd441df9ff0e21c2f7507918f0bb'},
    'white_source_handoff': {'bytes': 5379, 'sha256': '4f5e547c359b8e1c3e4ee87f7b2351ce8259b705e7a3e033509b4072f3862468'},
    'white_root_disposition': {'bytes': 2174, 'sha256': '90c66df22b5ff16b578f38a4aba811638ec9f10f2b6089f898227691aa8219db'},
}


def need(ok, message):
    W.need(ok, 'QUALIFICATION', message)


def same(a, b, message):
    P.equal(a, b, 'QUALIFICATION', message)


def control_specification(body):
    value = P.parse(body)
    P.closed(value, ('schema', 'phase', 'order', 'refusals', 'tails'), 'QUALIFICATION')
    same(value['schema'], 'ri125-white-only-control-expectations-v1', 'control expectation schema')
    same(value['phase'], 'source_specification_only', 'control specification is not execution')
    same(value['order'], CONTROL_IDS, 'complete 179-control order')
    need(type(value['refusals']) is list and len(value['refusals']) == 176, '176 exact refusal expectations')
    for name, record in zip(CONTROL_IDS[:-3], value['refusals']):
        P.closed(record, ('id', 'code', 'message'), 'QUALIFICATION')
        same(record['id'], name, 'refusal specification id')
        need(type(record['code']) is str and record['code'] and type(record['message']) is str
             and record['message'], 'literal refusal code/message')
    same(value['tails'], ['WT01', 'WT02', 'WT03'], 'separate positive-tail inventory')
    return value


def inspect_tail(postchecks):
    need(type(postchecks) is list and len(postchecks) == 2, 'both independent tail attempts retained')
    for record in postchecks:
        P.closed(record, ('role', 'pin', 'unchanged', 'error'), 'QUALIFICATION')
    same(postchecks[0]['role'], 'first', 'tail first role')
    same(postchecks[1]['role'], 'second', 'tail second role')
    need(postchecks[0]['unchanged'] is False and postchecks[0]['pin'] is None
         and type(postchecks[0]['error']) is str and 0 < len(postchecks[0]['error']) <= 1024,
         'first tail failure retained')
    need(postchecks[1]['unchanged'] is True and postchecks[1]['error'] is None,
         'second tail check ran independently')
    P.pin(postchecks[1]['pin'])


def check_control_report(report, specification, *, independent):
    P.closed(report, ('schema', 'phase', 'context', 'actual_scientific_input_opened',
                     'independent_validator_run', 'controls', 'counts', 'status'), 'QUALIFICATION')
    schema = ('ri125-independent-white-controls-v1' if independent
              else 'ri125-primary-complete-white-controls-v1')
    same(report['schema'], schema, 'exact control report schema')
    same(report['phase'], 'fabricated_qualification', 'control phase')
    same(report['context'], F.CONTEXT, 'control context')
    same(report['actual_scientific_input_opened'], False, 'no actual input in controls')
    same(report['independent_validator_run'], independent, 'control implementation identity')
    same(report['status'], 'all_declared_controls_passed', 'all controls actually passed')
    same(report['counts'], {'total': 179, 'passed': 179, 'failed': 0}, 'complete control counts')
    need(type(report['controls']) is list and len(report['controls']) == 179, 'complete control records')
    same([row['id'] for row in report['controls']], CONTROL_IDS, 'exact control order')
    for expected, row in zip(specification['refusals'], report['controls'][:-3]):
        P.closed(row, ('id', 'expected_code', 'expected_message', 'observed_code',
                       'observed_message', 'passed'), 'QUALIFICATION')
        same(row, {'id': expected['id'], 'expected_code': expected['code'],
                   'expected_message': expected['message'], 'observed_code': expected['code'],
                   'observed_message': expected['message'], 'passed': True},
             'first refusal code AND normalized message ' + expected['id'])
    tail = report['controls'][-3:]
    P.closed(tail[0], ('id', 'passed', 'postchecks'), 'QUALIFICATION')
    need(tail[0]['passed'] is True, 'positive independent-tail control passed')
    inspect_tail(tail[0]['postchecks'])
    for row, code in zip(tail[1:], ('EXACT', 'CUSTODY')):
        P.closed(row, ('id', 'passed', 'refusal'), 'QUALIFICATION')
        need(row['passed'] is True, 'first error / late failure control passed')
        refusal = row['refusal']
        P.closed(refusal, ('schema', 'status', 'phase', 'stage', 'code', 'message',
                          'scientific_disposition_emitted', 'postchecks'), 'QUALIFICATION')
        for key, value in (('schema', 'ri125-application-refusal-v1'), ('status', 'REFUSED'),
                           ('phase', 'fixed_saved_application'), ('stage', 'white'),
                           ('code', code), ('scientific_disposition_emitted', False)):
            same(refusal[key], value, 'complete refused-tail semantics ' + key)
        need(type(refusal['message']) is str and 0 < len(refusal['message']) <= 1024,
             'retained bounded refusal diagnostic')
        expected_message = ('first-error' if code == 'EXACT'
                            else 'one or more final source/input postchecks failed')
        same(refusal['message'].split(': ', 2)[-1], expected_message,
             'tail preserves literal first/late error')
        inspect_tail(refusal['postchecks'])
        same(refusal['postchecks'], tail[0]['postchecks'], 'tail keeps exact attempted checks')


def combine_primary(kernel, wrapper):
    # Save the two entire original reports before making this normalized aggregate.
    same(kernel['schema'], 'ri125-primary-kernel-controls-v1', 'new primary kernel report')
    same(wrapper['schema'], 'ri125-primary-white-controls-v1', 'sealed primary wrapper report')
    same(kernel['counts'], {'total': 37, 'passed': 37, 'failed': 0}, 'all 37 new kernel calls')
    same(wrapper['counts'], {'total': 142, 'passed': 142, 'failed': 0}, 'all 142 sealed controls')
    for report in (kernel, wrapper):
        P.closed(report, ('schema', 'phase', 'context', 'actual_scientific_input_opened',
                         'independent_validator_run', 'controls', 'counts', 'status'), 'QUALIFICATION')
        same(report['phase'], 'fabricated_qualification', 'primary control phase')
        same(report['context'], F.CONTEXT, 'primary control context')
        same(report['status'], 'all_declared_controls_passed', 'all primary controls passed')
        same(report['actual_scientific_input_opened'], False, 'primary controls no actual data')
        same(report['independent_validator_run'], False, 'primary report is not independent')
    return {'schema': 'ri125-primary-complete-white-controls-v1',
        'phase': 'fabricated_qualification', 'context': F.CONTEXT,
        'actual_scientific_input_opened': False, 'independent_validator_run': False,
        'controls': kernel['controls'] + wrapper['controls'],
        'counts': {'total': 179, 'passed': 179, 'failed': 0},
        'status': 'all_declared_controls_passed'}


def tree_snapshot(directory):
    """Retain all owned control artifacts, including intentional bad links.

    Never follow symlinks. Deliberate two-link files are control evidence, not
    admitted scientific inputs. Private lstat states support same-attempt custody;
    the serialized inventory records complete content/link identities.
    """
    root = P.literal_path(str(directory))
    records, states = [], {}
    def visit(path, depth):
        need(depth <= 8 and len(records) < 1024, 'bounded control-tree inventory')
        before = path.lstat()
        relative = str(path.relative_to(root))
        states[relative] = list(P.state(before))
        if stat.S_ISDIR(before.st_mode):
            records.append({'name': relative, 'kind': 'directory', 'pin': None, 'target': None})
            with os.scandir(path) as scan:
                children = sorted([entry.name for entry in scan])
            for name in children:
                visit(path / name, depth + 1)
        elif stat.S_ISLNK(before.st_mode):
            target = os.readlink(path)
            need(type(target) is str and len(target) <= 4096, 'bounded retained symlink target')
            records.append({'name': relative, 'kind': 'symlink', 'pin': None, 'target': target})
        else:
            need(stat.S_ISREG(before.st_mode) and 0 <= before.st_size <= P.LIMIT,
                 'bounded regular control artifact')
            digest, size = hashlib.sha256(), 0
            with os.fdopen(os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW), 'rb') as stream:
                same(list(P.state(os.fstat(stream.fileno()))), states[relative], 'opened control artifact')
                while True:
                    block = stream.read(65536)
                    if not block:
                        break
                    size += len(block)
                    need(size <= P.LIMIT, 'control artifact byte bound')
                    digest.update(block)
                same(list(P.state(os.fstat(stream.fileno()))), states[relative], 'closed control artifact')
            records.append({'name': relative, 'kind': 'file',
                            'pin': {'bytes': size, 'sha256': digest.hexdigest()}, 'target': None})
        same(list(P.state(path.lstat())), states[relative], 'control artifact path stable')
    visit(root, 0)
    return {'schema': 'ri125-fabricated-control-tree-v1', 'records': records}, states


def write_body(directory, name, body, ledger, artifacts):
    need(type(name) is str and '/' not in name and name not in ('', '.', '..'), 'literal artifact basename')
    need(type(body) is bytes and 0 < len(body) <= P.LIMIT, 'bounded complete artifact')
    path = directory / name
    record = {'path': str(path), 'pin': P.identity(body)}
    # Register before attempting the exclusive open. A failed/partial write
    # remains a failed postcheck, and the final namespace inventory retains its
    # actual bytes (or records the inspection failure), never an accepted pin.
    ledger.register('artifact:' + name, record)
    entry = ledger.entries[-1]
    with os.fdopen(os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600), 'wb') as stream:
        need(stream.write(body) == len(body), 'complete exclusive artifact write')
        stream.flush()
        os.fsync(stream.fileno())
        before = P.state(os.fstat(stream.fileno()))
    P.read_bound(record, before=before)
    entry[2] = before
    artifact = {'name': name, 'pin': record['pin']}
    artifacts.append(artifact)
    return artifact


def retained_controls(root, name, runner, ledger, artifacts, trees):
    """Retain a control tree even if its runner fails before returning a report."""
    tree = {'name': name, 'record': None, 'snapshot': None, 'states': None}
    trees.append(tree)
    report, first = None, None
    try:
        report = runner(str(root / name))
    except Exception as exc:
        first = exc
    try:
        inventory, states = tree_snapshot(root / name)
        tree['snapshot'], tree['states'] = inventory, states
        tree['record'] = write_body(root, name.upper() + '_TREE.json',
                                    P.serial(inventory), ledger, artifacts)
    except Exception as exc:
        if first is None:
            first = exc
    if first is not None:
        raise first
    return report


def read_artifact(directory, record):
    body, _ = P.read_bound({'path': str(directory / record['name']), 'pin': record['pin']}, keep=True)
    return body


def sources_check(bindings, validator, validator_controls):
    P.closed(bindings, SOURCE_ROLES, 'SOURCE')
    for role in SOURCE_ROLES:
        P.file_ref(bindings[role])
    need(len({x['path'] for x in bindings.values()}) == len(SOURCE_ROLES), 'distinct complete source bindings')
    for role, pin in FIXED_SOURCES.items():
        same(bindings[role]['pin'], pin, 'unchanged accepted white source ' + role)
    modules = {'white_kernel': W, 'white_path': P, 'wrapper_controls': C,
               'fixtures': F, 'kernel_controls': K, 'validator': validator,
               'validator_controls': validator_controls}
    for role, module in modules.items():
        need(type(module) is types.ModuleType, 'root-loaded module interface')
        same(str(Path(module.__file__).resolve()), bindings[role]['path'], 'loaded module path ' + role)
    same(str(Path(__file__).resolve()), bindings['orchestrator']['path'], 'loaded orchestrator path')
    need(callable(validator.validate_fixture_bytes)
         and callable(validator.validate_fabricated_assembly)
         and callable(validator_controls.run_controls), 'complete separate validator interface')


def run_white_qualification(directory, source_bindings, validator, validator_controls, *, phase):
    """One future root-admitted white-only attempt, without retries or fallback."""
    ledger, artifacts, first, result, report_pin = P.Ledger(), [], None, None, None
    trees = []
    root = None
    root_created = False
    try:
        same(phase, 'fabricated_qualification', 'explicit fabricated-only phase')
        sources_check(source_bindings, validator, validator_controls)
        for role in SOURCE_ROLES:
            ledger.register('source:' + role, source_bindings[role])
        ledger.read_all()
        root = P.literal_path(directory)
        need(root.parent.is_dir() and not os.path.lexists(root), 'fresh absent white-only directory')
        need(not any(Path(x['path']).is_relative_to(root) for x in source_bindings.values()),
             'source files outside output namespace')
        root.mkdir(mode=0o700)
        root_created = True
        body, _ = P.read_bound(source_bindings['control_expectations'], keep=True)
        specification = control_specification(body)
        cases = []
        for ordinal, case_id in enumerate(F.CASE_IDS, 1):
            operand = F.make_fixture(case_id)
            body = P.serial(operand)
            saved_operand = write_body(root, f'W{ordinal:02d}-operand.json', body, ledger, artifacts)
            primary = F.primary_fixture_bytes(body)
            primary_checks = F.expected_checks(operand, primary)
            saved_primary = write_body(root, f'W{ordinal:02d}-primary.json', P.serial(primary), ledger, artifacts)
            # No primary result or expected dictionary reaches the validator.
            independent = validator.validate_fixture_bytes(body)
            independent_checks = F.expected_checks(operand, independent)
            saved_independent = write_body(root, f'W{ordinal:02d}-independent.json', P.serial(independent), ledger, artifacts)
            same(independent, primary, 'every typed fixture field ' + case_id)
            same(independent_checks, primary_checks, 'same literal expected checks ' + case_id)
            cases.append({'id': case_id, 'kind': 'bound_predicate_only' if ordinal == 10 else 'white_primitive',
                'operand': saved_operand, 'primary': saved_primary, 'independent': saved_independent,
                'full_fields_match': True, 'expected_checks': primary_checks})
            del operand, body, primary, independent
        # The full eight-row assembly is additionally exercised only for W09.
        operand = F.make_fixture('W09_production_boundary_sparse')
        capture = {'dimensions': {'N': P.N, 'L': P.L, 'T': P.T},
                   'row_order': list(P.ROWS), 'rows': operand['full_rows'],
                   'schema': 'ri125-fabricated-capture-v1'}
        saved_capture = write_body(root, 'W09-complete-capture.json', P.serial(capture, compact=True), ledger, artifacts)
        capture_ref = {'path': str(root / saved_capture['name']), 'pin': saved_capture['pin']}
        primary_assembly = P.fabricated_white(capture_ref, operand['gram'],
            case_id='W09_production_boundary_sparse', context=F.CONTEXT)
        saved_pa = write_body(root, 'W09-primary-assembly.json', P.serial(primary_assembly), ledger, artifacts)
        independent_assembly = validator.validate_fabricated_assembly(capture_ref, operand['gram'],
            'W09_production_boundary_sparse', F.CONTEXT)
        saved_ia = write_body(root, 'W09-independent-assembly.json', P.serial(independent_assembly), ledger, artifacts)
        same(primary_assembly, independent_assembly, 'every complete W09 assembly field')
        assembly = {'id': 'W09_production_boundary_sparse', 'capture': saved_capture,
                    'gram_pin': P.json_pin(operand['gram']), 'primary': saved_pa,
                    'independent': saved_ia, 'full_fields_match': True}
        del operand, capture, primary_assembly, independent_assembly
        kernel_report = retained_controls(root, 'primary-kernel-controls', K.run_controls,
                                           ledger, artifacts, trees)
        saved_k = write_body(root, 'PRIMARY_KERNEL_CONTROLS.json', P.serial(kernel_report), ledger, artifacts)
        wrapper_report = retained_controls(root, 'primary-wrapper-controls', C.run_controls,
                                            ledger, artifacts, trees)
        saved_w = write_body(root, 'PRIMARY_WRAPPER_CONTROLS.json', P.serial(wrapper_report), ledger, artifacts)
        primary_report = combine_primary(kernel_report, wrapper_report)
        saved_p = write_body(root, 'PRIMARY_ALL_CONTROLS.json', P.serial(primary_report), ledger, artifacts)
        independent_report = retained_controls(root, 'independent-controls', validator_controls.run_controls,
                                                ledger, artifacts, trees)
        saved_i = write_body(root, 'INDEPENDENT_ALL_CONTROLS.json', P.serial(independent_report), ledger, artifacts)
        check_control_report(primary_report, specification, independent=False)
        check_control_report(independent_report, specification, independent=True)
        # Fresh independent reconstruction from all saved operands. It is not a
        # replay of labels or comparison against primary expected dictionaries.
        fresh_cases = []
        for row in cases:
            body = read_artifact(root, row['operand'])
            fresh = validator.validate_fixture_bytes(body)
            saved_primary = P.parse(read_artifact(root, row['primary']))
            saved_independent = P.parse(read_artifact(root, row['independent']))
            same(fresh, saved_primary, 'fresh complete primary comparison ' + row['id'])
            same(fresh, saved_independent, 'fresh complete independent comparison ' + row['id'])
            checks = F.expected_checks(P.parse(body), fresh)
            same(checks, row['expected_checks'], 'fresh full literal expectations ' + row['id'])
            fresh_cases.append({'id': row['id'], 'fresh_result_pin': P.json_pin(fresh), 'all_fields_match': True})
            del body, fresh, saved_primary, saved_independent
        operand = P.parse(read_artifact(root, cases[8]['operand']))
        fresh = validator.validate_fabricated_assembly(capture_ref, operand['gram'],
            'W09_production_boundary_sparse', F.CONTEXT)
        same(fresh, P.parse(read_artifact(root, saved_pa)), 'fresh complete primary assembly')
        same(fresh, P.parse(read_artifact(root, saved_ia)), 'fresh complete independent assembly')
        fresh_assembly_pin = P.json_pin(fresh)
        # Saved controls are fully checked, without claiming another control run.
        check_control_report(P.parse(read_artifact(root, saved_p)), specification, independent=False)
        check_control_report(P.parse(read_artifact(root, saved_i)), specification, independent=True)
        comparison = {'schema': 'ri125-white-only-fresh-saved-comparison-v1',
            'phase': 'fabricated_qualification', 'cases': fresh_cases,
            'assembly': {'id': assembly['id'], 'fresh_result_pin': fresh_assembly_pin, 'all_fields_match': True},
            'saved_control_envelopes_fully_checked': True, 'controls_rerun_by_comparator': False,
            'actual_data_evaluated': False, 'full_application_qualified': False}
        saved_fresh = write_body(root, 'FRESH_SAVED_COMPARISON.json', P.serial(comparison), ledger, artifacts)
        result = {'schema': 'ri125-white-only-qualification-v1', 'phase': 'fabricated_qualification',
            'status': 'all_white_only_gates_passed', 'context': F.CONTEXT,
            'scope': {'white_case_ids': list(F.CASE_IDS), 'white_case_count': 15,
                'full_application_case_count': 32, 'full_application_qualified': False,
                'actual_data_admitted': False, 'periodic_mean_or_join_executed': False,
                'physical_claim': False},
            'limits': dict(LIMITS), 'source_bindings': source_bindings,
            'cases': cases, 'complete_capture_assembly': assembly,
            'controls': {'order': list(CONTROL_IDS), 'per_implementation': 179,
                'kernel_per_implementation': 38, 'wrapper_and_tail_per_implementation': 141,
                'primary_kernel': saved_k, 'primary_wrapper': saved_w,
                'primary_complete': saved_p, 'independent_complete': saved_i,
                'both_exact_inventories_and_first_refusals_passed': True,
                'trees': [{'name': x['name'], 'inventory': x['record']} for x in trees]},
            'fresh_saved_comparison': saved_fresh, 'artifacts': list(artifacts),
            'limitations': ['Only W01-W15 and their white controls are covered.',
                'The full 32-case application, periodic/mean/join paths and actual-data admission remain pending.',
                'Separate root source/runtime/history/caller custody and genuine completion remain required.',
                'Exact fabricated arithmetic is not detector covariance, calibration, native geometry/gravity or physical validation.',
                'Original precision, domain, resource and protected-validation boundaries remain; RET is paused.']}
        saved_result = write_body(root, 'WHITE_ONLY_QUALIFICATION.json', P.serial(result), ledger, artifacts)
        report_pin = saved_result['pin']
    except Exception as exc:
        first = exc
    # Every tree and every registered source/artifact check is attempted,
    # preserving earlier failure and invalidating any apparently saved success.
    tree_postchecks = []
    for tree in trees:
        try:
            inventory, states = tree_snapshot(root / tree['name'])
            same(inventory, tree['snapshot'], 'complete control-tree contents unchanged')
            same(states, tree['states'], 'complete control-tree path states unchanged')
            tree_postchecks.append({'name': tree['name'], 'unchanged': True, 'error': None})
        except Exception as exc:
            tree_postchecks.append({'name': tree['name'], 'unchanged': False,
                                    'error': (type(exc).__name__ + ': ' + str(exc))[:1024]})
            if first is None:
                first = exc
    postchecks = ledger.finish()
    if first is None and not all(x['unchanged'] for x in postchecks):
        first = W.ApplicationError('CUSTODY', 'final white-only source/artifact postcheck failure')
    namespace = {'inventory': None, 'error': None}
    if root_created:
        try:
            inventory, _ = tree_snapshot(root)
            namespace['inventory'] = inventory
            if first is None:
                expected = sorted([x['name'] for x in artifacts] + [x['name'] for x in trees])
                observed = sorted(x['name'] for x in inventory['records']
                                  if x['name'] != '.' and '/' not in x['name'])
                same(observed, expected, 'complete owned output namespace')
                by_name = {x['name']: x for x in inventory['records']}
                for artifact in artifacts:
                    same(by_name[artifact['name']], {'name': artifact['name'], 'kind': 'file',
                         'pin': artifact['pin'], 'target': None}, 'final artifact identity')
                for tree in trees:
                    for record in tree['snapshot']['records']:
                        name = tree['name'] + ('' if record['name'] == '.' else '/' + record['name'])
                        same(by_name[name], {**record, 'name': name}, 'final control artifact identity')
        except Exception as exc:
            namespace['error'] = (type(exc).__name__ + ': ' + str(exc))[:1024]
            if first is None:
                first = exc
    if first is not None:
        return {'result': None, 'report_pin': report_pin, 'artifacts': artifacts,
            'postchecks': postchecks, 'tree_postchecks': tree_postchecks, 'namespace': namespace,
            'refusal': {'schema': 'ri125-white-only-qualification-refusal-v1',
                'status': 'REFUSED', 'phase': 'fabricated_qualification',
                'code': first.code if isinstance(first, W.ApplicationError) else 'FAILURE',
                'message': (type(first).__name__ + ': ' + str(first))[:1024],
                'white_stage_qualified': False, 'full_application_qualified': False,
                'actual_data_admitted': False}}
    return {'result': result, 'report_pin': report_pin, 'artifacts': artifacts,
            'postchecks': postchecks, 'tree_postchecks': tree_postchecks, 'namespace': namespace,
            'refusal': None}
