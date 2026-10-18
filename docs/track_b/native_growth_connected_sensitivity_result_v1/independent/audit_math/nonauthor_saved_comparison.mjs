// Saved JSON/type/byte review only. No target import, source evaluation,
// rational conversion, scientific arithmetic, subprocess, or file write.
import fs from 'node:fs';
import crypto from 'node:crypto';
const E = '/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx';
const D = '/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky';
const A = '/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn';
const errors = [];
const need = (ok, name) => { if (!ok) errors.push(name); };
const identity = raw => ({bytes: raw.length, sha256: crypto.createHash('sha256').update(raw).digest('hex')});
const pin = path => ({path, ...identity(fs.readFileSync(path))});
const kind = value => value === null ? 'null' : Array.isArray(value) ? 'array' : typeof value;
let comparedNodes = 0;
function exact(a, b, where) {
  comparedNodes++;
  if (kind(a) !== kind(b)) { errors.push(where + ':type'); return; }
  if (Array.isArray(a)) {
    need(a.length === b.length, where + ':length');
    a.forEach((v,i) => exact(v,b[i],where+'['+i+']'));
  } else if (a !== null && typeof a === 'object') {
    const ak = Object.keys(a).sort(), bk = Object.keys(b).sort();
    need(JSON.stringify(ak) === JSON.stringify(bk),where+':keys');
    ak.forEach(k => exact(a[k],b[k],where+'.'+k));
  } else need(Object.is(a,b),where+':value');
}
function sorted(value) {
  if (typeof value === 'number') {
    need(Number.isSafeInteger(value) && !Object.is(value,-0),'safe-JSON-integer');
    return value;
  }
  if (Array.isArray(value)) return value.map(sorted);
  if (value !== null && typeof value === 'object')
    return Object.fromEntries(Object.keys(value).sort().map(k => [k,sorted(value[k])]));
  return value;
}
function canonical(value) {
  const out = JSON.stringify(sorted(value))+'\n';
  need(!/[^\x00-\x7f]/.test(out),'ASCII-canonical-domain');
  return Buffer.from(out,'ascii');
}
const reportRaw=fs.readFileSync(E+'/audit-01/REPORT.json');
const witnessRaw=fs.readFileSync(E+'/witness-01/stdout.log');
const report=JSON.parse(reportRaw), cert=JSON.parse(witnessRaw);
const rootComparison=JSON.parse(fs.readFileSync(D+'/ROOT_COMPLETE_SAVED_AUDIT_COMPARISON.json'));
const descriptor=JSON.parse(fs.readFileSync(E+'/AUDIT_INPUT.json'));
const reportKeys=['accepted_source_identities','audit_source_identity','complete_top_level_sections','custody_semantics_self_adjudicated','declared_producer_controls','descriptor_identity','independence','independent_counted_operations','independently_rebuilt_decision_fixture_count','independently_rebuilt_family_fixture_count','independently_rebuilt_fixture_count','limits','payload_role_bindings','payload_role_count','postchecks','reconstructed_certificate','reconstructed_certificate_identity','schema','status','unique_payload_paths'];
const sectionKeys=['Q2_contrasts','V_contrasts','accepted_inputs','accepted_sources','arithmetic_limits','checker_sha256','common_gcd','connected_profiles','coverage','decision','decision_fixtures','family_fixtures','inputs','limitations','refusal_controls','root_fixtures','scale_domain','schema','stem_profiles'];
exact(Object.keys(report).sort(),reportKeys,'report-fields');
exact(Object.keys(cert).sort(),sectionKeys,'nineteen-certificate-fields');
need(reportRaw.equals(canonical(report)),'whole-report-canonical-bytes');
need(witnessRaw.equals(canonical(cert)),'whole-witness-canonical-bytes');
exact(report.reconstructed_certificate,cert,'all-reconstructed-fields');
need(witnessRaw.equals(canonical(report.reconstructed_certificate)),'whole-reconstructed-certificate-bytes');
exact(report.reconstructed_certificate_identity,identity(witnessRaw),'reconstructed-identity');
for (const suffix of ['/CERTIFICATE.json','/AUDIT_CANDIDATE.json','/closure/native_growth_connected_sensitivity_v1/CERTIFICATE.json'])
  need(fs.readFileSync(E+suffix).equals(witnessRaw),'whole-candidate-equality:'+suffix);
