from pathlib import Path
import hashlib, json, os, stat

Q = Path('/Volumes/AI_DATA/development/det-review-evidence/ri233-native-same-root-contrast-sa2lhrgp')
R = Path(__file__).resolve().parent
EXPECTED = {
 'AUTHOR_VERIFICATION.json': (39812, '829c58f7fc8781290d4f86a6818a0c8bca9e8b631c2c9714335035fd0f5430e5'),
 'HANDOFF.json': (18397, 'bcd0a7c893b4e1ebec2f79ac9c92047a88972de0e6800a2a299176c1ef8a7cf6'),
 'HANDOFF.md': (2099, '4a8ab82be95fdb00f0e450f9168a04da468b4b48a7d29de598f020d54a5ec115'),
 'OFFSET_ELIMINATION.md': (8137, 'cfd7c78c78fd39f9abef2873cae50fd8b903251da52ef3d1eafd99dca95b8efc'),
 'ROOT_TRANSPORT.md': (14353, '587b4033d350c6022b5a5ffcd990e2d1a8f5a073f02249d1c18e5bab75812440'),
 'SOURCE_REFERENCES.json': (67263, '836331259f615b9003f4d56d5d6eb34de5deb4037b2d155473ff1ea13b4d6a01'),
}
checks = 0
observed = {}
bodies = {}
def need(test, label):
 global checks
 checks += 1
 if not test:
  raise RuntimeError(label)
def stamp(s):
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read_pin(i):
 p = Path(i['path'])
 need(p.is_absolute() and str(p) == i['path'], 'absolute canonical path')
 need(p.name != 'CERTIFICATE.json', 'no scientific certificate body')
 need(not any(t.startswith('ri234-') for t in p.parts), 'no active measurement reservation')
 for parent in [p, *p.parents]:
  need(not parent.is_symlink(), 'no symlink component')
 a = p.stat()
 need(stat.S_ISREG(a.st_mode) and a.st_size <= 67108864, 'bounded regular')
 with p.open('rb') as f:
  need(stamp(os.fstat(f.fileno())) == stamp(a), 'fd before')
  b = f.read(a.st_size + 1)
  need(stamp(os.fstat(f.fileno())) == stamp(a), 'fd after')
 need(stamp(p.stat()) == stamp(a), 'path after')
 current = {'path':str(p), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest(), 'state':stamp(a)}
 need((current['bytes'],current['sha256']) == (i['bytes'],i['sha256']), 'expected identity')
 if str(p) in observed:
  need(current == observed[str(p)], 'stable whole state')
 observed[str(p)] = current
 bodies[str(p)] = b
 return b
for n, (size, digest) in EXPECTED.items():
 read_pin({'path':str(Q/n),'bytes':size,'sha256':digest})
need(sorted(x.name for x in Q.iterdir()) == sorted(EXPECTED), 'current exact namespace')
H = json.loads(bodies[str(Q/'HANDOFF.json')])
S = json.loads(bodies[str(Q/'SOURCE_REFERENCES.json')])
A = json.loads(bodies[str(Q/'AUTHOR_VERIFICATION.json')])
need(sorted(H['namespace']) == sorted(EXPECTED), 'declared namespace')
need(len(H['payloads']) == 5, 'five sealed payloads')
for i in H['payloads']:
 need(Path(i['path']).parent == Q, 'sealed local path')
 need((i['bytes'],i['sha256']) == EXPECTED[Path(i['path']).name], 'seal pin')
rows = S['direct_sources']
need(len(rows) == len({x['identity']['path'] for x in rows}) == 33, 'direct unique closure')
need([x['identity']['path'] for x in rows] == sorted(x['identity']['path'] for x in rows), 'ordered closure')
need(sum(x['identity']['bytes'] for x in rows) == S['direct_scope']['bytes'] == 846757, 'metadata byte count')
for x in rows:
 need(x['access'] in ('administrative-reference','accepted-analytic-text','opaque-historical-support'), 'access classification')
 read_pin(x['identity'])
by_path = {x['identity']['path']:x for x in rows}
def admin(i):
 need(i['path'] in by_path and by_path[i['path']]['access'] == 'administrative-reference', 'administrative decode only')
 need((i['bytes'],i['sha256']) == (observed[i['path']]['bytes'],observed[i['path']]['sha256']), 'administrative binding')
 return json.loads(bodies[i['path']])
