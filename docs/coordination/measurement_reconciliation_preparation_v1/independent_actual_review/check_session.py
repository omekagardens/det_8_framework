"""Independent additive actual tool linkage. Metadata only; never executes subjects."""
from pathlib import Path
import json,hashlib,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');T=B/'ri230-root-lower-combinations-review-v9mxbmtc';R=B/'ri230-independent-concrete-preparation-yehbzc6e'
labels=[]
def ck(value,label):
 labels.append(label)
 if not value:raise ValueError(label)
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def eq(a,b,label):ck(canonical(a)==canonical(b),label)
def load(name,size,sha):
 p=T/name;b=p.read_bytes();ck(len(b)==size and hashlib.sha256(b).hexdigest()==sha,'exact pin '+name)
 return json.loads(b),dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
a,ap=load('GENUINE_PREPARATION_TOOL.json',3113,'afe45fc3982de98e7bde448fe9be75974d273da2f91eee3e6bbb1b64e27a97d1')
b,bp=load('GENUINE_PREPARATION_SESSION_LINKAGE.json',2336,'f1c4420c94c34acae7cc947b6a7bf9b98f1639f06900ace2544d45767f1bec0e')
eq(sorted(b),sorted(['initial_session','intermediate_write_stdin_calls','original','original_transcript_unchanged','record_origin','schema','terminal_call']),'closed additive schema')
eq(b['schema'],'ri230-additive-actual-preparation-session-linkage-v1','schema');eq(b['original'],ap,'original whole pin');eq(b['original_transcript_unchanged'],True,'unchanged record declaration');eq(b['initial_session'],a['initial']['result']['session_id'],'initial-session linkage');eq(b['initial_session'],16198,'actual session');eq(b['intermediate_write_stdin_calls'],[],'no intervening calls');eq(sorted(b['terminal_call']),['arguments','result','tool'],'closed terminal call');eq(b['terminal_call']['tool'],'write_stdin','actual terminal tool');eq(b['terminal_call']['arguments'],dict(chars='',max_output_tokens=4000,session_id=16198,yield_time_ms=1000),'entire genuine terminal arguments');eq(b['terminal_call']['result'],a['terminal'],'entire terminal result including unchanged raw output');eq([a['initial']['result']['chunk_id'],a['terminal']['chunk_id'],a['terminal']['exit_code']],['0f12a4','1db8d4',0],'genuine exit chain');eq(b['record_origin'],'Direct root record of the actual sole write_stdin invocation retained in this conversation; no generated or proposed session receipt.','genuine root provenance disclosure')
p=R/'CHECK_RESULT.json';raw=p.read_bytes();ck(len(raw)==2639095 and hashlib.sha256(raw).hexdigest()=='72fc8a1717b0ce5b501d5080a83efa22979f3b58db37b8fd36e5c5bed2eb4440','original complete custody replay retained')
v=json.loads(raw);eq(v['status'],'PASS_COMPLETE_PREPARED_METADATA_AND_CURRENT_CUSTODY_PENDING_GENUINE_TERMINAL_ARGUMENTS','pending scope addressed separately');eq(v['actual_preparation_tool'],ap,'same actual preparation reviewed');eq([v['source_execution'],v['reconciliation_admitted'],v['frozen_custody_accepted'],v['scientific_decode'],v['qualification_credit']],[False,False,False,False,0],'no outcome promotion')
out=dict(schema='ri230-independent-session-check-v1',status='PASS_COMPLETE_GENUINE_PREPARATION_LINKAGE',checks=len(labels),labels=labels,inputs=[ap,bp,dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())],tool_origin_remains_genuine_root_receipt_premise=True,actual_preparation_only=True,reconciliation_executed=False,authority_issued=False)
data=(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+'\n').encode();p=R/'SESSION_CHECK_RESULT.json'
with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(report=dict(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()),checks=len(labels),status=out['status'])))
