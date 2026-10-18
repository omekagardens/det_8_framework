from pathlib import Path
import importlib.util,hashlib,json,gzip,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri242-root-canonical-review-vmbd1niz';D=B/'ri241-current-e-premode-wp58xz0h';P=B/'ri239-root-current-e-capture-mk6vocq1';E=B/'ri154-white-execution-proposed-42_uvw15'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=hp.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
assert not list(D.iterdir())
seen={}
def ref(path,size,sha):
 r=dict(path=str(path),bytes=size,sha256=sha);seen[r['path']]=m.verify(path,r);return r
def read(r):
 m.verify(r['path'],r);return m.load(r['path'])
def accepted(name,gz=False):
 rel='docs/coordination/measurement_current_e_capture_ri239_v1/root/'+name+('.gz' if gz else '')
 b=m.git('show','651911e278cb9b538328b3eb5fd460cf81f59490:'+rel)
 if gz:b=gzip.decompress(b)
 r=dict(path=str(P/name),**m.pin(b));return read(r),r
post,postref=accepted('POST_E.json');roles,rolesref=accepted('POST_ROLE_CUSTODY.json',True)
for row in post:
 p=E/row['relative'];st=p.lstat();assert [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
 else:assert m.identity(p)==row['identity']
for row in roles['observed_identities']:assert m.identity(row['path'])==row
assert len([r for r in post if r['kind']=='file'])==49 and len(post)==58
freeze=ref(E/'AUTHORIZED_FREEZE.json',26214,'9e0c0e4953c7213a76fea291d5f799984422de8628f039eac4e0d7b3c5758b14')
A=ref(B/'ri204-root-adapters-f04k2tg9/accepted_adapters/RUNTIME_ACCEPTANCE.json',22342,'6c11846207bb55f82057a80a63fddce8ba3b00b21550ffc1dc4326203dd15add')
snap=ref(B/'ri236-current-e-capture-3geu_r1s/PRE.stdout',7142026,'ee672c5014d38656e19230bdd10c9831fabf71387e30248e600a8b6d2d8f378e')
base=ref(B/'ri170-current-e-profile-normal-proposed-gikj2giy/PRE.stdout',7142026,'ee672c5014d38656e19230bdd10c9831fabf71387e30248e600a8b6d2d8f378e')
copy=ref(B/'ri226-freeze-reconciliation-operation-yvfg_p1b/FROZEN.json',127298,'a58eeff7d3652417cc2cb8a80f5a83c21be9779c0c92f412e5a136cfa937426c')
before=ref(P/'PRE_SUPPLIER_STABLE.json',1260447,'cf2e2cedecf1e9430081d769be5ae78395f0b1943967a040b9de03b702cfa4c2');after=ref(P/'POST_SUPPLIER_STABLE.json',1260447,'cf2e2cedecf1e9430081d769be5ae78395f0b1943967a040b9de03b702cfa4c2')
provenance=ref(P/'COLLECTION_PROVENANCE.json',2789,'2c96b9f19b43b597111edbb5d439999ed8f0359b137955af5c1d7789b5425202')
routes=ref(B/'ri156-operation-ri200-sidecars-ofv27lvp/observed_dyld_routes.json',771,'d428c7a943d1d13feecf1e55cbf0a80d80344636b11f922223e77d16b470fb38')
runtime=read(A);profiles=read(runtime['profile_review']);completion=read(profiles['completions']['profile_normal'])
assert profiles['schema']=='ri133-root-preparation-stage-review-v1' and profiles['status']=='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE' and profiles['stage']=='profiles' and profiles['environment_root']==str(E)
assert completion['artifacts']['PRE']==base and runtime['observed_dyld_routes']==routes
snapshot=read(snap);assert snapshot==read(base) and snapshot['preobserved_dyld_routes']==read(routes)
assert snapshot['runtime_inventory']==read(dict(path=runtime['runtime_inventory']['path'],**runtime['runtime_inventory']['pin']))
assert snapshot['interpreter']==runtime['interpreter']
assert read(before)==read(after)
proj,projref=accepted('SUPPLIER_PROJECTION_PROVENANCE.json');assert proj['records']['PRE']['projection']==before and proj['records']['POST']['projection']==after
assert read(copy)['source_states']==roles['source_states']
contract=read(ref(B/'ri236-current-e-normal-preparation-3geu_r1s/worker_proposal/CURRENT_E_AND_MODE_CONTRACT.json',9569,'b8794cbdb514dc79453b24c2cf55760a889d8e4569c807e1ab678389b0901354'))
assert contract['actual_runtime_record']['environment']==completion['environment'] and len(completion['environment'])==10
nextstep,_=accepted('RI241_MEASUREMENT_NEXT_STEP.json');assert nextstep['genuine_collection_tools']==provenance
obj=dict(schema='ri156-root-actual-mode-runtime-v1',phase='pre',mode='normal',freeze=m.pure(freeze),runtime_acceptance=A,environment=completion['environment'],snapshot=snap,baseline=base,copy_observation=copy,vendor_before=before,vendor_after=after,genuine_collection_tools=provenance,observed_dyld_routes=routes)
assert set(obj)==set(contract['actual_runtime_record']['fields']) and len(obj)==13 and set(obj['freeze'])=={'bytes','sha256'}
def write(name,v):
 p=D/name
 with p.open('xb') as f:f.write(m.canonical(v));f.flush();os.fsync(f.fileno())
 r=m.ref(p);assert m.pin(m.canonical(v))==m.pure(r) and read(r)==v;return r
actual=write('ACTUAL_RUNTIME_NORMAL.json',obj)
request=dict(freeze=freeze,mode='normal',actual_runtime=actual,baseline=base,copies=copy)
assert set(request)==set(contract['pre_mode_request']['fields']) and len(request)==5
requestref=write('PRE_MODE_REQUEST.json',request)
assert sorted(x.name for x in D.iterdir())==['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json']
for row in post:
 p=E/row['relative'];st=p.lstat();assert [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]==row['state']
 if row['kind']=='directory':assert sorted(x.name for x in p.iterdir())==row['entries']
 else:assert m.identity(p)==row['identity']
assert not (E/'ADMIT_NORMAL.json').exists() and not (E/'ADMIT_OPTIMIZED.json').exists()
result=dict(schema='ri241-root-unissued-runtime-assembly-v1',status='UNISSUED_RUNTIME13_REQUEST5_ASSEMBLED_PENDING_FINAL_INDEPENDENT_REVIEW',runtime=actual,request=requestref,field_counts=[13,5],freeze_field_counts=[2,3],fresh_opaque_identities_unchanged=len(roles['observed_identities']),full_E_files=49,full_E_directories=9,full_E_pre_and_post_equal=postref,source_role_custody=rolesref,role_counts={k:len(v) for k,v in roles['source_states'].items()},whole_snapshot_equals_baseline=True,whole_vendor_projections_equal=True,whole_observed_dyld_routes_equal=True,existing_provenance_preserved=provenance,source_contract=ref(B/'ri236-current-e-normal-preparation-3geu_r1s/worker_proposal/CURRENT_E_AND_MODE_CONTRACT.json',9569,'b8794cbdb514dc79453b24c2cf55760a889d8e4569c807e1ab678389b0901354'),installed_freeze_decoded=False,subject_execution=False,mode_admission_issued=False,pre_mode_admission_issued=False,scientific_execution=False,dependencies=list(seen.values()),next_action='Independent candidate review, then a fresh separate RI160 pre_mode12-field admission and unchanged monitored execution; review result9 before separate mode_card.',RET_paused=True)
print(json.dumps(dict(runtime=actual,request=requestref,receipt=m.save('RI241_UNISSUED_ASSEMBLY.json',result))))
