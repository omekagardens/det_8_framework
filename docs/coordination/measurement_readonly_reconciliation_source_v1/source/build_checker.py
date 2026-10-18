"""Administrative literal source adapter. Does not import a target."""
from pathlib import Path
import json,hashlib,difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence');OW=B/'ri222-freeze-cwd-repair-ypiy2jqw/worker_proposal';W=B/'ri226-directory-custody-recovery-yvfg_p1b/worker_proposal'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(n,b):
 with (W/n).open('xb') as f:f.write(b)
 assert (W/n).read_bytes()==b
old=(OW/'check_installation.py').read_text();s=old.replace('RI160 bindings/contract or a scientific helper.','RI160 bindings/contract or a scientific helper. Reconciles a retained failed write.').replace('ri222-freeze-cwd-repair-ypiy2jqw','ri226-directory-custody-recovery-yvfg_p1b').replace('ri222-freeze-install-operation-ypiy2jqw','ri226-freeze-reconciliation-operation-yvfg_p1b')
s=s.replace(next(x for x in s.splitlines() if x.startswith('REPAIR=')),'REPAIR='+repr(pin(W/'REPAIR_PROVENANCE.json')))
s=s.replace("'INSTALLATION_POSTCHECK.json'","'RECONCILIATION_POSTCHECK.json'").replace('INSTALL_BOOTSTRAP.py','RECONCILE_BOOTSTRAP.py').replace('ADMIT_INSTALL.json','ADMIT_RECONCILE.json')
s=s.replace("'ri209-root-genuine-installation-v1'","'ri226-root-genuine-reconciliation-v1'").replace("'ri209-root-freeze-installation-admission-v1','AUTHORIZE_ONE_EXACT_FREEZE_INSTALLATION'","'ri226-root-read-only-reconciliation-admission-v1','AUTHORIZE_ONE_READ_ONLY_RECONCILIATION'").replace("'ri209-proposal-source-pins-v1'","'ri226-proposal-source-pins-v1'")
s=s.replace("'check_installation.py','install_freeze.py'","'check_reconciliation.py','reconcile_freeze.py'").replace("'ACCEPT_RI209_INSTALLATION_SOURCE_ONLY'","'ACCEPT_RI226_READ_ONLY_RECONCILIATION_SOURCE_ONLY'")
s=s.replace("'ri209-root-installation-preflight-v1','FRESH_EXACT_INSTALLATION_PREFLIGHT'","'ri226-root-reconciliation-preflight-v1','FRESH_EXACT_READ_ONLY_RECONCILIATION_PREFLIGHT'")
# Independent saved-history reconstruction; it imports neither prior nor new subject.
history='''def retained_review(repair):
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

'''
s=s.replace('def main():',history+'def main():')
s=s.replace("inputs=load(INPUT);repair=load(REPAIR);g=", "inputs=load(INPUT);repair=load(REPAIR);retained=retained_review(repair);eq(source_review['retained_failure'],retained['original_complete'],'root acknowledges old failure');eq(source_review['retained_postflight'],retained['postflight'],'root acknowledges retained postflight');g=")
s=s.replace("eq(before['E'],sorted(load(inputs['roles']['historical_E']),key=lambda r:r['relative']),'retained original E baseline')","eq(before['E'],retained['E'],'complete retained postwrite E baseline')")
lo=s.index(" current=full_tree(E);old=");hi=s.index(' # Independently reconstruct every field;',lo)
s=s[:lo]+''' current=full_tree(E);now={r['relative']:r for r in current};check(len(current)==len(now)==58,'complete current58 members');eq(current,before['E'],'whole read-only E retained including all root state fields');eq(current,retained['E'],'whole current selection equals authenticated actual postwrite evidence')
 installed=m.identity(E/'AUTHORIZED_FREEZE.json');eq(installed,now['AUTHORIZED_FREEZE.json']['identity'],'whole existing freeze state');eq(m.pure(installed),m.pure(CANDIDATE),'complete installed pin');check(installed['state'][3]==1 and installed['symlink_chain']==[],'single-link existing file');m.verify(CANDIDATE['path'],CANDIDATE);check((E/'AUTHORIZED_FREEZE.json').read_bytes()==Path(CANDIDATE['path']).read_bytes(),'exact retained original bytes');eq(m.identity(E/'AUTHORIZED_FREEZE.json'),installed,'freeze stable across byte reread')
''' +s[hi:]
s=s.replace("eq(roles,before['source_states'],'complete48/124/30 before-after')","eq(roles,before['source_states'],'complete48/124/30 before-after');eq(roles,retained['source_states'],'complete roles retained from original attempt')")
s=s.replace("fields(c,'schema status admission candidate destination first_error independent_tails produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed scientific_execution mode_admission_issued ret_paused');eq([c['schema']", "fields(c,'schema status admission candidate destination original_complete original_status postflight E_read_only first_error independent_tails produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed scientific_execution mode_admission_issued ret_paused');eq([c['schema']")
s=s.replace("'ri213-installation-completion-v1','INSTALLED_PENDING_INDEPENDENT_ROOT_REVIEW'","'ri226-read-only-reconciliation-completion-v1','RECONCILED_PENDING_INDEPENDENT_ROOT_REVIEW'")
s=s.replace(" timing=c['timing'];fields(timing,'initial final elapsed')"," eq([c['original_complete'],c['original_status'],c['postflight'],c['E_read_only']],[retained['original_complete'],retained['original_status'],retained['postflight'],True],'explicit failure-preserving read-only scope')\n timing=c['timing'];fields(timing,'initial final elapsed')")
s=s.replace("dict(schema='ri209-exclusive-install-attempt-v1',admission=dispatch['admission'],candidate=CANDIDATE,destination=str(E/'AUTHORIZED_FREEZE.json'),no_retry=True,scientific_execution=False)","dict(schema='ri226-exclusive-read-only-reconciliation-attempt-v1',admission=dispatch['admission'],candidate=CANDIDATE,destination=str(E/'AUTHORIZED_FREEZE.json'),original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True,no_retry=True,scientific_execution=False)")
s=s.replace("fields(obs,'supplier_actual installation_write sources_actual binding_actual E_after source_states_after frozen');eq(obs['installation_write'],dict(error=None,cleanup_errors=[]),'write/close success')","fields(obs,'supplier_actual read_only_reconciliation sources_actual retained_failure_after binding_actual E_after source_states_after frozen');eq(obs['read_only_reconciliation'],dict(original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True),'complete read-only scope');eq(obs['retained_failure_after'],retained,'whole retained failure revalidated')")
s=s.replace('INSTALL.COMPLETION.json','RECONCILE.COMPLETION.json').replace('INSTALL.ATTEMPT.json','RECONCILE.ATTEMPT.json').replace('INSTALL.stderr','RECONCILE.stderr').replace('INSTALL.stdout','RECONCILE.stdout').replace("('INSTALL.'+key)","('RECONCILE.'+key)").replace("str(W/'install_freeze.py')","str(W/'reconcile_freeze.py')")
s=s.replace("schema='ri209-independent-installation-postcheck-v1',status='PASS_ADMINISTRATIVE_INSTALLATION_PENDING_ROOT_ACCEPTANCE'","schema='ri226-independent-reconciliation-postcheck-v1',status='PASS_READ_ONLY_RECONCILIATION_PENDING_ROOT_ACCEPTANCE'")
s=s.replace("candidate=CANDIDATE,installed_freeze=m.ref(E/'AUTHORIZED_FREEZE.json')","candidate=CANDIDATE,original_complete=retained['original_complete'],original_status=retained['original_status'],retained_postflight=retained['postflight'],E_read_only=True,installed_freeze=m.ref(E/'AUTHORIZED_FREEZE.json')")
assert 'INSTALLED_PENDING' not in s and "state'][:4]" not in s and "'install_freeze.py'" not in s
s=s.replace("eq(g['prospective_root'],str(E),'graph root')","eq(g['prospective_root'],str(E),'graph root');eq(sorted(load(inputs['roles']['historical_E']),key=lambda r:r['relative']),load(repair['roles']['original_before'])['E'],'entire old accepted E baseline')")
put('check_reconciliation.py',s.encode());put('CHECKER_DIFF.patch',''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile=str(OW/'check_installation.py'),tofile=str(W/'check_reconciliation.py'))).encode())
print(json.dumps(dict(checker=pin(W/'check_reconciliation.py'))))
