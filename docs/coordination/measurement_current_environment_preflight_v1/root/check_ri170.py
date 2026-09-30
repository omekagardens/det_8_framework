"""Independent finite metadata review and source identities only."""
from pathlib import Path
import hashlib, importlib.util, json
hp=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');b=hp.read_bytes()
assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
H=m.B/'ri170-measurement-current-e-preflight-gikj2giy';identities={};observations=0

def verify(r):
 global observations
 got=m.verify(r['path'],r);observations+=1
 if r['path'] in identities:assert identities[r['path']]==got
 identities[r['path']]=got
 return got

def walk(v):
 if isinstance(v,dict):
  if {'path','bytes','sha256'}<=set(v):verify(v)
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)

verify(dict(path=str(H/'SOURCE_ONLY_HANDOFF.json'),bytes=8755,sha256='8d3cfce3b18ac346a0dab3449de3eee686c5965957e4188933604dd392d66fce'))
h=m.load(H/'SOURCE_ONLY_HANDOFF.json');walk(h['files'])
assert sorted(p.name for p in H.iterdir())==sorted(['SOURCE_ONLY_HANDOFF.json']+[Path(r['path']).name for r in h['files']])
refs=m.load(H/'REFERENCE_BINDINGS.json');R=refs['references'];walk(R)
source=m.load(R['source_manifest']['path']);walk(source['dependencies']);walk(source['modules']);verify(source['adapter'])
deps=m.load(R['ri141_dependencies']['path']);walk(deps['opaque_files'])
graph=m.load(R['binding_graph']['path']);walk(graph['copied_files']);walk(graph['history_originals']);walk(graph['evidence'])
for r in graph['sources']:verify(dict(path=r['original'],**r['pin']))
for name,pin in refs['ri141_exact_source_map'].items():verify(dict(path=str(Path(R['ri141_prepare']['path']).parent/name),**pin))
# The old outcome is authoritative; this review reconciles its consumer fields, not a rerun.
decision=m.load(R['actual_inert106_root_decision']['path'])
for k in ('actual_summary','genuine_initial','genuine_terminal','independent_review'):verify(decision[k])
summary=m.load(decision['actual_summary']['path']);walk(summary)
initial=m.load(decision['genuine_initial']['path']);terminal=m.load(decision['genuine_terminal']['path'])
assert initial['actual']['chunk_id']=='f3f711' and initial['actual']['session_id']==66856
assert terminal['initial']==initial['actual'] and terminal['poll_arguments']['session_id']==66856
assert terminal['actual']['chunk_id']=='9921e9' and terminal['actual']['exit_code']==0
result=m.load(summary['result']['path']);inventory=m.load(R['inert_inventory']['path'])
assert result['status']=='ALL_DECLARED_PASSED' and result['counts']=={'failed':0,'passed':106,'total':106}
assert result['order']==inventory['combined_order'] and len(set(result['order']))==106
assert result['scientific_execution'] is False and result['runtime_or_tool_evidence_genuine'] is False
assert result['actual_admission_coverage'] is False and result['arithmetic_or_15_case_credit'] is False
assert result['full32_credit'] is False and result['ri131_credit'] is False
assert decision['status']=='ACCEPT_ONE_GENUINE_INERT_METADATA_QUALIFICATION' and decision['accepted_controls']==106 and decision['source_manifest']==R['source_manifest']
assert summary['genuine_initial']==decision['genuine_initial'] and summary['genuine_terminal']==decision['genuine_terminal']
proposal=m.load(H/'PREFLIGHT_PROPOSAL.json');assert all(not Path(p).exists() for p in proposal['paths_proposed_not_created'].values())
# No AST/import: independently match the consumer's literal closed field set.
fields=['schema','status','action','source_manifest','source_review','qualification','request','output','environment','bootstrap_preflight','bounds','genuine_outer_required']
needle="set(a)=={"+','.join(repr(x) for x in fields)+"}"
assert needle in Path(R['adapter']['path']).read_text() and len(fields)==12
assert 'closed13 fields' in (H/'FIELD_CONTRACT.md').read_text()
for r in list(identities.values()):assert m.verify(r['path'],r)==r
print(m.save('RI170_ROOT_METADATA_CHECK.json',dict(schema='ri170-root-independent-metadata-reconciliation-v1',status='PASS_WITH_DOCUMENTATION_COUNT_CORRECTION',observations=observations,unique_paths=len(identities),identities=list(identities.values()),fresh_recheck_count=len(identities),author_replay=m.ref(m.D/'ri170-metadata-replay/METADATA_CHECK.json'),exact_packet_namespace=16,adapter_field_count=12,documentation_claim=13,field_names_correct=True,actual_106_order_and_counts_match=True,genuine_tool_chain_matches=True,historical_fixture_tool_credentials_not_genuine=True,prospective_roots_still_absent=True,subject_execution=False,current_runtime_observed=False,scientific_body_decode=False)))
