const fs=require('fs'),p=require('path'),c=require('crypto');
const Q='/Volumes/AI_DATA/development/det-review-evidence/ri191-exact-pair-witness-source-uu414bjg',P='/Volumes/AI_DATA/development/det-review-evidence/ri189-coupled-record-contrast-y5nubaac';
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b), need=(b,m)=>{if(!b)throw Error(m)}, cache=new Map(), fields=['dev','ino','mode','size','mtimeNs','ctimeNs','nlink'];
function read(x){if(cache.has(x))return cache.get(x);need(p.isAbsolute(x)&&p.normalize(x)===x,'path '+x);let t='/';for(const k of x.split('/').filter(Boolean)){t=p.join(t,k);need(!fs.lstatSync(t).isSymbolicLink(),'link '+x);}const st=fs.lstatSync(x,{bigint:true}),same=a=>fields.every(k=>a[k]===st[k]);need(st.isFile()&&st.size<=67108864n,'regular/cap');const fd=fs.openSync(x,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);let b;try{need(same(fs.fstatSync(fd,{bigint:true})),'fd-before');const chunks=[];let length=0;const cap=Number(st.size)+1;while(length<cap){const block=Buffer.alloc(Math.min(65536,cap-length));const got=fs.readSync(fd,block,0,block.length,null);if(!got)break;chunks.push(block.subarray(0,got));length+=got;}b=Buffer.concat(chunks);need(b.length===Number(st.size),'size drift');need(same(fs.fstatSync(fd,{bigint:true})),'fd-after');}finally{fs.closeSync(fd);}need(same(fs.lstatSync(x,{bigint:true}))&&fs.realpathSync(x)===x,'path-after');const r={body:b,path:x,resolved_path:x,bytes:b.length,sha256:c.createHash('sha256').update(b).digest('hex'),symlinks:[],state:Object.fromEntries(fields.map(k=>[k,st[k].toString()]))};cache.set(x,r);return r;}
function pin(i){const a=read(i.path);for(const k of ['path','bytes','sha256'])need(a[k]===i[k],'pin '+i.path);if(i.resolved_path!==undefined)need(a.resolved_path===i.resolved_path,'resolved');if(i.symlinks!==undefined)need(eq(a.symlinks,i.symlinks),'symlinks');if(i.symlink_chain!==undefined)need(eq(a.symlinks,i.symlink_chain),'symlink_chain');return a;}
const simple=r=>({path:r.path,bytes:r.bytes,sha256:r.sha256});

