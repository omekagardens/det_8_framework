import hashlib, importlib.util, json, os
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri224-root-cwd-review-nyvru347'
P=B/'ri222-freeze-cwd-repair-ypiy2jqw'; W=P/'worker_proposal'
I=B/'ri222-independent-cwd-review-15d9v2ym'
H=B/'ri122-root-execution-review-6whn_vky/metadata.py'
assert len(H.read_bytes())==3144 and hashlib.sha256(H.read_bytes()).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('root_metadata',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
def seal(p,n,sha):
 m.verify(p,dict(bytes=n,sha256=sha));v=m.load(p)
 assert sorted(x.name for x in p.parent.iterdir())==sorted(v['namespace'])
 for r in v['files']:m.verify(r['path'],r)
 return m.ref(p)
subject=seal(W/'HANDOFF.json',9023,'5762caec4ca89f2687de17da71671ec82e1066e81854b9d45364ea3ed59c1330')
independent=seal(I/'HANDOFF.json',3964,'d6f37c7a433094ad13d49e4626c05cf2fc428c3986b6131c84cce1747afe768b')
assert m.load(I/'HANDOFF.json')['blocking_findings']==[]
assert m.load(I/'HANDOFF.json')['subject']==subject
def copy(src,name):
 raw=Path(src).read_bytes()
 with (D/name).open('xb') as f:assert f.write(raw)==len(raw);f.flush();os.fsync(f.fileno())
 assert (D/name).read_bytes()==raw
 return m.ref(D/name)
replay=copy('/private/tmp/ri224_source_replay.py','source_replay.py')
genuine=copy('/private/tmp/ri224_source_replay_genuine.json','SOURCE_REPLAY_GENUINE_TOOL.json')
for name in ('ADMIN_CHECK.json','CWD_CONTRACT_CHECK.json'):
 assert (D/('ROOT_RI222_'+name)).read_bytes()==(W/name).read_bytes()
meta=m.save('RI222_ROOT_METADATA_CHECK.json',dict(schema='ri224-root-ri222-source-review-v1',status='PASS_SOURCE_REVIEW_NOT_OPERATION',subject=subject,independent_review=independent,source_replay=replay,genuine_replay=genuine,replay_result=m.ref(D/'ROOT_RI222_ADMIN_CHECK.json'),cwd_result=m.ref(D/'ROOT_RI222_CWD_CONTRACT_CHECK.json'),actual_tool='2a8df3 exit0',predicates=6645,whole_source_projection=True,complete_manual_source_review=True,review_read_receipts=['077d00','87cfe0','0696a1','2e6e2a','7ce995','bb1f18','54871e','3033ca','903b15'],scope='Complete installer/checker and protocol delta reviewed; exact outer D versus child D/monitor contract. Unchanged bytes, clock, eight-tail and limit semantics. No subject execution.',source_only=True,qualification_credit=0))
review=dict(schema='ri222-root-installation-source-review-v1',status='ACCEPT_RI209_INSTALLATION_SOURCE_ONLY',reviewed_packet='RI222',source_manifest=m.ref(W/'SOURCE_PINS.json'),subject=subject,independent_review=independent,root_metadata=meta,scope='Exact repaired source only. No operational admission, installed freeze, runtime qualification or physical evidence.',findings=['Complete actual monitor cwd chain reconstructed: outer D, child literal D/monitor.','Whole inverse projection preserves every other installer/checker behavior and all clock, byte, tail and limit requirements.','All896 inputs and857 prior source rows preserved; prospective904 closure awaits preparation.','Earlier review missed the cwd mismatch; actual failed reservation and superseded readiness remain immutable.'],prior_RI218_readiness_remains_superseded=m.ref(B/'ri221-root-installation-ru2v15ie/RI218_OPERATIONAL_SUPERSESSION.json'),installation_admitted=False,scientific_execution=False,qualification_credit=0,RET_paused=True,next_action='Reviewed fresh preparation under -I -B, concrete generated bootstrap/preflight review, then distinct one-operation admission and actual outcome review.')
print(json.dumps(dict(metadata=meta,source_review=m.save(str(P/'ROOT_SOURCE_REVIEW.json'),review))))
