// Source-text repair, not Python parsing, qualification, or fixture generation.
import fs from 'node:fs';
const D='/Volumes/AI_DATA/development/det-review-evidence/ri176-supervisor-qualification-repair-3ausb2jo';
const cases=JSON.parse(fs.readFileSync(D+'/CASE_MANIFEST.json')).cases;
const late=['late_fsync','late_close','late_replacement','late_descriptor','late_drift','late_size'];
const budget=['S13.observer.nonreap','S13.journal.nonreap','S13.deadline_exhausted'];
const receipt=['receipt_preexists','receipt_partial','receipt_fsync','receipt_base_sync','receipt_post_receipt'];
const hard=['hard_ownership','hard_drain','hard_finalization','real_expiry'];
const quote=s=>JSON.stringify(s);
const rows=cases.map(c=>{const f=c.fault,s=c.stream|| (f.includes('.stderr.')?'stderr':'stdout');let terminal=c.kind, healthy={},reap='none';
if(c.kind==='whole'){
 terminal=receipt.includes(f)?'receipt_escape':hard.includes(f)?'hard_escape':budget.includes(f)?'deadline_escape':f==='fast_reparent'?'missing_identity_choice':'ordinary';
 reap=(budget.includes(f)||f==='S13.poll_unavailable')?'incomplete':(hard.includes(f)||f==='receipt_preexists')?'not_required':'reaped';
 if(terminal==='ordinary'){
  if(['none','timer','nonzero','late_observer'].includes(f))healthy={stdout:64,stderr:0};
  else if(f==='stderr'||late.includes(f)||f.startsWith('S05.fallback.')||f.startsWith('S10.journal.')||f.startsWith('S13.'))healthy={stdout:64,stderr:64};
  else if(f.startsWith('S04.')||f.startsWith('S05.caller.')||f.startsWith('S10.caller.'))healthy=f.endsWith('.short_write')||f.includes('.read_would_block.')?{stdout:64,stderr:64}:{[s==='stdout'?'stderr':'stdout']:64};
  else if(f==='cap_stdout_exact')healthy={stdout:8388608,stderr:0};
  else if(f==='cap_stdout_excess')healthy={stderr:0};
  else if(f==='cap_stderr_exact')healthy={stdout:0,stderr:8388608};
  else if(f==='cap_stderr_excess')healthy={stdout:0};
  else if(['observed_descendant','real_cutoffs','journal_cap'].includes(f))healthy={stdout:0,stderr:0};
  if(late.includes(f))delete healthy[s];
 }
}
return {id:c.id,kind:c.kind,fault:f,terminal,input_tag:(c.kind==='observer'?'ps':'caller')+':'+s,healthy,subject_reap:reap};});
// Literal finite map is inside the pinned checker, no new mutable policy input.
let map='\nLATE_FILES = '+JSON.stringify(late).replace('[','(').replace(']',',)')+'\n';
map+='CASE_OBLIGATIONS = {\n'+rows.map(r=>'    '+quote(r.id)+': '+JSON.stringify({kind:r.kind,fault:r.fault,terminal:r.terminal,input_tag:r.input_tag,healthy:r.healthy,subject_reap:r.subject_reap})+',').join('\n')+'\n}\n';
let t=fs.readFileSync(D+'/check_saved.py','utf8');
function r(a,b){if(t.split(a).length!==2)throw Error('literal nonunique '+a.slice(0,80));t=t.replace(a,b)}
r('import types\n','import types\n'+map);
r("'hard_injection':{'phase'}, 'fsync_attempt':{'tag'}, 'file_mutation':{'tag','fault'},", "'hard_injection':{'phase'}, 'fsync_attempt':{'tag'}, 'fsync_complete':{'tag'},\n        'file_mutation':{'tag','fault','before','after','before_first_byte'}, 'close_complete':{'tag'},\n        'sync_base_complete':{'ordinal'}, 'leaf_recovery_signal':{'identity','signal'},");
r("'popen_acquired':{'kind','pid'}", "'popen_acquired':{'handle_id','kind','pid'}");
r("    events = lambda name: [e for e in trace if e['event'] == name]", "    events = lambda name: [e for e in trace if e['event'] == name]\n    obligation = CASE_OBLIGATIONS[case['id']]\n    check('finite exact case obligation', obligation['kind'] == case['kind'] and obligation['fault'] == f)\n    input_tag = obligation['input_tag']\n    def indices(event, tag=None):\n        return [i for i,e in enumerate(trace) if e['event']==event and (tag is None or e.get('tag')==tag)]\n    def exact_input_injection(event, message, kind='OSError'):\n        found = [i for i,e in enumerate(trace) if e['event']==event and e.get('message')==message]\n        check('exact role stream injection '+message, len(found)==1 and trace[found[0]]['tag']==input_tag and trace[found[0]]['type']==kind)\n        at=found[0]\n        check('same pipe registered before injection '+message, any(i<at for i in indices('register_installed',input_tag)))\n        return at");
r("    if case['kind']=='whole' and case['expect'] in ('captured','failed'):\n        check('whole receipt required',receipt is not None)",`    if case['kind']=='whole' and case['expect'] in ('captured','failed'):
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
`);
r("            check('read injection reached',any(e.get('tag')=='caller:'+stream for e in events('read_error')))", "            exact_input_injection('read_error','RI167_F01_READ')");
r("            check('real registration installed first',any(e.get('tag')=='caller:'+stream for e in events('register_installed')))", "            exact_input_injection('register_error','RI167_F01_REGISTER')");
r("                check('exactly one transient read',len([e for e in events('read_error') if e.get('message')=='RI169_READ_TRANSIENT'])==1)\n                check('intact postrace read',any(e.get('tag')=='caller:'+stream and e.get('bytes')==64 for e in events('read')))", `                at=exact_input_injection('read_error','RI169_READ_TRANSIENT','BlockingIOError')
                later=[i for i in indices('read',input_tag) if i>at and trace[i]['bytes']==64 and trace[i]['sha256']==hashlib.sha256(b'R'*64).hexdigest()]
                check('same pipe successful read after transient',len(later)==1)
                through=later[0]
                check('same pipe remains active through retry',not any(e['event'] in ('unregister_attempt','pipe_close_attempt','pipe_closed','register_installed') and e.get('tag')==input_tag for e in trace[at+1:through]))
                check('same pipe EOF follows retry',any(i>through and trace[i]['bytes']==0 for i in indices('read',input_tag)))`);
