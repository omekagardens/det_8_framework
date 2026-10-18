
const fs=require('fs'),p=require('path'),c=require('crypto');
const need=(v,m)=>{if(!v)throw Error(m)},fields=['dev','ino','mode','size','mtimeNs','ctimeNs','nlink'];
function readExact(i){const x=i.path;need(p.isAbsolute(x)&&p.normalize(x)===x,'absolute normalized');let a='/';for(const k of x.split('/').filter(Boolean)){a=p.join(a,k);need(!fs.lstatSync(a).isSymbolicLink(),'symlink');}const s=fs.lstatSync(x,{bigint:true});need(s.isFile()&&s.size<=67108864n,'regular cap');if(i.bytes!==undefined)need(s.size===BigInt(i.bytes),'initial size');const same=t=>fields.every(k=>t[k]===s[k]);const fd=fs.openSync(x,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);let b;try{need(same(fs.fstatSync(fd,{bigint:true})),'fd-before');const chunks=[];let n=0,cap=Number(s.size)+1;while(n<cap){const z=Buffer.alloc(Math.min(65536,cap-n)),g=fs.readSync(fd,z,0,z.length,null);if(!g)break;chunks.push(z.subarray(0,g));n+=g;}b=Buffer.concat(chunks);need(b.length===Number(s.size)&&same(fs.fstatSync(fd,{bigint:true})),'fd-after/length');}finally{fs.closeSync(fd);}need(same(fs.lstatSync(x,{bigint:true}))&&fs.realpathSync(x)===x,'path-after');const r={path:x,bytes:b.length,sha256:c.createHash('sha256').update(b).digest('hex')};if(i.sha256!==undefined)need(r.sha256===i.sha256,'hash');return {...r,body:b};}
const simple=r=>({path:r.path,bytes:r.bytes,sha256:r.sha256});

