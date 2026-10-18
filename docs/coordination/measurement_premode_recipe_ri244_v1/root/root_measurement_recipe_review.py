from pathlib import Path
import importlib.util,hashlib,gzip,json
h=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');b=h.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=m.B/'ri245-root-hook-review-ichvs643';R=m.D
report=Path('/private/tmp/ri244-independent-recipe-bf62fb.txt');rp=dict(bytes=7826,sha256='58d3d0bc6b2134697e68e22d4a57e15b7dd6ae97b7394491f2786ca3b9cbfcca');m.verify(report,rp)
with (R/'RI244_INDEPENDENT_RECIPE.txt').open('xb') as f:f.write(report.read_bytes())
assert (R/'RI244_INDEPENDENT_RECIPE.txt').read_bytes()==report.read_bytes()
pins=[('ri160-white-fixture-custody-repair-ufok1zpo/SOURCE_SET.json',147447,'3c01d5825ce66ccf0b071329c46341ea01e28ef4cb76320e5776dd3ae6b53a4f'),('ri160-root-fixture-adjudication-0rmgmo7y/RI160_ROOT_ADJUDICATION.json',2582,'667e157b07b210952b819f9b9e4907abb4eb3dddb1c7bdcce4d3d6d04ad873b4'),('ri172-root-review-fkjv3v0z/RI162_CONSUMER_QUALIFICATION.json',4041,'0e27e1393c949a24a244ef2e2367ed8c72a10df1d3e3a6057cee8a4d20c9e0d7'),('ri241-current-e-premode-wp58xz0h/PRE_MODE_REQUEST.json',1013,'6aeb27d703ec8487b22d61fea4f992fe54ff4cd87b335fbfbd1675d89d0ce001'),('ri241-current-e-premode-wp58xz0h/ACTUAL_RUNTIME_NORMAL.json',2653,'ad393dee1a8c10a7798f9c961a732888d8273a003b19232ea5782977684d4379'),('ri242-root-canonical-review-vmbd1niz/RI241_ROOT_INPUT_ADJUDICATION.json',2744,'2731edec8f87afa381e11cd5a91168fdd5eb5a27f21667d7e834f81994aebd37'),('ri141-white-bootstrap-source-h58ls076/prepare.py',45721,'8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe')]
seen={}
def verify(r):
 v=m.verify(r['path'],r)
 if r['path'] in seen:assert seen[r['path']]==v
 seen[r['path']]=v;return v
for rel,n,sha in pins:verify(dict(path=str(m.B/rel),bytes=n,sha256=sha))
S=m.load(m.B/pins[0][0]);Q=m.load(m.B/pins[2][0]);request=m.load(m.B/pins[3][0]);runtime=m.load(m.B/pins[4][0])
assert len(S['dependencies'])==567 and len(S['modules'])==11
for r in [S['adapter'],*S['modules'].values(),*S['dependencies']]:verify(r)
assert Q['source_manifest']=={k:seen[str(m.B/pins[0][0])][k] for k in ('path','bytes','sha256')}
assert Q['status']=='ACCEPT_EXACT_INERT_ADAPTER_CONTROLS' and Q['all_passed'] is True and Q['scientific_execution'] is False and len(Q['controls'])==106
for k in ('genuine_outer','independent_review','report'):verify(Q[k])
assert set(request)=={'freeze','mode','actual_runtime','baseline','copies'} and len(runtime)==13 and runtime['mode']==request['mode']=='normal'
assert set(runtime['freeze'])=={'bytes','sha256'} and set(request['freeze'])=={'path','bytes','sha256'} and runtime['freeze']==m.pure(request['freeze'])
for r in request.values():
 if isinstance(r,dict):verify(r)
for r in runtime.values():
 if isinstance(r,dict) and set(r)=={'path','bytes','sha256'}:verify(r)