pin({path:Q+'/SOURCE_DEPENDENCIES.json',bytes:361715,sha256:'fe70e052338c041032ffd0f3ab9d1a567fff762be095dbae386489a5daa3449f'});
pin({path:Q+'/SOURCE_IDENTITIES.json',bytes:140523,sha256:'166fd6b734cf5048ac52d0e7ec5e902402b115803dd6f463f6b54bd7d8878bee'});
pin({path:Q+'/pair_witness.py',bytes:20354,sha256:'26aaa5138f6ebd1f9791e9c6ea66225376f81931ec8235de4ee399a5e6514357'});
pin({path:Q+'/CONTRACT.md',bytes:15024,sha256:'8d9d8e483df41cc50a80590719e787576ca61728a274f6aefe722447915526ac'});
pin({path:Q+'/NEGATIVE_CASES.md',bytes:23841,sha256:'4cfebccd39adf994612a31c5926479ae5bcb51db0ba5bbb419e89fd77d3d93c2'});
pin({path:Q+'/DEPENDENCY_NOTES.md',bytes:19961,sha256:'8d1e134de7cc300eb260f1be2dd0d8b3f242497b0a2f7eebfd773c611f75e90d'});
const D=JSON.parse(read(Q+'/SOURCE_DEPENDENCIES.json').body),S=JSON.parse(read(Q+'/SOURCE_IDENTITIES.json').body),M=new Map(D.protected_files.map(r=>[r.path,r]));
need(M.size===389&&eq([...M.keys()],[...M.keys()].sort()),'count/sort');
D.protected_files.forEach((r,i)=>{need(r.role==='dep_'+String(i+1).padStart(4,'0')&&r.path===r.identity.path,'row');pin(r.identity)});
need(D.protected_files.reduce((n,r)=>n+r.identity.bytes,0)===23201553,'total selected bytes');
const old=JSON.parse(read(P+'/SOURCE_DEPENDENCIES.json').body),oldS=JSON.parse(read(P+'/SOURCE_IDENTITIES.json').body),omit=r=>Object.fromEntries(Object.entries(r).filter(([k])=>k!=='role'));
need(old.protected_files.length===374,'old374');
for(const r of old.protected_files)need(eq(omit(r),omit(M.get(r.path))),'inherited row');
for(const k of ['governance_stopping_boundary','historical_phase_record_boundary','predecessor_author_support_boundary','ri172_author_support_boundary','ri173_author_support_boundary','ri122_literal_read_exception','ri175_author_support_boundary','ri178_author_support_boundary','ri181_author_support_boundary','ri185_author_support_boundary','ri187_author_support_boundary'])need(eq(D[k],old[k]),'inherited boundary '+k);
for(const k of ['accepted_ri187_premises','accepted_ri185_premises','accepted_ri181_premises','accepted_ri178_premises','accepted_ri175_premises','accepted_ri173_premises','historical_fixed_prefix_premise','accepted_ri172_predecessor','accepted_ri168_premises','accepted_ri166_premises','accepted_ri157_premises','accepted_ri157_margin_scope','accepted_ri155_premises','accepted_ri153_premises','excluded_historical_inferences','accepted_ri151_premises','accepted_ri149_premises','root_accepted_additional_observation','accepted_ri147_premises','accepted_ri145_premises','accepted_analytic_packets','premise_texts','actual_source_text_reads','source_text_counterparts','immutable_numerical_certificate','unchanged_obligations','inherited_scope_clarification','identity_interpretation'])need(eq(S[k],oldS[k]),'inherited S '+k);
need(eq(S.governance.inherited_analytic_and_operational_governance,oldS.governance),'whole inherited governance');
const namespaces=[];
for(const[dir,count]of[[P,8]]){
const h=JSON.parse(read(dir+'/HANDOFF.json').body),names=fs.readdirSync(dir).sort();
need(names.length===count&&eq(names,[...h.namespace].sort())&&eq(names,[...h.payloads.map(i=>p.basename(i.path)),'HANDOFF.json'].sort()),'historical namespace '+dir);
h.payloads.forEach(pin);namespaces.push({dir,names});
}
need(eq(D.historical_phase_record_boundary,S.governance.RI166_phase_record_boundary),'phase S boundary');
need(eq(D.predecessor_author_support_boundary,S.governance.RI168_author_support_boundary),'support S boundary');
need(eq(D.ri172_author_support_boundary,S.governance.RI172_author_support_boundary),'old support S boundary');
need(eq(D.ri173_author_support_boundary,S.governance.RI173_author_support_boundary),'old support S boundary');
need(eq(D.ri175_author_support_boundary,S.governance.RI175_author_support_boundary),'old support S boundary');
need(eq(D.ri178_author_support_boundary,S.governance.RI178_author_support_boundary),'old support S boundary');
need(eq(D.ri181_author_support_boundary,S.governance.RI181_author_support_boundary),'old181 support S boundary');
need(eq(D.ri185_author_support_boundary,S.governance.RI185_author_support_boundary),'old185 support S boundary');
need(eq(D.ri187_author_support_boundary,S.governance.RI187_author_support_boundary),'new187 support S boundary');
for(const b of [D.historical_phase_record_boundary,D.predecessor_author_support_boundary,D.ri172_author_support_boundary,D.ri173_author_support_boundary,D.ri175_author_support_boundary,D.ri178_author_support_boundary,D.ri181_author_support_boundary,D.ri185_author_support_boundary,D.ri187_author_support_boundary,D.ri189_author_support_boundary])need(M.get(b.path).classification==='opaque-historical-acceptance-or-source-support'&&b.typed_reference_expansion===false,'author boundary routing');
need(eq(D.ri189_author_support_boundary,S.governance.RI189_author_support_boundary),'new189 support S boundary');
need(D.ri189_author_support_boundary.path===P+'/AUTHOR_VERIFICATION.json','new author boundary path');
need(M.get('/Volumes/AI_DATA/development/det-review-evidence/ri188-root-endpoint-profile-review-1jg_i948/check_ri189.py').classification==='opaque-historical-acceptance-or-source-support','root checker opaque only');
const ex=D.ri122_literal_read_exception,oldDecision='/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/RI122_ROOT_FINAL_ADJUDICATION.json',scope='/Volumes/AI_DATA/development/det-review-evidence/ri174-root-preparation-review-wm18ymsq/RI175_HISTORICAL_PREMISE_SCOPE.json';
need(ex.path===oldDecision&&ex.literal_read_authority===scope&&ex.automated_typed_reference_expansion===false&&M.get(oldDecision).classification==='opaque-historical-acceptance-or-source-support','historical literal-read exception');
need(S.historical_fixed_prefix_premise.permission.path===scope&&S.historical_fixed_prefix_premise.final_acceptance.path===oldDecision&&S.historical_fixed_prefix_premise.final_decision_automated_typed_reference_expansion===false,'exception S binding');

