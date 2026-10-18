// Administrative metadata only; no target Python import/parse/compile/run.
import fs from 'node:fs';import crypto from 'node:crypto';import path from 'node:path';
const B='/Volumes/AI_DATA/development/det-review-evidence',D=B+'/ri182-compound-cleanup-oracle-repair-6835ytb8',S=B+'/ri176-supervisor-qualification-repair-3ausb2jo',V=B+'/ri180-supervisor-independent-review-4xwmvctt',R=B+'/ri179-root-upper-review-lf_39rs0';
function pin(p){let b=fs.readFileSync(p);return {path:p,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')}}const got=new Map();
function verify(p){let q=pin(p.path);if(q.bytes!==p.bytes||q.sha256!==p.sha256)throw Error('identity '+p.path);got.set(p.path,q);return q}
const assignment=verify({path:R+'/RI182_REPAIR_ASSIGNMENT.json',bytes:2756,sha256:'995bfb2a00824297e714dec4fef2fe1dfdc7540fae7f41ca789ba717e190a4c1'});const a=JSON.parse(fs.readFileSync(assignment.path));for(const k of ['nonauthor_review','root_adjudication','subject'])verify(a[k]);
for(const dir of [S,V]){const h=JSON.parse(fs.readFileSync(dir+'/HANDOFF.json'));if(JSON.stringify(fs.readdirSync(dir).sort())!==JSON.stringify(h.namespace.slice().sort()))throw Error('namespace '+dir);h.payloads.forEach(verify)}
const deps=JSON.parse(fs.readFileSync(S+'/DEPENDENCY_BINDINGS.json'));deps.fresh_originals.forEach(verify);verify(deps.inherited_closure.pin);got.set(R+'/RI180_ROOT_REVIEW.md',pin(R+'/RI180_ROOT_REVIEW.md'));
if(JSON.stringify(fs.readdirSync(D).sort())!==JSON.stringify(['authenticate.mjs']))throw Error('nonempty reservation');
for(const name of ['protocol.py','qualify_supervisor.py','case_worker.py','inert_payload.py','check_saved.py','CASE_MANIFEST.json','CASE_OBLIGATIONS.json'])fs.copyFileSync(S+'/'+name,D+'/'+name,fs.constants.COPYFILE_EXCL);
fs.writeFileSync(D+'/AUTHENTICATION.json',JSON.stringify({schema:'ri182-initial-authentication-v1',assignment,observed:[...got.values()],fresh_unique_files:got.size,subject_namespace:33,review_namespace:10,source_execution:false,current_runtime_observed:false},null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({authenticated:got.size,source_payloads_copied:7,reservation:D}));
