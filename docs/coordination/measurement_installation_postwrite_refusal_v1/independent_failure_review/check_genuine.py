"""Administrative linkage only; no subject, vendor, host or checker invocation."""
from pathlib import Path
import hashlib,json,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');T=B/'ri224-root-cwd-review-nyvru347';D=B/'ri222-freeze-cwd-repair-ypiy2jqw';R=Path(__file__).resolve().parent
n=0
def need(v,msg):
 global n
 n+=1
 if not v:raise ValueError(msg)
def c(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def eq(a,b,msg):need(c(a)==c(b),msg)
def pin(p):
 p=Path(p);v=p.read_bytes();return dict(path=str(p),bytes=len(v),sha256=hashlib.sha256(v).hexdigest())
def load(p):return json.loads(Path(p).read_bytes())
refs=[]
for name,size,sha in [('GENUINE_INSTALLATION_TOOL.json',3634,'e2506eb89947fce6b0e7368540a782a5e8e7af52c904974e44f2fc70d1778bdd'),('GENUINE_POST_HOST_TOOL.json',1540,'a679f2ff04d2d4f95e46a722ae4cc130ff7aa65d772e751673b65aaec42e969a'),('POST_FAILURE_CUSTODY.json',5932,'8b62febd21d4f3e0ad9fdf53195f05b922db395ab5b9bf265b441e1ff659f4e3')]:
 row=dict(path=str(T/name),bytes=size,sha256=sha);eq(pin(row['path']),row,'root complete pin');refs.append(row)
genuine=load(refs[0]['path']);host=load(refs[1]['path']);root=load(refs[2]['path']);dispatch=load(D/'DISPATCH.json');own=load(R/'CHECK_RESULT.json')
eq(genuine['initial_arguments'],dict(cmd=dispatch['shell_command'],workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000),'whole actual command arguments')
eq({k:v for k,v in genuine['transport_arguments'].items() if k not in ('sandbox_permissions','justification')},genuine['initial_arguments'],'transport retains exact operation arguments')
eq(genuine['transport_arguments']['sandbox_permissions'],'require_escalated','actual transport approval')
eq([genuine['initial_result']['chunk_id'],genuine['initial_result']['session_id'],genuine['initial_result']['output']],['8081b8',81601,''],'actual initial session')
need(genuine['initial_result'].get('exit_code') is None,'initial pending')
eq(genuine['intermediate_calls'],[],'no invented intermediate polls');eq(genuine['terminal_arguments'],dict(session_id=81601,chars='',yield_time_ms=1000,max_output_tokens=4000),'whole actual terminal arguments')
eq([genuine['terminal_result']['chunk_id'],genuine['terminal_result']['exit_code']],['17185d',1],'genuine terminal refusal');need(genuine['terminal_result'].get('session_id') is None,'terminal completed')
need(genuine['terminal_result']['output'].endswith('ValueError: bounded child refused: INSTALL\n'),'outer traceback accurately distinguishes monitor refusal')
eq([genuine['schema'],genuine['status'],genuine['success']],['ri224-genuine-refused-installation-transcript-v1','ACTUAL_FAILED_INSTALLATION_RETAIN_ALL_PARTIALS',False],'actual refusal attribution')
eq(json.loads(host['result']['output']),host['observation'],'complete actual post-host stdout');eq([host['result']['chunk_id'],host['result']['exit_code']],['e67a20',0],'post-host genuine successful event')
eq(host['observation'],load(D/'HOST_GENUINE_TOOL.json')['observation'],'whole host bracket')
for key in ('candidate','installed_partial'):
 row=root[key];eq(pin(row['path']),{k:row[k] for k in ('path','bytes','sha256')},'full root candidate/partial pin')
eq(root['installed_partial'],own['installed'],'root exact retained partial selection');eq(root['candidate'],own['candidate'],'candidate selection')
eq(root['root_before'],own['before_root'],'all before root fields');eq(root['root_after'],{k:own['after_root'][k] for k in ('entries','state')},'all after root fields')
eq(root['first_error'],own['first_error'],'first failure');eq(root['failed_tails'],own['failed_tails'],'failed tail identities');eq(root['passed_tail_count'],len(own['passed_tails']),'six complete passed tails')
for row in root['monitor_files']+root['operation_files']:eq(pin(row['path']),row,'all root artifact pins')
monitor=load(D/'monitor/INSTALL.COMPLETION.json');eq(root['monitor_summary'],{k:monitor[k] for k in root['monitor_summary']},'entire root monitor summary');eq(root['samples'],len(monitor['samples']),'all42samples')
eq([root['status'],root['qualification_credit'],root['success_checker_not_run'],root['no_mode_cards'],root['no_retry']],['REFUSAL_AND_RETAINED_PARTIALS_CONFIRMED_NOT_INSTALLATION_ACCEPTANCE',0,True,True,True],'root failure boundary')
for row in (dispatch['bootstrap'],dispatch['monitor_source']):eq(pin(row['path']),row,'whole actual bootstrap/unchanged monitor pin')
result=dict(schema='ri224-independent-genuine-failure-linkage-v1',status='PASS_LINKAGE_NOT_INSTALLATION_ACCEPTANCE',checks=n,root_records=refs,genuine_initial='8081b8',genuine_terminal='17185d',genuine_host='e67a20',all_own_findings_match_root_saved_custody=True,full_source_supplier_repository_postflight='Root-reported actual4f8009/session26037 to13f7b9 exit0; not independently replayed in this bounded failure review.',tool_origin_remains_external=True,subject_execution=False,qualification_credit=0)
data=c(result)
with (R/'GENUINE_LINKAGE.json').open('xb') as f:need(f.write(data)==len(data),'whole own result');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(result=pin(R/'GENUINE_LINKAGE.json'),checks=result['checks'],status=result['status'])))
