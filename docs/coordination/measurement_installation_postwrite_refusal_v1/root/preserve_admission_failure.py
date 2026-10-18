import hashlib,importlib.util,json,os
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri224-root-cwd-review-nyvru347'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
def copy(src,name):
 raw=Path(src).read_bytes()
 with (R/name).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert (R/name).read_bytes()==raw
 return m.ref(R/name)
source=copy('/private/tmp/ri224_issue_installation.py','issue_installation_failed.py')
input_ref=copy('/private/tmp/ri224_predispatch_genuine.json','PREDISPATCH_TRANSCRIPTION_FAILED.json')
old=m.load(input_ref['path']);correct=json.loads(old['terminal']['result']['output']);assert old['observation']!=correct
old['observation']=correct
fixed=m.save('PREDISPATCH_TRANSCRIPTION_CORRECTED.json',old)
concrete=m.load(R/'ROOT_CONCRETE_PREPARATION_CHECK.json');observation=json.loads(concrete['polls'][-1]['result']['output']);assert concrete['observation']!=observation
concrete['observation']=observation
fixed_concrete=m.save('ROOT_CONCRETE_PREPARATION_CHECK_CORRECTED.json',concrete)
D=B/'ri222-freeze-cwd-repair-ypiy2jqw';E=B/'ri154-white-execution-proposed-42_uvw15'
paths=[D/'ADMIT_INSTALL.json',D/'DISPATCH.json',B/'ri222-freeze-install-operation-ypiy2jqw',E/'AUTHORIZED_FREEZE.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json',R/'FRESH_PREDISPATCH_CHECK.json',R/'CONCRETE_PREPARATION_ACCEPTANCE.json',R/'ROOT_INSTALLATION_ADMISSION_DECISION.json']
assert all(not os.path.lexists(p) for p in paths)
report=m.save('ADMISSION_WRITER_FAILURE.json',dict(schema='ri224-root-admission-transcription-failure-v1',status='FAILED_BEFORE_AUTHORITY_OR_OPERATION',actual_tool=dict(chunk_id='3d6bd4',exit_code=1),source=source,failed_input=input_ref,corrected_input=fixed,prior_concrete_record=m.ref(R/'ROOT_CONCRETE_PREPARATION_CHECK.json'),corrected_concrete_record=fixed_concrete,cause='JavaScript JSON.parse converted large integer filesystem nanosecond states to rounded Numbers in the redundant observation views. Exact original tool stdout strings are preserved unchanged. Python integer-preserving decode reconstructs the correct observations.',correction='Only redundant observation values are replaced in separately named records, decoded from untouched genuine stdout. Failed originals remain immutable.',absent_paths=[str(p) for p in paths],installation_attempted=False,qualification_credit=0))
print(json.dumps(dict(failure=report,corrected=fixed,corrected_concrete=fixed_concrete)))