r("elif f=='nonzero' or f.startswith('late_'):", "elif f=='nonzero' or f in LATE_FILES:");
r("            check('first real observer precedes late fault',bool(events('discover')) and events('observer_double')[0]['ordinal']==2)", `            doubles=indices('observer_double')
            check('dedicated second observer fault',bool(doubles) and [trace[i]['ordinal'] for i in doubles]==list(range(2,len(doubles)+2)) and all(trace[i]['message']=='RI171_OBSERVER_FAILURE' for i in doubles))
            check('successful first real observer precedes late fault',len([e for e in trace[:doubles[0]] if e['event']=='popen_acquired' and e['kind']=='ps'])==1 and any(e['event']=='discover' for e in trace[:doubles[0]]) and monitor_review['raw_records']==1)
            check('late observer retains caller buffers and reap',outputs['stdout']==b'R'*64 and outputs['stderr']==b'' and receipt['caller_reaped'] is True and receipt['observed_cleanup'] is False)`);
r("        if f.startswith('late_'):\n", "        if f in LATE_FILES:\n");
r("            check('all comparable final file checks',all(any(e.get('tag')==name for e in events('close_attempt')) for name in ('stdout','stderr','processes')))", `            check('all comparable final file checks',all(any(e.get('tag')==name for e in events('close_attempt')) for name in ('stdout','stderr','processes')))
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
                    check('fixed complete late stream preimage',original==b'R'*64)`);