P = admin(S['predecessor_references'])
PH = admin(S['predecessor_handoff'])
IN = admin(S['inherited_manifest_by_reference']['identity'])
ASSIGN = admin(S['assignment'])
DEC = admin(S['accepted_predecessor'])
need(ASSIGN['reservation'] == str(Q) and ASSIGN['status'] == 'ASSIGNED_AFTER_RI231_ADJUDICATION', 'assignment')
need(ASSIGN['predecessor'] == S['accepted_predecessor'] and ASSIGN['predecessor_packet'] == S['predecessor_handoff'], 'assignment predecessor')
need(DEC['status'] == 'ACCEPT_CONDITIONAL_SIX_ROOT_SUBSTITUTION_AND_COMPLETE_CANONICAL_CAPACITY', 'accepted predecessor')
need(S['inherited_manifest_by_reference'] == P['inherited_manifest_by_reference'], 'unchanged inherited manifest boundary')
blocks = {k:v for k,v in IN.items() if k not in ('schema','status','protected_files','scope')}
need(len(IN['protected_files']) == 423 and len(blocks) == 15, 'inherited boundary counts only')
need(blocks == S['inherited_manifest_by_reference']['boundary_objects'], 'whole inherited boundary objects')
for k in ('inherited_original_six_admissions','inherited_additional_admissions','inherited_RI189_analytic_admission','inherited_shared_affine_admission','inherited_RI223_literal_admissions','inherited_RI225_disconnected_admission','inherited_RI228_construction_admissions','predecessor_literal_exception_boundary','inherited_RI216_native_premises_by_reference','predecessor_lower_law_metadata_boundary'):
 need(S[k] == P[k], 'unchanged admission '+k)
need(S['historical_RI231_literal_exception'] == P['separate_current_literal_exception'], 'old exception is preserved historical metadata')
old = S['historical_RI231_literal_exception']
need(old['body']['path'] not in by_path and old['authority']['path'] not in by_path, 'old body and authority outside fresh closure')
need(not S['current_no_body_boundary']['new_body_or_coordinate_authority'] and not S['current_no_body_boundary']['new_original_body_read'] and S['current_no_body_boundary']['historical_exception_does_not_renew'], 'no new body admission')
need(S['scope'] == H['scope'] == A['scope'], 'scope consistency')
for k in ('canonical_kappa_or_competing_values_determined','actual_rank_or_feasibility_decided','native_lifting_direction_found','native_inconsistency_identity_found','scientific_body_vector_or_new_coordinate_inspected','automatic_scientific_JSON_parsing_or_proof_arithmetic','graph_LP_subject_runtime_fixture_card_execution','repository_Git_index_or_measurement_written','successor_designed_or_started'):
 need(S['scope'][k] is False, 'bounded claim '+k)
need(S['executable_obligations'] == P['executable_obligations'] == H['executable_obligations'] == A['executable_obligations'] and S['scope']['qualification_credit'] == 0, 'uncredited executable routes')
predecessor = Path(S['predecessor_handoff']['path']).parent
need(sorted(x.name for x in predecessor.iterdir()) == S['predecessor_namespace'] == PH['namespace'] and len(PH['namespace']) == 6, 'predecessor namespace')
need(A['current_diagnostics']['failed_orchestration_attempts'] == 1 and H['actual_author_checks']['diagnostics'] == A['current_diagnostics'], 'retained author diagnostic')
replay_bytes = (R/'AUTHOR_REPLAY.json').read_bytes()
REPLAY = json.loads(replay_bytes)
need(REPLAY['stage'] == 'final6' and REPLAY['whole_identity_fresh_rechecks'] == 39 and REPLAY['explicit_selected_reference_checks'] == 46, 'actual retained replay counts')
need(REPLAY['direct_sources'] == 33 and REPLAY['direct_bytes'] == 846757 and REPLAY['inherited_boundary_objects_preserved'] == 15, 'actual retained replay scope')
for i in REPLAY['current_payloads']:
 need((i['bytes'],i['sha256']) == EXPECTED[Path(i['path']).name], 'actual replay current pins')
need((R/'author_metadata_checker.js').read_bytes() == A['administrative_checker']['retained_source'].encode(), 'retained checker exact')
need(len(observed) == 39, 'actual distinct identity count')
for i in list(observed.values()):
 read_pin(i)
need(sorted(x.name for x in Q.iterdir()) == sorted(EXPECTED), 'final namespace')
result = {'schema':'ri233-independent-administrative-check-v1','status':'PASS_METADATA_NOT_MATHEMATICAL_ACCEPTANCE','predicates':checks,'whole_file_identities':len(observed),'direct_sources':33,'direct_bytes':846757,'inherited_boundaries':15,'inherited423_collection_replayed':False,'subject_namespace':6,'predecessor_namespace':6,'original_scientific_body_read':False,'scientific_body_decoded':False,'automatic_mathematical_arithmetic':False,'subject_execution':False,'Git_operations':False,'identities':list(observed.values())}
print(json.dumps(result,indent=2))
