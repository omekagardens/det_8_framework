import hashlib,importlib.util
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri206-root-freeze-5e_n5lj_'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
v=m.load('/private/tmp/ri206_genuine_inputs.json');assert 'session_id' not in v['initial_result'] and v['initial_result']==v['actual_result'] and v['actual_result']['exit_code']==0
print(m.save('GENUINE_TOOL.json',v))
with (D/'ri206_save_genuine.py').open('xb') as f:f.write(Path(__file__).read_bytes())
