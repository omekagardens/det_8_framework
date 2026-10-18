// Read-only metadata/opaque-byte review. No scientific values are computed.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { isDeepStrictEqual as equal } from 'node:util';

const E = '/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx';
const D = '/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky';
const errors = [];
const need = (condition, label) => { if (!condition) errors.push(label); };
const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const short = x => ({ bytes: x.bytes, sha256: x.sha256 });
const literal = x => ({ path: x.path, ...short(x) });
const signature = s => ['dev', 'ino', 'size', 'mode', 'mtimeNs', 'ctimeNs'].map(k => String(s[k]));
const observed = new Map();
function inspect(p) {
  if (observed.has(p)) return observed.get(p);
  need(path.isAbsolute(p) && path.normalize(p) === p, 'nonliteral path: ' + p);
  let ancestor = '/';
  const ancestry = [];
  for (const part of p.split('/').filter(Boolean)) {
    ancestor = path.join(ancestor, part);
    const s = fs.lstatSync(ancestor, { bigint: true });
    need(!s.isSymbolicLink(), 'symlink ancestry: ' + ancestor);
    need(ancestor === p ? s.isFile() : s.isDirectory(), 'wrong ancestry type: ' + ancestor);
    ancestry.push(ancestor);
  }
  const before = fs.lstatSync(p, { bigint: true });
  const raw = fs.readFileSync(p);
  const after = fs.lstatSync(p, { bigint: true });
  need(equal(signature(before), signature(after)), 'changed during read: ' + p);
  need(fs.realpathSync.native(p) === p, 'realpath differs: ' + p);
  const identity = { path: p, resolved_path: p, bytes: raw.length,
    sha256: crypto.createHash('sha256').update(raw).digest('hex'), symlinks: [] };
  const result = { identity, device: String(after.dev), inode: String(after.ino),
    ancestry_components_checked: ancestry.length, regular_literal_nonsymlink: true };
  observed.set(p, result);
  return result;
}
function checkIdentity(x, label) {
  const actual = inspect(x.path).identity;
  need(equal(short(x), short(actual)), label + ': bytes/hash');
  if ('resolved_path' in x) need(equal(x, actual), label + ': full identity');
  return actual;
}
const binding = read(E + '/AUDIT_BINDING.json');
const descriptorPath = binding.descriptor.path;
checkIdentity(binding.descriptor, 'binding descriptor');
const descriptor = read(descriptorPath);
const report = read(E + '/audit-01/REPORT.json');
const freeze = read(E + '/AUDIT_EXECUTION_FREEZE.json');
const prepared = read(E + '/audit-01/prepared.json');
const receipt = read(E + '/audit-01/receipt.json');
const root = read(E + '/AUDIT_ROOT_COMPLETE_REVIEW.json');
const source = read(E + '/ROOT_SOURCE_ADJUDICATION.json');
const outer = read(E + '/AUDIT_OUTER_TOOL_RESULT.json');
const chain = read(D + '/AUDIT_GENUINE_TOOL_CHAIN.json');
const premises = ['ri88', 'ri111', 'ri109_adjudication', 'ri111_adjudication',
  'ri115_adjudication', 'ri117', 'ri117_connected', 'ri117_adjudication'];
const sources = ['checker', 'protocol', 'contract'];
const custody = ['producer_witness_stdout', 'producer_witness_custody',
  'producer_normal_custody', 'producer_optimized_custody', 'consumer_source_review'];
