"""Root administrative equality/custody adjudication; no subject execution."""
import hashlib, importlib.util
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=Path(__file__).parent
helper=B/'ri122-root-execution-review-6whn_vky/metadata.py'
raw=helper.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',helper);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=D
R=B/'ri159-independent-grid-review-p1uvnluc';Q=B/'ri159-final-witness-grid-source-47ofu03n'
a=m.load(D/'METADATA_CHECK.json');b=m.load(R/'METADATA_CHECK.json')
assert {k:v for k,v in a.items() if k!='schema'}=={k:v for k,v in b.items() if k!='schema'}
for row in a['observed_identities']:assert m.identity(row['path'])==row
h=m.load(R/'HANDOFF.json');assert sorted(x.name for x in R.iterdir())==sorted(h['namespace'])
for row in h['payloads']:m.verify(row['path'],row)
final=m.load(R/'FINAL_PIN_CHECK.json')
for row in final['own_review_preseal_files']:m.verify(row['path'],row)
v=m.load(R/'VERDICT.json');assert not v['blocking_source_findings'] and v['cases_executed']==0
print(m.save('ROOT_METADATA_REPLAY.json',dict(schema='ri159-root-exact-metadata-replay-v1',status='PASS_ADMINISTRATIVE_ONLY',subject=m.ref(Q/'HANDOFF.json'),review=m.ref(R/'HANDOFF.json'),independent_full_report=m.ref(R/'METADATA_CHECK.json'),root_full_report=m.ref(D/'METADATA_CHECK.json'),replay_command_chunk='24a7d6',replay_exit_code=0,all_report_fields_equal_except_schema=True,predicates=a['predicates'],dependencies=a['dependencies'],selected_bytes=a['selected_bytes'],fresh_full_identities_rechecked=len(a['observed_identities']),review_payloads_rechecked=len(h['payloads']),review_preseal_pins_rechecked=len(final['own_review_preseal_files']),historical_states_compared_to_current=False,source_control_execution=False,scientific_body_decode=False)))
