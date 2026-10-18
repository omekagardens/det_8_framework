// Literal Python source edits only. No import, compilation, AST, fixture, or execution.
import fs from 'node:fs';const D='/Volumes/AI_DATA/development/det-review-evidence/ri182-compound-cleanup-oracle-repair-6835ytb8';
let p=fs.readFileSync(D+'/protocol.py','utf8');const from="SOURCE_DIRECTORY = BASE + '/ri176-supervisor-qualification-repair-3ausb2jo'",to="SOURCE_DIRECTORY = BASE + '/ri182-compound-cleanup-oracle-repair-6835ytb8'";if(p.split(from).length!==2)throw Error('directory literal');fs.writeFileSync(D+'/protocol.py',p.replace(from,to));
let t=fs.readFileSync(D+'/check_saved.py','utf8');function r(a,b){if(t.split(a).length!==2)throw Error('missing/nonunique literal '+a.slice(0,80));t=t.replace(a,b)}
const helper=`    def compound_cleanup_lifetime(read, unregister, close_error, subject_pid):
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
`;
r("    duration = (report['entry_end_monotonic_ns'] - report['entry_start_monotonic_ns'])/1000000000",helper+"    duration = (report['entry_end_monotonic_ns'] - report['entry_start_monotonic_ns'])/1000000000");
const old="            check('all failing cleanups same pipe order and retry',read<u<c and any(i>c for i in indices('pipe_closed',tags)))";
const addition=`
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
            compound_cleanup_lifetime(read,u,c,receipt['caller_pid'])`;
r(old,old+addition);
const observer="                    check('observer same-pipe cleanup order',injected<u<c and any(i>c for i in indices('pipe_closed',input_tag)))";
r(observer,observer+`\n                    expected_errors=['ps pump:'+stream+': OSError: RI167_F01_READ', 'ps unregister:'+stream+': OSError: RI171_UNREGISTER', 'ps pipe_close:'+stream+': OSError: RI171_PIPE_CLOSE']
                    check('compound observer retained ordered primary and secondary errors',record['errors'][:3]==expected_errors and all(record['errors'].count(want)==1 for want in expected_errors))
                    compound_cleanup_lifetime(injected,u,c,record['pid'])`);
fs.writeFileSync(D+'/check_saved.py',t);
console.log(JSON.stringify({changed:['protocol.py','check_saved.py'],source_only:true,executed_cases:0}));
