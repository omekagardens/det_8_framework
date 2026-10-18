import fs from 'node:fs'; import crypto from 'node:crypto';
const B='/Volumes/AI_DATA/development/det-review-evidence',D=B+'/ri171-supervisor-qualification-source-zksymhs1',S=B+'/ri169-write-would-block-repair-7_868hay',R=B+'/ri168-root-coupling-review-jihb5l4y';
const pin=path=>{const b=fs.readFileSync(path);return {path,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')}};
const assignment={path:R+'/RI171_SUPERVISOR_QUALIFICATION_ASSIGNMENT.json',bytes:2251,sha256:'022920bd238bf262570246467a738e2b52451b74686f011d659eb5512d692e7c'};
const decision={path:R+'/RI169_ROOT_ADJUDICATION.json',bytes:1087,sha256:'f5247462bb582f4fcc67461d5b4ec5d7c8379f271e1d89c20e8f98e1ffc1a87f'};
for(const e of [assignment,decision])if(JSON.stringify(e)!==JSON.stringify(pin(e.path)))throw Error('authentication '+e.path);
const handoff=JSON.parse(fs.readFileSync(S+'/HANDOFF.json')); for(const e of handoff.payloads)if(JSON.stringify(e)!==JSON.stringify(pin(e.path)))throw Error('predecessor '+e.path);
const rootDecision=JSON.parse(fs.readFileSync(decision.path)); for(const key of ['subject','review','actual_metadata_check']){const e=rootDecision[key];if(!['path','bytes','sha256'].every(k=>e[k]===pin(e.path)[k]))throw Error('decision premise '+key)}
const save=(n,o)=>fs.writeFileSync(D+'/'+n,JSON.stringify(o,null,2)+'\n',{flag:'wx'});
save('AUTHENTICATION.json',{schema:'ri171-preparation-authentication-v1',assignment,decision,predecessor_handoff:pin(S+'/HANDOFF.json'),predecessor_payloads:handoff.payloads,root_review:rootDecision.review,root_metadata:rootDecision.actual_metadata_check,passed:true,current_runtime_observed:false});
const cases=[];
function add(id,kind,fault,expect,predicate,extra={}){cases.push({id,group:id.split('.')[0],kind,fault,expect,predicate,scope:kind==='direct'?'Exact exported function with declared finite operands/doubles':kind==='observer'?'Exact process_snapshot with declared observer command/I/O doubles':'Whole captured RI169 module supervise with inert ARGV/PREFIX and declared fault instrumentation',...extra,executed:false})}
add('S01.healthy','whole','none','captured','Real owned inert process, full ordinary capture and cleanup');
add('S02.timer','whole','timer','captured','Actual parent active timer and actual inert child zero timer');
add('S03.nonzero','whole','nonzero','failed','Actual caller returncode is nonzero');
add('S03.stderr','whole','stderr','failed','Actual nonempty caller stderr');
for(const stream of ['stdout','stderr'])for(const suffix of ['exact','excess'])add(`S04.${stream}.${suffix}`,'whole','cap_'+stream+'_'+suffix,stream==='stdout'&&suffix==='exact'?'captured':'failed','Exact8MiB per-stream capture and first excess byte',{stream});
add('S04.dual.excess','whole','cap_dual_excess','failed','Both per-stream capture caps; explicit first excess and comparable sibling');
for(const fault of ['real','duplicate','malformed','nonascii','empty','nonzero','stderr','overflow','timeout'])add('S05.observer.'+fault,'observer','ps_'+fault,fault==='real'?'rows':'refusal','Whole observer raw capture/parser '+fault);
add('S06.observed_descendant','whole','observed_descendant','failed','Real separate-session descendant observed while parent lives, then rejected and recovered');
add('S07.fast_reparent','whole','fast_reparent','failed','Caller exits before first observation; no complete-fork coverage');
for(const fault of ['birth','pgid','unverified_member','safe_second'])add('S08.'+fault,'direct','identity_'+fault,'refusal','Exact discover/signal_observed identity/group branch');
add('S09.real_cutoffs','whole','real_cutoffs','failed','Actual310 TERM and312 KILL under original315 bound',{clock:'real'});
add('S09.real_expiry','whole','real_expiry','hard','Actual315 hard timer with explicit stale-observer double',{clock:'real; stale table is a declared double, not real nonreap'});
for(const stream of ['stdout','stderr','processes'])for(const fault of ['fsync','close','replacement','drift'])add(`S10.${stream}.${fault}`,'whole','late_'+fault,'failed','Exact independent final '+fault+' after earlier actual nonzero caller',{stream,earlier_nonzero:true});
for(const fault of ['preexists','partial','fsync','base_sync','post_receipt'])add('S11.'+fault,'whole','receipt_'+fault,fault==='preexists'?'failed':'escape','Final receipt exclusive/partial/durability/late escape boundary');
for(const fault of ['ownership','drain','finalization'])add('S12.'+fault,'whole','hard_'+fault,'hard','Actual production HardStop path; separate fixture recovery');
add('S13.journal_cap','whole','journal_cap','failed','Actual journal cap predicate with oversized canonical-output double');
add('S13.descendant_cap','direct','descendant_cap','refusal','Actual discover sixty-four-known cap');
add('S13.ps_max','observer','ps_max','rows','Actual262144-byte observer capture and parser via inert producer');
add('S13.late_observer','whole','late_observer','failed','Second real-observation call substituted refusal');
const retained=JSON.parse(fs.readFileSync(S+'/FOCUSED_VARIANTS.json'));
for(const r of retained.variants){let kind='whole', fault=r.id, expect='failed'; if(r.id.startsWith('S05.ps.')||r.id.startsWith('S10.ps.'))kind='observer'; if(r.id.endsWith('.short_write'))expect='failed'; add(r.id,kind,fault,kind==='observer'?'refusal':expect,'Exact retained RI167 recipe '+r.id,{inherited_recipe:r,clock:r.id.endsWith('nonreap')||r.id==='S13.deadline_exhausted'?'Explicit branch clock double; no real deadline credit':'real'});}
for(const r of JSON.parse(fs.readFileSync(S+'/WRITE_READ_VARIANTS.json')).variants)add(r.id,'whole',r.id,'failed','Exact RI169 recipe '+r.id,{inherited_recipe:r});
if(new Set(cases.map(c=>c.id)).size!==cases.length)throw Error('duplicate case');
save('CASE_MANIFEST.json',{schema:'ri171-supervisor-case-manifest-v1',status:'SOURCE_ONLY_UNEXECUTED',groups:Array.from({length:13},(_,i)=>'S'+String(i+1).padStart(2,'0')),retained_recipes:28,added_RI169_recipes:6,base_cases:cases.length-34,total_cases:cases.length,subject:handoff.source,cases,real_clock_cases:['S09.real_cutoffs','S09.real_expiry'],scope:'Finite supervisor qualification only. Each case carries declared substitutions; neither positive synthetic branch nor external fixture recovery proves native qualification, hermetic execution or complete descendant coverage.'});
console.log(JSON.stringify({passed:true,cases:cases.length,base_cases:cases.length-34,recipe_cases:34,subject:handoff.source}));