const admission=S.original_prefix_identity_authorization;
need(admission.status==='ADMIT_OPAQUE_WHOLE_IDENTITY_ONLY'&&admission.certificate_selected_in_inherited_374===false&&admission.new_path_observed_only_after_explicit_root_admission===true&&admission.scientific_body_or_coefficient_values_decoded===false&&admission.admission_supplies_pair_magnitude_or_execution_authority===false&&admission.automated_certificate_reference_expansion===false,'opaque authority scope');
const admissionExpected={path:'/Volumes/AI_DATA/development/det-review-evidence/ri188-root-endpoint-profile-review-1jg_i948/RI191_OPAQUE_PREFIX_ADMISSION.json',bytes:2123,sha256:'992a107e022f32be8d06bff3b0a859f87730e70d43c96402d3b4e2ebc0df186d'};
const certificateExpected={path:'/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json',bytes:2845,sha256:'3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969'};
need(eq(admission.admission,admissionExpected)&&eq(admission.original_certificate,certificateExpected)&&eq(S.additional_source_paths_beyond_base_387,[admissionExpected,certificateExpected]),'exact added two');
need(M.get(admissionExpected.path).classification==='selected-administrative-proof-provenance'&&M.get(certificateExpected.path).classification==='opaque-scientific-historical-premise','opaque admission routing');
pin(admissionExpected);pin(certificateExpected);
const roles=['certificate','original_source','original_manuscript','prefix_completion','component_routing','coupled_contrast','accepted_predecessor','accepted_manual_review','assignment'];
need(eq(Object.keys(S.verifier_input_bindings),roles),'nine input roles');
need(eq(S.verifier_input_bindings.certificate,certificateExpected),'certificate binding');
for(const i of Object.values(S.verifier_input_bindings)){need(M.has(i.path),'input selected');pin(i);}
need(eq(S.verifier_input_bindings.assignment,S.assignment),'assignment binding');
need(S.scope.execution_admitted===false&&S.scope.scientific_body_or_actual_vector_decoded===false&&S.scope.new_verifier_or_controls_executed===false&&S.scope.controls_92_recipes_34_mutation_families_35_waived_or_credited===false&&S.scope.obligations_31_139_20_42_waived_or_credited===false&&S.scope.ret_paused===true,'source scope');