need(equal(Object.keys(descriptor).sort(), ['accepted_sources','audit_source','custody_dependencies','files','phase','schema']), 'descriptor keys');
need(descriptor.schema === 'ri120-independent-audit-input-v1' && descriptor.phase === 'fixed_saved_certificate_audit', 'descriptor schema/phase');
need(equal(Object.keys(descriptor.files).sort(), [...premises, 'candidate'].sort()), 'descriptor file roles');
need(equal(Object.keys(descriptor.accepted_sources).sort(), [...sources].sort()), 'descriptor source roles');
need(equal(descriptor.custody_dependencies.map(x => x.role), custody), 'descriptor custody order');
const entries = [
  ...[...premises, 'candidate'].map(role => ({ role: 'files.' + role, ...descriptor.files[role] })),
  ...sources.map(role => ({ role: 'accepted_sources.' + role, ...descriptor.accepted_sources[role] })),
  { role: 'audit_source', ...descriptor.audit_source },
  ...descriptor.custody_dependencies.map(x => ({ role: 'custody.' + x.role, ...literal(x) }))
];
need(equal(entries, report.payload_role_bindings), 'complete ordered 18 report bindings');
need(report.payload_role_count === 18 && report.unique_payload_paths === 18, 'report payload counts');
const protectedEntries = [...entries, { role: 'descriptor', ...literal(binding.descriptor) }];
need(new Set(protectedEntries.map(x => x.path)).size === 19, '19 distinct literal paths');
const freezeByPath = new Map();
for (const x of freeze.inputs) {
  if (!freezeByPath.has(x.path)) freezeByPath.set(x.path, []);
  freezeByPath.get(x.path).push(x);
}
const rows = [];
for (const x of protectedEntries) {
  need(Number.isSafeInteger(x.bytes) && x.bytes > 0 && x.bytes <= 8388608, x.role + ': positive bounded bytes');
  need(/^[0-9a-f]{64}$/.test(x.sha256), x.role + ': canonical hash');
  const actual = checkIdentity(x, x.role);
  const records = freezeByPath.get(x.path) || [];
  need(records.length > 0, x.role + ': in freeze');
  for (const record of records) {
    need(equal(record.identity, actual), x.role + ': frozen identity ' + record.role);
    for (const [name, group] of [['prepared',prepared.observed_inputs],['before',receipt.inputs_before],['after',receipt.inputs_after]]) {
      const v = group[record.role];
      need(v?.ok === true && equal(v.identity, actual), x.role + ': ' + name + ' ' + record.role);
    }
  }
  const posts = report.postchecks.filter(p => p.path === x.path);
  need(posts.length === 1 && posts[0].unchanged === true && equal(posts[0].identity, short(actual)), x.role + ': report postcheck');
  rows.push({ role: x.role, ...inspect(x.path), frozen_roles: records.map(z => z.role),
    freeze_prepared_before_after_match: true, report_postcheck_matches: true });
}
need(report.postchecks.length === 19, '19 exact postchecks');
const postOrder = [descriptor.audit_source.path, ...entries.filter(x => x.role !== 'audit_source').map(x => x.path), descriptorPath];
need(equal(report.postchecks.map(x => x.path), postOrder), 'source-defined postcheck order');
need(new Set(rows.map(x => x.device + ':' + x.inode)).size === 19, '19 distinct physical files');
need(equal(report.descriptor_identity, short(binding.descriptor)), 'report descriptor identity');
need(equal(report.audit_source_identity, short(descriptor.audit_source)), 'report audit source identity');
need(equal(report.accepted_source_identities, Object.fromEntries(sources.map(k => [k, short(descriptor.accepted_sources[k])]))), 'report accepted sources');
const argv = ['/opt/homebrew/bin/python3', '-I', '-S', '-B', descriptor.audit_source.path, descriptorPath, String(binding.descriptor.bytes), binding.descriptor.sha256];
for (const [name,v] of [['freeze',freeze], ['prepared',prepared], ['receipt',receipt]]) need(equal(v.argv, argv), name + ': exact descriptor argv');
const pairRoles = ['checker', 'auditor', 'implementation', 'audit_contract', ...premises];
const pairs = [];
for (const role of pairRoles) {
  const original = freeze.inputs.find(x => x.role === role + '_original');
  const copy = freeze.inputs.find(x => x.role === role + '_copy');
  need(Boolean(original && copy), 'pair missing: ' + role);
  if (!original || !copy) continue;
  const a = checkIdentity(original.identity, role + ' original');
  const b = checkIdentity(copy.identity, role + ' copy');
  need(a.path !== b.path && equal(short(a), short(b)), role + ': distinct-path equal-byte pins');
  need(fs.readFileSync(a.path).equals(fs.readFileSync(b.path)), role + ': whole bytes equal');
  pairs.push({ role, original: a, copy: b, whole_bytes_equal: true });
}
for (const [role,x] of Object.entries(source.accepted_sources)) checkIdentity(x, 'accepted current ' + role);
checkIdentity(source.independent_review, 'current independent source review');
const sourceReview = read(source.independent_review.path);
need(equal(sourceReview.sources, source.accepted_sources), 'current independent review exact accepted source set');
need(sourceReview.status === 'PASS_COMPLETE_SOURCE_REVIEW_ONLY' && sourceReview.execution_authorized === false, 'independent source-only review status');
checkIdentity(source.ri120_source_adjudication, 'accepted RI120 source decision');
const sourceDecision120 = read(source.ri120_source_adjudication.path);
checkIdentity(sourceDecision120.handoff, 'accepted RI120 handoff');
const handoff120 = read(sourceDecision120.handoff.path);
const sourceFiles120 = ['check.py', 'audit_saved_certificate.py', 'IMPLEMENTATION.md', 'AUDIT_CONTRACT.md'];
for (const f of sourceFiles120) {
  const entry = handoff120.artifacts.find(x => x.file === f);
  need(Boolean(entry), 'RI120 accepted artifact: ' + f);
  if (entry) checkIdentity({ path: path.dirname(sourceDecision120.handoff.path) + '/' + f, ...short(entry) }, 'RI120 accepted artifact ' + f);
}
for (const [role,x] of Object.entries(binding)) {
  if (x && typeof x === 'object' && !Array.isArray(x)) {
    if ('path' in x) checkIdentity(x, 'binding ' + role);
    else for (const [r,y] of Object.entries(x)) checkIdentity(y, 'binding ' + role + '.' + r);
  }
}
for (const [role,x] of Object.entries(root.outputs)) checkIdentity(x, 'root output ' + role);
for (const role of ['applicability','authorization','freeze','genuine_outer','receipt','root_admission','source_adjudication']) checkIdentity(root[role], 'root ' + role);
need(fs.readFileSync(E + '/audit-01/REPORT.json').equals(fs.readFileSync(E + '/audit-01/stdout.log')), 'REPORT is entire stdout copy');
need(fs.readFileSync(descriptor.files.candidate.path).equals(fs.readFileSync(descriptor.custody_dependencies[0].path)), 'candidate is entire witness copy');
for (const x of Object.values(binding.candidates)) need(fs.readFileSync(x.path).equals(fs.readFileSync(descriptor.custody_dependencies[0].path)), 'native candidate whole bytes: ' + x.path);
need(equal(outer.invocation, chain.invocation) && equal(outer.result, chain.completion), 'saved genuine tool transcriptions agree');
const outerSummary = JSON.parse(outer.result.output);
need(outer.result.exit_code === 0 && outer.result.chunk_id === '402c12' && !('session_id' in outer.result), 'outer completed exit metadata');
need(equal(outerSummary, { mode: 'audit', receipt: E + '/audit-01/receipt.json', receipt_sha256: inspect(E + '/audit-01/receipt.json').identity.sha256, success: true }), 'outer summary binds current receipt');
need(equal(report.reconstructed_certificate_identity, short(descriptor.files.candidate)), 'reported reconstructed whole certificate identity');
const result = {
  schema: 'ri122-nonauthor-actual-audit-binding-metadata-review-v1',
  status: errors.length ? 'FAIL_METADATA_BINDING_REVIEW' : 'PASS_METADATA_BINDING_REVIEW_ONLY',
  reviewer: '/root/ri122_actual_audit_bindings',
  observed_at_utc: new Date().toISOString(),
  actual_report: inspect(E + '/audit-01/REPORT.json').identity,
  actual_descriptor: inspect(descriptorPath).identity,
  actual_binding: inspect(E + '/AUDIT_BINDING.json').identity,
  source_adjudication: inspect(E + '/ROOT_SOURCE_ADJUDICATION.json').identity,
  root_completed_review: inspect(E + '/AUDIT_ROOT_COMPLETE_REVIEW.json').identity,
  frozen_descriptor_argv: argv,
  protected_files: rows,
  original_copy_pairs: pairs,
  current_source_identities: source.accepted_sources,
  all_opaque_observed_identities: [...observed.values()].map(x => x.identity),
  distinct_protected_literal_paths: new Set(rows.map(x => x.identity.path)).size,
  distinct_protected_device_inode_pairs: new Set(rows.map(x => x.device + ':' + x.inode)).size,
  saved_outer_chunk: outer.result.chunk_id,
  saved_outer_exit_code: outer.result.exit_code,
  saved_outer_transcription_agreement: true,
  report_whole_bytes_equal_stdout: true,
  all_three_candidates_whole_bytes_equal_witness: true,
  source_defined_report_postcheck_order_matches: true,
  scientific_arithmetic_performed: false,
  target_or_existing_helper_executed: false,
  independent_runtime_custody_adjudication: false,
  actual_tool_history_independently_observed: false,
  errors
};
console.log(JSON.stringify(result, null, 2));
if (errors.length) process.exitCode = 1;
