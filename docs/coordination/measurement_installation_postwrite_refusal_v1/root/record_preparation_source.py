import hashlib,importlib.util,json,os,sys
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri224-root-cwd-review-nyvru347'
H=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=H.read_bytes()
assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',H);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
review=Path(sys.argv[1]);m.verify(review,dict(bytes=int(sys.argv[2]),sha256=sys.argv[3]));hand=m.load(review)
for r in hand['files']:m.verify(r['path'],r)
def copy(src,name,expected=None):
 if expected:m.verify(src,expected)
 raw=Path(src).read_bytes()
 with (D/name).open('xb') as f:assert f.write(raw)==len(raw);f.flush();os.fsync(f.fileno())
 assert (D/name).read_bytes()==raw
 return m.ref(D/name)
source=copy('/private/tmp/ri224_install_preparation_draft.py','prepare_installation.py',dict(bytes=18455,sha256='9af0db33f4a57036b0f9bb911822dfd1ea905b6bddca1edc274d78dc00b05e80'))
host=copy('/private/tmp/ri224_fresh_host.json','GENUINE_PREPARATION_HOST_TOOL.json')
receipt=m.load(host['path']);assert receipt['result']['chunk_id']=='343dae' and receipt['result']['exit_code']==0 and json.loads(receipt['result']['output'])==receipt['observation']
acceptance=m.save('PREPARATION_SOURCE_ACCEPTANCE.json',dict(schema='ri224-root-preparation-source-acceptance-v1',status='ACCEPT_EXACT_ADMINISTRATIVE_PREPARATION_SOURCE',source=source,independent_review=m.ref(review),root_read_receipts=['e18ba1','193cb9','903b15'],fresh_host_tool=host,mandatory_invocation=['/opt/homebrew/bin/python3','-I','-B'],writes='Nine exact preparation files and two fresh empty control directories in fixed D222 only; partials retained on failure.',source_closure='902 existing opaque source rows plus root review and generated bootstrap =904.',cwd_contract='Outer D222; generated out=D222/monitor; unchanged Popen cwd=out; corrected installer guard requires literal D222/monitor.',scope='Administrative preparation only; no admission, dispatch, installer/monitor invocation, E modification or scientific operation.',remaining_premises=['Authentic root host tool origin','Stable host and selected source/supplier/E state','Root invocation with isolated/no-bytecode flags'],installation_admitted=False,qualification_credit=0,RET_paused=True))
print(json.dumps(dict(source=source,host=host,acceptance=acceptance)))