assert runtime['environment']['TMPDIR']==str(m.B/'ri154-white-execution-proposed-42_uvw15/tmp')
assert m.pure(runtime['snapshot'])==m.pure(runtime['baseline']) and m.pure(runtime['vendor_before'])==m.pure(runtime['vendor_after'])
assert sorted(x.name for x in (m.B/'ri241-current-e-premode-wp58xz0h').iterdir())==['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json']
D=m.B/'ri244-current-normal-premode-2kfsmiea';O=m.B/'ri156-operation-ri244-premode-2kfsmiea';assert not list(D.iterdir()) and not O.exists()
# Authenticate the historical E reference against the existing committed copy,
# then compare current metadata without decoding installed scientific material.
erel='docs/coordination/measurement_current_e_capture_ri239_v1/root/POST_E.json'
body=m.git('show','c4545e056d84d3880342a2df7c30cb1836cb3624:'+erel)
ep=m.B/'ri239-root-current-e-capture-mk6vocq1/POST_E.json';assert ep.read_bytes()==body;verify(dict(path=str(ep),**m.pin(body)))
old=json.loads(body);E=m.B/'ri154-white-execution-proposed-42_uvw15'
for r in old:
 p=E/r['relative'];s=p.lstat();assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==r['state']
 if r['kind']=='directory':assert sorted(x.name for x in p.iterdir())==r['entries']
 else:assert m.identity(p)==r['identity']
assert sum(x['kind']=='directory' for x in old)==9 and len(old)==58
for v in list(seen.values()):assert m.identity(v['path'])==v
print(m.save('RI244_ROOT_RECIPE_CHECK.json',dict(schema='ri245-ri244-root-recipe-check-v1',status='PASS_RECIPE_SOURCE_AND_CURRENT_E_METADATA',identities=list(seen.values()),unique_identities=len(seen),source_dependencies=567,adapter_and_modules=12,accepted_controls=106,current_E_files=49,current_E_directories=9,unchanged_E=True,whole_vendor_preflight_performed=False,dispatch_performed=False,admission_issued=False,scientific_execution=False)))
decision=dict(schema='ri245-ri244-root-recipe-adjudication-v1',status='ACCEPT_CONCRETE_PREPARATION_RECIPE_NOT_OPERATIONAL_ADMISSION',independent_recipe=m.ref(R/'RI244_INDEPENDENT_RECIPE.txt'),root_source_check=m.ref(R/'RI244_ROOT_RECIPE_CHECK.json'),manual_source_reads=['594418','077131','c50e52','3f2b1d'],scope='Exact12-field admission recipe, unchanged RI141 monitored launch interface and9-field pre_mode output. Source/path/environment mapping only.',resolved=['Fresh output is immediate evidence-parent sibling ri156-operation-ri244-premode-2kfsmiea; D244/output would refuse.','Operation environment TMPDIR is D244/tmp; accepted runtime13 environment remains E/tmp.','Outer cwd D244, child cwd D244/monitor, label PRE_MODE, unchanged180second monitor and960second outer alarm.','RI241 input adjudication is preparation provenance, not a substitute for original RI160 source_review and not a13th admission field.'],remaining=['Prepare fresh complete source/supplier/host/E/role union and actual bootstrap preflight.','Authenticate historical E and new controls; selected interpreter binding exactly equals accepted SOURCE_SET binding.','Independently review concrete controls, then root issues separate actual12-field admission and dispatches unchanged pre_mode once.','Preserve genuine initial/poll/terminal and complete monitor/action tails; independent9-field result review before separate mode_card.'],active_source_proposal='archive_repro_review is assigned a temporary source-only RI244 preparation proposal; no operational writes, admission, collection or execution.',source_proposal_accepted=False,admission_issued=False,dispatch_performed=False,mode_card_issued=False,scientific_qualification=False,RET_paused=True,diagnostics=['Root7f361c attempted an absent RI236_CAPTURE_ACCEPTANCE.json with stderr suppressed before a successful filename inventory. No body or claim was derived from that absent lookup; accepted source paths were subsequently read explicitly.'])
print(m.save('RI244_ROOT_RECIPE_ADJUDICATION.json',decision))
