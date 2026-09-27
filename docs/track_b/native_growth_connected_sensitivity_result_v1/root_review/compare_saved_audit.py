"""Compare complete actual saved objects without importing either native target."""
from metadata import *
N=B/'ri122-native-caller-source-jgehvvxx'
def exact(a,b):
    assert type(a) is type(b)
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a: exact(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):exact(x,y)
    else:assert a==b
def scientific(v):
    return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
c=load(N/'CERTIFICATE.json');a=load(N/'audit-01/REPORT.json');desc=load(N/'AUDIT_INPUT.json')
assert a['schema']=='ri120-independent-complete-connected-sensitivity-audit-v1'
assert a['status']=='all_saved_fields_independently_match'
assert len(c)==19
exact(c,a['reconstructed_certificate'])
assert scientific(c)==(N/'CERTIFICATE.json').read_bytes()==(N/'witness-01/stdout.log').read_bytes()
assert (N/'audit-01/stdout.log').read_bytes()==scientific(a)==(N/'audit-01/REPORT.json').read_bytes()
assert a['reconstructed_certificate_identity']==pin(scientific(c))
assert a['complete_top_level_sections']=={k:pin(scientific(v))for k,v in c.items()}
assert a['descriptor_identity']==pure(ref(N/'AUDIT_INPUT.json'))
bindings=[]
for section in ('files','accepted_sources'):
    for role,row in desc[section].items():bindings.append(dict(role=section+'.'+role,**row))
bindings.append(dict(role='audit_source',**desc['audit_source']))
for row in desc['custody_dependencies']:bindings.append(dict(role='custody.'+row['role'],**{k:row[k]for k in ('path','bytes','sha256')}))
assert len(bindings)==18 and len({r['path']for r in bindings})==18
assert {r['role']:r for r in bindings}=={r['role']:r for r in a['payload_role_bindings']}
for r in bindings:verify(r['path'],r)
post={r['path']:r for r in a['postchecks']}
assert len(a['postchecks'])==len(post)==19
for row in bindings+[ref(N/'AUDIT_INPUT.json')]:
    assert post[row['path']]==dict(path=row['path'],unchanged=True,identity=pure(row))
assert a['unique_payload_paths']==a['payload_role_count']==18
assert a['audit_source_identity']==pure(desc['audit_source'])
assert a['accepted_source_identities']=={role:pure(row)for role,row in desc['accepted_sources'].items()}
assert a['independently_rebuilt_fixture_count']==len(c['root_fixtures'])==16
assert a['independently_rebuilt_family_fixture_count']==len(c['family_fixtures'])==10
assert a['independently_rebuilt_decision_fixture_count']==len(c['decision_fixtures'])==6
assert a['declared_producer_controls']==dict(count=166,ordered_pairs=c['refusal_controls'],producer_controls_executed_by_consumer=False)
assert a['custody_semantics_self_adjudicated'] is False
assert type(a['independent_counted_operations'])is int and 0<a['independent_counted_operations']<=200000
normal=load(N/'normal-01/stdout.log');optimized=load(N/'optimized-01/stdout.log')
exact(normal,optimized)
assert (N/'normal-01/stdout.log').read_bytes()==(N/'optimized-01/stdout.log').read_bytes()
assert normal['status']=='PASS' and normal['refusal_count']==166
assert normal['root_fixture_count']==16 and normal['family_fixture_count']==10 and normal['decision_fixture_count']==6
assert normal['decision']==c['decision']
runtime=[]
for mode in ('witness','normal','optimized','audit'):
    p=D/(mode+'-pre-runtime/RUNTIME_METADATA_RESULT.json');q=D/(mode+'-post-runtime/RUNTIME_METADATA_RESULT.json')
    before,after=load(p),load(q)
    assert before['status']==after['status']=='PASS_CURRENT_METADATA_ONLY'
    assert before['errors']==after['errors']==[]
    for k in ('runtime_files','namespace_before','namespace_after','host_before','host_after','manifest_before','manifest_after'):
        exact(before[k],after[k])
    runtime.append(dict(mode=mode,pre=ref(p),post=ref(q),summary=before['summary'],complete_observed_fields_equal=True))
print(save('ROOT_COMPLETE_SAVED_AUDIT_COMPARISON.json',dict(schema='ri122-root-full-saved-audit-comparison-v1',status='COMPLETE_CERTIFICATE_AND_ALL_AUDIT_BINDINGS_MATCH',certificate=ref(N/'CERTIFICATE.json'),audit=ref(N/'audit-01/REPORT.json'),descriptor=ref(N/'AUDIT_INPUT.json'),sections=a['complete_top_level_sections'],independently_rebuilt_root_fixtures=16,independently_rebuilt_family_fixtures=10,independently_rebuilt_decision_fixtures=6,producer_controls_actually_traversed_per_successful_mode=166,consumer_executes_producer_mutations=False,counted_auditor_operations=a['independent_counted_operations'],payloads=18,postchecks=19,actual_normal_optimized_whole_bytes_equal=True,external_runtime_observations=runtime,decision=c['decision'],scope='Full strict saved-data/type/canonical-byte/provenance/postcheck comparison. Actual independent arithmetic is the separately authored auditor execution, not this comparison.',programme_complete=False)))
