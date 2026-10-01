import hashlib,importlib.util,json
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri204-root-adapters-f04k2tg9'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
v=json.loads(Path('/private/tmp/ri204_genuine_inputs.json').read_bytes());g=m.save('GENUINE_TOOL.json',v['genuine']);v['terminal']['original_genuine_record']=g
print(g);print(m.save('GENUINE_TERMINAL_ARGUMENTS.json',v['terminal']))
