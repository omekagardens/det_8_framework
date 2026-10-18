
const fs=require('fs'),p=require('path'),c=require('crypto');
const need=(v,m)=>{if(!v)throw Error(m)},fields=['dev','ino','mode','size','mtimeNs','ctimeNs','nlink'];
function readExact(i){const x=i.path;need(p.isAbsolute(x)&&p.normalize(x)===x,'absolute normalized');let a='/';for(const k of x.split('/').filter(Boolean)){a=p.join(a,k);need(!fs.lstatSync(a).isSymbolicLink(),'symlink');}const s=fs.lstatSync(x,{bigint:true});need(s.isFile()&&s.size<=67108864n,'regular cap');if(i.bytes!==undefined)need(s.size===BigInt(i.bytes),'initial size');const same=t=>fields.every(k=>t[k]===s[k]);const fd=fs.openSync(x,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);let b;try{need(same(fs.fstatSync(fd,{bigint:true})),'fd-before');const chunks=[];let n=0,cap=Number(s.size)+1;while(n<cap){const z=Buffer.alloc(Math.min(65536,cap-n)),g=fs.readSync(fd,z,0,z.length,null);if(!g)break;chunks.push(z.subarray(0,g));n+=g;}b=Buffer.concat(chunks);need(b.length===Number(s.size)&&same(fs.fstatSync(fd,{bigint:true})),'fd-after/length');}finally{fs.closeSync(fd);}need(same(fs.lstatSync(x,{bigint:true}))&&fs.realpathSync(x)===x,'path-after');const r={path:x,bytes:b.length,sha256:c.createHash('sha256').update(b).digest('hex')};if(i.sha256!==undefined)need(r.sha256===i.sha256,'hash');return {...r,body:b};}
const simple=r=>({path:r.path,bytes:r.bytes,sha256:r.sha256});

