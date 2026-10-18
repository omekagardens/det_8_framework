"""UNEXECUTED independent administrative postcheck. Never imports installer,
RI160 bindings/contract or a scientific helper. Reconciles a retained failed write. Root reviews genuine origin and
supplier startup applicability separately; this code cannot issue acceptance.
"""
import argparse,hashlib,importlib.util,json,os,shlex,stat,time
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri226-directory-custody-recovery-yvfg_p1b';W=D/'worker_proposal'
E=B/'ri154-white-execution-proposed-42_uvw15';O=B/'ri226-freeze-reconciliation-operation-yvfg_p1b'
CANDIDATE=dict(path=str(B/'ri156-operation-ri206-freeze-5e_n5lj_/RESULT.json'),bytes=26214,sha256='9e0c0e4953c7213a76fea291d5f799984422de8628f039eac4e0d7b3c5758b14')
INPUT=dict(path=str(W/'INPUT_PINS.json'),bytes=677925,sha256='ba05f97194b141f4546ea3b0323d97f0ef5461d4cd33c0523174ac291bb98a84')
REPAIR={'path': '/Volumes/AI_DATA/development/det-review-evidence/ri226-directory-custody-recovery-yvfg_p1b/worker_proposal/REPAIR_PROVENANCE.json', 'bytes': 82537, 'sha256': 'ad7253f46b76dc4c5e72fa32ac0beabbe834606133dd4a46b26a516606dd41f3'}
VENDOR='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
ENV=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0')
LIMITS=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864)
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=h.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('metadata helper pin')
s=importlib.util.spec_from_file_location('ri209_independent_metadata',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
checks=0

def check(ok,msg):
 global checks
 checks+=1
 if not ok:raise ValueError('RI209_CHECK: '+msg)
def eq(a,b,msg):check(m.canonical(a)==m.canonical(b),msg)
def fields(v,n):check(type(v) is dict and set(v)==set(n.split()),'closed '+n)
def load(ref):
 fields(ref,'path bytes sha256');p=Path(ref['path']);check(p.resolve()==p and not p.is_symlink() and 0<ref['bytes']<=67108864,'regular literal bounded metadata');before=m.identity(p);eq(m.pure(before),m.pure(ref),'metadata pin');body=p.read_bytes();eq(m.pin(body),m.pure(ref),'read bytes')
 def pairs(rows):
  value={}
  for k,v in rows:check(k not in value,'duplicate key');value[k]=v
  return value
 def bad(x):raise ValueError('nonfinite metadata')
 value=json.loads(body,object_pairs_hook=pairs,parse_constant=bad);eq(body.decode(),m.canonical(value).decode(),'canonical metadata');eq(m.identity(p),before,'read selection');return value

def selection(path):
 v=m.identity(path);check(v['resolved_path']==str(path) and v['symlink_chain']==[],'no source/card link');return {k:v[k] for k in ('path','bytes','sha256','state')}
def state(p):
 z=p.lstat();return [z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
def full_tree(root):
 result=[];total=0;stack=[(root,0)]
 while stack:
  p,depth=stack.pop();before=state(p);check(depth<=16 and len(result)<25000,'tree bounds');check(not p.is_symlink(),'no links in installation tree');r=dict(relative=str(p.relative_to(root)),state=before)
  if p.is_dir():
   names=sorted(x.name for x in p.iterdir());r.update(kind='directory',entries=names);stack.extend((p/n,depth+1) for n in reversed(names))
  else:
   check(stat.S_ISREG(before[2]) and before[4]<=67108864,'bounded regular file');v=m.identity(p);total+=v['bytes'];check(total<=536870912,'tree aggregate');r.update(kind='file',identity=v)
  eq(state(p),before,'tree entry stable');result.append(r)
 # Recheck all directory memberships/states after descendant traversal.
 for row in result:
  p=root/row['relative'];eq(state(p),row['state'],'tree final state')
  if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'],'tree final membership')
 return sorted(result,key=lambda r:r['relative'])

def retained_review(repair):
 refs=repair['roles'];root=B/'ri222-freeze-install-operation-ypiy2jqw';before=load(refs['original_before']);obs=load(refs['original_observations']);c=load(refs['original_complete']);post=load(refs['postflight']);sup=load(refs['supersession'])
 fields(before,'E source_states source_observations bindings');fields(obs,'E_after binding_actual installation_write sources_actual supplier_actual')
 fields(c,'schema status admission candidate destination first_error independent_tails produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed scientific_execution mode_admission_issued ret_paused')
 err={'message':'RI209: root device inode mode links','secondary':[],'type':'ValueError'}
 eq([c['schema'],c['status'],c['candidate'],c['destination'],c['first_error'],c['complete_not_self_hashed'],c['scientific_execution'],c['mode_admission_issued'],c['ret_paused']],['ri213-installation-completion-v1','REFUSED_RETAIN_ALL_PARTIALS',CANDIDATE,str(E/'AUTHORIZED_FREEZE.json'),err,True,False,False,True],'actual prior refused receipt remains refused')
 eq(sup['status'],'OPERATIONAL_READINESS_SUPERSEDED_AFTER_ACTUAL_POSTWRITE_REFUSAL','no retained operative acceptance')
 eq([post['status'],post['first_error'],post['failed_tails'],post['passed_tail_count']],['REFUSAL_AND_RETAINED_PARTIALS_CONFIRMED_NOT_INSTALLATION_ACCEPTANCE',err,['E_and_frozen','final_E'],6],'original postflight scope')
 names=['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json'];eq(sorted(p.name for p in root.iterdir()),names,'exact original four retained files')
 for n in names:
  v=m.identity(root/n);check(v['resolved_path']==str(root/n) and v['symlink_chain']==[] and stat.S_ISREG(v['state'][2]) and v['state'][3]==1 and v['bytes']<=67108864,'original output type and selection')
 pins={n:m.ref(root/n) for n in names if n!='COMPLETE.json'};eq(c['produced_outputs'],pins,'all original prior outputs');eq(post['operation_files'],[m.ref(root/n) for n in names],'entire postflight original operation')
 eq(c['admission'],{k:before['bindings']['admission'][k] for k in ('path','bytes','sha256')},'original admission binding');eq(load(refs['original_attempt']),dict(schema='ri209-exclusive-install-attempt-v1',admission=c['admission'],candidate=CANDIDATE,destination=str(E/'AUTHORIZED_FREEZE.json'),no_retry=True,scientific_execution=False),'whole original attempt')
 expected_sources=load(refs['original_sources']);eq(len(expected_sources),904,'all historical sources');eq(before['source_observations'],expected_sources,'original source before');eq(obs['sources_actual'],expected_sources,'original source after');eq(obs['binding_actual'],before['bindings'],'original whole binding after');eq(obs['installation_write'],dict(error=None,cleanup_errors=[]),'retained successful write and close only')
 for row in expected_sources:eq(m.identity(row['path']),row,'original complete source state retained')
 for row in before['bindings'].values():eq(m.identity(row['path']),row,'original whole control state retained')
 t=c['independent_tails'];fields(t,'source_inputs root_bindings supplier E_and_frozen save_observations ordinary_outputs final_E output_namespace')
 expected_tails={n:dict(value=None,error=err) for n in ['E_and_frozen','final_E']}
 for name,value in dict(source_inputs=expected_sources,root_bindings=before['bindings'],supplier=obs['supplier_actual'],save_observations=pins['OBSERVATIONS.json'],ordinary_outputs=pins,output_namespace=[m.identity(root/n) for n in sorted(pins)]).items():expected_tails[name]=dict(value=value,error=None)
 eq(t,expected_tails,'every whole historical tail value and error')
 tt=c['timing'];fields(tt,'initial final elapsed')
 for row in tt.values():fields(row,'value error');check(row['error'] is None and type(row['value']) in (int,float) and float('-inf')<row['value']<float('inf'),'original finite clocks')
 eq(tt['elapsed']['value'],c['elapsed_seconds_before_complete_write'],'original elapsed receipt');eq(tt['elapsed']['value'],tt['final']['value']-tt['initial']['value'],'original clock arithmetic');check(0<=tt['elapsed']['value']<=180,'original elapsed limit')
 prior={r['relative']:r for r in before['E']};after={r['relative']:r for r in obs['E_after']}
 check(len(before['E'])==len(prior)==57 and len(obs['E_after'])==len(after)==58 and set(after)-set(prior)=={'AUTHORIZED_FREEZE.json'} and set(prior)-set(after)==set(),'original exact sole member addition')
 eq(prior['.'],post['root_before'],'entire pinned prior root');eq({k:after['.'][k] for k in ['state','entries']},post['root_after'],'entire pinned resulting root')
 eq(after['.']['kind'],'directory','same root type');eq(prior['.']['state'][:3],after['.']['state'][:3],'actual stable device inode mode');eq([prior['.']['state'][3],after['.']['state'][3]],[23,24],'only pinned actual nlink transition');eq(after['.']['entries'],sorted(prior['.']['entries']+['AUTHORIZED_FREEZE.json']),'exact root membership transition')
 for n,row in prior.items():
  if n!='.':eq(after[n],row,'entire old member unchanged '+n)
 check(sum(r['kind']=='file' for r in after.values())==49 and sum(r['kind']=='directory' for r in after.values())==9,'entire resulting domain')
 for row in after.values():
  if row['kind']=='file':check(stat.S_ISREG(row['identity']['state'][2]) and row['identity']['state'][3]==1 and row['identity']['symlink_chain']==[],'every retained ordinary file single-link')
 eq(after['AUTHORIZED_FREEZE.json']['identity'],post['installed_partial'],'entire installed partial identity');eq(m.pure(post['installed_partial']),m.pure(CANDIDATE),'complete candidate pin')
 return dict(E=obs['E_after'],source_states=before['source_states'],original_complete=refs['original_complete'],postflight=refs['postflight'],original_status=c['status'])

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--outer',required=True);parser.add_argument('--report',required=True);args=parser.parse_args()
 report=Path(args.report);check(report.parent==D and report.name=='RECONCILIATION_POSTCHECK.json' and not os.path.lexists(report),'exclusive external report')
 outer_ref=m.ref(args.outer);outer=load(outer_ref);fields(outer,'schema dispatch tool_transcript monitor post_supplier post_host_tools');eq(outer['schema'],'ri226-root-genuine-reconciliation-v1','outer schema')
 dispatch=load(outer['dispatch']);fields(dispatch,'outer_argv shell_command cwd login admission bootstrap monitor_source external_timeout_seconds single_attempt actual_execution_not_yet_started')
 eq(dispatch['cwd'],str(D),'outer cwd');eq(dispatch['login'],False,'login false');eq(dispatch['external_timeout_seconds'],960,'outer deadline');eq(dispatch['single_attempt'],True,'single attempt');eq(dispatch['actual_execution_not_yet_started'],True,'retained pre-execution dispatch declaration')
 for key in ('bootstrap','monitor_source'):load_ref=dispatch[key];m.verify(load_ref['path'],load_ref)
 check(dispatch['bootstrap']['path']==str(D/'RECONCILE_BOOTSTRAP.py'),'literal bootstrap path')
 eq(dispatch['monitor_source'],dict(path=str(B/'ri141-white-bootstrap-source-h58ls076/prepare.py'),bytes=45721,sha256='8c80242fb1e3756bd2aa06f1593cf6f17c3191eb6a850c175bad85578ac05cfe'),'whole unchanged monitor')
 argv=['/usr/bin/env','-i',*[k+'='+v for k,v in ENV.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',VENDOR,'-I','-B',dispatch['bootstrap']['path']]
 eq(dispatch['outer_argv'],argv,'full outer vector');eq(dispatch['shell_command'],shlex.join(argv),'full shell quoting')
 transcript=load(outer['tool_transcript']);fields(transcript,'initial_arguments initial_result intermediate_calls terminal_arguments terminal_result')
 eq(transcript['initial_arguments'],dict(cmd=dispatch['shell_command'],workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000),'literal genuine initial arguments')
 first=transcript['initial_result'];check(type(first.get('chunk_id')) is str and first.get('output')=='','initial tool result');check(type(transcript['intermediate_calls']) is list and len(transcript['intermediate_calls'])<=960,'bounded complete polls')
 if first.get('session_id') is None:
  eq(transcript['intermediate_calls'],[],'no invented polls');eq(transcript['terminal_arguments'],None,'no terminal args');eq(transcript['terminal_result'],None,'no terminal result');last=first
 else:
  check(type(first['session_id']) is int and first['session_id']>0 and first.get('exit_code') is None,'pending session');poll=dict(session_id=first['session_id'],chars='',yield_time_ms=1000,max_output_tokens=4000)
  for row in transcript['intermediate_calls']:
   fields(row,'arguments result');eq(row['arguments'],poll,'poll arguments');check(row['result'].get('session_id')==first['session_id'] and row['result'].get('exit_code') is None and row['result'].get('output')=='' and type(row['result'].get('chunk_id')) is str,'pending poll')
  eq(transcript['terminal_arguments'],poll,'terminal arguments');last=transcript['terminal_result']
 check(type(last.get('exit_code')) is int and last['exit_code']==0 and last.get('output')=='' and last.get('session_id') is None and type(last.get('chunk_id')) is str,'genuine zero completion')
 a=load(dispatch['admission']);fields(a,'schema status source_manifest source_review preflight output environment limits genuine_outer_required')
 eq([a['schema'],a['status'],a['output'],a['environment'],a['limits'],a['genuine_outer_required']],['ri226-root-read-only-reconciliation-admission-v1','AUTHORIZE_ONE_READ_ONLY_RECONCILIATION',str(O),ENV,LIMITS,True],'exact root admission');eq(dispatch['admission']['path'],str(D/'ADMIT_RECONCILE.json'),'literal card')
 manifest=load(a['source_manifest']);fields(manifest,'schema status files');eq([manifest['schema'],manifest['status']],['ri226-proposal-source-pins-v1','SOURCE_ONLY_NOT_ADMISSION'],'source manifest scope');eq([Path(r['path']).name for r in manifest['files']],['INPUT_PINS.json','PROTOCOL.md','REPAIR_PROVENANCE.json','check_reconciliation.py','reconcile_freeze.py'],'full source payloads')
 for r in manifest['files']:check(Path(r['path']).parent==W,'exact source path');m.verify(r['path'],r)
 source_review=load(a['source_review']);eq(source_review['source_manifest'],a['source_manifest'],'root review source binding');eq(source_review['status'],'ACCEPT_RI226_READ_ONLY_RECONCILIATION_SOURCE_ONLY','root source disposition')
 inputs=load(INPUT);repair=load(REPAIR);retained=retained_review(repair);eq(source_review['retained_failure'],retained['original_complete'],'root acknowledges old failure');eq(source_review['retained_postflight'],retained['postflight'],'root acknowledges retained postflight');g=load(inputs['roles']['graph']);accepted=load(inputs['roles']['candidate_acceptance']);eq(accepted['result'],CANDIDATE,'accepted complete candidate');eq(accepted['status'],'ACCEPT_COMPLETE_ADMINISTRATIVE_FREEZE_CANDIDATE','candidate acceptance');check(accepted['candidate_is_complete_canonical_result'] is True and accepted['freeze_installed'] is False,'candidate scope');check(len(g['copied_files'])==48 and len(g['history_originals'])==124 and len(g['sources'])==30,'exact graph sizes');eq(g['prospective_root'],str(E),'graph root');eq(sorted(load(inputs['roles']['historical_E']),key=lambda r:r['relative']),load(repair['roles']['original_before'])['E'],'entire old accepted E baseline')
 pre=load(a['preflight']);fields(pre,'schema status sources supplier E_before host_tool_receipts monitor_bootstrap source_manifest environment scientific_execution');eq([pre['schema'],pre['status'],pre['source_manifest'],pre['environment'],pre['scientific_execution']],['ri226-root-reconciliation-preflight-v1','FRESH_EXACT_READ_ONLY_RECONCILIATION_PREFLIGHT',a['source_manifest'],ENV,False],'root preflight scope')
 eq(pre['monitor_bootstrap'],dispatch['bootstrap'],'full monitor bootstrap closure');source_rows=load(pre['sources']);expected_refs={r['path']:r for r in inputs['files']+repair['files']+manifest['files']+[a['source_manifest'],a['source_review'],pre['monitor_bootstrap']]};eq([r['path'] for r in source_rows],sorted(expected_refs),'full source selection domain')
 for r in source_rows:eq(m.pure(r),m.pure(expected_refs[r['path']]),'source declared pin');eq(m.identity(r['path']),r,'fresh whole source identity')
 before=load(m.ref(O/'BEFORE.json'));fields(before,'E source_states source_observations bindings');eq(before['E'],load(pre['E_before']),'actual admitted before');eq(before['E'],retained['E'],'complete retained postwrite E baseline');eq(before['source_observations'],source_rows,'captured source baseline')
 binding_refs=dict(admission=dispatch['admission'],preflight=a['preflight'],source_manifest=a['source_manifest'],source_review=a['source_review'],sources=pre['sources'],supplier=pre['supplier'],E_before=pre['E_before'],host_tool_receipts=pre['host_tool_receipts'],monitor_bootstrap=pre['monitor_bootstrap'])
 eq(before['bindings'],{name:m.identity(row['path']) for name,row in binding_refs.items()},'all actual root binding states');
 for name,row in binding_refs.items():eq(m.pure(before['bindings'][name]),m.pure(row),'whole root pin '+name)
 current=full_tree(E);now={r['relative']:r for r in current};check(len(current)==len(now)==58,'complete current58 members');eq(current,before['E'],'whole read-only E retained including all root state fields');eq(current,retained['E'],'whole current selection equals authenticated actual postwrite evidence')
 installed=m.identity(E/'AUTHORIZED_FREEZE.json');eq(installed,now['AUTHORIZED_FREEZE.json']['identity'],'whole existing freeze state');eq(m.pure(installed),m.pure(CANDIDATE),'complete installed pin');check(installed['state'][3]==1 and installed['symlink_chain']==[],'single-link existing file');m.verify(CANDIDATE['path'],CANDIDATE);check((E/'AUTHORIZED_FREEZE.json').read_bytes()==Path(CANDIDATE['path']).read_bytes(),'exact retained original bytes');eq(m.identity(E/'AUTHORIZED_FREEZE.json'),installed,'freeze stable across byte reread')
 # Independently reconstruct every field; never call installer or bindings.py.
 roles=dict(copies=[dict(relative=r['relative'],original=selection(r['source']['path']),copy=selection(r['destination'])) for r in g['copied_files']],history=[selection(r['path']) for r in g['history_originals']],target_originals=[selection(r['original']) for r in g['sources']])
 eq(roles,before['source_states'],'complete48/124/30 before-after');eq(roles,retained['source_states'],'complete roles retained from original attempt')
 for row,decl in zip(roles['copies'],g['copied_files']):eq(m.pure(row['original']),m.pure(decl['source']),'original pin');eq(m.pure(row['copy']),m.pure(decl['source']),'copy pin')
 for row,decl in zip(roles['history'],g['history_originals']):eq(m.pure(row),m.pure(decl),'history pin')
 for row,decl in zip(roles['target_originals'],g['sources']):eq(m.pure(row),decl['pin'],'target original pin')
 expected_frozen=dict(schema='ri156-complete-copy-card-observation-v1',root=str(E),stage='frozen',source_states=roles,cards={'AUTHORIZED_FREEZE.json':selection(E/'AUTHORIZED_FREEZE.json')},tree=[dict(relative=r['relative'],kind=r['kind'],**(m.pure(r['identity']) if r['kind']=='file' else {})) for r in current],tmp_empty=True,scientific_body_decoded=False,source_acceptance_created=False)
 for name in ('tmp','runs/normal','runs/optimized'):eq(now[name]['entries'],[],'empty unadmitted directories')
 frozen=load(m.ref(O/'FROZEN.json'));eq(frozen,expected_frozen,'all nine frozen fields');check(len(frozen)==9,'nine fields')
 check(not os.path.lexists(E/'ADMIT_NORMAL.json') and not os.path.lexists(E/'ADMIT_OPTIMIZED.json'),'no mode cards')
 c=load(m.ref(O/'COMPLETE.json'));fields(c,'schema status admission candidate destination original_complete original_status postflight E_read_only first_error independent_tails produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed scientific_execution mode_admission_issued ret_paused');eq([c['schema'],c['status'],c['admission'],c['candidate'],c['destination'],c['first_error'],c['complete_not_self_hashed'],c['scientific_execution'],c['mode_admission_issued'],c['ret_paused']],['ri226-read-only-reconciliation-completion-v1','RECONCILED_PENDING_INDEPENDENT_ROOT_REVIEW',dispatch['admission'],CANDIDATE,str(E/'AUTHORIZED_FREEZE.json'),None,True,False,False,True],'complete success receipt');check(type(c['elapsed_seconds_before_complete_write']) in (int,float) and 0<=c['elapsed_seconds_before_complete_write']<=180,'inner elapsed')
 eq([c['original_complete'],c['original_status'],c['postflight'],c['E_read_only']],[retained['original_complete'],retained['original_status'],retained['postflight'],True],'explicit failure-preserving read-only scope')
 timing=c['timing'];fields(timing,'initial final elapsed')
 for name,row in timing.items():
  fields(row,'value error');eq(row['error'],None,'successful '+name+' timing has no error');check(type(row['value']) in (int,float) and float('-inf')<row['value']<float('inf'),'finite numeric '+name+' timing')
 eq(timing['elapsed']['value'],c['elapsed_seconds_before_complete_write'],'entire elapsed binding')
 eq(timing['final']['value']-timing['initial']['value'],timing['elapsed']['value'],'recorded clock arithmetic');check(timing['elapsed']['value']>=0,'nonnegative elapsed')
 names=['ATTEMPT.json','BEFORE.json','FROZEN.json','OBSERVATIONS.json'];pins={n:m.ref(O/n) for n in names};eq(c['produced_outputs'],pins,'all four produced file pins');eq(sorted(x.name for x in O.iterdir()),sorted(names+['COMPLETE.json']),'exact five operation files')
 for p in O.iterdir():check(not p.is_symlink() and p.is_file() and p.stat().st_nlink==1 and p.stat().st_size<=67108864,'ordinary output type/size')
 at=load(pins['ATTEMPT.json']);eq(at,dict(schema='ri226-exclusive-read-only-reconciliation-attempt-v1',admission=dispatch['admission'],candidate=CANDIDATE,destination=str(E/'AUTHORIZED_FREEZE.json'),original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True,no_retry=True,scientific_execution=False),'complete attempt')
 obs=load(pins['OBSERVATIONS.json']);fields(obs,'supplier_actual read_only_reconciliation sources_actual retained_failure_after binding_actual E_after source_states_after frozen');eq(obs['read_only_reconciliation'],dict(original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True),'complete read-only scope');eq(obs['retained_failure_after'],retained,'whole retained failure revalidated');eq(obs['sources_actual'],source_rows,'all observed sources');eq(obs['binding_actual'],before['bindings'],'observed bindings');eq(obs['E_after'],current,'whole E after');eq(obs['source_states_after'],roles,'all source selections');eq(obs['frozen'],frozen,'entire frozen record')
 t=c['independent_tails'];fields(t,'source_inputs root_bindings supplier E_and_frozen save_observations ordinary_outputs final_E output_namespace')
 for r in t.values():fields(r,'value error');eq(r['error'],None,'each independent tail passed')
 eq(t['source_inputs']['value'],source_rows,'source tail');eq(t['root_bindings']['value'],before['bindings'],'binding tail');eq(t['supplier']['value'],obs['supplier_actual'],'supplier tail');eq(t['E_and_frozen']['value'],pins['FROZEN.json'],'frozen tail');eq(t['save_observations']['value'],pins['OBSERVATIONS.json'],'saved observation tail');eq(t['ordinary_outputs']['value'],pins,'all output tails');eq(t['final_E']['value'],current,'last whole E observation');eq(t['output_namespace']['value'],[m.identity(O/n) for n in sorted(names)],'final complete namespace plus only COMPLETE')
 supplier=load(pre['supplier']);post=load(outer['post_supplier']);history=load(inputs['roles']['historical_supplier']);eq(supplier['environment'],ENV,'supplier env');eq({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in history.items() if k not in ('environment','observed_at_unix_ns')},'whole inherited supplier scope');eq({k:v for k,v in post.items() if k!='observed_at_unix_ns'},{k:v for k,v in supplier.items() if k!='observed_at_unix_ns'},'whole fresh supplier bracket')
 sf=[m.identity(r['path']) for r in supplier['vendor']+supplier['tools']];eq(sf,supplier['vendor']+supplier['tools'],'all fresh vendor/tool identities');ns=[]
 for r in supplier['namespace']:
  p=Path(r['path']);z=dict(path=str(p),kind=r['kind'],state=state(p));z.update(entries=sorted(x.name for x in p.iterdir())) if r['kind']=='directory' else z.update(target=os.readlink(p));ns.append(z)
 eq(ns,supplier['namespace'],'whole supplier namespace');absences=[dict(path=p,absent=not os.path.lexists(p)) for p in supplier['absent']];check(all(r['absent'] for r in absences),'all supplier absences');eq(list(os.uname()),supplier['host']['uname'],'host uname')
 eq(obs['supplier_actual'],dict(files=sf,namespace=ns,absent=absences,uname=list(os.uname())),'entire observed supplier result');
 for href in (pre['host_tool_receipts'],outer['post_host_tools']):
  hv=load(href);fields(hv,'schema command environment returncode stdout stderr uname genuine_tool');eq([hv['schema'],hv['command'],hv['environment'],hv['returncode'],hv['stdout'],hv['stderr'],hv['uname']],['ri209-root-host-command-record-v1',supplier['host']['argv'],{'PATH':'/usr/bin:/bin','LC_ALL':'C'},0,supplier['host']['stdout'],'',supplier['host']['uname']],'complete host command observation');load(hv['genuine_tool'])
 # Unchanged RI141 child monitor. Tool origin and host-command receipts require
 # separate root review; hashes and child pass labels cannot authenticate them.
 monitor=load(outer['monitor']);fields(monitor,'child_exit_code command elapsed_seconds environment final_sample_gap_passed final_sample_to_reap_gap_seconds first_error monitor_attempts passed peak_sampled_rss_kib samples stderr stdout stop_reason tail_errors wall_seconds');eq(outer['monitor']['path'],str(D/'monitor/RECONCILE.COMPLETION.json'),'literal monitor completion');eq(sorted(x.name for x in (D/'monitor').iterdir()),['RECONCILE.ATTEMPT.json','RECONCILE.COMPLETION.json','RECONCILE.stderr','RECONCILE.stdout'],'four monitor files')
 command=[VENDOR,'-I','-B',str(W/'reconcile_freeze.py'),'--admission',dispatch['admission']['path']]
 eq(monitor['command'],command,'exact installer child command');eq(monitor['environment'],ENV,'child environment');eq(monitor['wall_seconds'],180,'wall');eq([monitor['child_exit_code'],monitor['first_error'],monitor['tail_errors'],monitor['stop_reason'],monitor['passed'],monitor['final_sample_gap_passed']],[0,None,[],None,True,True],'whole monitor successful status');check(0<monitor['elapsed_seconds']<180,'child duration');check(0<len(monitor['samples'])<=len(monitor['monitor_attempts'])<=len(monitor['samples'])+1,'all samples/attempts')
 previous=0
 for a,sample in zip(monitor['monitor_attempts'],monitor['samples']):
  fields(a,'elapsed_seconds returncode stdout stderr');fields(sample,'elapsed_seconds rss_kib gap_seconds');check(type(a['returncode']) is int and a['returncode']==0 and a['stderr']=='' and a['stdout'].strip().isdigit(),'raw successful ps');eq(int(a['stdout'].strip()),sample['rss_kib'],'raw rss');eq(a['elapsed_seconds'],sample['elapsed_seconds'],'raw sample time');check(abs(sample['gap_seconds']-(sample['elapsed_seconds']-previous))<1e-12 and 0<=sample['gap_seconds']<=.1 and type(sample['rss_kib']) is int and 0<=sample['rss_kib']<=524288,'gap/rss bounds');previous=sample['elapsed_seconds']
 if len(monitor['monitor_attempts'])>len(monitor['samples']):
  a=monitor['monitor_attempts'][-1];fields(a,'elapsed_seconds returncode stdout stderr');check(a['returncode']==1 and a['stdout'].strip()=='' and a['stderr']=='' and previous<=a['elapsed_seconds']<=monitor['elapsed_seconds'],'confirmed-exit race retained, not a sample')
 check(abs(monitor['final_sample_to_reap_gap_seconds']-(monitor['elapsed_seconds']-previous))<1e-12 and 0<=monitor['final_sample_to_reap_gap_seconds']<=.1,'final reap gap');eq(monitor['peak_sampled_rss_kib'],max(s['rss_kib'] for s in monitor['samples']),'peak')
 for key in ('stdout','stderr'):eq(monitor[key]['path'],str(D/'monitor'/('RECONCILE.'+key)),'monitor stream path');m.verify(monitor[key]['path'],monitor[key]);eq(monitor[key]['bytes'],0,'empty stream')
 ma=load(m.ref(D/'monitor/RECONCILE.ATTEMPT.json'));fields(ma,'command environment wall_seconds pid_owner scientific_target_entry');eq([ma['command'],ma['environment'],ma['wall_seconds'],ma['scientific_target_entry']],[command,ENV,180,False],'full monitor attempt');check(type(ma['pid_owner']) is int and ma['pid_owner']>0,'monitor parent pid, not child identity');check(list((D/'tmp').iterdir())==[],'external tmp empty')
 result=dict(schema='ri226-independent-reconciliation-postcheck-v1',status='PASS_READ_ONLY_RECONCILIATION_PENDING_ROOT_ACCEPTANCE',checks=checks,admission=dispatch['admission'],candidate=CANDIDATE,original_complete=retained['original_complete'],original_status=retained['original_status'],retained_postflight=retained['postflight'],E_read_only=True,installed_freeze=m.ref(E/'AUTHORIZED_FREEZE.json'),frozen_observation=pins['FROZEN.json'],complete=m.ref(O/'COMPLETE.json'),whole_E=current,source_files=len(source_rows),copy_pairs=48,history_roles=124,target_original_roles=30,E_files=49,E_directories=9,prior_roles=inputs['prior_role_count'],operation_files=5,monitor_files=4,genuine_outer=outer_ref,external_tool_origin_and_host_receipts_require_root_review=True,scientific_execution=False,mode_admission_issued=False,ret_paused=True)
 with report.open('xb') as f:f.write(m.canonical(result));f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(report=m.ref(report),checks=checks,status=result['status'])))
if __name__=='__main__':main()
