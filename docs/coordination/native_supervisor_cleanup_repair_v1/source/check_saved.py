"""RI171 separately implemented saved-record oracle; same author, not nonauthor review.
No subject, worker, payload or control execution. Root supplies genuine outer provenance.
"""
import hashlib
import json
import os
import sys
import types

LATE_FILES = ("late_fsync","late_close","late_replacement","late_descriptor","late_drift","late_size",)
CASE_OBLIGATIONS = {
    "S01.healthy": {"kind":"whole","fault":"none","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":0},"subject_reap":"reaped"},
    "S02.timer": {"kind":"whole","fault":"timer","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":0},"subject_reap":"reaped"},
    "S03.nonzero": {"kind":"whole","fault":"nonzero","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":0},"subject_reap":"reaped"},
    "S03.stderr": {"kind":"whole","fault":"stderr","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S04.stdout.exact": {"kind":"whole","fault":"cap_stdout_exact","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":8388608,"stderr":0},"subject_reap":"reaped"},
    "S04.stdout.excess": {"kind":"whole","fault":"cap_stdout_excess","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":0},"subject_reap":"reaped"},
    "S04.stderr.exact": {"kind":"whole","fault":"cap_stderr_exact","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":0,"stderr":8388608},"subject_reap":"reaped"},
    "S04.stderr.excess": {"kind":"whole","fault":"cap_stderr_excess","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":0},"subject_reap":"reaped"},
    "S04.dual.excess": {"kind":"whole","fault":"cap_dual_excess","terminal":"ordinary","input_tag":"caller:stdout","healthy":{},"subject_reap":"reaped"},
    "S05.observer.real": {"kind":"observer","fault":"ps_real","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.duplicate": {"kind":"observer","fault":"ps_duplicate","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.malformed": {"kind":"observer","fault":"ps_malformed","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.nonascii": {"kind":"observer","fault":"ps_nonascii","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.empty": {"kind":"observer","fault":"ps_empty","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.nonzero": {"kind":"observer","fault":"ps_nonzero","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.stderr": {"kind":"observer","fault":"ps_stderr","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.overflow": {"kind":"observer","fault":"ps_overflow","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.observer.timeout": {"kind":"observer","fault":"ps_timeout","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S06.observed_descendant": {"kind":"whole","fault":"observed_descendant","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":0,"stderr":0},"subject_reap":"reaped"},
    "S07.fast_reparent": {"kind":"whole","fault":"fast_reparent","terminal":"missing_identity_choice","input_tag":"caller:stdout","healthy":{},"subject_reap":"reaped"},
    "S08.birth": {"kind":"direct","fault":"identity_birth","terminal":"direct","input_tag":"caller:stdout","healthy":{},"subject_reap":"none"},
    "S08.pgid": {"kind":"direct","fault":"identity_pgid","terminal":"direct","input_tag":"caller:stdout","healthy":{},"subject_reap":"none"},
    "S08.unverified_member": {"kind":"direct","fault":"identity_unverified_member","terminal":"direct","input_tag":"caller:stdout","healthy":{},"subject_reap":"none"},
    "S08.safe_second": {"kind":"direct","fault":"identity_safe_second","terminal":"direct","input_tag":"caller:stdout","healthy":{},"subject_reap":"none"},
    "S09.real_cutoffs": {"kind":"whole","fault":"real_cutoffs","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":0,"stderr":0},"subject_reap":"reaped"},
    "S09.real_expiry": {"kind":"whole","fault":"real_expiry","terminal":"hard_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"not_required"},
    "S10.stdout.fsync": {"kind":"whole","fault":"late_fsync","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S10.stdout.close": {"kind":"whole","fault":"late_close","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S10.stdout.replacement": {"kind":"whole","fault":"late_replacement","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S10.stdout.drift": {"kind":"whole","fault":"late_drift","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S10.stderr.fsync": {"kind":"whole","fault":"late_fsync","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S10.stderr.close": {"kind":"whole","fault":"late_close","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S10.stderr.replacement": {"kind":"whole","fault":"late_replacement","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S10.stderr.drift": {"kind":"whole","fault":"late_drift","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S10.processes.fsync": {"kind":"whole","fault":"late_fsync","terminal":"ordinary","input_tag":"caller:processes","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S10.processes.close": {"kind":"whole","fault":"late_close","terminal":"ordinary","input_tag":"caller:processes","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S10.processes.replacement": {"kind":"whole","fault":"late_replacement","terminal":"ordinary","input_tag":"caller:processes","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S10.processes.drift": {"kind":"whole","fault":"late_drift","terminal":"ordinary","input_tag":"caller:processes","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S11.preexists": {"kind":"whole","fault":"receipt_preexists","terminal":"receipt_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"not_required"},
    "S11.partial": {"kind":"whole","fault":"receipt_partial","terminal":"receipt_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"reaped"},
    "S11.fsync": {"kind":"whole","fault":"receipt_fsync","terminal":"receipt_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"reaped"},
    "S11.base_sync": {"kind":"whole","fault":"receipt_base_sync","terminal":"receipt_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"reaped"},
    "S11.post_receipt": {"kind":"whole","fault":"receipt_post_receipt","terminal":"receipt_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"reaped"},
    "S12.ownership": {"kind":"whole","fault":"hard_ownership","terminal":"hard_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"not_required"},
    "S12.drain": {"kind":"whole","fault":"hard_drain","terminal":"hard_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"not_required"},
    "S12.finalization": {"kind":"whole","fault":"hard_finalization","terminal":"hard_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"not_required"},
    "S13.journal_cap": {"kind":"whole","fault":"journal_cap","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":0},"subject_reap":"reaped"},
    "S13.descendant_cap": {"kind":"direct","fault":"descendant_cap","terminal":"direct","input_tag":"caller:stdout","healthy":{},"subject_reap":"none"},
    "S13.ps_max": {"kind":"observer","fault":"ps_max","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S13.late_observer": {"kind":"whole","fault":"late_observer","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":0},"subject_reap":"reaped"},
    "S08.signal_birth": {"kind":"direct","fault":"identity_signal_birth","terminal":"direct","input_tag":"caller:stdout","healthy":{},"subject_reap":"none"},
    "S08.signal_pgid": {"kind":"direct","fault":"identity_signal_pgid","terminal":"direct","input_tag":"caller:stdout","healthy":{},"subject_reap":"none"},
    "S10.stdout.descriptor": {"kind":"whole","fault":"late_descriptor","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S10.stdout.size": {"kind":"whole","fault":"late_size","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S10.stderr.descriptor": {"kind":"whole","fault":"late_descriptor","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S10.stderr.size": {"kind":"whole","fault":"late_size","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S10.processes.descriptor": {"kind":"whole","fault":"late_descriptor","terminal":"ordinary","input_tag":"caller:processes","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S10.processes.size": {"kind":"whole","fault":"late_size","terminal":"ordinary","input_tag":"caller:processes","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S04.stdout.read": {"kind":"whole","fault":"S04.stdout.read","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S04.stdout.write": {"kind":"whole","fault":"S04.stdout.write","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S04.stdout.partial_write": {"kind":"whole","fault":"S04.stdout.partial_write","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S04.stdout.short_write": {"kind":"whole","fault":"S04.stdout.short_write","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S04.stderr.read": {"kind":"whole","fault":"S04.stderr.read","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S04.stderr.write": {"kind":"whole","fault":"S04.stderr.write","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S04.stderr.partial_write": {"kind":"whole","fault":"S04.stderr.partial_write","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S04.stderr.short_write": {"kind":"whole","fault":"S04.stderr.short_write","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S05.caller.stdout.registration": {"kind":"whole","fault":"S05.caller.stdout.registration","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S05.caller.stderr.registration": {"kind":"whole","fault":"S05.caller.stderr.registration","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S05.ps.stdout.registration": {"kind":"observer","fault":"S05.ps.stdout.registration","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.ps.stderr.registration": {"kind":"observer","fault":"S05.ps.stderr.registration","terminal":"observer","input_tag":"ps:stderr","healthy":{},"subject_reap":"none"},
    "S05.ps.stdout.read": {"kind":"observer","fault":"S05.ps.stdout.read","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S05.ps.stderr.read": {"kind":"observer","fault":"S05.ps.stderr.read","terminal":"observer","input_tag":"ps:stderr","healthy":{},"subject_reap":"none"},
    "S05.fallback.alive": {"kind":"whole","fault":"S05.fallback.alive","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S05.fallback.already_exited": {"kind":"whole","fault":"S05.fallback.already_exited","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S10.caller.stdout.unregister_close": {"kind":"whole","fault":"S10.caller.stdout.unregister_close","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S10.caller.stderr.unregister_close": {"kind":"whole","fault":"S10.caller.stderr.unregister_close","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S10.ps.stdout.unregister_close": {"kind":"observer","fault":"S10.ps.stdout.unregister_close","terminal":"observer","input_tag":"ps:stdout","healthy":{},"subject_reap":"none"},
    "S10.ps.stderr.unregister_close": {"kind":"observer","fault":"S10.ps.stderr.unregister_close","terminal":"observer","input_tag":"ps:stderr","healthy":{},"subject_reap":"none"},
    "S10.journal.alive": {"kind":"whole","fault":"S10.journal.alive","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S10.journal.already_exited": {"kind":"whole","fault":"S10.journal.already_exited","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S13.observer.kill_failure": {"kind":"whole","fault":"S13.observer.kill_failure","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S13.observer.nonreap": {"kind":"whole","fault":"S13.observer.nonreap","terminal":"deadline_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"incomplete"},
    "S13.journal.kill_failure": {"kind":"whole","fault":"S13.journal.kill_failure","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S13.journal.nonreap": {"kind":"whole","fault":"S13.journal.nonreap","terminal":"deadline_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"incomplete"},
    "S13.poll_unavailable": {"kind":"whole","fault":"S13.poll_unavailable","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"incomplete"},
    "S13.deadline_exhausted": {"kind":"whole","fault":"S13.deadline_exhausted","terminal":"deadline_escape","input_tag":"caller:stdout","healthy":{},"subject_reap":"incomplete"},
    "S04.stdout.write_would_block.zero_progress": {"kind":"whole","fault":"S04.stdout.write_would_block.zero_progress","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S04.stdout.write_would_block.after_prefix": {"kind":"whole","fault":"S04.stdout.write_would_block.after_prefix","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stderr":64},"subject_reap":"reaped"},
    "S04.stdout.read_would_block.transient": {"kind":"whole","fault":"S04.stdout.read_would_block.transient","terminal":"ordinary","input_tag":"caller:stdout","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
    "S04.stderr.write_would_block.zero_progress": {"kind":"whole","fault":"S04.stderr.write_would_block.zero_progress","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S04.stderr.write_would_block.after_prefix": {"kind":"whole","fault":"S04.stderr.write_would_block.after_prefix","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64},"subject_reap":"reaped"},
    "S04.stderr.read_would_block.transient": {"kind":"whole","fault":"S04.stderr.read_would_block.transient","terminal":"ordinary","input_tag":"caller:stderr","healthy":{"stdout":64,"stderr":64},"subject_reap":"reaped"},
}


def bootstrap(path, digest):
    with open(path, 'rb') as f:
        raw = f.read(262145)
    if len(raw) > 262144 or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('checker request digest/cap')
    cfg = json.loads(raw)
    p = cfg['sources']['protocol']
    with open(p['path'], 'rb') as f:
        body = f.read(1048577)
    if len(body) != p['bytes'] or hashlib.sha256(body).hexdigest() != p['sha256']:
        raise ValueError('checker protocol identity')
    m = types.ModuleType('ri171_readonly_protocol')
    m.__file__ = p['path']
    exec(compile(body, p['path'], 'exec'), m.__dict__)
    return m


def inspect(P, req, case, current):
    op = req['operation']
    pins, checks = [], []
    def check(label, condition):
        checks.append({'id': label, 'passed': condition is True})
        P.need(condition is True, 'saved oracle: '+label)
    def load(name, cap=33554432):
        raw, pin, _ = P.capture(os.path.join(op, name), cap)
        pins.append(pin)
        return P.decode(raw)
    collection, report, trace = load('COLLECTION.json'), load('CASE.json'), load('TRACE.json')
    check('closed top namespace', sorted(os.listdir(op)) == sorted(['REQUEST_CAPTURE.json','worker.stdout','worker.stderr','CASE.json','TRACE.json','COLLECTION.json','body']))
    check('captured request typed equality', P.canonical(load('REQUEST_CAPTURE.json')) == P.canonical(req))
    check('closed22field successful collection',set(collection)=={'schema','case_id','status','before','after','command','environment','cwd','worker_pid','worker_returncode','worker_reaped','errors','body_tree','subject_deadline_seconds','controller_collection_timeout_seconds','new_subject_cleanup_budget','start_monotonic_ns','worker_stdout','worker_stderr','case_report','trace','end_before_final_record_monotonic_ns'})
    check('driver collection complete', collection['status'] == 'CAPTURED_FOR_INDEPENDENT_SAVED_REVIEW' and not collection['errors'] and collection['worker_returncode'] == 0 and collection['worker_reaped'] is True)
    check('driver command exact', collection['command'] == [P.VENDOR,'-I','-S','-B',req['sources']['worker']['path'],current['request']['path'],current['request']['sha256']])
    check('driver environment exact', P.canonical(collection['environment']) == P.canonical(P.ENV) and collection['cwd'] == P.BASE)
    check('selection', collection['case_id'] == report['case_id'] == case['id'] and report['entry'] == case['kind'] and report['fault'] == case['fault'])
    check('subject exact pin', P.canonical(report['source_subject']) == P.canonical(req['sources']['subject']))
    check('closed worker result', set(report) == {'schema','case_id','before','source_subject','entry','fault','return','exception','worker_errors','journal','recovery','entry_start_monotonic_ns','entry_end_monotonic_ns','after_sources','body_tree'})
    check('worker complete own tails', not report['worker_errors'] and report['schema'] == 'ri171-case-observation-v1')
    check('whole source/request custody', P.canonical(collection['before']) == P.canonical(collection['after']) == P.canonical(report['before']) == P.canonical(current) and P.canonical(report['after_sources']) == P.canonical(current['sources']))
    for stream in ('stdout','stderr'):
        raw, pin, state = P.capture(os.path.join(op,'worker.'+stream),1048576)
        pins.append(pin)
        check('empty worker '+stream, raw == b'' and P.canonical(collection['worker_'+stream]) == P.canonical({'pin':pin,'state':state}))
    for role, name in [('case_report','CASE.json'),('trace','TRACE.json')]:
        check('saved '+role+' pin', collection[role] == next(p for p in pins if p['path'] == os.path.join(op,name)))
    actual_tree = P.tree(os.path.join(op,'body'))
    check('entire body tree post-exit', P.canonical(actual_tree) == P.canonical(collection['body_tree']) == P.canonical(report['body_tree']))
    shapes={
        'read_error':{'tag','type','message'}, 'write_error':{'tag','type','message'},
        'fsync_error':{'tag','type','message'}, 'close_error':{'tag','type','message'},
        'direct_kill_error':{'tag','type','message'}, 'unregister_error':{'tag','type','message'},
        'pipe_close_error':{'tag','type','message'}, 'poll_error':{'tag','type','message'},
        'register_error':{'tag','type','message'}, 'read':{'tag','bytes','sha256'},
        'hard_injection':{'phase'}, 'fsync_attempt':{'tag'}, 'fsync_complete':{'tag'},
        'file_mutation':{'tag','fault','before','after','before_first_byte'}, 'close_complete':{'tag'},
        'sync_base_complete':{'ordinal'}, 'leaf_recovery_signal':{'identity','signal'}, 'observer_entry':{'deadline_monotonic_ns'},
        'close_attempt':{'tag'}, 'file_acquired':{'tag','path','fd'}, 'sync_base_attempt':{'ordinal'},
        'fixture_directory_sync':{'path'}, 'source_error':{'stage','type','message'}, 'receipt_candidate':{'value'},
        'canonical_double':{'bytes','value'}, 'journal_candidate':{'value'}, 'ready_barrier':{'path'},
        'recovery_identity_observation':{'pid','returncode','stdout_hex','stderr_hex'},
        'popen_attempt':{'kind','subject_argv','actual_argv','parent_timer'},
        'popen_acquired':{'handle_id','kind','pid'}, 'inert_pre_observer_exit':{'pid','returncode'},
        'observer_double':{'ordinal','message'}, 'clock_double':{'nanoseconds','genuine_timing_credit'},
        'stale_table_double':{'ordinal'}, 'discover':{'caller','live','known'},
        'signal_group':{'pgid','signal'}, 'pipe_close_attempt':{'tag'}, 'pipe_closed':{'tag'},
        'poll_double':{'kind','observed_returncode','genuine_reap'}, 'poll':{'kind','pid','returncode'},
        'direct_kill_attempt':{'kind','pid'}, 'register_installed':{'tag'},
        'unregister_attempt':{'tag'}, 'selector_close_attempt':set(),
        'direct_operand':{'target','table','known'}, 'signal_double':{'pgid','signal'}
    }
    for e in trace:
        extra=set(e)-{'event','monotonic_ns'}
        check('closed event '+str(e.get('event')),extra in ({'tag','requested','written'},{'tag','requested','written','injection'}) if e.get('event')=='write' else e.get('event') in shapes and extra==shapes[e['event']])
    check('finite event schema/order', type(trace) is list and len(trace) <= 131072 and all(type(x) is dict and type(x.get('event')) is str and type(x.get('monotonic_ns')) is int for x in trace) and all(trace[i]['monotonic_ns'] <= trace[i+1]['monotonic_ns'] for i in range(len(trace)-1)))
    f, stream = case['fault'], case.get('stream') or ('stderr' if '.stderr.' in case['fault'] else 'stdout')
    events = lambda name: [e for e in trace if e['event'] == name]
    obligation = CASE_OBLIGATIONS[case['id']]
    check('finite exact case obligation', obligation['kind'] == case['kind'] and obligation['fault'] == f)
    input_tag = obligation['input_tag']
    def indices(event, tag=None):
        return [i for i,e in enumerate(trace) if e['event']==event and (tag is None or e.get('tag')==tag)]
    def exact_input_injection(event, message, kind='OSError'):
        found = [i for i,e in enumerate(trace) if e['event']==event and e.get('message')==message]
        check('exact role stream injection '+message, len(found)==1 and trace[found[0]]['tag']==input_tag and trace[found[0]]['type']==kind)
        at=found[0]
        check('same pipe registered before injection '+message, any(i<at for i in indices('register_installed',input_tag)))
        if event=='read_error':
            check('first read on same pipe is injected '+message,not any(i<at for i in indices('read',input_tag)))
        return at
    def compound_cleanup_lifetime(read, unregister, close_error, subject_pid):
        # These four cases have exactly one owned process of the selected role.
        # Whole caller cases may have many *other-role* ps lifetimes; never merge
        # their equal stream names with this caller's pipes. Observer-only cases
        # have one ps lifetime. Refuse ambiguous same-role reuse rather than
        # pretending tag-only events identify two different acquired handles.
        role='ps' if case['kind']=='observer' else 'caller'
        acquisitions=[(i,e) for i,e in enumerate(trace) if e['event']=='popen_acquired' and e['kind']==role]
        check('compound unique owned role lifetime',len(acquisitions)==1 and type(subject_pid) is int and acquisitions[0][1]['pid']==subject_pid and type(acquisitions[0][1]['handle_id']) is int)
        begin,owner=acquisitions[0]
        check('compound injection belongs to owned lifetime',begin<read<unregister<close_error and input_tag==role+':'+stream)
        for name in ('stdout','stderr'):
            tag=role+':'+name
            related=[i for i,e in enumerate(trace) if e.get('tag')==tag and e['event'] in ('register_installed','unregister_attempt','pipe_close_attempt','pipe_closed','unregister_error','pipe_close_error')]
            check('compound pipe events follow acquisition '+tag,all(i>begin for i in related))
            installed=indices('register_installed',tag)
            successes=indices('pipe_closed',tag)
            check('compound one successful close '+tag,len(installed)==1 and len(successes)==1 and begin<installed[0]<successes[0])
            success=successes[0]
            # Attempt events precede the underlying call: a rejected second
            # close/unregister is forbidden even if no second success is emitted.
            unregisters=indices('unregister_attempt',tag); closes=indices('pipe_close_attempt',tag)
            check('compound no attempt after successful close '+tag,not any(i>success for i in unregisters+closes))
            if name==stream:
                check('compound failed pipe exact attempt counts '+tag,len(unregisters)==2 and len(closes)==2)
                check('compound failed-close then successful retry '+tag,installed[0]<read<unregisters[0]<unregister<closes[0]<close_error<unregisters[1]<closes[1]<success)
            else:
                check('compound healthy pipe exact attempt counts '+tag,len(unregisters)==1 and len(closes)==1)
                check('compound healthy pipe ordered close '+tag,installed[0]<unregisters[0]<closes[0]<success)
    duration = (report['entry_end_monotonic_ns'] - report['entry_start_monotonic_ns'])/1000000000
    check('elapsed positive', duration >= 0)
    check('original limits in collection', collection['subject_deadline_seconds'] == 315 and collection['controller_collection_timeout_seconds'] == 335 and collection['new_subject_cleanup_budget'] is False)
    allowed_body={'PAYLOAD_START.json','READY.json','LEAF.json','RECOVERY_IDENTITY.json','DESCENDANT_OBSERVED.json','OBSERVER_READY.json','outer.stdout','outer.stderr','outer.processes.jsonl','outer.completion.json','outer.stdout.original','outer.stderr.original','outer.processes.jsonl.original','outer.stdout.fd_replacement','outer.stderr.fd_replacement','outer.processes.jsonl.fd_replacement'}
    check('body namespace only declared leaves', all(x['kind']=='file' and x['path'] in allowed_body for x in actual_tree))
    outputs = {}
    for name in ('stdout','stderr','processes.jsonl','completion.json'):
        path=os.path.join(op,'body','outer.'+name)
        if os.path.exists(path):
            raw,pin,_=P.capture(path,67108864)
            pins.append(pin)
            outputs[name]=raw
    receipt = None
    candidates = events('receipt_candidate')
    if candidates:
        check('one complete receipt candidate', len(candidates)==1)
        receipt=candidates[0]['value']
    if 'completion.json' in outputs and f not in ('receipt_preexists','receipt_partial'):
        actual = P.decode(outputs['completion.json'])
        check('complete receipt canonical bytes', P.canonical(actual)==outputs['completion.json'])
        check('complete receipt equals serialized source candidate', receipt is not None and P.canonical(actual)==P.canonical(receipt))
    if receipt is not None:
        check('closed17field receipt', set(receipt)=={'schema','status','command','environment','cwd','start_monotonic_ns','deadline_monotonic_ns','caller_pid','caller_reaped','caller_returncode','observed_cleanup','complete_fork_coverage','scientific_acceptance','errors','streams','observed_processes','end_before_receipt_monotonic_ns'})
        check('no inflated authority', receipt['schema']=='ri165-observed-outer-completion-v1' and receipt['complete_fork_coverage'] is False and receipt['scientific_acceptance'] is False)
        check('source exact315deadline', receipt['deadline_monotonic_ns']-receipt['start_monotonic_ns']==315000000000)
        check('inert command and environment', receipt['command']==[P.VENDOR,'-I','-S','-B',req['sources']['payload']['path'],'caller',f,os.path.join(op,'body')] and receipt['environment']==P.ENV and receipt['cwd']==P.BASE)
        check('three complete capture objects', set(receipt['streams'])=={'stdout','stderr','processes'})
        for name,saved in receipt['streams'].items():
            check('capture fields '+name,set(saved)=={'path','eof','overflow_byte','durable_close','readback'})
            data_name='processes.jsonl' if name=='processes' else name
            check('capture pathname '+name,saved['path']==os.path.join(op,'body','outer.'+data_name))
            rb=saved['readback']
            if rb is not None:
                data=outputs[data_name]
                check('capture pin '+name,rb['bytes']==len(data) and rb['sha256']==hashlib.sha256(data).hexdigest() and rb['path']==saved['path'])
        if case['expect']=='captured':
            check('positive whole result',receipt['status']=='CAPTURED_FOR_ROOT_REVIEW' and not receipt['errors'] and report['return']==0 and report['exception'] is None and receipt['caller_reaped'] is True and receipt['caller_returncode']==0 and receipt['observed_cleanup'] is True)
        elif case['expect'] in ('failed','missing_identity_rejection'):
            check('negative whole result',receipt['status']=='FAILED' and bool(receipt['errors']))
    if case['kind']=='whole' and case['expect'] in ('captured','failed'):
        check('whole receipt required',receipt is not None)
    # Finite terminal policy: no generic candidate-only failed completion.
    if case['kind']=='whole':
        ordinary = obligation['terminal']=='ordinary' or (obligation['terminal']=='missing_identity_choice' and receipt is not None)
        if ordinary:
            wanted_return=0 if case['expect']=='captured' else 2
            check('ordinary exact return and no escape',type(report['return']) is int and report['return']==wanted_return and report['exception'] is None)
            check('ordinary complete durable receipt bytes',receipt is not None and outputs.get('completion.json')==P.canonical(receipt))
            made=[i for i,e in enumerate(trace) if e['event']=='file_acquired' and e['tag']=='completion']
            synced=indices('fsync_complete','completion'); closed=indices('close_complete','completion')
            done=[i for i,e in enumerate(trace) if e['event']=='sync_base_complete' and e['ordinal']==2]
            starts=indices('receipt_candidate')
            writes=[(i,e) for i,e in enumerate(trace) if e['event']=='write' and e['tag']=='completion']
            check('ordinary receipt ordered complete durability',len(starts)==len(made)==len(synced)==len(closed)==len(done)==1 and starts[0]<made[0]<synced[0]<closed[0]<done[0] and bool(writes) and all(made[0]<i<synced[0] and type(e['written']) is int and 0<e['written']<=e['requested'] for i,e in writes) and sum(e['written'] for i,e in writes)==len(outputs['completion.json']))
            check('ordinary receipt no hidden write or durability fault',not any(e['event'] in ('write_error','fsync_error','close_error') and e.get('tag')=='completion' for e in trace))
        elif obligation['terminal']=='deadline_escape':
            check('declared deadline escape only',report['return'] is None and report['exception']=={'type':'Refusal','message':'completion durability exceeded315s'} and receipt is not None and outputs.get('completion.json')==P.canonical(receipt))
            check('declared branch clock not actual duration',bool(events('clock_double') or events('poll_double')) and receipt['caller_reaped'] is False and receipt['observed_cleanup'] is False and any(e['stage']=='final_deadline' for e in receipt['errors']))
        else:
            check('declared whole escape has no return',report['return'] is None)
            if obligation['terminal']=='hard_escape' or (obligation['terminal']=='missing_identity_choice' and receipt is None):
                check('hard escape has no invented receipt',receipt is None and 'completion.json' not in outputs)
        if obligation['subject_reap']=='incomplete' and receipt is not None:
            check('declared incomplete subject has no invented reap or code',receipt['caller_reaped'] is False and receipt['caller_returncode'] is None and receipt['observed_cleanup'] is False)
        if obligation['subject_reap']=='reaped' and receipt is not None:
            check('required subject caller reap',receipt['caller_reaped'] is True and type(receipt['caller_returncode']) is int)
        if ordinary:
            for name,count in obligation['healthy'].items():
                saved=receipt['streams'][name]
                check('complete healthy capture '+name,outputs.get(name)==b'R'*count and saved['eof'] is True and saved['durable_close'] is True and saved['readback'] is not None and saved['overflow_byte'] is None)
                check('healthy capture successful durability '+name,bool(indices('fsync_complete',name)) and bool(indices('close_complete',name)))
            for name,saved in receipt['streams'].items():
                expected_bad_durability=f in ('late_fsync','late_close') and name==stream
                check('all comparable capture durability '+name,saved['durable_close'] is (not expected_bad_durability) and saved['readback'] is not None)
            check('all comparable final file closes',all(indices('close_complete',name) for name in ('stdout','stderr','processes')))

    first = receipt['errors'][0] if receipt is not None and receipt['errors'] else None
    if first is None and events('source_error'):
        first = {k: events('source_error')[0][k] for k in ('stage','type','message')}
    def primary(stage, kind, message):
        check('exact earliest error', P.canonical(first)==P.canonical({'stage':stage,'type':kind,'message':message}))
    monitor_review={'status':'NOT_A_WHOLE_SUPERVISOR_CASE','raw_records':0,'independent_observed_processes':[]}
    if case['kind']=='whole':
        journal_bytes=outputs.get('processes.jsonl',b'')
        altered=f.startswith('late_') and stream=='processes' and f in ('late_drift','late_size','late_replacement')
        partial_journal=f.startswith(('S10.journal.','S13.journal.'))
        if altered:
            # The deliberate data-file mutation is itself the negative case.
            # Do not invent its unavailable original bytes or call the damaged
            # journal an independently valid process observation.
            monitor_review={'status':'INTENTIONALLY_MUTATED_JOURNAL_NO_COMPLETE_MONITOR_CREDIT','raw_records':None,'independent_observed_processes':None}
        else:
            rows=[]
            if partial_journal:
                rows=[e['value'] for e in events('journal_candidate')]
                check('failed journal complete candidates retained',bool(rows) and journal_bytes==P.canonical(rows[0])[:17])
            elif f=='journal_cap':
                rows=[e['value'] for e in events('canonical_double')]
                check('capped journal complete candidates retained',bool(rows) and not journal_bytes)
            elif journal_bytes:
                check('complete raw journal framing',journal_bytes.endswith(b'\n'))
                rows=[P.decode(line+b'\n') for line in journal_bytes.splitlines()]
                check('exact raw journal canonical bodies',b''.join(P.canonical(row) for row in rows)==journal_bytes)
            known={}
            failed_observations=0
            callers=[e['pid'] for e in events('popen_acquired') if e['kind']=='caller']
            caller=callers[0] if callers else None
            last_table=None
            for row in rows:
                check('closed complete raw ps record',set(row)=={'command','start_monotonic_ns','pid','returncode','reaped','eof','overflow','end_monotonic_ns','errors','stdout_hex','stderr_hex'})
                check('raw ps command and timing',row['command']==['/bin/ps','-axo','pid=,ppid=,pgid=,lstart='] and type(row['start_monotonic_ns']) is int and type(row['end_monotonic_ns']) is int and row['start_monotonic_ns']<=row['end_monotonic_ns'])
                data=bytes.fromhex(row['stdout_hex']); other=bytes.fromhex(row['stderr_hex'])
                check('bounded whole raw ps capture',len(data)<=262145 and len(other)<=262145 and type(row['errors']) is list and all(type(e) is str for e in row['errors']) and type(row['reaped']) is bool and set(row['eof'])=={'stdout','stderr'})
                if row['errors']:
                    failed_observations+=1
                    check('failed ps observation never credited to positive case',case['expect']!='captured')
                    continue
                check('successful whole ps capture',len(data)<=262144 and not other and row['returncode']==0 and row['reaped'] is True and row['eof']=={'stdout':True,'stderr':True} and not row['overflow'])
                table={}
                for line in data.decode('ascii').splitlines():
                    fields=line.split()
                    check('whole ps exact row domain',len(fields)==8 and all(x.isdigit() for x in fields[:3]))
                    pid,ppid,pgid=map(int,fields[:3])
                    check('whole ps unique positive identity',pid>0 and ppid>=0 and pgid>=0 and pid not in table)
                    table[pid]={'pid':pid,'ppid':ppid,'pgid':pgid,'birth':' '.join(fields[3:])}
                check('whole ps nonempty',bool(table))
                if not known and caller in table and table[caller]['pgid']==caller:
                    known[caller]=dict(table[caller])
                live=set(known).intersection(table)
                check('whole observed identity stable',all(table[k]['birth']==known[k]['birth'] and table[k]['pgid']==known[k]['pgid'] for k in live))
                growing=True
                while growing:
                    growing=False
                    for pid,row_value in table.items():
                        if pid not in known and row_value['ppid'] in live:
                            check('whole descendant cap',len(known)<64)
                            known[pid]=dict(row_value);live.add(pid);growing=True
                last_table=table
            # Candidate-only journal rows are retained observations whose durable
            # source journal failed. They must never imply successful custody.
            if partial_journal or f=='journal_cap':
                monitor_review={'status':'FAILED_JOURNAL_WITH_COMPLETE_CANDIDATES','raw_records':len(rows),'independent_observed_processes':list(known.values())}
            else:
                monitor_review={'status':'COMPLETE_RECORDS_WITH_FAILED_OBSERVATION' if failed_observations else 'COMPLETE_RETAINED_JOURNAL_PARSED','raw_records':len(rows),'independent_observed_processes':list(known.values()),'failed_observations':failed_observations}
                if receipt is not None:
                    check('whole saved observed identities',P.canonical(list(known.values()))==P.canonical(receipt['observed_processes']))
                    if receipt['observed_cleanup']:
                        groups={r['pgid'] for r in known.values()}
                        check('last complete table excludes observed groups',last_table is not None and not set(known).intersection(last_table) and not any(r['pgid'] in groups for r in last_table.values()))
            if case['expect']=='captured':
                check('positive has actual complete monitoring',bool(rows) and monitor_review['status']=='COMPLETE_RETAINED_JOURNAL_PARSED')
    if case['kind']=='whole':
        if '.write_would_block.' in f:
            msg='RI169_WRITE_AFTER_PREFIX' if f.endswith('after_prefix') else 'RI169_WRITE_ZERO_PROGRESS'
            primary('pump:'+stream,'BlockingIOError',msg)
            check('named write reached',any(e.get('tag')==stream and e.get('message')==msg for e in events('write_error')))
            expected=17 if f.endswith('after_prefix') else 0
            check('retained exact failed prefix',outputs[stream]==b'R'*expected)
            check('successful consumed read before failure',any(e.get('tag')=='caller:'+stream and e.get('bytes')==64 and e.get('sha256')==hashlib.sha256(b'R'*64).hexdigest() for e in events('read')))
            check('failed pump never EOF',receipt['streams'][stream]['eof'] is False)
            if expected:
                check('partial readback remains secondary',any(e['stage']=='readback:'+stream for e in receipt['errors'][1:]))
        elif f.endswith('.read') or f.endswith('.unregister_close'):
            primary('pump:'+stream,'OSError','RI167_F01_READ')
            exact_input_injection('read_error','RI167_F01_READ')
        elif f.endswith('.write') or f.endswith('.partial_write'):
            primary('pump:'+stream,'OSError','RI167_F01_PARTIAL_WRITE' if f.endswith('.partial_write') else 'RI167_F01_WRITE')
            check('retained original write prefix',outputs[stream]==b'R'*(17 if f.endswith('.partial_write') else 0))
        elif f.endswith('.registration'):
            primary('register:'+stream,'OSError','RI167_F01_REGISTER')
            exact_input_injection('register_error','RI167_F01_REGISTER')
        elif f.endswith('.short_write') or '.read_would_block.' in f:
            primary('supervision','Refusal','caller outer stderr nonempty')
            check('positive pump exact bytes',outputs['stdout']==outputs['stderr']==b'R'*64 and receipt['streams']['stdout']['eof'] is True and receipt['streams']['stderr']['eof'] is True)
            if '.read_would_block.' in f:
                at=exact_input_injection('read_error','RI169_READ_TRANSIENT','BlockingIOError')
                later=[i for i in indices('read',input_tag) if i>at and trace[i]['bytes']==64 and trace[i]['sha256']==hashlib.sha256(b'R'*64).hexdigest()]
                check('same pipe successful read after transient',len(later)==1)
                through=later[0]
                check('same pipe remains active through retry',not any(e['event'] in ('unregister_attempt','pipe_close_attempt','pipe_closed','register_installed') and e.get('tag')==input_tag for e in trace[at+1:through]))
                check('same pipe EOF follows retry',any(i>through and trace[i]['bytes']==0 for i in indices('read',input_tag)))
            else:
                check('actual short writes reached',any(e.get('tag')==stream and 0<e['written']<e['requested'] for e in events('write')))
        elif f.startswith(('S05.fallback.','S13.observer.')) or f in ('S13.poll_unavailable','S13.deadline_exhausted'):
            primary('supervision','Refusal','RI171_OBSERVER_FAILURE')
        elif f.startswith(('S10.journal.','S13.journal.')):
            primary('supervision','Refusal','ps journal: OSError: RI171_JOURNAL_WRITE')
            check('real partial journal write',len(outputs['processes.jsonl'])==17 and any(e.get('tag')=='processes' for e in events('write_error')))
        elif f=='nonzero' or f in LATE_FILES:
            primary('supervision','Refusal','caller/outer failed')
            check('actual nonzero reap',receipt['caller_returncode']==7 and receipt['caller_reaped'] is True)
        elif f=='stderr':
            primary('supervision','Refusal','caller outer stderr nonempty')
        elif f.startswith('cap_'):
            selected=['stdout','stderr'] if f=='cap_dual_excess' else ['stdout' if 'stdout' in f else 'stderr']
            for name in selected:
                check('complete bounded payload '+name,outputs[name]==b'R'*8388608)
                check('overflow predicate '+name,receipt['streams'][name]['overflow_byte']==(82 if f.endswith('excess') else None))
            if f.endswith('excess'):
                check('cap primary exact', first['stage'] in ['capture:'+n for n in selected] and first['type']=='Refusal' and first['message']=='8 MiB outer stream cap')
            elif 'stderr' in f:
                primary('supervision','Refusal','caller outer stderr nonempty')
        elif f=='observed_descendant':
            primary('supervision','Refusal','observed descendant/group remains after caller exit')
            check('descendant observed before parent exit','DESCENDANT_OBSERVED.json' in {x['path'] for x in actual_tree} and any(len(e['known'])>=2 for e in events('discover')))
        elif f=='fast_reparent':
            primary('supervision','Refusal','caller identity was not observed as owned leader')
            check('controlled preobserver exit',len(events('inert_pre_observer_exit'))==1)
            if receipt is None:
                check('missing identity ends only at real hard deadline without a receipt',report['exception']=={'type':'HardStop','message':'outer signal 14'} and duration>=315 and duration<316)
            else:
                check('ordinary missing identity rejection retained',receipt['status']=='FAILED' and report['return']==2 and report['exception'] is None)
        elif f=='late_observer':
            primary('supervision','Refusal','RI171_OBSERVER_FAILURE')
            doubles=indices('observer_double')
            check('dedicated second observer fault',bool(doubles) and [trace[i]['ordinal'] for i in doubles]==list(range(2,len(doubles)+2)) and all(trace[i]['message']=='RI171_OBSERVER_FAILURE' for i in doubles))
            check('successful first real observer precedes late fault',len([e for e in trace[:doubles[0]] if e['event']=='popen_acquired' and e['kind']=='ps'])==1 and any(e['event']=='discover' for e in trace[:doubles[0]]) and monitor_review['raw_records']==1)
            check('late observer retains caller buffers and reap',outputs['stdout']==b'R'*64 and outputs['stderr']==b'' and receipt['caller_reaped'] is True and receipt['observed_cleanup'] is False)
        elif f=='journal_cap':
            primary('supervision','Refusal','ps journal: Refusal: process journal cap')
            check('exact unlowered cap operand',events('canonical_double')[0]['bytes']==67108865)
        elif f=='real_cutoffs':
            primary('deadline','Refusal','310-second work cutoff')
            start=receipt['start_monotonic_ns']
            term=[e for e in events('signal_group') if e['signal']==15]
            kill=[e for e in events('signal_group') if e['signal']==9]
            check('actual310/312 clock',bool(term) and bool(kill) and (term[0]['monotonic_ns']-start)>=310000000000 and (kill[0]['monotonic_ns']-start)>=312000000000 and duration>=312 and duration<315.5 and not events('clock_double'))
        elif f=='real_expiry':
            check('real315 hard signal',report['exception'] is not None and report['exception']['type']=='HardStop' and report['exception']['message']=='outer signal 14' and duration>=315 and duration<316 and not events('clock_double') and bool(events('stale_table_double')))
        elif f.startswith('hard_'):
            check('exact hard branch',report['exception']=={'type':'HardStop','message':'RI171_HARD_'+f.split('_',1)[1].upper()} and events('hard_injection')[0]['phase']==f.split('_',1)[1])
        elif f.startswith('receipt_'):
            exc=report['exception']
            check('receipt escape required',exc is not None)
            if f=='receipt_preexists':
                primary('supervision','Refusal','completion already exists')
                check('preserved preexisting receipt',outputs['completion.json']==b'RI171 preexisting\n' and exc['type']=='FileExistsError' and not events('popen_acquired'))
            elif f=='receipt_partial':
                check('exact partial receipt prefix',receipt is not None and outputs['completion.json']==P.canonical(receipt)[:17] and exc=={'type':'OSError','message':'RI171_RECEIPT_WRITE'})
            else:
                msg={'receipt_fsync':'RI171_RECEIPT_FSYNC','receipt_base_sync':'RI171_RECEIPT_BASE_SYNC','receipt_post_receipt':'RI171_POST_RECEIPT'}[f]
                check('late exception despite saved receipt',exc=={'type':'OSError','message':msg} and receipt['status']=='CAPTURED_FOR_ROOT_REVIEW')
        elif f in ('none','timer'):
            check('healthy64byte payload',outputs['stdout']==b'R'*64 and outputs['stderr']==b'')
        else:
            check('closed whole fault inventory',False)
        if f=='timer':
            payload=load('body/PAYLOAD_START.json',4096)
            parent=[x for x in events('popen_attempt') if x['kind']=='caller'][0]
            check('actual separate timers',payload['timer']==[0.0,0.0] and parent['parent_timer'][0]>0 and parent['parent_timer'][1]==0)
            check('inert bootstrap flags',payload['executable']==P.VENDOR and payload['environment']==P.ENV and payload['flags']=={'isolated':1,'no_site':1,'dont_write_bytecode':1,'optimize':0})
        if f.endswith('.write') or f.endswith('.partial_write') or '.write_would_block.' in f:
            msg=('RI169_WRITE_AFTER_PREFIX' if f.endswith('after_prefix') else 'RI169_WRITE_ZERO_PROGRESS') if '.write_would_block.' in f else ('RI167_F01_PARTIAL_WRITE' if f.endswith('.partial_write') else 'RI167_F01_WRITE')
            kind='BlockingIOError' if '.write_would_block.' in f else 'OSError'
            faults=[i for i,e in enumerate(trace) if e['event']=='write_error' and e['message']==msg]
            check('exact output stream fault',len(faults)==1 and trace[faults[0]]['tag']==stream and trace[faults[0]]['type']==kind)
            at=faults[0];reads=[i for i in indices('read',input_tag) if trace[i]['bytes']==64 and trace[i]['sha256']==hashlib.sha256(b'R'*64).hexdigest()]
            check('consumed same caller pipe before write fault',len(reads)==1 and reads[0]<at)
            prefix=17 if f.endswith('.partial_write') or f.endswith('after_prefix') else 0
            writes=[e for e in trace[:at] if e['event']=='write' and e['tag']==stream]
            check('exact actually written prefix before failure',sum(e['written'] for e in writes)==prefix and (not prefix or len(writes)==1 and writes[0]['written']==17 and writes[0].get('injection')=='real-prefix'))
        if f.endswith('.registration'):
            at=exact_input_injection('register_error','RI167_F01_REGISTER')
            stops=indices('unregister_attempt',input_tag);closes=indices('pipe_closed',input_tag)
            check('caller partial registration cleanup reached',any(i>at for i in stops) and len(closes)==1 and any(at<i<closes[0] for i in stops))
        if f.endswith('.unregister_close'):
            tags='caller:'+stream
            read=exact_input_injection('read_error','RI167_F01_READ')
            u=exact_input_injection('unregister_error','RI171_UNREGISTER');c=exact_input_injection('pipe_close_error','RI171_PIPE_CLOSE')
            check('all failing cleanups same pipe order and retry',read<u<c and any(i>c for i in indices('pipe_closed',tags)))
            expected_errors=[{'stage':'pump:'+stream,'type':'OSError','message':'RI167_F01_READ'},
                             {'stage':'unregister:'+stream,'type':'OSError','message':'RI171_UNREGISTER'},
                             {'stage':'pipe_close:'+stream,'type':'OSError','message':'RI171_PIPE_CLOSE'}]
            check('compound caller retained ordered primary and secondary errors',P.canonical(receipt['errors'][:3])==P.canonical(expected_errors) and all(sum(P.canonical(e)==P.canonical(want) for e in receipt['errors'])==1 for want in expected_errors))
            source_positions=[]
            for want in expected_errors:
                matched=[i for i,e in enumerate(trace) if e['event']=='source_error' and P.canonical({k:e[k] for k in ('stage','type','message')})==P.canonical(want)]
                check('compound caller exact source error '+want['stage'],len(matched)==1)
                source_positions.append(matched[0])
            check('compound caller source error order',read<source_positions[0]<u<source_positions[1]<c<source_positions[2])
            compound_cleanup_lifetime(read,u,c,receipt['caller_pid'])
        if f.startswith(('S04.','S05.caller.','S10.caller.')) and not f.endswith('.short_write') and '.read_would_block.' not in f:
            other='stdout' if stream=='stderr' else 'stderr'
            check('healthy sibling retained',outputs[other]==b'R'*64 and receipt['streams'][other]['eof'] is True)
            check('failed stream never claims EOF',receipt['streams'][stream]['eof'] is False)
            if f.endswith('.read') or f.endswith('.registration') or f.endswith('.unregister_close'):
                check('failed unread stream has no invented bytes',outputs[stream]==b'')
            failure_indices=[i for i,e in enumerate(trace) if e['event'] in ('write_error','read_error','register_error') and e.get('tag') in (stream,'caller:'+stream)]
            check('failed pump not read after refusal',bool(failure_indices) and not any(e['event']=='read' and e.get('tag')=='caller:'+stream for e in trace[failure_indices[0]+1:]))
        if f in LATE_FILES:
            expected='readback' if f in ('late_drift','late_size','late_descriptor','late_replacement') else f.split('_')[1]
            check('late intended predicate reached',any(e['stage']==expected+':'+stream for e in receipt['errors'][1:]))
            check('all comparable final file checks',all(any(e.get('tag')==name for e in events('close_attempt')) for name in ('stdout','stderr','processes')))
            if f in ('late_drift','late_size'):
                mutations=events('file_mutation')
                check('one intended mutation',len(mutations)==1 and mutations[0]['tag']==stream and mutations[0]['fault']==f)
                m=mutations[0];data=outputs['processes.jsonl' if stream=='processes' else stream]
                expected_path=receipt['streams'][stream]['path']
                check('closed mutation before after pins',all(set(m[k])=={'path','bytes','sha256'} and m[k]['path']==expected_path for k in ('before','after')))
                first_byte=123 if stream=='processes' else 82
                check('nonempty intended mutation operand',m['before_first_byte']==first_byte and type(m['before']['bytes']) is int and m['before']['bytes']>0)
                original=(bytes([first_byte])+data[1:]) if f=='late_drift' else data[:-1]
                check('mutation original length and hash',len(original)==m['before']['bytes'] and hashlib.sha256(original).hexdigest()==m['before']['sha256'])
                check('mutation saved length and hash',len(data)==m['after']['bytes'] and hashlib.sha256(data).hexdigest()==m['after']['sha256'])
                check('isolated same-size hash drift' if f=='late_drift' else 'isolated appended-byte size drift',data==(b'Q'+original[1:] if f=='late_drift' else original+b'Q') and len(data)==len(original)+(0 if f=='late_drift' else 1) and m['before']['sha256']!=m['after']['sha256'])
                if stream in ('stdout','stderr'):
                    check('fixed complete late stream preimage',original==b'R'*64)
        if f.startswith(('S05.fallback.','S13.observer.','S10.journal.','S13.journal.')) or f in ('S13.poll_unavailable','S13.deadline_exhausted'):
            if f.endswith('already_exited'):
                check('real exited reap retained',receipt['caller_reaped'] is True and receipt['caller_returncode']==0)
                exited=events('inert_pre_observer_exit')
                check('already reaped handle is never killed',len(exited)==1 and exited[0]['pid']==receipt['caller_pid'] and exited[0]['returncode']==0 and not [e for e in events('direct_kill_attempt') if e['kind']=='caller'])
            elif f.endswith('nonreap') or f=='S13.deadline_exhausted':
                check('declared branch clock no fabricated reap',receipt['caller_reaped'] is False and any(e['stage']=='direct_handle_reap' for e in receipt['errors']) and bool(events('poll_double') or events('clock_double')))
            elif f=='S13.poll_unavailable':
                check('independent reap attempt failure',bool(events('poll_error')) and any(e['stage']=='direct_handle_reap' for e in receipt['errors']))
            else:
                check('independent owned reap',receipt['caller_reaped'] is True and bool([e for e in events('poll') if e['kind']=='caller' and e['returncode'] is not None]))
            check('no group cleanup from direct reap',receipt['observed_cleanup'] is False)
            if not f.endswith('already_exited'):
                attempts=[i for i,e in enumerate(trace) if e['event']=='direct_kill_attempt' and e['kind']=='caller' and e['pid']==receipt['caller_pid']]
                check('fallback owned kill attempt retained',len(attempts)==1)
                if obligation['subject_reap']=='reaped':
                    check('fallback independent owned poll after kill',any(i>attempts[0] and e['event']=='poll' and e['kind']=='caller' and e['pid']==receipt['caller_pid'] and e['returncode']==receipt['caller_returncode'] for i,e in enumerate(trace)))
            if f.endswith('.kill_failure'):
                faults=indices('direct_kill_error','caller'); attempts=indices('direct_kill_attempt')
                check('defining direct kill failure reached',len(faults)==1 and trace[faults[0]]['type']=='OSError' and trace[faults[0]]['message']=='RI171_KILL_FAILURE' and any(i<faults[0] and trace[i]['kind']=='caller' and trace[i]['pid']==receipt['caller_pid'] for i in attempts))
                check('defining kill failure is secondary',any(e=={'stage':'direct_handle_kill','type':'OSError','message':'RI171_KILL_FAILURE'} for e in receipt['errors'][1:]))
                check('reap independent after failed kill',any(i>faults[0] and e['event']=='poll' and e['kind']=='caller' and e['pid']==receipt['caller_pid'] and e['returncode']==receipt['caller_returncode'] for i,e in enumerate(trace)))
            if obligation['terminal']=='deadline_escape':
                for name in ('stdout','stderr'):
                    data=outputs[name];saved=receipt['streams'][name]
                    check('declared incomplete capture is bounded real prefix '+name,data==b'R'*len(data) and len(data)<=64 and type(saved['eof']) is bool)
                    reads=[e for e in events('read') if e['tag']=='caller:'+name]
                    check('incomplete capture matches all consumed input '+name,sum(e['bytes'] for e in reads)==len(data) and all(e['sha256']==hashlib.sha256(b'R'*e['bytes']).hexdigest() for e in reads))
                    check('incomplete EOF never inferred '+name,saved['eof']==any(e['bytes']==0 for e in reads))
    elif case['kind']=='observer':
        check('one full raw observer journal',len(report['journal'])==1)
        record=report['journal'][0]
        check('complete observer raw fields',set(record)=={'command','start_monotonic_ns','pid','returncode','reaped','eof','overflow','end_monotonic_ns','errors','stdout_hex','stderr_hex'})
        raw=bytes.fromhex(record['stdout_hex']); err=bytes.fromhex(record['stderr_hex'])
        check('raw observer bounds',len(raw)<=262145 and len(err)<=262145)
        line=b'123 1 123 Wed Sep 30 00:00:00 2026\n'
        fixed={'ps_duplicate':(line+line,b''),'ps_malformed':(b'123 1 123 Wed Sep\n',b''),'ps_nonascii':(b'\xff\n',b''),'ps_empty':(b'',b''),'ps_nonzero':(line,b''),'ps_stderr':(line,b'ps-inert-stderr\n'),'ps_overflow':(b'x'*262145,b''),'ps_timeout':(line,b'')}
        if f in fixed:
            check('entire independent fixed observer operands',(raw,err)==fixed[f])
        if f=='ps_nonzero':check('actual observer nonzero code',record['returncode']==9 and record['reaped'] is True)
        if f=='ps_overflow':check('exact observer first excess',record['overflow']=={'stdout':120} and record['eof']['stdout'] is False)
        if f=='ps_timeout':check('actual observer work cutoff',record['end_monotonic_ns']-record['start_monotonic_ns']>=200000000 and record['reaped'] is True)
        if case['expect']=='rows':
            rows={}
            for line in raw.decode('ascii').splitlines():
                v=line.split()
                check('independent observer row shape',len(v)==8 and all(x.isdigit() for x in v[:3]))
                pid,ppid,pgid=map(int,v[:3]); check('independent observer ids',pid>0 and ppid>=0 and pgid>=0 and str(pid) not in rows)
                rows[str(pid)]={'pid':pid,'ppid':ppid,'pgid':pgid,'birth':' '.join(v[3:])}
            check('whole independently parsed row map',P.canonical(rows)==P.canonical(report['return']) and bool(rows) and report['exception'] is None and not record['errors'] and record['returncode']==0 and record['reaped'] is True and all(record['eof'].values()) and not err)
            if f=='ps_max':check('exact observer cap',len(raw)==262144)
        else:
            check('observer refusal complete',report['exception'] is not None and report['exception']['type']=='Refusal' and bool(record['errors']))
            first_ps=record['errors'][0]
            expected={'ps_duplicate':'Refusal: ps identifiers','ps_malformed':'Refusal: ps row shape','ps_empty':'Refusal: ps empty table','ps_nonzero':'Refusal: ps observation failed','ps_stderr':'Refusal: ps observation failed','ps_overflow':'ps stdout cap','ps_timeout':'ps work deadline'}
            if f=='ps_nonascii':check('nonascii exact parser failure',first_ps.startswith('UnicodeDecodeError:'))
            elif f in expected:check('exact observer first predicate',first_ps==expected[f])
            else:
                stage='register' if f.endswith('.registration') else 'pump'
                msg='RI167_F01_REGISTER' if stage=='register' else 'RI167_F01_READ'
                check('exact observer fault first',first_ps=='ps '+stage+':'+stream+': OSError: '+msg)
                injected=exact_input_injection('register_error' if stage=='register' else 'read_error',msg)
                check('observer owns exact bounded reap',record['reaped'] is True and type(record['returncode']) is int and any(e['kind']=='ps' and e['pid']==record['pid'] for e in events('popen_acquired')))
                invocation=events('observer_entry')
                check('literal observer call deadline recorded',len(invocation)==1 and type(invocation[0]['deadline_monotonic_ns']) is int and 0<invocation[0]['deadline_monotonic_ns']-invocation[0]['monotonic_ns']<=400000000)
                finish=min(invocation[0]['deadline_monotonic_ns'],record['start_monotonic_ns']+400000000)
                check('observer own successful poll inside original finish deadline',any(i>injected and e['event']=='poll' and e['kind']=='ps' and e['pid']==record['pid'] and e['returncode']==record['returncode'] and e['monotonic_ns']<=finish for i,e in enumerate(trace)))
                check('observer complete timestamps',record['start_monotonic_ns']<=record['end_monotonic_ns']<=report['entry_end_monotonic_ns'])
                check('failed observer stream unread and no false EOF',bytes.fromhex(record[stream+'_hex'])==b'' and record['eof'][stream] is False)
                other='stdout' if stream=='stderr' else 'stderr'
                check('healthy observer sibling preserved',bytes.fromhex(record[other+'_hex'])==(b'123 1 123 Wed Sep 30 00:00:00 2026\n' if other=='stdout' else b'ps-inert-stderr\n') and record['eof'][other] is True)
                check('failed observer pump disabled',not any(i>injected for i in indices('read',input_tag)))
                if f.endswith('.registration'):
                    stops=indices('unregister_attempt',input_tag);closes=indices('pipe_closed',input_tag)
                    check('observer partial registration cleanup reached',len(closes)==1 and any(injected<i<closes[0] for i in stops))
                if f.endswith('.unregister_close'):
                    check('observer independent cleanup errors',any(x=='ps unregister:'+stream+': OSError: RI171_UNREGISTER' for x in record['errors']) and any(x=='ps pipe_close:'+stream+': OSError: RI171_PIPE_CLOSE' for x in record['errors']))
                    u=exact_input_injection('unregister_error','RI171_UNREGISTER');c=exact_input_injection('pipe_close_error','RI171_PIPE_CLOSE')
                    check('observer same-pipe cleanup order',injected<u<c and any(i>c for i in indices('pipe_closed',input_tag)))
                    expected_errors=['ps pump:'+stream+': OSError: RI167_F01_READ', 'ps unregister:'+stream+': OSError: RI171_UNREGISTER', 'ps pipe_close:'+stream+': OSError: RI171_PIPE_CLOSE']
                    check('compound observer retained ordered primary and secondary errors',record['errors'][:3]==expected_errors and all(record['errors'].count(want)==1 for want in expected_errors))
                    compound_cleanup_lifetime(injected,u,c,record['pid'])
    else:
        check('direct refusal observed',report['exception'] is not None and report['exception']['type']=='Refusal')
        operands=events('direct_operand');check('complete direct operands',len(operands)==1)
        base={'pid':12001,'ppid':1,'pgid':12001,'birth':'Wed Sep 30 00:00:00 2026'}
        expected_table={'12001':dict(base)}; expected_known={'12001':dict(base)}
        if f=='descendant_cap':
            for number in range(12002,12066):
                expected_table[str(number)]={'pid':number,'ppid':12001,'pgid':number,'birth':base['birth']}
        elif f.endswith('birth') or f.endswith('pgid'):
            key='birth' if f.endswith('birth') else 'pgid'
            expected_table['12001'][key]='changed' if key=='birth' else 12002
        else:
            expected_table['12002']={'pid':12002,'ppid':1,'pgid':12001,'birth':base['birth']}
            if f=='identity_safe_second':
                b={'pid':13001,'ppid':1,'pgid':13001,'birth':base['birth']}
                expected_table['13001']=dict(b); expected_known['13001']=dict(b)
        check('full literal direct operands',P.canonical(operands[0]['table'])==P.canonical(expected_table) and P.canonical(operands[0]['known'])==P.canonical(expected_known))
        if f=='descendant_cap':
            check('descendant cap exact',report['exception']['message']=='observed descendant count cap' and len(operands[0]['table'])==65)
        elif f in ('identity_birth','identity_pgid'):
            check('discover identity exact',report['exception']['message']=='observed PID identity/group changed')
        elif f in ('identity_signal_birth','identity_signal_pgid'):
            check('signal identity exact',report['exception']['message']=='signal identity/group mismatch for 12001' and not events('signal_double'))
        else:
            check('unsafe group refusal',report['exception']['message']=='group contains unverified process: 12001')
            signals=events('signal_double')
            check('safe second independently signalled', [e['pgid'] for e in signals]==([13001] if f=='identity_safe_second' else []))
    # Identity-complete fixture recovery is separate from subject reap/cleanup.
    acquired=events('popen_acquired')
    check('acquired handle ordinals',all(set(e)=={'event','monotonic_ns','handle_id','kind','pid'} and type(e['handle_id']) is int and e['handle_id']==i+1 and e['kind'] in ('caller','ps') and type(e['pid']) is int and e['pid']>1 for i,e in enumerate(acquired)))
    recovery=report['recovery']
    check('complete recovery list',type(recovery) is list)
    owned=[r for r in recovery if r.get('kind')!='leaf'];leaves=[r for r in recovery if r.get('kind')=='leaf']
    check('every owned handle recovered exactly once in acquisition order',len(owned)==len(acquired) and len(recovery)==len(owned)+len(leaves))
    for actual,expected in zip(owned,acquired):
        check('recovery exact acquired identity '+str(expected['handle_id']),type(actual.get('handle_id')) is int and type(actual.get('pid')) is int and type(actual.get('kind')) is str and {k:actual.get(k) for k in ('handle_id','kind','pid')}=={k:expected[k] for k in ('handle_id','kind','pid')})
        if 'error' in actual:
            check('closed owned recovery failure',set(actual)=={'handle_id','kind','pid','error'} and type(actual['error']) is str and bool(actual['error']))
        else:
            check('closed owned recovery observation',set(actual)=={'handle_id','kind','pid','returncode','reaped'} and type(actual['reaped']) is bool and (type(actual['returncode']) is int or actual['returncode'] is None) and actual['reaped']==(actual['returncode'] is not None))
    needs_leaf=f in ('observed_descendant','fast_reparent')
    check('complete leaf obligation membership',len(leaves)==(1 if needs_leaf else 0) and (not leaves or recovery[-1] is leaves[0]))
    if needs_leaf:
        leaf=leaves[0];names={r['path'] for r in actual_tree}
        check('leaf never claims resolved recovery',leaf.get('requires_external_recovery_review') is True)
        if 'RECOVERY_IDENTITY.json' not in names:
            check('honest unavailable leaf identity',leaf=={'kind':'leaf','identity_unavailable':True,'requires_external_recovery_review':True})
        else:
            identity=load('body/RECOVERY_IDENTITY.json',4096);child=load('body/LEAF.json',4096)
            check('retained original leaf scope',set(identity)=={'pid','ppid','pgid','birth'} and set(child)=={'pid','ppid','pgid'} and identity['pid']==child['pid']==identity['pgid']==child['pgid'])
            check('leaf recovery stable recorded identity',all(leaf['identity'][k]==identity[k] for k in ('pid','pgid','birth')))
            if 'error' in leaf:
                check('closed failed leaf recovery',set(leaf)=={'kind','identity','error','requires_external_recovery_review'} and P.canonical(leaf['identity'])==P.canonical(identity) and type(leaf['error']) is str and bool(leaf['error']))
            else:
                check('closed unresolved signalled leaf',set(leaf)=={'kind','identity','kill_sent','absence_proven','requires_external_recovery_review'} and leaf['kill_sent'] is True and leaf['absence_proven'] is False)
                signals=events('leaf_recovery_signal')
                check('exact actual leaf signal evidence',len(signals)==1 and signals[0]['signal']==9 and P.canonical(signals[0]['identity'])==P.canonical(leaf['identity']))
                observations=events('recovery_identity_observation')
                check('leaf fresh matching identity before signal',len(observations)==2 and observations[1]['monotonic_ns']<=signals[0]['monotonic_ns'])
                raw=bytes.fromhex(observations[1]['stdout_hex']);fields=raw.decode('ascii').split()
                check('complete leaf current observation',observations[1]['pid']==identity['pid'] and observations[1]['returncode']==0 and not bytes.fromhex(observations[1]['stderr_hex']) and len(fields)==8 and all(x.isdigit() for x in fields[:3]))
                observed={'pid':int(fields[0]),'ppid':int(fields[1]),'pgid':int(fields[2]),'birth':' '.join(fields[3:])}
                check('leaf full fresh identity equals recovery row',P.canonical(observed)==P.canonical(leaf['identity']))
    for observed in pins:
        _, current_pin, _ = P.capture(observed['path'], 67108864)
        check('final read-set identity '+observed['path'], current_pin == observed)
    final_custody, final_failures = P.postcheck(req, current['request']['path'], current['request']['sha256'])
    check('final complete current custody', not final_failures and P.canonical(final_custody) == P.canonical(current))
    check('final complete body namespace', P.canonical(P.tree(os.path.join(op,'body'))) == P.canonical(actual_tree))
    incomplete=[r for r in report['recovery'] if r.get('requires_external_recovery_review') or r.get('reaped') is False or 'error' in r]
    return {'schema':'ri171-independent-saved-case-check-v1','status':'FINITE_CASE_MATCHED_REQUIRES_ROOT_ORIGIN_AND_RECOVERY_REVIEW' if incomplete else 'FINITE_CASE_MATCHED_REQUIRES_ROOT_GENUINE_ORIGIN_REVIEW',
            'case_id':case['id'],'checks':checks,'read_inputs':pins,'entry_duration_seconds':duration,'monitor_review':monitor_review,
            'external_recovery_obligations':incomplete,'saved_observations_only':True,'subject_reexecuted':False,
            'authorship':'Same author as driver; independent saved interpretation, not nonauthor acceptance.',
            'qualification_acceptance':False,'native_or_scientific_acceptance':False}


def main():
    if len(sys.argv)!=7 or sys.argv[1]!='--request' or sys.argv[3]!='--request-sha256' or sys.argv[5]!='--output':
        raise ValueError('fixed saved-checker invocation')
    P=bootstrap(sys.argv[2],sys.argv[4])
    out=os.path.abspath(sys.argv[6])
    P.need(os.path.dirname(os.path.dirname(out))==P.BASE and os.path.basename(os.path.dirname(out)).startswith('ri171-saved-review-'), 'separate reviewer output reservation')
    req,case,_,current=P.request(sys.argv[2],sys.argv[4])
    value=inspect(P,req,case,current)
    P.put(out,value)
    return 0


if __name__=='__main__':
    sys.exit(main())
