from pathlib import Path
import hashlib,importlib.util,json,os,time
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri239-root-current-e-capture-mk6vocq1';D=B/'ri236-current-e-normal-preparation-3geu_r1s';W=D/'worker_proposal'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
m.verify(W/'CAPTURE_RECIPE.json',dict(bytes=12114,sha256='3f46d182e4adedf6b6e346ebd5e5dd6eae60cf42b4e77b073a957531e4c68195'))
recipe=m.load(W/'CAPTURE_RECIPE.json');pre=m.load(R/'PRE_CUSTODY.json')
m.verify(R/'PRE_CUSTODY.json',dict(bytes=4686,sha256='5203443312f7d3cc1fef2f1504e8e239713cdfeb400961113d871b331aa9cfb4'))
assert pre['status']=='PASS_FRESH_PRE_CUSTODY'
for ref in pre['refs'].values():m.verify(ref['path'],ref)
for row in m.load(R/'PRE_ROLE_CUSTODY.json')['observed_identities']:assert m.identity(row['path'])==row
for row in m.load(R/'PRE_E.json'):
 p=Path(recipe['paths']['environment_root'])/row['relative'];st=p.lstat()
 assert [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
assert not os.path.lexists(recipe['paths']['capture_output'])
assert m.snapshot()==m.load(R/'REPO_ENTRY.json')
preflight=dict(schema='ri239-genuine-capture-preflight-v1',status='PASS_FRESH_ROOT_CAPTURE_PREFLIGHT',selected_interpreter_binding=pre['selected_interpreter_binding'],host=pre['host'],environment=pre['environment'],custody=m.ref(R/'PRE_CUSTODY.json'),genuine_host=pre['refs']['host'],supplier=pre['refs']['supplier'],frozen_tree=pre['refs']['E'],all_sources=pre['refs']['sources'],all_role_custody=pre['refs']['role_custody'],observed_at_unix_ns=time.time_ns(),scientific_execution=False)
pref=m.save('CAPTURE_PREFLIGHT.json',preflight)
r=recipe['admission_field_recipe']['source_review']
for key in ['must_adopt','must_preserve','must_bind_new_frozen_acceptance']:m.verify(r[key]['path'],r[key])
design=B/'ri237-root-cross-root-review-jkfg7vlx/RI236_ROOT_DESIGN_ADJUDICATION.json'
m.verify(design,dict(bytes=2656,sha256='9d669a14732daea258b6659d1861c19f41063ca26fc8089901ee28f020cb5d4f'))
adoption=dict(schema='ri239-root-one-capture-source-adoption-v1',status='ADOPT_UNCHANGED_RI141_FOR_ONE_CURRENT_E_METADATA_CAPTURE',adopted_source_adjudication=r['must_adopt'],preserved_historical_application=r['must_preserve'],frozen_custody_acceptance=r['must_bind_new_frozen_acceptance'],current_design_acceptance=m.ref(design),reviewed_recipe=m.ref(W/'CAPTURE_RECIPE.json'),fresh_preflight=pref,sources=recipe['source_roles'],environment=recipe['environment'],output=recipe['paths']['capture_output'],scope='One unchanged metadata capture; no profile/guard rerun, candidate interpreter startup, mode-card insertion or scientific execution. Historical refusals remain unchanged.',scientific_execution=False,ret_paused=True)
adopt=m.save('ROOT_CAPTURE_SOURCE_ADOPTION.json',adoption)
card={}
for key,item in recipe['admission_field_recipe'].items():
 if 'literal' in item:card[key]=item['literal']
 elif 'fresh_observation_equals_historical' in item:card[key]=item['fresh_observation_equals_historical']
 elif key=='bootstrap_host_preflight':card[key]=pref
 elif key=='source_review':card[key]=adopt
 else:raise AssertionError(key)
assert len(card)==17 and card['host']==pre['host']
v=pre['selected_interpreter_binding'];assert card['bootstrap']==dict(named_path=v['path'],resolved_path=v['resolved_path'],symlink_chain=v['symlink_chain'],target=m.pure(v))
admit=m.save('ADMIT_CAPTURE.json',card)
m.D=R
record=dict(schema='ri239-root-issued-capture-controls-v1',controls={name:m.identity(D/name) for name in ['CAPTURE_PREFLIGHT.json','ROOT_CAPTURE_SOURCE_ADOPTION.json','ADMIT_CAPTURE.json']},recipe=m.ref(W/'CAPTURE_RECIPE.json'),preflight_custody=m.ref(R/'PRE_CUSTODY.json'),issuer='root coordinator',single_attempt=True,scientific_execution=False,repository_unchanged=m.snapshot()==m.load(R/'REPO_ENTRY.json'))
print(json.dumps(dict(receipt=m.save('ISSUED_CAPTURE_CONTROLS.json',record),admission=admit,controls=len(record['controls']))))
