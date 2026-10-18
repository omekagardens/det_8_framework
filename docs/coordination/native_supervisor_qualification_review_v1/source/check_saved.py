"""RI171 separately implemented saved-record oracle; same author, not nonauthor review.
No subject, worker, payload or control execution. Root supplies genuine outer provenance.
"""
import hashlib
import json
import os
import sys
import types


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
        'hard_injection':{'phase'}, 'fsync_attempt':{'tag'}, 'file_mutation':{'tag','fault'},
        'close_attempt':{'tag'}, 'file_acquired':{'tag','path','fd'}, 'sync_base_attempt':{'ordinal'},
        'fixture_directory_sync':{'path'}, 'source_error':{'stage','type','message'}, 'receipt_candidate':{'value'},
        'canonical_double':{'bytes','value'}, 'journal_candidate':{'value'}, 'ready_barrier':{'path'},
        'recovery_identity_observation':{'pid','returncode','stdout_hex','stderr_hex'},
        'popen_attempt':{'kind','subject_argv','actual_argv','parent_timer'},
        'popen_acquired':{'kind','pid'}, 'inert_pre_observer_exit':{'pid','returncode'},
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
            check('read injection reached',any(e.get('tag')=='caller:'+stream for e in events('read_error')))
        elif f.endswith('.write') or f.endswith('.partial_write'):
            primary('pump:'+stream,'OSError','RI167_F01_PARTIAL_WRITE' if f.endswith('.partial_write') else 'RI167_F01_WRITE')
            check('retained original write prefix',outputs[stream]==b'R'*(17 if f.endswith('.partial_write') else 0))
        elif f.endswith('.registration'):
            primary('register:'+stream,'OSError','RI167_F01_REGISTER')
            check('real registration installed first',any(e.get('tag')=='caller:'+stream for e in events('register_installed')))
        elif f.endswith('.short_write') or '.read_would_block.' in f:
            primary('supervision','Refusal','caller outer stderr nonempty')
            check('positive pump exact bytes',outputs['stdout']==outputs['stderr']==b'R'*64 and receipt['streams']['stdout']['eof'] is True and receipt['streams']['stderr']['eof'] is True)
            if '.read_would_block.' in f:
                check('exactly one transient read',len([e for e in events('read_error') if e.get('message')=='RI169_READ_TRANSIENT'])==1)
                check('intact postrace read',any(e.get('tag')=='caller:'+stream and e.get('bytes')==64 for e in events('read')))
            else:
                check('actual short writes reached',any(e.get('tag')==stream and 0<e['written']<e['requested'] for e in events('write')))
        elif f.startswith(('S05.fallback.','S13.observer.')) or f in ('S13.poll_unavailable','S13.deadline_exhausted'):
            primary('supervision','Refusal','RI171_OBSERVER_FAILURE')
        elif f.startswith(('S10.journal.','S13.journal.')):
            primary('supervision','Refusal','ps journal: OSError: RI171_JOURNAL_WRITE')
            check('real partial journal write',len(outputs['processes.jsonl'])==17 and any(e.get('tag')=='processes' for e in events('write_error')))
        elif f=='nonzero' or f.startswith('late_'):
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
            check('first real observer precedes late fault',bool(events('discover')) and events('observer_double')[0]['ordinal']==2)
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
        if f.endswith('.unregister_close'):
            tags='caller:'+stream
            check('all failing cleanups and retry',len([e for e in events('unregister_error') if e['tag']==tags])==1 and len([e for e in events('pipe_close_error') if e['tag']==tags])==1 and any(e['tag']==tags for e in events('pipe_closed')))
        if f.startswith(('S04.','S05.caller.','S10.caller.')) and not f.endswith('.short_write') and '.read_would_block.' not in f:
            other='stdout' if stream=='stderr' else 'stderr'
            check('healthy sibling retained',outputs[other]==b'R'*64 and receipt['streams'][other]['eof'] is True)
            check('failed stream never claims EOF',receipt['streams'][stream]['eof'] is False)
            if f.endswith('.read') or f.endswith('.registration') or f.endswith('.unregister_close'):
                check('failed unread stream has no invented bytes',outputs[stream]==b'')
            failure_indices=[i for i,e in enumerate(trace) if e['event'] in ('write_error','read_error','register_error') and e.get('tag') in (stream,'caller:'+stream)]
            check('failed pump not read after refusal',bool(failure_indices) and not any(e['event']=='read' and e.get('tag')=='caller:'+stream for e in trace[failure_indices[0]+1:]))
        if f.startswith('late_'):
            expected='readback' if f in ('late_drift','late_size','late_descriptor','late_replacement') else f.split('_')[1]
            check('late intended predicate reached',any(e['stage']==expected+':'+stream for e in receipt['errors'][1:]))
            check('all comparable final file checks',all(any(e.get('tag')==name for e in events('close_attempt')) for name in ('stdout','stderr','processes')))
        if f.startswith(('S05.fallback.','S13.observer.','S10.journal.','S13.journal.')) or f in ('S13.poll_unavailable','S13.deadline_exhausted'):
            if f.endswith('already_exited'):
                check('real exited reap retained',receipt['caller_reaped'] is True and receipt['caller_returncode']==0)
            elif f.endswith('nonreap') or f=='S13.deadline_exhausted':
                check('declared branch clock no fabricated reap',receipt['caller_reaped'] is False and any(e['stage']=='direct_handle_reap' for e in receipt['errors']) and bool(events('poll_double') or events('clock_double')))
            elif f=='S13.poll_unavailable':
                check('independent reap attempt failure',bool(events('poll_error')) and any(e['stage']=='direct_handle_reap' for e in receipt['errors']))
            else:
                check('independent owned reap',receipt['caller_reaped'] is True and bool([e for e in events('poll') if e['kind']=='caller' and e['returncode'] is not None]))
            check('no group cleanup from direct reap',receipt['observed_cleanup'] is False)
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
                check('failed observer stream unread and no false EOF',bytes.fromhex(record[stream+'_hex'])==b'' and record['eof'][stream] is False)
                other='stdout' if stream=='stderr' else 'stderr'
                check('healthy observer sibling preserved',bytes.fromhex(record[other+'_hex'])==(b'123 1 123 Wed Sep 30 00:00:00 2026\n' if other=='stdout' else b'ps-inert-stderr\n') and record['eof'][other] is True)
                if f.endswith('.unregister_close'):
                    check('observer independent cleanup errors',any(x.startswith('ps unregister:'+stream+':') for x in record['errors']) and any(x.startswith('ps pipe_close:'+stream+':') for x in record['errors']))
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
