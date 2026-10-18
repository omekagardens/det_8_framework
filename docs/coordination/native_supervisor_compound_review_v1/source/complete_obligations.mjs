import fs from 'node:fs';const D='/Volumes/AI_DATA/development/det-review-evidence/ri176-supervisor-qualification-repair-3ausb2jo';let t=fs.readFileSync(D+'/check_saved.py','utf8');
function r(a,b){if(t.split(a).length!==2)throw Error('missing/nonunique '+a.slice(0,90));t=t.replace(a,b)}
r("        else:\n            check('declared whole escape has no return',report['return'] is None)","        else:\n            check('declared whole escape has no return',report['return'] is None)\n            if obligation['terminal']=='hard_escape' or (obligation['terminal']=='missing_identity_choice' and receipt is None):\n                check('hard escape has no invented receipt',receipt is None and 'completion.json' not in outputs)");
r("            check('retained original write prefix',outputs[stream]==b'R'*(17 if f.endswith('.partial_write') else 0))", "            check('retained original write prefix',outputs[stream]==b'R'*(17 if f.endswith('.partial_write') else 0))");
// Applies to both would-block and ordinary write recipes, independently of branch summaries.
r("        if f.endswith('.unregister_close'):\n            tags='caller:'+stream",`        if f.endswith('.write') or f.endswith('.partial_write') or '.write_would_block.' in f:
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
            tags='caller:'+stream`);
r("            if f.endswith('already_exited'):\n                check('real exited reap retained',receipt['caller_reaped'] is True and receipt['caller_returncode']==0)",`            if f.endswith('already_exited'):
                check('real exited reap retained',receipt['caller_reaped'] is True and receipt['caller_returncode']==0)
                exited=events('inert_pre_observer_exit')
                check('already reaped handle is never killed',len(exited)==1 and exited[0]['pid']==receipt['caller_pid'] and exited[0]['returncode']==0 and not [e for e in events('direct_kill_attempt') if e['kind']=='caller'])`);
r("            check('no group cleanup from direct reap',receipt['observed_cleanup'] is False)",`            check('no group cleanup from direct reap',receipt['observed_cleanup'] is False)
            if not f.endswith('already_exited'):
                attempts=[i for i,e in enumerate(trace) if e['event']=='direct_kill_attempt' and e['kind']=='caller' and e['pid']==receipt['caller_pid']]
                check('fallback owned kill attempt retained',len(attempts)==1)
                if obligation['subject_reap']=='reaped':
                    check('fallback independent owned poll after kill',any(i>attempts[0] and e['event']=='poll' and e['kind']=='caller' and e['pid']==receipt['caller_pid'] and e['returncode']==receipt['caller_returncode'] for i,e in enumerate(trace)))`);
r("                check('healthy observer sibling preserved',bytes.fromhex(record[other+'_hex'])==(b'123 1 123 Wed Sep 30 00:00:00 2026\\n' if other=='stdout' else b'ps-inert-stderr\\n') and record['eof'][other] is True)",`                check('healthy observer sibling preserved',bytes.fromhex(record[other+'_hex'])==(b'123 1 123 Wed Sep 30 00:00:00 2026\\n' if other=='stdout' else b'ps-inert-stderr\\n') and record['eof'][other] is True)
                check('failed observer pump disabled',not any(i>injected for i in indices('read',input_tag)))
                if f.endswith('.registration'):
                    stops=indices('unregister_attempt',input_tag);closes=indices('pipe_closed',input_tag)
                    check('observer partial registration cleanup reached',len(closes)==1 and any(injected<i<closes[0] for i in stops))`);
fs.writeFileSync(D+'/check_saved.py',t);