const Q="/Volumes/AI_DATA/development/det-review-evidence/ri231-native-six-root-witness-qboypkl8",P="/Volumes/AI_DATA/development/det-review-evidence/ri228-native-lower-combinations-lt3ry78x";
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
const currentFour=[{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri231-native-six-root-witness-qboypkl8/CANONICAL_CAPACITY.md","bytes":15205,"sha256":"0069e8c7314f6e84b2803d2502f317d8640df0a0192731ccd79914b88ecf7faa"},{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri231-native-six-root-witness-qboypkl8/HANDOFF.md","bytes":2327,"sha256":"9354d1054bee8af0e298ce19af276bd5fc4537005a5a15838883db0c4c26e690"},{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri231-native-six-root-witness-qboypkl8/SIX_ROOT_WITNESS.md","bytes":9417,"sha256":"9ff04c11ff551fca8e64d606fd46d265836dde9e1b7d7af6f03269b44dab2c03"},{"path":"/Volumes/AI_DATA/development/det-review-evidence/ri231-native-six-root-witness-qboypkl8/SOURCE_REFERENCES.json","bytes":65520,"sha256":"43e9fc923eca8da42424df62faa66f6abdcace71b1d1da5478bef539ec8b6572"}];currentFour.forEach(pin);
const S=JSON.parse(cache.get(Q+'/SOURCE_REFERENCES.json').body);
need(S.schema==='ri231-compact-accepted-source-references-v1','source schema');
const M=new Map(S.direct_sources.map(r=>[r.identity.path,r]));
need(M.size===32&&S.direct_scope.files===32,'direct32');
need(S.direct_sources.reduce((n,r)=>n+r.identity.bytes,0)===796922&&S.direct_scope.bytes===796922,'direct bytes');
need(eq([...M.keys()],[...M.keys()].sort()),'source sort');
for(const r of S.direct_sources){
 need(['administrative-reference','accepted-analytic-text','opaque-historical-support','exact-literal-scientific-exception'].includes(r.access),'access class');
 pin(r.identity);
}
function admin(i){need(M.get(i.path)?.access==='administrative-reference','administrative JSON only');return JSON.parse(pin(i).body);}
let references=0;
function selected(i){need(M.has(i.path),'selected direct '+i.path);pin(i);references++;}
for(const i of [S.assignment,S.accepted_predecessor,S.predecessor_handoff,S.predecessor_references,S.inherited_manifest_by_reference.identity,S.accepted_four_root_witness])selected(i);
const assignment=admin(S.assignment),decision=admin(S.accepted_predecessor);
need(assignment.reservation===Q&&assignment.status==='ASSIGNED_AFTER_RI228_INDEPENDENT_ADJUDICATION','assignment');
need(eq(assignment.predecessor,S.accepted_predecessor)&&eq(assignment.predecessor_packet,S.predecessor_handoff)&&eq(assignment.predecessor_references,S.predecessor_references),'assignment bindings');
need(assignment.owner_thread==='01a074c4-4b09-76a3-8cb2-0caf116f6b9c'&&assignment.new_scientific_execution_authority===false&&assignment.RET_paused===true&&assignment.qualification_credit===0,'assignment bounds');
need(decision.status==='ACCEPT_CONDITIONAL_LOWER_COMBINATION_ROUTING_AND_BOUNDS'&&decision.scientific_body_read===false&&decision.scientific_execution===false&&decision.qualification_credit===0,'decision');
for(const k of ['packet','root_manual_review','root_metadata_replay','independent_review'])selected(decision[k]);
need(eq(decision.packet,S.predecessor_handoff),'decision packet');
const prior=admin(S.predecessor_handoff),priorRefs=admin(S.predecessor_references);
const priorNames=fs.readdirSync(P).sort();
need(eq(priorNames,S.predecessor_namespace)&&eq(priorNames,prior.namespace)&&priorNames.length===6&&prior.payloads.length===5,'prior namespace');
prior.payloads.forEach(selected);
need(eq(prior.payloads.map(i=>p.basename(i.path)).concat('HANDOFF.json').sort(),priorNames),'prior seal coverage');
const inherited=admin(S.inherited_manifest_by_reference.identity);
const boundaries=Object.fromEntries(Object.entries(inherited).filter(([k])=>!['schema','status','protected_files','scope'].includes(k)));
need(inherited.protected_files.length===423&&S.inherited_manifest_by_reference.selected_paths===423,'manifest423');
need(eq(boundaries,S.inherited_manifest_by_reference.boundary_objects)&&Object.keys(boundaries).length===15,'15 boundaries');
need(eq(S.inherited_manifest_by_reference,priorRefs.inherited_manifest_by_reference),'whole inherited boundary unchanged');
const byInheritedPath=new Map(inherited.protected_files.map(r=>[r.identity.path,r]));
function inheritedAnalytic(i){
 const row=byInheritedPath.get(i.path);
 need(row&&eq(simple(row.identity),simple(i)),'inherited analytic identity');
 need(row.classification==='analytic-source-text-or-review'&&row.access_policy==='text-reading-and-opaque-identity-no-execution','inherited analytic boundary');
}
need(eq(S.inherited_original_six_admissions,assignment.source_admission)&&eq(S.inherited_original_six_admissions,priorRefs.inherited_original_six_admissions)&&assignment.source_admission.length===6,'original six');
need(eq(S.inherited_additional_admissions,assignment.inherited_additional_admissions)&&eq(S.inherited_additional_admissions,priorRefs.inherited_additional_admissions),'additional two');
need(eq(S.inherited_RI189_analytic_admission,assignment.inherited_RI189_analytic_admission)&&eq(S.inherited_RI189_analytic_admission,priorRefs.inherited_RI189_analytic_admission),'RI189 two');
for(const row of [...S.inherited_original_six_admissions,...S.inherited_RI189_analytic_admission]){
 need(row.typed_reference_expansion===false&&row.inherited_matches.length>0,'inherited flags');
 for(const i of row.inherited_matches){inheritedAnalytic(i);need(i.bytes===row.identity.bytes&&i.sha256===row.identity.sha256,'inherited byte match');}
}
const A=S.inherited_shared_affine_admission;
need(eq(A,priorRefs.inherited_shared_affine_admission)&&eq(A.authority,assignment.additional_shared_affine_admission),'shared admission unchanged');
selected(A.authority);selected(A.reference);
const shared=admin(A.authority);
need(shared.status==='ADMIT_EXACT_EXISTING_ANALYTIC_TEXT_ONLY'&&eq(shared.reference,A.reference)&&eq(shared.inherited_match,A.inherited_match)&&eq(shared.inherited_manifest,S.inherited_manifest_by_reference.identity),'shared source binding');
need(eq(byInheritedPath.get(A.reference.path),A.inherited_match),'shared full inherited row');inheritedAnalytic(A.reference);
for(const k of ['typed_reference_expansion','scientific_body_admission','execution_admitted','automatic_scientific_arithmetic'])need(shared[k]===false,'shared bounds');
need(A.typed_reference_expansion===false&&shared.qualification_credit===0,'shared credit');
need(eq(S.inherited_RI223_literal_admissions,priorRefs.inherited_RI223_literal_admissions)&&eq(S.inherited_RI223_literal_admissions,assignment.current_inherited_literal_admissions)&&S.inherited_RI223_literal_admissions.length===2,'RI223 renewal');
for(const B of S.inherited_RI223_literal_admissions){
 selected(B.authority);selected(B.reference);const adm=admin(B.authority);
 need(adm.status==='ADMIT_EXACT_EXISTING_ANALYTIC_TEXT_ONLY'&&adm.reservation==='/Volumes/AI_DATA/development/det-review-evidence/ri223-native-active-amplitude-63hp1o02','RI223 origin');
 need(eq(adm.reference,B.reference)&&eq(adm.inherited_matches,B.inherited_matches)&&eq(adm.inherited_manifest,S.inherited_manifest_by_reference.identity),'RI223 exact binding');
 for(const row of B.inherited_matches){need(eq(byInheritedPath.get(row.identity.path),row),'RI223 full row');inheritedAnalytic(row.identity);need(row.identity.bytes===B.reference.bytes&&row.identity.sha256===B.reference.sha256,'RI223 same bytes');}
 for(const k of ['typed_reference_expansion','scientific_body_admission','execution_admitted','automatic_scientific_arithmetic'])need(adm[k]===false,'RI223 limits');
 need(B.typed_reference_expansion===false&&adm.qualification_credit===0,'RI223 credit');
}
const D=S.inherited_RI225_disconnected_admission;
need(eq(D,priorRefs.inherited_RI225_disconnected_admission)&&eq(D.authority,assignment.additional_disconnected_admission),'RI225 unchanged');
selected(D.authority);selected(D.reference);const da=admin(D.authority);
need(da.status==='ADMIT_EXACT_EXISTING_ANALYTIC_TEXT_ONLY'&&da.reservation==='/Volumes/AI_DATA/development/det-review-evidence/ri225-native-shared-mobility-yftvo6zl','RI225 origin');
need(eq(da.reference,D.reference)&&eq(da.inherited_match,D.inherited_match)&&eq(da.inherited_manifest,S.inherited_manifest_by_reference.identity)&&eq(byInheritedPath.get(D.reference.path),D.inherited_match),'RI225 exact row');
inheritedAnalytic(D.reference);
for(const k of ['typed_reference_expansion','scientific_body_admission','execution_admitted','automatic_scientific_arithmetic'])need(da[k]===false,'RI225 bounds');
need(D.typed_reference_expansion===false&&da.qualification_credit===0,'RI225 credit');
const C=S.inherited_RI228_construction_admissions;
need(C.length===2&&eq(C,priorRefs.additional_literal_admissions)&&eq(C.map(r=>r.authority),assignment.renewed_RI228_construction_admissions),'RI228 construction renewal');
for(const B of C){
 selected(B.authority);selected(B.reference);const ca=admin(B.authority);
 need(ca.status==='ADMIT_EXACT_EXISTING_ANALYTIC_TEXT_ONLY'&&eq(ca.assignment,prior.assignment)&&ca.reservation===P,'RI228 origin');
 need(eq(ca.reference,B.reference)&&eq(ca.inherited_match,B.inherited_match)&&eq(ca.inherited_manifest,S.inherited_manifest_by_reference.identity)&&eq(byInheritedPath.get(B.reference.path),B.inherited_match),'RI228 exact row');
 inheritedAnalytic(B.reference);
 for(const k of ['typed_reference_expansion','scientific_body_admission','execution_admitted','automatic_scientific_arithmetic'])need(ca[k]===false,'RI228 bounds');
 need(B.typed_reference_expansion===false&&ca.qualification_credit===0,'RI228 credit');
}
need(assignment.same_exact_analytic_reads_renewed_for_current_reservation===true,'current renewal');
const F=S.predecessor_literal_exception_boundary;
need(eq(F,priorRefs.predecessor_literal_exception_boundary)&&F.typed_reference_expansion===false&&F.new_body_read_authority===false&&F.new_coefficient_coordinate_resolution===false&&F.historical_source_body_not_reopened===true,'old exception historical unchanged, not current permission');
need(eq(S.inherited_RI216_native_premises_by_reference,priorRefs.inherited_RI216_native_premises_by_reference),'old premise history');
need(eq(S.predecessor_lower_law_metadata_boundary,priorRefs.predecessor_lower_law_metadata_boundary),'old lower hint history');
need(eq(assignment.accepted_four_root_witness,S.accepted_four_root_witness)&&eq(F.prior_exception.witness_acceptance,S.accepted_four_root_witness),'four-root acceptance binding');
const w=admin(S.accepted_four_root_witness);
need(w.status==='ACCEPT_FIXED_PREFIX_FOUR_ROOT_WITNESS'&&w.new_scientific_execution===false,'four-root premise only');
const E=S.separate_current_literal_exception;
selected(E.authority);selected(E.body);
const ea=admin(E.authority);
need(ea.status==='ADMIT_EXACT_SIX_ROOT_LITERAL_MATHEMATICAL_INSPECTION_ONLY'&&eq(ea.assignment,S.assignment)&&eq(ea.predecessor_proof,S.accepted_predecessor)&&ea.reservation===Q&&ea.owner_thread===assignment.owner_thread,'current literal exception binding');
need(eq(simple(ea.identity),E.body)&&eq(ea.inherited_manifest,S.inherited_manifest_by_reference.identity)&&eq(ea.inherited_body_row_not_reclassified,E.inherited_body_row_not_reclassified),'current exception exact metadata');
need(eq(byInheritedPath.get(E.body.path),E.inherited_body_row_not_reclassified),'opaque body inherited row unchanged');
need(E.inherited_body_row_not_reclassified.classification==='opaque-scientific-historical-premise'&&E.inherited_body_row_not_reclassified.access_policy==='whole-byte-identity-only-no-decoding-or-execution','inherited body classification not changed');
need(eq(ea.keys,E.allowed_keys)&&eq(E.allowed_keys,[[2,3,0],[6,3,0],[70,3,0],[70,7,0],[70,9,0],[70,9,1]]),'exact six-key authorization whitelist only');
need(ea.typed_reference_expansion===false&&ea.source_inventory_expansion===false&&ea.admitted_program_execution===false&&ea.qualification_credit===0&&ea.RET_paused===true,'new exception limits');
for(const k of ['automatic_scientific_JSON_parsing','full_vector_instantiation','other_coordinate_resolution','program_execution','typed_reference_expansion'])need(E[k]===false,'current literal declaration '+k);
need(E.complete_literal_display===true&&E.before_and_after_receipt.exit_code===0&&E.old_exception_is_historical_not_permission===true&&E.historical_state_array_not_compared_to_current_stat===true,'literal receipt and state boundary');
const literalRows=S.direct_sources.filter(r=>r.access==='exact-literal-scientific-exception');
need(literalRows.length===1&&eq(literalRows[0].identity,E.body),'only one direct scientific exception');
need(eq(E.body,F.prior_exception.body),'same unchanged original body, distinct current permission');
for(const group of S.current_literal_reads){need(group.receipt.exit_code===0,'read receipt');group.files.forEach(selected);}
need(S.predecessor_complete_proof_read.receipt.exit_code===0,'predecessor complete proof receipt');S.predecessor_complete_proof_read.files.forEach(selected);
need(eq(S.inherited_analytic_read_history_by_reference.identity,S.predecessor_references)&&S.inherited_analytic_read_history_by_reference.field==='inherited_analytic_read_history'&&S.inherited_analytic_read_history_by_reference.typed_reference_expansion===false,'old read history by reference only');
selected(S.predecessor_author_support.identity);
need(S.predecessor_author_support.access==='opaque-historical-support'&&S.predecessor_author_support.typed_reference_expansion===false,'prior author opaque');
const yes=["manual_analysis_only","original_quarter_rejection_immutable","accepted_small_amplitude_family_preserved","six_named_roots_resolved_with_original_indices_and_provenance","corresponding_alpha_gamma_combinations_only","scientific_body_literal_read_under_separate_current_exception","complete_canonical_P_ideal_inventory_proved","complete_four_family_incidence_and_marked_components_proved","every_original_record_and_canonical_correction_preserved","stronger_kappa_bound_and_sector_tightness_proved","exact_conditional_capacity_identity_proved","native_exchange_objective_includes_all_affected_parents","actual_scales_and_full_normalized_system_unchanged","inherited_finite_premises_remain_conditional","ret_paused"];
const no=["canonical_kappa_or_competing_values_determined","native_improvement_or_optimality_decided","native_lifting_direction_found","native_inconsistency_identity_found","maximal_full_amplitude_decided","numerical_amplitude_selected","automatic_scientific_JSON_parsing_or_proof_arithmetic","full_vector_or_other_coordinate_resolution","other_scientific_body_read","H_or_z_reconstruction","actual_rho_s_theta_evaluated","graph_LP_subject_runtime_fixture_card_execution","repository_Git_index_or_measurement_written","full_QM_geometry_or_physical_claim","all_size_continuation_claim","successor_designed_or_started"];
for(const k of yes)need(S.scope[k]===true,'declared scope true '+k);
for(const k of no)need(S.scope[k]===false,'declared scope false '+k);
need(S.scope.qualification_credit===0&&eq(S.executable_obligations,priorRefs.executable_obligations)&&S.executable_obligations.new_credit===0,'unchanged executable obligations');
const stage=process.argv[1]||'preseal4';need(['preseal4','final6'].includes(stage),'stage');
const final=['AUTHOR_VERIFICATION.json','CANONICAL_CAPACITY.md','HANDOFF.json','HANDOFF.md','SIX_ROOT_WITNESS.md','SOURCE_REFERENCES.json'];
const expected=stage==='final6'?final:final.filter(n=>!['AUTHOR_VERIFICATION.json','HANDOFF.json'].includes(n));
need(eq(fs.readdirSync(Q).sort(),expected),'current namespace');
const payloads=expected.map(n=>{const r=readExact({path:Q+'/'+n});cache.set(r.path,r);return simple(r);});
for(const n of ['CANONICAL_CAPACITY.md','SIX_ROOT_WITNESS.md','HANDOFF.md']){
 const t=cache.get(Q+'/'+n).body.toString('utf8');
 need(!/^(<{7}|={7}|>{7})( |$)/m.test(t)&&!/[ \t]+$/m.test(t),'Markdown hygiene');
 for(const m of t.matchAll(/\[[^\]]+\]\(([^)]+)\)/g))need(final.includes(m[1]),'local link target');
}
if(stage==='final6'){
 const h=JSON.parse(cache.get(Q+'/HANDOFF.json').body),a=JSON.parse(cache.get(Q+'/AUTHOR_VERIFICATION.json').body);
 need(eq(h.namespace,final)&&h.payloads.length===5&&eq(h.payloads.map(i=>p.basename(i.path)).sort(),final.filter(n=>n!=='HANDOFF.json')),'current seal coverage');
 h.payloads.forEach(pin);selected(h.assignment);selected(h.accepted_predecessor);selected(h.separate_literal_exception);
 need(eq(h.scope,S.scope)&&eq(h.executable_obligations,S.executable_obligations),'handoff scope');
 need(a.status==='AUTHOR_SIX_ROOT_WITNESS_AND_CANONICAL_CAPACITY_WITH_OPEN_FULL_WITNESS_NOT_INDEPENDENT_ACCEPTANCE'&&a.preseal.actual_result.current_namespace===4&&a.final6_not_yet_run_at_author_creation===true,'author phase');
 a.preseal.actual_result.current_payloads.forEach(pin);
 need(eq(a.scope,S.scope)&&eq(a.executable_obligations,S.executable_obligations),'author scope');
}
const all=[...cache.values()].map(simple);need(all.length===32+expected.length,'fresh scope');
all.forEach(readExact);
need(eq(fs.readdirSync(Q).sort(),expected)&&eq(fs.readdirSync(P).sort(),priorNames),'post namespaces');
console.log(JSON.stringify({
 schema:'ri231-compact-administrative-check-v1',status:'IDENTITY_MATCH_NOT_MATHEMATICAL_ACCEPTANCE',stage,
 direct_sources:32,direct_bytes:796922,inherited423_manifest_by_reference:true,
 fresh_inherited423_collection_replay:false,inherited_boundary_objects_preserved:15,
 inherited_exact_analytic_admissions_renewed_without_expansion:true,
 new_separate_literal_scientific_exception:1,authorized_keys:6,scientific_body_JSON_parsed:false,
 old_exception_not_used_as_current_permission:true,inherited_opaque_body_row_not_reclassified:true,
 historical_state_arrays_not_current_stat_expectations:true,
 explicit_selected_reference_checks:references,predecessor_namespace:6,current_namespace:expected.length,
 whole_identity_fresh_rechecks:all.length,current_payloads:payloads,
 declared_local_Markdown_targets:stage==='final6'?'all-present':'final-presence-pending',
 automated_proof_arithmetic:false,subject_execution:false
},null,2));