r("            check('no group cleanup from direct reap',receipt['observed_cleanup'] is False)", `            check('no group cleanup from direct reap',receipt['observed_cleanup'] is False)
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
                    check('incomplete EOF never inferred '+name,saved['eof']==any(e['bytes']==0 for e in reads))`);
r("                check('exact observer fault first',first_ps=='ps '+stage+':'+stream+': OSError: '+msg)", `                check('exact observer fault first',first_ps=='ps '+stage+':'+stream+': OSError: '+msg)
                injected=exact_input_injection('register_error' if stage=='register' else 'read_error',msg)
                check('observer owns exact bounded reap',record['reaped'] is True and type(record['returncode']) is int and any(e['kind']=='ps' and e['pid']==record['pid'] for e in events('popen_acquired')))
                finish=min(report['entry_start_monotonic_ns']+400000000,record['start_monotonic_ns']+400000000)
                check('observer own successful poll inside original finish deadline',any(i>injected and e['event']=='poll' and e['kind']=='ps' and e['pid']==record['pid'] and e['returncode']==record['returncode'] and e['monotonic_ns']<=finish for i,e in enumerate(trace)))
                check('observer complete timestamps',record['start_monotonic_ns']<=record['end_monotonic_ns']<=report['entry_end_monotonic_ns'])`);
r("                    check('observer independent cleanup errors',any(x.startswith('ps unregister:'+stream+':') for x in record['errors']) and any(x.startswith('ps pipe_close:'+stream+':') for x in record['errors']))", `                    check('observer independent cleanup errors',any(x=='ps unregister:'+stream+': OSError: RI171_UNREGISTER' for x in record['errors']) and any(x=='ps pipe_close:'+stream+': OSError: RI171_PIPE_CLOSE' for x in record['errors']))
                    u=exact_input_injection('unregister_error','RI171_UNREGISTER');c=exact_input_injection('pipe_close_error','RI171_PIPE_CLOSE')
                    check('observer same-pipe cleanup order',injected<u<c and any(i>c for i in indices('pipe_closed',input_tag)))`);
r("            check('all failing cleanups and retry',len([e for e in events('unregister_error') if e['tag']==tags])==1 and len([e for e in events('pipe_close_error') if e['tag']==tags])==1 and any(e['tag']==tags for e in events('pipe_closed')))", `            read=exact_input_injection('read_error','RI167_F01_READ')
            u=exact_input_injection('unregister_error','RI171_UNREGISTER');c=exact_input_injection('pipe_close_error','RI171_PIPE_CLOSE')
            check('all failing cleanups same pipe order and retry',read<u<c and any(i>c for i in indices('pipe_closed',tags)))`);
const recovery=`    # Identity-complete fixture recovery is separate from subject reap/cleanup.
    acquired=events('popen_acquired')
    check('acquired handle ordinals',all(set(e)=={'event','monotonic_ns','handle_id','kind','pid'} and type(e['handle_id']) is int and e['handle_id']==i+1 and e['kind'] in ('caller','ps') and type(e['pid']) is int and e['pid']>1 for i,e in enumerate(acquired)))
    recovery=report['recovery']
    check('complete recovery list',type(recovery) is list)
    owned=[r for r in recovery if r.get('kind')!='leaf'];leaves=[r for r in recovery if r.get('kind')=='leaf']
    check('every owned handle recovered exactly once in acquisition order',len(owned)==len(acquired) and len(recovery)==len(owned)+len(leaves))
    for actual,expected in zip(owned,acquired):
        check('recovery exact acquired identity '+str(expected['handle_id']),{k:actual.get(k) for k in ('handle_id','kind','pid')}=={k:expected[k] for k in ('handle_id','kind','pid')})
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
`;
r("    for observed in pins:\n",recovery+"    for observed in pins:\n");
fs.writeFileSync(D+'/check_saved.py',t);
fs.writeFileSync(D+'/CASE_OBLIGATIONS.json',JSON.stringify({schema:'ri176-finite-obligations-v1',status:'UNEXECUTED_SOURCE_SPECIFICATION',not_operational_input:true,rows},null,2)+'\n',{flag:'wx'});