need(fs.readFileSync(E+'/audit-01/stdout.log').equals(reportRaw),'whole-report-stdout-equality');
need(fs.readFileSync(E+'/normal-01/stdout.log').equals(fs.readFileSync(E+'/optimized-01/stdout.log')),'whole-mode-byte-equality');
const sections=Object.fromEntries(sectionKeys.map(k=>[k,identity(canonical(cert[k]))]));
exact(report.complete_top_level_sections,sections,'all-section-byte-identities');
exact(rootComparison.sections,sections,'root-section-comparison');
exact(rootComparison.decision,cert.decision,'root-decision');
const sourcePins={checker:pin(A+'/check.py'),protocol:pin(A+'/IMPLEMENTATION.md'),contract:pin(A+'/AUDIT_CONTRACT.md')};
for(const [role,p] of Object.entries(sourcePins)) {
  exact(report.accepted_source_identities[role],{bytes:p.bytes,sha256:p.sha256},'source-'+role);
  need(fs.readFileSync(p.path).equals(fs.readFileSync(descriptor.accepted_sources[role].path)),'source-copy-'+role);
}
const auditorPin=pin(A+'/audit_saved_certificate.py');
exact(report.audit_source_identity,{bytes:auditorPin.bytes,sha256:auditorPin.sha256},'auditor-identity');
need(fs.readFileSync(auditorPin.path).equals(fs.readFileSync(descriptor.audit_source.path)),'auditor-copy');
exact(report.descriptor_identity,identity(fs.readFileSync(E+'/AUDIT_INPUT.json')),'descriptor-identity');
const premiseRoles=['ri88','ri111','ri109_adjudication','ri111_adjudication','ri115_adjudication','ri117','ri117_connected','ri117_adjudication','candidate'];
const expectedBindings=[...premiseRoles.map(role=>({role:'files.'+role,...descriptor.files[role]})),...['checker','protocol','contract'].map(role=>({role:'accepted_sources.'+role,...descriptor.accepted_sources[role]})),{role:'audit_source',...descriptor.audit_source},...descriptor.custody_dependencies.map(({role,...item})=>({role:'custody.'+role,...item}))];
exact(report.payload_role_bindings,expectedBindings,'eighteen-ordered-bindings');
need(new Set(expectedBindings.map(x=>x.path)).size===18,'eighteen-unique-paths');
const postByPath=new Map(report.postchecks.map(x=>[x.path,x]));
need(postByPath.size===19 && report.postchecks.length===19,'nineteen-postcheck-paths');
for(const entry of [...expectedBindings,{path:E+'/AUDIT_INPUT.json',...report.descriptor_identity}]) {
  exact(postByPath.get(entry.path),{path:entry.path,identity:{bytes:entry.bytes,sha256:entry.sha256},unchanged:true},'postcheck:'+entry.path);
  exact(identity(fs.readFileSync(entry.path)),{bytes:entry.bytes,sha256:entry.sha256},'fresh-opaque-pin:'+entry.path);
}
exact(report.declared_producer_controls,{count:166,ordered_pairs:cert.refusal_controls,producer_controls_executed_by_consumer:false},'complete-control-declarations');
need(cert.refusal_controls.length===166,'166-refusals');
need(report.independently_rebuilt_fixture_count===16&&cert.root_fixtures.length===16,'16-root-fixtures');
need(report.independently_rebuilt_family_fixture_count===10&&cert.family_fixtures.length===10,'10-family-fixtures');
need(report.independently_rebuilt_decision_fixture_count===6&&cert.decision_fixtures.length===6,'6-decision-fixtures');
for(const f of cert.root_fixtures){need(f.native_model_claimed===false,'root-fixture-native:'+f.name);exact(f.expected_distinct_real_roots,f.root_certificate.distinct_real_roots,'root-fixture-count:'+f.name);}
for(const f of cert.family_fixtures){need(f.native_model_claimed===false&&f.input_polynomials.length===15,'family-fixture-domain:'+f.name);exact(f.expected_gcd,f.common_gcd.gcd_monic,'family-gcd:'+f.name);exact(f.expected_distinct_real_roots,f.common_gcd.root_certificate?.distinct_real_roots??null,'family-count:'+f.name);}
for(const f of cert.decision_fixtures){need(f.native_model_claimed===false&&f.V_deltas.length===7,'decision-fixture-domain:'+f.name);exact(f.expected_f2_status,f.decision.f2_status,'fixture-f2:'+f.name);exact(f.expected_f3_status,f.decision.f3_status,'fixture-f3:'+f.name);exact(f.expected_rejected,f.decision.restricted_28_child_repair_rejected,'fixture-rejection:'+f.name);}
need(report.independent_counted_operations===10058&&report.independent_counted_operations<=cert.arithmetic_limits.counted_operations,'reported-operations-within-bound');
need(report.custody_semantics_self_adjudicated===false,'custody-boundary');
need(report.schema==='ri120-independent-complete-connected-sensitivity-audit-v1'&&report.status==='all_saved_fields_independently_match','report-mode');
need(report.unique_payload_paths===18&&report.payload_role_count===18,'report-binding-counts');
// Lossless deduplicated display: never convert rational strings to numbers.
const defs=[],index=new Map();
function pack(v){
  if(v===null||typeof v!=='object'&&!(typeof v==='string'&&v.length>90))return v;
  const key=JSON.stringify(v); if(index.has(key))return '@'+index.get(key);
  const out=Array.isArray(v)?v.map(pack):typeof v==='string'?v:Object.fromEntries(Object.entries(v).map(([k,x])=>[k,pack(x)]));
  const id=defs.length; defs.push(out);index.set(key,id);return '@'+id;
}
const root=pack(report.reconstructed_certificate);
function expand(v){
  if(typeof v==='string'&&/^@[0-9]+$/.test(v))return expand(defs[Number(v.slice(1))]);
  if(Array.isArray(v))return v.map(expand);
  if(v!==null&&typeof v==='object')return Object.fromEntries(Object.entries(v).map(([k,x])=>[k,expand(x)]));
  return v;
}
exact(expand(root),cert,'lossless-display-expansion');
if(process.argv[2]==='--display') {
  const start=Number(process.argv[3]),end=Number(process.argv[4]);
  console.log(defs.slice(start,end).map((v,i)=>(start+i)+' '+JSON.stringify(v)).join('\n'));
  console.log(JSON.stringify({start,end,definitions:defs.length,root,errors}));
} else {
  console.log(JSON.stringify({schema:'ri122-nonauthor-saved-audit-comparison-v1',status:errors.length?'BLOCKED':'PASS_SAVED_REPORT_CONSISTENCY_ONLY',scope:'Complete strict saved JSON/types/bytes and opaque pin comparison; no scientific arithmetic or execution custody adjudication.',report:pin(E+'/audit-01/REPORT.json'),witness:pin(E+'/witness-01/stdout.log'),descriptor:pin(E+'/AUDIT_INPUT.json'),root_comparison:pin(D+'/ROOT_COMPLETE_SAVED_AUDIT_COMPARISON.json'),root_custody_review:pin(E+'/AUDIT_ROOT_COMPLETE_REVIEW.json'),source_pins:sourcePins,auditor_pin:auditorPin,compared_nodes:comparedNodes,section_identities:sections,report_fields:reportKeys,fixture_counts:{root:16,family:10,decision:6},producer_refusal_declarations:166,reported_auditor_counted_operations:report.independent_counted_operations,payload_bindings:18,protected_postchecks:19,lossless_display_definitions:defs.length,lossless_display_root:root,new_scientific_arithmetic:false,third_numerical_reconstruction:false,final_custody_accepted:false,errors},null,2));
}
