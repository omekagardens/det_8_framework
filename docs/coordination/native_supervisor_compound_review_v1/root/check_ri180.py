"""Root authentication of independently reviewed source metadata; no subject runs."""
from pathlib import Path
import hashlib
import importlib.util
D=Path(__file__).parent
hp=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
raw=hp.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('metadata',hp);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=D
R=m.B/'ri180-supervisor-independent-review-4xwmvctt'
S=m.B/'ri176-supervisor-qualification-repair-3ausb2jo'
m.verify(R/'HANDOFF.json',dict(bytes=4180,sha256='62270fcfc8fccd571d884ac13ca45ba0d2034b34e6cccb849659aee142c3a500'))
m.verify(S/'HANDOFF.json',dict(bytes=14679,sha256='572fe0bfc79489dc3b9c4a6df9bc4d7bbb0ff455de1c68eb2fbb00e6d870421e'))
seen={}
def capture(row):
    actual=m.verify(row['path'],row)
    if row['path'] in seen:assert seen[row['path']]==actual
    seen[row['path']]=actual
    return actual
for base,count in ((R,10),(S,33)):
    h=m.load(base/'HANDOFF.json')
    assert sorted(x.name for x in base.iterdir())==sorted(h['namespace'])
    assert len(h['namespace'])==count and len(h['payloads'])==count-1
    assert {Path(x['path']).name for x in h['payloads']}==set(h['namespace'])-{'HANDOFF.json'}
    capture(m.ref(base/'HANDOFF.json'))
    for row in h['payloads']:
        assert Path(row['path']).parent==base
        capture(row)
admin=m.load(R/'ADMIN_CHECK.json')
assert admin['status']=='EXACT_SOURCE_METADATA_MATCH_NOT_QUALIFICATION'
assert len(admin['checks'])==admin['check_count']==6972
assert len(admin['observed_identities'])==admin['observed_count']==98
assert admin['cases']==92 and admin['recipes']==34 and admin['mutation_families']==26
assert admin['executed_cases']==0 and admin['subject_import_compile_AST_probe'] is False
assert admin['subject_helper_vendor_executed'] is False and admin['scientific_decode'] is False
for row in admin['observed_identities']:
    actual=capture(row)
    assert all(actual[k]==v for k,v in row.items())
deps=m.load(S/'DEPENDENCY_BINDINGS.json')
assert len(deps['fresh_originals'])==64
for row in deps['fresh_originals']:capture(row)
manifest=m.load(S/'CASE_MANIFEST.json')
compound=[c for c in manifest['cases'] if c['fault'].endswith('.unregister_close')]
assert len(compound)==4 and all(c['executed'] is False for c in compound)
verdict=m.load(R/'VERDICT.json')
assert verdict['decision']=='REQUIRE_NARROW_F04_R_REPAIR_BEFORE_QUALIFICATION_ADMISSION'
commands=m.load(R/'COMMAND_OUTCOMES.json')
assert any(x['chunk_id']=='70e5da' and x['exit_code']==0 for x in commands['records'])
assert any(x['chunk_id']=='ff585f' and x['exit_code']==1 for x in commands['records'])
for row in list(seen.values()):assert m.identity(row['path'])==row
print(m.save('RI180_ROOT_AUTHENTICATION.json',dict(schema='ri180-root-authentication-v1',status='MATCHED_REVIEW_AND_SOURCE_NOT_QUALIFICATION',identities=list(seen.values()),identity_count=len(seen),subject_files=33,review_files=10,independent_reported_predicates=6972,independent_inputs_reobserved=98,external_inputs=64,compound_recipes=compound,reviewer_actual_checks=['70e5da exit0','8ad9ab exit0','4730cd exit0'],reviewer_failed_check='ff585f exit1; literal diff alignment, preserved',subject_execution=False,mathematical_execution=False,scientific_decode=False,ret_paused=True)))
