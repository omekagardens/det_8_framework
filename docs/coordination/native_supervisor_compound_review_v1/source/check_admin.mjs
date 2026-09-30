// RI176 administrative opaque hashes, literal comparisons, JSON metadata only.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import cp from 'node:child_process';
const B='/Volumes/AI_DATA/development/det-review-evidence',D=B+'/ri176-supervisor-qualification-repair-3ausb2jo',S=B+'/ri171-supervisor-qualification-source-zksymhs1',V=B+'/ri171-independent-supervisor-source-review-fw3b83xu';
const checks=[],seen=new Map();
function check(id,v){checks.push({id,passed:v===true});if(v!==true)throw Error(id)}
function pin(p){let b=fs.readFileSync(p);return {path:p,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')}}
function same(a,b){return a.path===b.path&&a.bytes===b.bytes&&a.sha256===b.sha256}
function verify(x){let p=pin(x.path);check('opaque identity '+x.path,same(p,x));seen.set(x.path,p);return p}
const auth=JSON.parse(fs.readFileSync(D+'/AUTHENTICATION.json'));auth.assignment_and_seals.forEach(verify);verify(auth.review);
for(const p of [S,V]){let h=JSON.parse(fs.readFileSync(p+'/HANDOFF.json'));check('exact sealed namespace '+p,JSON.stringify(fs.readdirSync(p).sort())===JSON.stringify(h.namespace.slice().sort()));h.payloads.forEach(verify);}
const deps=JSON.parse(fs.readFileSync(S+'/DEPENDENCY_BINDINGS.json'));deps.fresh_originals.forEach(verify);
const names=['protocol.py','qualify_supervisor.py','case_worker.py','inert_payload.py','check_saved.py','CASE_MANIFEST.json'];
const old=Object.fromEntries(names.map(n=>[n,fs.readFileSync(S+'/'+n,'utf8')])),now=Object.fromEntries(names.map(n=>[n,fs.readFileSync(D+'/'+n,'utf8')]));
check('manifest exact byte equality',now['CASE_MANIFEST.json']===old['CASE_MANIFEST.json']);
check('driver exact byte equality',now['qualify_supervisor.py']===old['qualify_supervisor.py']);
check('protocol only source-directory relocation',now['protocol.py']===old['protocol.py'].replace("SOURCE_DIRECTORY = BASE + '/ri171-supervisor-qualification-source-zksymhs1'","SOURCE_DIRECTORY = BASE + '/ri176-supervisor-qualification-repair-3ausb2jo'"));
const m=JSON.parse(now['CASE_MANIFEST.json']),o=JSON.parse(fs.readFileSync(D+'/CASE_OBLIGATIONS.json'));
check('all92 literal cases',m.cases.length===92&&new Set(m.cases.map(x=>x.id)).size===92&&m.cases.every(x=>x.executed===false));
check('all34 inherited recipes',m.cases.filter(x=>x.inherited_recipe).length===34);
check('all13 groups',new Set(m.cases.map(x=>x.group)).size===13);
const counts=Object.fromEntries(['whole','observer','direct'].map(k=>[k,m.cases.filter(x=>x.kind===k).length]));check('entry counts69/16/7',counts.whole===69&&counts.observer===16&&counts.direct===7);
check('obligation ordered case bijection',o.rows.length===92&&o.rows.every((r,i)=>r.id===m.cases[i].id&&r.kind===m.cases[i].kind&&r.fault===m.cases[i].fault));
for(const row of o.rows){const {id,...body}=row;check('literal source obligation '+id,now['check_saved.py'].includes('    '+JSON.stringify(id)+': '+JSON.stringify(body)+','));}
check('no suffix-only input selection',!now['case_worker.py'].includes("endswith(':'+self.target_stream)")&&!now['case_worker.py'].includes("endswith(':'+self.i.target_stream)"));
check('four exact role routing predicates',now['case_worker.py'].includes('selected = tag == self.target_input_tag')&&(now['case_worker.py'].match(/== self.i.target_input_tag/g)||[]).length===3);
check('late observer no generic primary capture',!now['check_saved.py'].includes("f=='nonzero' or f.startswith('late_')")&&!now['check_saved.py'].includes("        if f.startswith('late_'):"));
check('payload closed late-file semantics',now['inert_payload.py'].includes("if both or fault == 'stderr' or fault in LATE_FILES:")&&now['inert_payload.py'].includes("return 7 if fault == 'nonzero' or fault in LATE_FILES else 0"));
for(const label of ['ordinary exact return and no escape','ordinary complete durable receipt bytes','ordinary receipt ordered complete durability','dedicated second observer fault','same pipe remains active through retry','defining direct kill failure reached','defining kill failure is secondary','observer own successful poll inside original finish deadline','every owned handle recovered exactly once in acquisition order','complete leaf obligation membership','isolated same-size hash drift','isolated appended-byte size drift'])check('repair predicate '+label,now['check_saved.py'].includes(label));
for(const [n,t] of Object.entries(now).filter(([n])=>n.endsWith('.py')))check('bounded source '+n,Buffer.byteLength(t)<1048576&&!t.includes('\r'));
let diffs='';for(const n of names){const r=cp.spawnSync('/usr/bin/diff',['-u',S+'/'+n,D+'/'+n],{encoding:'utf8'});check('diff status '+n,r.status===(old[n]===now[n]?0:1));diffs+=r.stdout;check('no diff stderr '+n,r.stderr==='');}
fs.writeFileSync(D+'/SOURCE_DIFF.patch',diffs,{flag:'wx'});
// Function spans are plain line-delimited text; no Python tokenizer or AST.
function spans(text){const lines=text.split(/(?<=\n)/),a=[];for(let i=0;i<lines.length;i++)if(/^(?:    )?def [A-Za-z_]/.test(lines[i]))a.push(i);return a.map((v,i)=>({heading:lines[v].trim(),text:lines.slice(v,a[i+1]??lines.length).join('')}))}
const unchanged=[];for(const n of names.filter(n=>n.endsWith('.py'))){const a=spans(old[n]),b=spans(now[n]);for(const x of a){let y=b.find(t=>t.heading===x.heading);if(y&&x.text===y.text)unchanged.push({file:n,heading:x.heading,bytes:Buffer.byteLength(x.text),sha256:crypto.createHash('sha256').update(x.text).digest('hex')});}}
const inherited={pin:verify(deps.inherited_external_closure),reference_count:deps.inherited_reference_count,recursively_reobserved:false,meaning:'Retained provenance; no current runtime or vendor observation.'};
const roles=JSON.parse(fs.readFileSync(S+'/SOURCE_PINS.json')).roles;const newroles={};for(const [role,p] of Object.entries(roles))newroles[role]=role==='subject'?verify(p):pin(D+'/'+path.basename(p.path));
for(const p of seen.values())check('final reread '+p.path,same(pin(p.path),p));
const report={schema:'ri176-administrative-check-v1',passed:true,checks,checks_count:checks.length,fresh_external_identities:[...seen.values()],fresh_external_count:seen.size,source_roles:newroles,unchanged_function_text_spans:unchanged,entry_counts:counts,case_count:92,recipe_count:34,all_92_unexecuted:true,inherited_closure:inherited,limitations:['No Python import/compile/AST/probe/execution.','Literal and opaque comparisons do not establish syntax, reachability, runtime behavior or qualification readiness.','No current runtime inventory, proposed request lookup, scientific decoding, fixtures, operational cards, repository or Git changes.']};
fs.writeFileSync(D+'/ADMIN_CHECK.json',JSON.stringify(report,null,2)+'\n',{flag:'wx'});
fs.writeFileSync(D+'/SOURCE_PINS.json',JSON.stringify({schema:'ri176-source-role-pins-v1',status:'NOT_AN_ADMISSION',roles:newroles},null,2)+'\n',{flag:'wx'});
fs.writeFileSync(D+'/DEPENDENCY_BINDINGS.json',JSON.stringify({schema:'ri176-source-dependencies-v1',fresh_originals:[...seen.values()],inherited_closure:inherited,original_prerequisites_unchanged:true,current_runtime_or_vendor_observed:false},null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({passed:true,checks:checks.length,fresh_external_identities:seen.size,unchanged_function_text_spans:unchanged.length,source_roles:newroles,case_count:92,executed_cases:0}));
