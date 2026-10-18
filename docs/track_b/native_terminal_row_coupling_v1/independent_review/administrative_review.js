"use strict";
// Independent administrative byte/reference audit only. No subject source execution.
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const own = "/Volumes/AI_DATA/development/det-review-evidence/ri168-independent-proof-review-ioq3jbwc";
const subject = "/Volumes/AI_DATA/development/det-review-evidence/ri168-terminal-row-coupling-f50p8xyj";
const prior = "/Volumes/AI_DATA/development/det-review-evidence/ri166-native-contrast-gap-2j9ykuoq";
const assignment = "/Volumes/AI_DATA/development/det-review-evidence/ri168-root-coupling-review-jihb5l4y/INDEPENDENT_REVIEW_ASSIGNMENT.json";
const observations = new Map();
const fields = ["dev", "ino", "mode", "size", "mtimeNs", "ctimeNs", "nlink"];
const requireThat = (yes, why) => { if (!yes) throw new Error(why); };
const sha = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const equal = (a, b) => JSON.stringify(canonical(a)) === JSON.stringify(canonical(b));
function read(name, fresh = false) {
  if (!fresh && observations.has(name)) return observations.get(name);
  requireThat(path.isAbsolute(name) && path.normalize(name) === name, "noncanonical path " + name);
  let prefix = "/";
  for (const part of name.split("/").filter(Boolean)) {
    prefix = path.join(prefix, part);
    requireThat(!fs.lstatSync(prefix).isSymbolicLink(), "symlink " + prefix);
  }
  const before = fs.lstatSync(name, {bigint: true});
  requireThat(before.isFile() && before.size <= 67108864n, "file/cap " + name);
  const same = s => fields.every(k => s[k] === before[k]);
  const descriptor = fs.openSync(name, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  let bytes;
  try {
    requireThat(same(fs.fstatSync(descriptor, {bigint: true})), "before-open drift " + name);
    const chunks = [];
    let n = 0;
    while (n <= Number(before.size)) {
      const b = Buffer.alloc(Math.min(65536, Number(before.size) + 1 - n));
      const got = fs.readSync(descriptor, b, 0, b.length, null);
      if (!got) break;
      chunks.push(b.subarray(0, got));
      n += got;
    }
    bytes = Buffer.concat(chunks);
    requireThat(bytes.length === Number(before.size) && same(fs.fstatSync(descriptor, {bigint: true})), "descriptor drift " + name);
  } finally { fs.closeSync(descriptor); }
  requireThat(same(fs.lstatSync(name, {bigint: true})) && fs.realpathSync(name) === name, "path drift " + name);
  const observation = {path: name, bytes: bytes.length, sha256: sha(bytes), fresh_state: Object.fromEntries(fields.map(k => [k, before[k].toString()])), body: bytes};
  observations.set(name, observation);
  return observation;
}
function pin(identity) {
  const got = read(identity.path);
  requireThat(Number.isSafeInteger(identity.bytes) && identity.bytes >= 0 && /^[a-f0-9]{64}$/.test(identity.sha256), "malformed identity");
  requireThat(got.bytes === identity.bytes && got.sha256 === identity.sha256, "pin mismatch " + identity.path);
  if (identity.resolved_path !== undefined) requireThat(identity.resolved_path === identity.path, "resolved path mismatch");
  for (const k of ["symlinks", "symlink_chain"]) if (identity[k] !== undefined) requireThat(equal(identity[k], []), "declared symlink chain");
  return got;
}
// Only explicitly administrative JSON bodies are decoded below.
const admin = name => JSON.parse(read(name).body.toString("utf8"));
pin({path: assignment, bytes: 1743, sha256: "3e75b93c919252a28bbc2ca2f59a1adba66d67446da8a67e349c809c8e2cf8d3"});
const authority = admin(assignment);
requireThat(authority.reservation === own, "write reservation");
pin(authority.subject);
const handoff = admin(authority.subject.path);
requireThat(handoff.reservation === subject, "subject reservation");
const names = fs.readdirSync(subject).sort();
requireThat(equal(names, handoff.namespace) && names.length === 8, "subject namespace");
requireThat(equal(handoff.payloads.map(i => path.basename(i.path)).sort(), names.filter(n => n !== "HANDOFF.json")), "subject payload coverage");
handoff.payloads.forEach(pin);
pin(handoff.assignment); pin(handoff.accepted_analytic_predecessor); pin(handoff.operational_governance_predecessor);
const dependencies = admin(subject + "/SOURCE_DEPENDENCIES.json");
const identities = admin(subject + "/SOURCE_IDENTITIES.json");
const selected = new Map();
const classification = {};
let selectedBytes = 0;
for (const [index, row] of dependencies.protected_files.entries()) {
  requireThat(row.path === row.identity.path && row.role === "dep_" + String(index + 1).padStart(4, "0"), "row identity/role");
  requireThat(!selected.has(row.path), "duplicate dependency");
  selected.set(row.path, row);
  pin(row.identity);
  selectedBytes += row.identity.bytes;
  classification[row.classification] = (classification[row.classification] || 0) + 1;
}
requireThat(selected.size === 264 && equal([...selected.keys()], [...selected.keys()].sort()), "selection count/order");
requireThat(selectedBytes === 16875258, "selected bytes");
const predecessorDependencies = admin(prior + "/SOURCE_DEPENDENCIES.json");
const predecessorIdentities = admin(prior + "/SOURCE_IDENTITIES.json");
const omitRole = r => Object.fromEntries(Object.entries(r).filter(([k]) => k !== "role"));
requireThat(predecessorDependencies.protected_files.length === 252, "inherited count");
for (const row of predecessorDependencies.protected_files) requireThat(equal(omitRole(row), omitRole(selected.get(row.path))), "changed inherited row " + row.path);
requireThat(equal(dependencies.governance_stopping_boundary, predecessorDependencies.governance_stopping_boundary), "inherited governance boundary");
for (const k of ["premise_texts", "actual_source_text_reads", "source_text_counterparts", "immutable_numerical_certificate", "unchanged_obligations"]) requireThat(equal(identities[k], predecessorIdentities[k]), "changed inherited source field " + k);
const predecessorHandoff = admin(prior + "/HANDOFF.json");
const predecessorNames = fs.readdirSync(prior).sort();
requireThat(predecessorNames.length === 8 && equal(predecessorNames, [...predecessorHandoff.namespace].sort()), "predecessor namespace");
requireThat(equal(predecessorNames, [...predecessorHandoff.payloads.map(i => path.basename(i.path)), "HANDOFF.json"].sort()), "predecessor seal coverage");
predecessorHandoff.payloads.forEach(pin);
const phase = dependencies.historical_phase_record_boundary;
requireThat(phase.path === prior + "/AUTHOR_CHECKS.json" && phase.typed_reference_expansion === false, "historical phase stop");
requireThat(selected.get(phase.path).classification === "opaque-historical-acceptance-or-source-support", "phase classification");
requireThat(equal(phase, identities.governance.predecessor_phase_record_boundary), "phase disclosure consistency");
const governance = dependencies.governance_stopping_boundary;
requireThat(governance.typed_reference_expansion === false && equal(governance, identities.governance.operational_stopping_boundary), "governance consistency");
let historicalRefs = 0, currentRefs = 0, oldStates = 0, extended = 0;
function scan(node, current = false) {
  if (node === null || typeof node !== "object") return;
  if (!Array.isArray(node) && typeof node.path === "string" && Number.isSafeInteger(node.bytes) && typeof node.sha256 === "string") {
    requireThat(selected.has(node.path) || node.path === subject + "/SOURCE_DEPENDENCIES.json", "unclosed typed reference " + node.path);
    pin(node);
    if (current) currentRefs++; else {
      historicalRefs++;
      if (node.state !== undefined) oldStates++;
      if (node.symlink_chain !== undefined) extended++;
    }
    // Historical state arrays are not compared to any fresh filesystem stat.
  }
  for (const value of Object.values(node)) scan(value, current);
}
const expanded = [], opaque = [];
for (const row of selected.values()) {
  if (row.classification === "selected-administrative-proof-provenance") {
    expanded.push(row.path); scan(admin(row.path));
  } else opaque.push({path: row.path, classification: row.classification, action: "whole-byte identity only; no recursive JSON decoding"});
}
scan(identities, true);
requireThat(expanded.length === 93 && historicalRefs === 2348 && currentRefs === 114, "reference totals");
requireThat(oldStates === 17 && extended === 17, "historical state accounting");
let equalPairs = 0;
for (const [key, identity] of Object.entries(identities.source_text_counterparts.published)) {
  requireThat(read(identity.path).body.equals(read(identities.premise_texts[key].path).body), "counterpart inequality " + key); equalPairs++;
}
requireThat(equalPairs === 4, "counterpart count");
const beforeRecheck = [...observations.values()].map(({body, ...r}) => r);
for (const old of beforeRecheck) {
  const now = read(old.path, true);
  requireThat(now.bytes === old.bytes && now.sha256 === old.sha256, "final byte drift " + old.path);
}
requireThat(equal(fs.readdirSync(subject).sort(), names) && equal(fs.readdirSync(prior).sort(), predecessorNames), "namespace drift");
const report = {
  schema: "ri168-independent-administrative-review-v1",
  status: "MATCH_WITH_EXPLICIT_HISTORICAL_OPAQUE_BOUNDARIES_NOT_MATHEMATICAL_ACCEPTANCE",
  assignment: {path: assignment, bytes: read(assignment).bytes, sha256: read(assignment).sha256},
  subject: authority.subject,
  checked_dependencies: selected.size, selected_bytes: selectedBytes,
  preserved_inherited_rows: predecessorDependencies.protected_files.length,
  classification_counts: classification,
  subject_namespace: names, predecessor_namespace: predecessorNames,
  full_administrative_bodies: expanded.length,
  historical_typed_reference_occurrences: historicalRefs, current_typed_reference_occurrences: currentRefs,
  historical_state_arrays_explicitly_not_compared_to_fresh_stat: oldStates,
  extended_reference_occurrences: extended, distinct_path_equal_byte_pairs: equalPairs,
  uncached_final_byte_rechecks: beforeRecheck.length,
  phase_boundary: phase, governance_boundary: governance,
  administrative_expansion_paths: expanded,
  nonexpanded_dependencies: opaque,
  observations: beforeRecheck,
  author_checker_source_was_read_not_executed: true,
  mathematical_arithmetic_or_graph_executed: false,
  scientific_json_or_vector_decoded: false,
  subject_vendor_or_helper_import_compile_ast_execution: false,
  historical_phase_pins_recertified_as_current: false,
  continuous_custody_or_operational_admission_claim: false,
  writes: [own + "/ADMINISTRATIVE_REVIEW.json"],
  note: "Read-window checks use fresh stat observations; old state arrays remain historical. Literal proof reading is recorded separately. No command-history receipt is authenticated as an executed event merely by hashing its containing record."
};
fs.writeFileSync(own + "/ADMINISTRATIVE_REVIEW.json", JSON.stringify(report, null, 2) + "\n", {flag: "wx"});
console.log(JSON.stringify({status: report.status, dependencies: selected.size, selected_bytes: selectedBytes, inherited_rows: 252, administrative_bodies: expanded.length, historical_refs: historicalRefs, current_refs: currentRefs, state_noncomparisons: oldStates, final_rechecks: beforeRecheck.length, report: own + "/ADMINISTRATIVE_REVIEW.json"}, null, 2));
