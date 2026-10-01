import hashlib,importlib.util
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri206-root-freeze-5e_n5lj_'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
print(m.save('PREPARATION_ACTUAL_RECEIPTS.json',m.load('/private/tmp/ri206_prepare_receipts.json')))
for src,name in [('/private/tmp/ri206_root_prepare_decision.py','ri206_root_prepare_decision.py'),(__file__,'ri206_save_preparation.py')]:
 with (D/name).open('xb') as f:f.write(Path(src).read_bytes())
m.D=B/'ri207-root-four-maxima-review-rrel_hre'
print(m.save('ROOT_COORDINATION.json',dict(schema='ri207-root-coordination-v1',predecessor=m.ref(m.D/'RI205_ROOT_ADJUDICATION.json'),assignment=m.ref(m.D/'RI208_NATIVE_ASSIGNMENT.json'),successfully_dispatched_after_adjudication=True,worker_thread='01a074c4-4b09-76a3-8cb2-0caf116f6b9c',observed_cursor='cec29fb8-71f0-4394-a689-daf6147d954c:15',observed_revision=15,observed_turn='01a0f57f-384a-79b3-b2c4-24d6b2575ba9',observed_status='active',observed_response='Five-maxima class only; six-maxima and global conclusion remain outside assignment.',active_worker_unmodified=True,ret_paused=True)))
