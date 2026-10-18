import hashlib,importlib.util,json,os
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri224-root-cwd-review-nyvru347';D=B/'ri222-freeze-cwd-repair-ypiy2jqw';E=B/'ri154-white-execution-proposed-42_uvw15'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
I=B/'ri224-independent-concrete-review-fof5xp1w';m.verify(I/'HANDOFF.json',dict(bytes=4088,sha256='bc5202d6adcaaa7c4ff3cc6a1da9c4758839bd642bd64a5aac278182bcecb474'));ih=m.load(I/'HANDOFF.json')
assert sorted(p.name for p in I.iterdir())==ih['namespace'] and ih['blocking_findings']==[]
for row in ih['files']:m.verify(row['path'],row)
pre=m.load('/private/tmp/ri224_predispatch_genuine.json');assert pre['terminal']['result']['exit_code']==0 and pre['terminal']['result']['chunk_id']=='5dfba4'
assert json.loads(pre['terminal']['result']['output'])==pre['observation']
assert pre['observation']['host']==m.load(D/'HOST_GENUINE_TOOL.json')['observation']
for row in pre['observation']['custody']['exact_prepared_files']:assert m.identity(row['path'])==row
for p in [D/'ADMIT_INSTALL.json',D/'DISPATCH.json',B/'ri222-freeze-install-operation-ypiy2jqw',E/'AUTHORIZED_FREEZE.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:assert not os.path.lexists(p)
fresh=m.save('FRESH_PREDISPATCH_CHECK.json',pre)
accept=m.save('CONCRETE_PREPARATION_ACCEPTANCE.json',dict(schema='ri224-root-concrete-preparation-acceptance-v1',status='ACCEPT_REVIEWED_ADMINISTRATIVE_PREPARATION',independent_review=m.ref(I/'HANDOFF.json'),root_check=m.ref(R/'ROOT_CONCRETE_PREPARATION_CHECK.json'),fresh_predispatch=fresh,proposal=m.ref(D/'INSTALLATION_PROPOSAL.json'),source_review=m.ref(D/'ROOT_SOURCE_REVIEW.json'),scope='Prepared source/host/supplier/E records and concrete bootstrap accepted; actual installation remains unperformed at this decision.',qualification_credit=0,RET_paused=True))
p=m.load(D/'INSTALLATION_PROPOSAL.json');m.verify(D/'INSTALLATION_PROPOSAL.json',ih['proposal']);m.verify(D/'PREPARATION_CUSTODY.json',ih['custody'])
decision=m.save('ROOT_INSTALLATION_ADMISSION_DECISION.json',dict(schema='ri224-root-installation-decision-v1',status='AUTHORIZE_EXACT_SINGLE_REVIEWED_INSTALLATION',preparation_acceptance=accept,fresh_check=fresh,independent_review=m.ref(I/'HANDOFF.json'),proposal=m.ref(D/'INSTALLATION_PROPOSAL.json'),source_review=m.ref(D/'ROOT_SOURCE_REVIEW.json'),one_attempt=True,scope='Install only the exact accepted26214-byte administrative candidate as E/AUTHORIZED_FREEZE.json with the reviewed command and unchanged monitor/limits. Preserve all failures; no retry or scientific mode.',startup_premises=['Authentic selected direct isolated vendor/startup and captured whole unchanged monitor.','Stable host, no descendants, Apple loader/shared-cache and source/pyc applicability remain external premises. Sampled sole-child RSS is not continuous process-group accounting.'],qualification_credit=0,RET_paused=True))
card=m.save(str(D/'ADMIT_INSTALL.json'),p['proposed_admission']);assert card==p['prospective_admission_pin']
dispatch=m.save(str(D/'DISPATCH.json'),p['proposed_dispatch'])
print(json.dumps(dict(decision=decision,admission=card,dispatch=dispatch)))