const Q="/Volumes/AI_DATA/development/det-review-evidence/ri220-native-amplitude-range-9eljeyc1",P="/Volumes/AI_DATA/development/det-review-evidence/ri216-native-determinant-sign-qs_a79vs";
function canon(x){if(Array.isArray(x))return x.map(canon);if(x&&typeof x==='object')return Object.fromEntries(Object.keys(x).sort().map(k=>[k,canon(x[k])]));return x;}
const eq=(a,b)=>JSON.stringify(canon(a))===JSON.stringify(canon(b));
const cache=new Map();
function pin(i){
 need(Object.keys(i).every(k=>['path','bytes','sha256','resolved_path','symlinks'].includes(k)),'identity fields');
 let r=cache.get(i.path);if(!r){r=readExact(i);cache.set(i.path,r);}
 need(r.bytes===i.bytes&&r.sha256===i.sha256,'pin '+i.path);
 if(i.resolved_path!==undefined)need(i.resolved_path===i.path,'resolved path');
 if(i.symlinks!==undefined)need(eq(i.symlinks,[]),'symlink declaration');
 return r;
}
const currentFour=[{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri220-native-amplitude-range-9eljeyc1/AMPLITUDE_RANGE.md","bytes":8742,"sha256":"ed50a70c5c5a968dee1b1e7230230694e6a26d7fb709d8255ff69af581356748"},{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri220-native-amplitude-range-9eljeyc1/HANDOFF.md","bytes":2288,"sha256":"bf288fee0e76009917e6c834089a0e3546e931ceece192d2f0a47c36b53b6c36"},{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri220-native-amplitude-range-9eljeyc1/SHARED_COMPATIBILITY.md","bytes":11045,"sha256":"10f67367f8b48d559480c88b2051391f3058493e03ce41dab2d6aa18e2f0f45e"},{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri220-native-amplitude-range-9eljeyc1/SOURCE_REFERENCES.json","bytes":41660,"sha256":"ed585f683b59a2c8c20d23f869184cb039e941a7b0e6009660cb14190aa477b6"}];currentFour.forEach(pin);
const S=JSON.parse(cache.get(Q+'/SOURCE_REFERENCES.json').body);
need(S.schema==='ri220-compact-accepted-source-references-v1','source schema');
const M=new Map(S.direct_sources.map(r=>[r.identity.path,r]));
need(M.size===21&&S.direct_scope.files===21,'direct21');
need(S.direct_sources.reduce((n,r)=>n+r.identity.bytes,0)===652815&&S.direct_scope.bytes===652815,'direct bytes');
need(eq([...M.keys()],[...M.keys()].sort()),'source sort');
for(const r of S.direct_sources){
 need(['administrative-reference','accepted-analytic-text','opaque-historical-support'].includes(r.access),'no scientific body source class');
 pin(r.identity);
}
let references=0;
function selected(i){need(M.has(i.path),'selected direct reference '+i.path);pin(i);references++;}
for(const i of [S.assignment,S.accepted_predecessor,S.predecessor_handoff,S.predecessor_references,S.inherited_manifest_by_reference.identity,S.accepted_four_root_witness])selected(i);
for(const group of S.current_literal_reads){need(group.receipt.exit_code===0,'declared read receipt');group.files.forEach(selected);}
const assignment=JSON.parse(pin(S.assignment).body);
need(assignment.reservation===Q&&assignment.status==='ASSIGNED_AFTER_RI216_INDEPENDENT_ADJUDICATION','assignment');
need(eq(assignment.predecessor,S.accepted_predecessor)&&eq(assignment.predecessor_packet,S.predecessor_handoff)&&eq(assignment.predecessor_references,S.predecessor_references)&&assignment.new_scientific_execution_authority===false,'assignment binding and boundary');
const decision=JSON.parse(pin(S.accepted_predecessor).body);
need(decision.status==='ACCEPT_RI216_CONDITIONAL_FIXED_H30_OBSTRUCTION'&&decision.scientific_execution===false&&decision.qualification_credit===0,'predecessor status');
for(const k of ['subject','manual_review','root_metadata','independent_review'])selected(decision[k]);
need(eq(decision.subject,S.predecessor_handoff),'predecessor subject binding');
const prior=JSON.parse(pin(S.predecessor_handoff).body);
const priorNames=fs.readdirSync(P).sort();
need(eq(priorNames,S.predecessor_namespace)&&eq(priorNames,prior.namespace)&&priorNames.length===6&&prior.payloads.length===5,'prior namespace');
prior.payloads.forEach(selected);
need(eq(prior.payloads.map(i=>p.basename(i.path)).concat('HANDOFF.json').sort(),priorNames),'prior seal coverage');
const priorRefs=JSON.parse(pin(S.predecessor_references).body);
const inherited=JSON.parse(pin(S.inherited_manifest_by_reference.identity).body);
const boundaries=Object.fromEntries(Object.entries(inherited).filter(([k])=>!['schema','status','protected_files','scope'].includes(k)));
need(inherited.protected_files.length===423&&S.inherited_manifest_by_reference.selected_paths===423,'inherited423 metadata');
need(eq(boundaries,S.inherited_manifest_by_reference.boundary_objects)&&eq(boundaries,priorRefs.inherited_manifest_by_reference.boundary_objects)&&Object.keys(boundaries).length===15,'15 boundaries');
need(eq(S.inherited_manifest_by_reference,priorRefs.inherited_manifest_by_reference),'whole inherited boundary');
need(eq(S.inherited_original_six_admissions,assignment.source_admission)&&eq(S.inherited_original_six_admissions,priorRefs.inherited_original_six_admissions)&&assignment.source_admission.length===6,'six inherited admissions');
need(eq(S.inherited_additional_admissions,assignment.inherited_additional_admissions)&&eq(S.inherited_additional_admissions,priorRefs.inherited_additional_admissions),'two inherited additional admissions');
need(eq(S.inherited_RI189_analytic_admission,assignment.inherited_RI189_analytic_admission)&&eq(S.inherited_RI189_analytic_admission,priorRefs.new_literal_analytic_admission),'RI189 admissions inherited');
const byInheritedPath=new Map(inherited.protected_files.map(r=>[r.identity.path,r]));
function inheritedAnalytic(i){
 const row=byInheritedPath.get(i.path);
 need(row&&eq(simple(row.identity),simple(i)),'inherited analytic identity');
 need(row.classification==='analytic-source-text-or-review'&&row.access_policy==='text-reading-and-opaque-identity-no-execution','inherited analytic boundary');
}
for(const row of [...S.inherited_original_six_admissions,...S.inherited_RI189_analytic_admission]){
 need(row.typed_reference_expansion===false&&row.inherited_matches.length>0,'inherited flags');
 for(const i of row.inherited_matches){inheritedAnalytic(i);need(i.bytes===row.identity.bytes&&i.sha256===row.identity.sha256,'inherited matching bytes');}
}
const F=S.predecessor_literal_exception_boundary;
need(eq(F.reference_manifest,S.predecessor_references)&&eq(F.prior_exception,priorRefs.four_root_literal_exception),'old exception preserved');
need(F.typed_reference_expansion===false&&F.new_body_read_authority===false&&F.new_coefficient_coordinate_resolution===false&&F.historical_source_body_not_reopened===true,'old exception not reused');
need(!M.has(F.prior_exception.body.path),'no original scientific body in current scope');
need(eq(assignment.accepted_four_root_witness,S.accepted_four_root_witness)&&eq(F.prior_exception.witness_acceptance,S.accepted_four_root_witness),'witness accepted by reference');
const witness=JSON.parse(pin(S.accepted_four_root_witness).body);
need(witness.status==='ACCEPT_FIXED_PREFIX_FOUR_ROOT_WITNESS'&&witness.new_scientific_execution===false,'witness status only');
const A=S.additional_shared_affine_admission;
selected(A.authority);selected(A.reference);
const admission=JSON.parse(pin(A.authority).body);
need(admission.status==='ADMIT_EXACT_EXISTING_ANALYTIC_TEXT_ONLY'&&eq(admission.assignment,S.assignment)&&admission.reservation===Q,'new analytic admission');
need(eq(admission.reference,A.reference)&&eq(admission.inherited_match,A.inherited_match)&&eq(admission.inherited_manifest,S.inherited_manifest_by_reference.identity),'new admission source binding');
need(eq(byInheritedPath.get(A.reference.path),A.inherited_match),'complete inherited row');
inheritedAnalytic(A.reference);
need(A.typed_reference_expansion===false&&admission.typed_reference_expansion===false&&admission.scientific_body_admission===false&&admission.execution_admitted===false&&admission.automatic_scientific_arithmetic===false&&admission.qualification_credit===0,'new admission limits');
selected(S.predecessor_author_support.identity);
need(S.predecessor_author_support.access==='opaque-historical-support'&&S.predecessor_author_support.typed_reference_expansion===false,'prior author opaque');
const yes=['manual_analysis_only','original_quarter_amplitude_rejection_immutable','distinct_symbolic_amplitude_family','exact_local_amplitude_interval_proved','original_local_variables_and_strict_endpoints_preserved','complete_shared_affine_consistency_proved','explicit_symbolic_shared_solution_proved','full_through_eight_small_amplitude_subfamily_proved','inherited_finite_sign_premises_remain_conditional','ret_paused'];
const no=['maximal_full_amplitude_decided','numerical_amplitude_selected','new_scientific_body_vector_or_certificate_read','new_coefficient_coordinates_resolved','automatic_scientific_parsing_or_proof_arithmetic','H_or_z_reconstruction','actual_scales_or_full_vector_evaluated','graph_LP_subject_runtime_fixture_card_execution','repository_Git_index_or_measurement_written','physical_correspondence_or_full_QM_proved','all_size_record_blind_extension_proved','successor_designed_or_started'];
for(const k of yes)need(S.scope[k]===true,'declared true scope '+k);
for(const k of no)need(S.scope[k]===false,'declared false scope '+k);
need(S.scope.qualification_credit===0&&eq(S.executable_obligations,priorRefs.executable_obligations)&&S.executable_obligations.new_credit===0,'unchanged qualification');
const stage=process.argv[1]||'preseal4';need(['preseal4','final6'].includes(stage),'mode');
const final=['AMPLITUDE_RANGE.md','AUTHOR_VERIFICATION.json','HANDOFF.json','HANDOFF.md','SHARED_COMPATIBILITY.md','SOURCE_REFERENCES.json'];
const expected=stage==='final6'?final:final.filter(n=>!['AUTHOR_VERIFICATION.json','HANDOFF.json'].includes(n));
need(eq(fs.readdirSync(Q).sort(),expected),'current namespace');
const payloads=expected.map(n=>{const r=readExact({path:Q+'/'+n});cache.set(r.path,r);return simple(r);});
for(const n of ['AMPLITUDE_RANGE.md','SHARED_COMPATIBILITY.md','HANDOFF.md']){
 const t=cache.get(Q+'/'+n).body.toString('utf8');
 need(!/^(<{7}|={7}|>{7})( |$)/m.test(t)&&!/[ \t]+$/m.test(t),'Markdown hygiene');
 for(const m of t.matchAll(/\[[^\]]+\]\(([^)]+)\)/g))need(final.includes(m[1]),'declared local Markdown target');
}
if(stage==='final6'){
 const h=JSON.parse(cache.get(Q+'/HANDOFF.json').body),a=JSON.parse(cache.get(Q+'/AUTHOR_VERIFICATION.json').body);
 need(eq(h.namespace,final)&&h.payloads.length===5&&eq(h.payloads.map(i=>p.basename(i.path)).sort(),final.filter(n=>n!=='HANDOFF.json')),'current seal');
 h.payloads.forEach(pin);
 selected(h.assignment);selected(h.accepted_predecessor);selected(h.additional_literal_admission);
 need(eq(h.scope,S.scope)&&eq(h.executable_obligations,S.executable_obligations),'handoff scope');
 need(a.status==='AUTHOR_MANUAL_PROOF_NOT_INDEPENDENT_ACCEPTANCE'&&a.preseal.actual_result.current_namespace===4&&a.final6_not_yet_run_at_author_creation===true,'author phase');
 a.preseal.actual_result.current_payloads.forEach(pin);
 need(eq(a.executable_obligations,S.executable_obligations)&&eq(a.scope,S.scope),'author obligations');
}
const all=[...cache.values()].map(simple);need(all.length===21+expected.length,'fresh scope');
all.forEach(readExact);
need(eq(fs.readdirSync(Q).sort(),expected)&&eq(fs.readdirSync(P).sort(),priorNames),'post namespaces');
console.log(JSON.stringify({schema:'ri220-compact-administrative-check-v1',status:'IDENTITY_MATCH_NOT_MATHEMATICAL_ACCEPTANCE',stage,direct_sources:21,direct_bytes:652815,inherited423_manifest_by_reference:true,fresh_inherited423_or_previous_source_collection_replay:false,inherited_boundary_objects_preserved:15,inherited_analytic_admissions:'six plus two plus two by reference unchanged',new_analytic_matches:1,old_scientific_body_exception_not_reused:true,scientific_body_read_or_JSON_parsed:false,explicit_selected_reference_checks:references,predecessor_namespace:6,current_namespace:expected.length,whole_identity_fresh_rechecks:all.length,current_payloads:payloads,declared_local_Markdown_targets:stage==='final6'?'all-present':'future-seal-targets-declared-final-presence-pending',automated_proof_arithmetic:false,subject_execution:false},null,2));