let refs=0,extended=0,states=0;
function scan(x,current=false){
if(!x||typeof x!=='object')return;
if(!Array.isArray(x)&&typeof x.path==='string'&&Number.isSafeInteger(x.bytes)&&typeof x.sha256==='string'){
need(M.has(x.path)||(current&&x.path===Q+'/SOURCE_DEPENDENCIES.json'),'reference closure '+x.path);
pin(x);refs++;if(x.symlink_chain!==undefined)extended++;if(x.state!==undefined)states++;
}
Object.values(x).forEach(v=>scan(v,current));
}
const governance='/Volumes/AI_DATA/development/det-review-evidence/ri164-root-static-review-xr1qffz8/RI164_ROOT_ADJUDICATION.json';
need(D.governance_stopping_boundary.path===governance&&D.governance_stopping_boundary.typed_reference_expansion===false&&eq(D.governance_stopping_boundary,S.governance.operational_stopping_boundary),'governance rule');
const classes={};
for(const r of D.protected_files){
classes[r.classification]=(classes[r.classification]||0)+1;
if(r.classification==='selected-administrative-proof-provenance')scan(JSON.parse(read(r.path).body));
else if(r.classification==='selected-administrative-governance-boundary')need(r.path===governance,'exact governance boundary');
}
need(classes['selected-administrative-proof-provenance']===143&&classes['selected-administrative-governance-boundary']===1&&classes['analytic-source-text-or-review']===142&&classes['opaque-historical-acceptance-or-source-support']===101&&classes['opaque-scientific-historical-premise']===2,'class counts');
need(refs===6893&&extended===18&&states===18,'historical reference counts');
refs=0;scan(S,true);need(refs===222,'current S references');
let pairs=0;
for(const[k,i]of Object.entries(S.source_text_counterparts.published)){need(read(i.path).body.equals(read(S.premise_texts[k].path).body),'separate path byte equality');pairs++}
need(pairs===4,'pair count');
const final=['pair_witness.py','CONTRACT.md','NEGATIVE_CASES.md','DEPENDENCY_NOTES.md','SOURCE_DEPENDENCIES.json','SOURCE_IDENTITIES.json','HANDOFF.md','AUTHOR_VERIFICATION.json','HANDOFF.json'].sort(),stage=process.argv[1]||'preseal7';
need(['preseal7','final9'].includes(stage),'stage');
const expected=stage==='final9'?final:final.filter(n=>!['AUTHOR_VERIFICATION.json','HANDOFF.json'].includes(n));
need(eq(fs.readdirSync(Q).sort(),expected),'current namespace');
const payloads=expected.map(n=>simple(read(Q+'/'+n)));let references=0;
for(const n of ['pair_witness.py','CONTRACT.md','NEGATIVE_CASES.md','DEPENDENCY_NOTES.md','HANDOFF.md']){
 const txt=read(Q+'/'+n).body.toString('utf8');need(!/^(<{7}|={7}|>{7})( |$)/m.test(txt),'conflict marker');need(!/[ \t]+$/m.test(txt),'trailing whitespace');
 if(n.endsWith('.md')) for(const m of txt.matchAll(/(\/Volumes\/[^\s\x60|]+\.(?:md|json|py))(?:[\s\x60|]|$)/g)){need(M.has(m[1])||expected.some(f=>Q+'/'+f===m[1]),'literal source path '+m[1]);references++}
 if(n.endsWith('.md')) for(const m of txt.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)){need(!m[1].includes('://')&&expected.includes(m[1]),'current markdown link '+m[1]);read(Q+'/'+m[1])}
}
if(stage==='final9'){
 const h=JSON.parse(read(Q+'/HANDOFF.json').body);need(eq(h.namespace,final)&&h.payloads.length===8,'current seal');
 need(eq(h.payloads.map(i=>p.basename(i.path)).sort(),final.filter(n=>n!=='HANDOFF.json')),'seal coverage');
 h.payloads.forEach(pin);pin(h.assignment);pin(h.accepted_analytic_predecessor);pin(h.operational_governance_predecessor);pin(h.opaque_prefix_admission);
 need(h.source_only_exact_verifier===true&&h.nine_immutable_input_bindings===true&&h.complete_declared_root_and_override_validation===true&&h.bounded_nonexecuted_source_design===true&&h.sufficient_inconclusive_refusal_distinguished===true&&h.original_certificate_opaque_only===true&&h.actual_core_gap_predicate_decided===false&&h.original_parser_compatibility_established===false&&h.actual_W_sign_claimed===false&&h.actual_109_vector_read===false&&h.verifier_import_compile_AST_probe_run===false&&h.scientific_execution===false&&h.fixtures_or_operational_cards_created===false&&h.obligations_waived_or_credited===false&&h.repository_or_Git_written===false&&h.ret_paused===true,'result scope');
}
const before=[...cache.values()].map(simple);cache.clear();before.forEach(pin);
need(before.length===389+expected.length,'exact fresh check scope');
need(eq(fs.readdirSync(Q).sort(),expected),'end namespace');
for(const n of namespaces)need(eq(fs.readdirSync(n.dir).sort(),n.names),'end historical namespace');
console.log(JSON.stringify({schema:'ri191-author-administrative-check-v1',status:'MATCH_NOT_MATHEMATICAL_OR_OPERATIONAL_ACCEPTANCE',stage,dependencies:389,selected_bytes:23201553,inherited:374,classifications:classes,historical_typed_references:6893,current_typed_references:222,historical_extended_state_noncomparisons:18,separate_byte_equal_pairs:4,predecessor_namespace_counts:[8],current_namespace:expected.length,literal_manuscript_reference_occurrences:references,final_fresh_identity_rechecks:before.length,current_payloads:payloads,mathematical_formula_evaluated_by_script:false,scientific_or_target_execution:false},null,2));
