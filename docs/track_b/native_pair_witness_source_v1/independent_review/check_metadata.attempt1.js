'use strict';
// RI195 reviewer-owned administrative comparison. No Python source is executed,
// imported, compiled, AST-parsed or evaluated. Scientific bodies stay opaque.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {isDeepStrictEqual} = require('util');
const B = '/Volumes/AI_DATA/development/det-review-evidence';
const S = B + '/ri191-exact-pair-witness-source-uu414bjg';
const P = B + '/ri189-coupled-record-contrast-y5nubaac';
const OUT = B + '/ri195-pair-witness-independent-review-cf5d6lpb';
const A = B + '/ri192-root-optimized-profile-gtsq3_01/RI195_REVIEW_ASSIGNMENT.json';
const facts = [];
function demand(condition, name) {
  if (!condition) throw new Error(name);
  facts.push(name);
}
function equal(a, b, name) { demand(isDeepStrictEqual(a, b), name); }
const observed = new Map();
const statFields = ['dev', 'ino', 'mode', 'nlink', 'size', 'mtimeNs', 'ctimeNs'];
function state(s) { return statFields.map(k => s[k].toString()); }
function read(file) {
  if (observed.has(file)) return observed.get(file);
  demand(path.isAbsolute(file) && path.normalize(file) === file, 'normalized:' + file);
  let parent = '/';
  for (const part of file.split('/').filter(Boolean)) {
    parent = path.join(parent, part);
    const item = fs.lstatSync(parent);
    demand(!item.isSymbolicLink(), 'no-link:' + parent);
    if (parent !== file) demand(item.isDirectory(), 'directory:' + parent);
  }
  const before = fs.lstatSync(file, {bigint: true});
  demand(before.isFile() && before.size >= 0n && before.size <= 67108864n, 'regular-cap:' + file);
  const fd = fs.openSync(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  let body;
  try {
    equal(state(fs.fstatSync(fd, {bigint: true})), state(before), 'fd-before:' + file);
    const parts = []; let length = 0; const maximum = Number(before.size) + 1;
    while (length < maximum) {
      const buf = Buffer.alloc(Math.min(65536, maximum - length));
      const n = fs.readSync(fd, buf, 0, buf.length, null);
      if (n === 0) break;
      parts.push(buf.subarray(0, n)); length += n;
    }
    body = Buffer.concat(parts);
    equal(body.length, Number(before.size), 'complete-size:' + file);
    equal(state(fs.fstatSync(fd, {bigint: true})), state(before), 'fd-after:' + file);
  } finally { fs.closeSync(fd); }
  equal(state(fs.lstatSync(file, {bigint: true})), state(before), 'path-after:' + file);
  equal(fs.realpathSync(file), file, 'realpath:' + file);
  const record = {path: file, bytes: body.length,
    sha256: crypto.createHash('sha256').update(body).digest('hex'), state: state(before), body};
  observed.set(file, record);
  return record;
}
function simple(r) { return {path: r.path, bytes: r.bytes, sha256: r.sha256}; }
function pin(i) {
  demand(typeof i.path === 'string' && Number.isSafeInteger(i.bytes)
    && /^[a-f0-9]{64}$/.test(i.sha256), 'typed-pin:' + i.path);
  const r = read(i.path);
  equal(simple(r), {path: i.path, bytes: i.bytes, sha256: i.sha256}, 'pin:' + i.path);
  if ('resolved_path' in i) equal(i.resolved_path, i.path, 'historic-resolved:' + i.path);
  for (const key of ['symlinks', 'symlink_chain']) if (key in i) equal(i[key], [], key + ':' + i.path);
  // Historical state is deliberately NOT compared with this read's stat tuple.
  return r;
}
function admin(file) { return JSON.parse(read(file).body.toString('utf8')); }
pin({path: A, bytes: 2739, sha256: '2f52986a657c8e389a3d338ddc6b46a8b8262e2463da61759e1ca291fbf1fb35'});
const assignment = admin(A);
pin(assignment.subject_handoff); pin(assignment.opaque_admission); pin(assignment.predecessor);
const H = admin(S + '/HANDOFF.json');
equal(fs.readdirSync(S).sort(), H.namespace.slice().sort(), 'source exact namespace');
equal(H.payloads.map(x => path.basename(x.path)).sort(), H.namespace.filter(x => x !== 'HANDOFF.json').sort(), 'source exact payload coverage');
equal(H.namespace.length, 9, 'source nine files');
H.payloads.forEach(pin);
const D = admin(S + '/SOURCE_DEPENDENCIES.json');
const I = admin(S + '/SOURCE_IDENTITIES.json');
const author = admin(S + '/AUTHOR_VERIFICATION.json');
const admission = admin(assignment.opaque_admission.path);
equal(admission.status, 'ADMIT_OPAQUE_WHOLE_IDENTITY_ONLY', 'opaque admission scope');
equal(admission.scientific_execution, false, 'no scientific admission');
equal(simple(pin(admission.identity)), I.original_prefix_identity_authorization.original_certificate, 'certificate opaque pin');
const rows = D.protected_files, selection = new Map(rows.map(r => [r.path, r]));
equal(selection.size, 389, '389 distinct dependencies');
equal(rows.map(r => r.path), [...selection.keys()].sort(), 'complete sorted selection');
const classes = {};
for (const [i, r] of rows.entries()) {
  equal(r.role, 'dep_' + String(i + 1).padStart(4, '0'), 'sequential role:' + r.path);
  equal(r.path, r.identity.path, 'row identity path:' + r.path); pin(r.identity);
  classes[r.classification] = (classes[r.classification] || 0) + 1;
}
equal(rows.reduce((n, r) => n + r.identity.bytes, 0), 23201553, 'complete selected byte total');
equal(classes, {'analytic-source-text-or-review':142, 'opaque-historical-acceptance-or-source-support':101,
  'opaque-scientific-historical-premise':2, 'selected-administrative-proof-provenance':143,
  'selected-administrative-governance-boundary':1}, 'complete five-class map');
equal(selection.get(admission.identity.path).classification, 'opaque-scientific-historical-premise', 'certificate never decoded');
const oldD = admin(P + '/SOURCE_DEPENDENCIES.json'), oldI = admin(P + '/SOURCE_IDENTITIES.json');
const withoutRole = r => Object.fromEntries(Object.entries(r).filter(([k]) => k !== 'role'));
equal(oldD.protected_files.length, 374, '374 inherited paths');
for (const r of oldD.protected_files) equal(withoutRole(r), withoutRole(selection.get(r.path)), 'entire inherited row:' + r.path);
const boundaries = Object.keys(oldD).filter(k => !['schema', 'status', 'protected_files', 'scope'].includes(k));
equal(boundaries.length, 11, 'eleven inherited boundary objects');
for (const k of boundaries) equal(D[k], oldD[k], 'unchanged boundary:' + k);
const inherited = Object.keys(I).filter(k => Object.hasOwn(oldI, k) && ![
  'schema', 'status', 'assignment', 'governance', 'dependency_manifest', 'scope'].includes(k));
equal(inherited.length, 28, '28 inherited premise objects');
for (const k of inherited) equal(I[k], oldI[k], 'unchanged premise:' + k);
equal(I.governance.inherited_analytic_and_operational_governance, oldI.governance, 'whole inherited governance');
const oldH = admin(P + '/HANDOFF.json');
equal(fs.readdirSync(P).sort(), oldH.namespace.slice().sort(), 'predecessor exact namespace');
equal(oldH.namespace.length, 8, 'predecessor eight files'); oldH.payloads.forEach(pin);
const roles = ['certificate','original_source','original_manuscript','prefix_completion','component_routing','coupled_contrast','accepted_predecessor','accepted_manual_review','assignment'];
equal(Object.keys(I.verifier_input_bindings), roles, 'nine ordered roles');
const source = read(S + '/pair_witness.py').body.toString('utf8');
const begin = source.indexOf('FIXED_INPUTS = {'), end = source.indexOf('\n\n\nclass Refused', begin);
demand(begin >= 0 && end > begin, 'fixed dictionary literal text span');
const literal = source.slice(begin, end);
const matches = [...literal.matchAll(/    "([a-z_]+)": \{\n        "path": "([^"\n]+)",\n        "bytes": ([0-9]+),\n        "sha256": "([a-f0-9]{64})",\n    \},/g)];
equal(matches.map(m => m[1]), roles, 'all literal role blocks recognized as text, no AST');
for (const m of matches) {
  const i = {path:m[2], bytes:Number(m[3]), sha256:m[4]};
  equal(i, I.verifier_input_bindings[m[1]], 'literal binding equals manifest:' + m[1]); pin(i);
}
const referenceCounts = {historical:0, current:0, historical_extended:0, historical_state:0};
function scan(value, current = false) {
  if (!value || typeof value !== 'object') return;
  if (!Array.isArray(value) && typeof value.path === 'string' && Number.isSafeInteger(value.bytes) && typeof value.sha256 === 'string') {
    demand(selection.has(value.path) || (current && value.path === S + '/SOURCE_DEPENDENCIES.json'), 'reference within selected closure:' + value.path);
    pin(value); referenceCounts[current ? 'current' : 'historical']++;
    if (!current && Object.hasOwn(value, 'symlink_chain')) referenceCounts.historical_extended++;
    if (!current && Object.hasOwn(value, 'state')) referenceCounts.historical_state++;
  }
  Object.values(value).forEach(v => scan(v, current));
}
for (const r of rows) if (r.classification === 'selected-administrative-proof-provenance') scan(admin(r.path));
scan(I, true);
equal(referenceCounts, {historical:6893, current:222, historical_extended:18, historical_state:18}, 'all typed reference counts');
let pairs = 0;
for (const [key, identity] of Object.entries(I.source_text_counterparts.published)) {
  demand(read(identity.path).body.equals(read(I.premise_texts[key].path).body), 'complete separate byte-equal pair:' + key); pairs++;
}
equal(pairs, 4, 'four text pairs');
const negatives = read(S + '/NEGATIVE_CASES.md').body.toString('utf8');
equal([...negatives.split('## 4.')[0].matchAll(/^\| (A\d\d) \|/gm)].map(m => m[1]), Array.from({length:28}, (_,i) => 'A' + String(i+1).padStart(2,'0')), 'A01-A28 exact original table');
equal([...negatives.matchAll(/^\| (P\d\d) \|/gm)].map(m => m[1]), Array.from({length:12}, (_,i) => 'P' + String(i+1).padStart(2,'0')), 'P01-P12 exact original table');
equal(JSON.parse(author.administrative_preseal.terminal.output), author.administrative_preseal.parsed_result, 'saved preseal raw/parsed identity');
equal(author.administrative_preseal.parsed_result.stage, 'preseal7', 'old preseal stage retained');
equal(author.administrative_preseal.parsed_result.final_fresh_identity_rechecks, 396, 'old396 retained');
const replay = JSON.parse(fs.readFileSync(OUT + '/AUTHOR_REPLAY_RESULT.json'));
equal(replay.stage, 'final9', 'own replay final9');
for (const [key, expected] of Object.entries({dependencies:389, selected_bytes:23201553, inherited:374,
  historical_typed_references:6893, current_typed_references:222, current_namespace:9, final_fresh_identity_rechecks:398}))
  equal(replay[key], expected, 'replayed author count:' + key);
equal(author.administrative_preseal.script, fs.readFileSync(OUT + '/AUTHOR_ADMIN_LITERAL.js','utf8'), 'entire read script retained');
equal(author.administrative_preseal.script.replace("stage=process.argv[1]||'preseal7'", "stage=process.argv[2]||'preseal7'"), fs.readFileSync(OUT + '/AUTHOR_ADMIN_REPLAY.js','utf8'), 'only file-CLI argument adaptation');
const closureBefore = [...observed.values()].map(simple);
observed.clear(); closureBefore.forEach(pin);
equal(fs.readdirSync(S).sort(), H.namespace.slice().sort(), 'final source namespace');
equal(fs.readdirSync(P).sort(), oldH.namespace.slice().sort(), 'final predecessor namespace');
const result = {schema:'ri195-independent-administrative-review-v1', status:'PASS_SOURCE_PROVENANCE_ONLY',
  subject:simple(read(S+'/HANDOFF.json')), assignment:simple(read(A)),
  selected_dependencies:389, selected_bytes:23201553, inherited_rows:374, boundaries:11, inherited_premises:28,
  classifications:classes, reference_counts:referenceCounts, nine_literal_source_bindings:I.verifier_input_bindings,
  prospective_cases:{arguments:28,fixed_io:12,executed:0}, separately_equal_text_pairs:pairs,
  whole_identity_closure:closureBefore, fresh_identity_rechecks:closureBefore.length,
  historical_state_not_compared_to_current:true, author_preseal_retained:author.administrative_preseal.parsed_result,
  own_author_replay:replay, predicate_count:facts.length,
  no_scientific_decode_or_target_execution:true, no_mathematical_formula_evaluated:true};
fs.writeFileSync(OUT+'/INDEPENDENT_ADMIN_CHECK.json',JSON.stringify(result,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({status:result.status,selected_dependencies:389,selected_bytes:23201553,
  fresh_identity_rechecks:closureBefore.length,predicates:facts.length,reference_counts:referenceCounts}));
