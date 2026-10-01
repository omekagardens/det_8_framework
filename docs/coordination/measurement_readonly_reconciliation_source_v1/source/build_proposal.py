"""Administrative source-text builder only; never imports or executes targets."""
from pathlib import Path
import hashlib,json,difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence');OLD=B/'ri222-freeze-cwd-repair-ypiy2jqw';OW=OLD/'worker_proposal';OO=B/'ri222-freeze-install-operation-ypiy2jqw';R=B/'ri224-root-cwd-review-nyvru347';D=B/'ri226-directory-custody-recovery-yvfg_p1b';W=D/'worker_proposal'
def body(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def emit(n,b):
 p=W/n
 with p.open('xb') as f:f.write(b)
 assert p.read_bytes()==b
 return pin(p)
assignment=R/'RI226_MEASUREMENT_ASSIGNMENT.json'
assert pin(assignment)==dict(path=str(assignment),bytes=3315,sha256='077b790342bae3450756b5b734894d46024b17c49f9b9360acd1105b75346416')
a=json.loads(assignment.read_bytes())
for k in ['actual_outcome','exact_checker','exact_installer','postflight','predecessor_supersession','source_handoff']:assert pin(a[k]['path'])==a[k]
base=json.loads((OW/'INPUT_PINS.json').read_bytes());prior=json.loads((OW/'REPAIR_PROVENANCE.json').read_bytes())
roles=dict(assignment=pin(assignment),original_before=pin(OO/'BEFORE.json'),original_complete=pin(OO/'COMPLETE.json'),original_observations=pin(OO/'OBSERVATIONS.json'),original_attempt=pin(OO/'ATTEMPT.json'),postflight=a['postflight'],supersession=a['predecessor_supersession'],genuine_failure=a['actual_outcome'],postflight_tool=pin(R/'POST_FAILURE_CHECK_TOOL.json'),original_sources=pin(OLD/'SOURCES_BEFORE.json'),original_supplier=pin(OLD/'SUPPLIER_BEFORE.json'))
extra_names=['RI226_MEASUREMENT_ASSIGNMENT.json','POST_FAILURE_CUSTODY.json','RI222_OPERATIONAL_SUPERSESSION.json','GENUINE_INSTALLATION_TOOL.json','POST_FAILURE_CHECK_TOOL.json','GENUINE_POST_HOST_TOOL.json','GENUINE_PREPARATION_HOST_TOOL.json','GENUINE_PREPARATION_TOOL.json','ADMISSION_TRANSCRIPTION_CORRECTION_REVIEW.json','ADMISSION_WRITER_FAILURE.json','CONCRETE_PREPARATION_ACCEPTANCE.json','FRESH_PREDISPATCH_CHECK.json','PREDISPATCH_TRANSCRIPTION_CORRECTED.json','PREDISPATCH_TRANSCRIPTION_FAILED.json','PREPARATION_SOURCE_ACCEPTANCE.json','ROOT_CONCRETE_PREPARATION_CHECK.json','ROOT_CONCRETE_PREPARATION_CHECK_CORRECTED.json','ROOT_INSTALLATION_ADMISSION_DECISION.json','ROOT_RI222_ADMIN_CHECK.json','ROOT_RI222_CWD_CONTRACT_CHECK.json','RI222_ROOT_METADATA_CHECK.json','SOURCE_REPLAY_GENUINE_TOOL.json','check_preparation.py','issue_installation_failed.py','issue_installation_v2.py','postfailure.py','prepare_installation.py','preserve_admission_failure.py','record_preparation_source.py','seal_source.py','source_replay.py']
groups=dict(inherited_repair=prior['files'],ri222_seal=[pin(p) for p in sorted(OW.iterdir()) if p.is_file()],retained_root_operation=[pin(p) for p in sorted(OLD.iterdir()) if p.is_file()],retained_monitor=[pin(p) for p in sorted((OLD/'monitor').iterdir())],retained_operation=[pin(p) for p in sorted(OO.iterdir())],actual_failure_and_diagnostics=[pin(R/n) for n in extra_names])
assert len(groups['ri222_seal'])==16 and len(groups['retained_monitor'])==4 and len(groups['retained_operation'])==4
files={}
for rr in groups.values():
 for r in rr:
  assert r['path'] not in files or files[r['path']]==r
  files[r['path']]=r
assert not set(files)&{r['path'] for r in base['files']}
provenance=dict(schema='ri226-read-only-recovery-provenance-v1',status='SOURCE_ONLY_NOT_ADMISSION',roles=roles,groups=groups,files=[files[k] for k in sorted(files)],base_input_manifest=pin(OW/'INPUT_PINS.json'),base_inputs=806,prior_role_count=810,original_operation_status='REFUSED_RETAIN_ALL_PARTIALS',original_source_readiness_superseded=True,qualification_credit=0,scientific_execution=False)
emit('INPUT_PINS.json',(OW/'INPUT_PINS.json').read_bytes());repair_ref=emit('REPAIR_PROVENANCE.json',body(provenance))
old=(OW/'install_freeze.py').read_text();s=old
s=s.replace('"""UNEXECUTED RI209 proposal: one root-admitted byte installation, no subject load.','"""UNEXECUTED RI226 proposal: one root-admitted READ-ONLY reconciliation, no E write.')
s=s.replace('ri222-freeze-cwd-repair-ypiy2jqw','ri226-directory-custody-recovery-yvfg_p1b').replace('ri222-freeze-install-operation-ypiy2jqw','ri226-freeze-reconciliation-operation-yvfg_p1b')
s=s.replace(next(x for x in s.splitlines() if x.startswith('REPAIR=')),'REPAIR='+repr(repair_ref))
s=s.replace("OUT=B/'ri226-freeze-reconciliation-operation-yvfg_p1b'","OUT=B/'ri226-freeze-reconciliation-operation-yvfg_p1b'\nOLD_OUT=B/'ri222-freeze-install-operation-ypiy2jqw'")
s=s.replace(" need(type(data) is bytes and len(data)<=CAP,'bounded output');fd=None;first=None;secondary=[]"," need(Path(path).parent==OUT,'only fresh external output writes');need(type(data) is bytes and len(data)<=CAP,'bounded output');fd=None;first=None;secondary=[]")
lo=s.index('def difference(');hi=s.index('\ndef main():',lo)
s=s[:lo]+'''def retained_failure(repair):
 # All operands are closed, exact-pinned ADMINISTRATIVE saved records. No
 # scientific body is decoded. Genuine tool origin remains root's premise.
 refs=repair['roles'];old_before=load(refs['original_before']);old_obs=load(refs['original_observations']);c=load(refs['original_complete']);post=load(refs['postflight']);sup=load(refs['supersession'])
 keys(old_before,'E source_states source_observations bindings','original before')
 keys(old_obs,'E_after binding_actual installation_write sources_actual supplier_actual','original partial observations')
 keys(c,'schema status admission candidate destination first_error independent_tails produced_outputs elapsed_seconds_before_complete_write timing complete_not_self_hashed scientific_execution mode_admission_issued ret_paused','original refused receipt')
 expected_error=dict(type='ValueError',message='RI209: root device inode mode links',secondary=[])
 same([c['schema'],c['status'],c['candidate'],c['destination'],c['first_error'],c['complete_not_self_hashed'],c['scientific_execution'],c['mode_admission_issued'],c['ret_paused']],['ri213-installation-completion-v1','REFUSED_RETAIN_ALL_PARTIALS',CANDIDATE,str(DEST),expected_error,True,False,False,True],'preserved actual original refusal')
 same(sup['status'],'OPERATIONAL_READINESS_SUPERSEDED_AFTER_ACTUAL_POSTWRITE_REFUSAL','old readiness superseded')
 same(post['status'],'REFUSAL_AND_RETAINED_PARTIALS_CONFIRMED_NOT_INSTALLATION_ACCEPTANCE','postflight narrow scope')
 same(post['first_error'],expected_error,'postflight original error');same(post['failed_tails'],['E_and_frozen','final_E'],'two exact failed tails');same(post['passed_tail_count'],6,'six original successful tails')
 same(old_obs['installation_write'],dict(error=None,cleanup_errors=[]),'original write and closes completed')
 names=['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json']
 same(sorted(p.name for p in OLD_OUT.iterdir()),names,'retained original four-file namespace')
 for n in names:
  r=m.identity(OLD_OUT/n);need(r['symlink_chain']==[] and r['resolved_path']==str(OLD_OUT/n) and stat.S_ISREG(r['state'][2]) and r['state'][3]==1 and r['bytes']<=CAP,'original regular single-link output')
 pins={n:m.ref(OLD_OUT/n) for n in names if n!='COMPLETE.json'};same(c['produced_outputs'],pins,'original three produced files');same(post['operation_files'],[m.ref(OLD_OUT/n) for n in names],'entire pinned original operation')
 same(c['admission'],{k:old_before['bindings']['admission'][k] for k in ('path','bytes','sha256')},'original admission pin')
 at=load(refs['original_attempt']);same(at,dict(schema='ri209-exclusive-install-attempt-v1',admission=c['admission'],candidate=CANDIDATE,destination=str(DEST),no_retry=True,scientific_execution=False),'original complete attempt')
 old_sources=load(refs['original_sources']);same(len(old_sources),904,'original source count');same(old_before['source_observations'],old_sources,'original complete source baseline');same(old_obs['sources_actual'],old_sources,'original full source tail');same(old_obs['binding_actual'],old_before['bindings'],'original full binding tail')
 t=c['independent_tails'];keys(t,'source_inputs root_bindings supplier E_and_frozen save_observations ordinary_outputs final_E output_namespace','all eight original tails')
 values=dict(source_inputs=old_sources,root_bindings=old_before['bindings'],supplier=old_obs['supplier_actual'],save_observations=pins['OBSERVATIONS.json'],ordinary_outputs=pins,output_namespace=[m.identity(OLD_OUT/n) for n in sorted(pins)])
 for name in ('E_and_frozen','final_E'):same(t[name],dict(value=None,error=expected_error),'exact failed original tail '+name)
 for name,value in values.items():same(t[name],dict(value=value,error=None),'whole successful original tail '+name)
 for r in old_sources:same(m.identity(r['path']),r,'retained original source selection')
 for r in old_before['bindings'].values():same(m.identity(r['path']),r,'retained original binding selection')
 timing=c['timing'];keys(timing,'initial final elapsed','original timing')
 for row in timing.values():keys(row,'value error','original clock record');need(row['error'] is None and type(row['value']) in (int,float) and float('-inf')<row['value']<float('inf'),'original finite successful clocks')
 same(timing['elapsed']['value'],c['elapsed_seconds_before_complete_write'],'original elapsed binding');same(timing['final']['value']-timing['initial']['value'],timing['elapsed']['value'],'original elapsed arithmetic');need(0<=timing['elapsed']['value']<=180,'original inner bound')
 old={r['relative']:r for r in old_before['E']};after=old_obs['E_after'];new={r['relative']:r for r in after}
 need(len(old)==57 and len(new)==58 and len(old_before['E'])==57 and len(after)==58 and set(new)==set(old)|{'AUTHORIZED_FREEZE.json'},'exact original sole addition')
 same(old['.'],post['root_before'],'pinned original root');same({k:new['.'][k] for k in ('state','entries')},post['root_after'],'pinned retained root')
 same(new['.']['kind'],'directory','root kind');same(new['.']['state'][:3],old['.']['state'][:3],'root device inode mode retained');same([old['.']['state'][3],new['.']['state'][3]],[23,24],'exact recorded host-specific link transition')
 same(new['.']['entries'],sorted(old['.']['entries']+['AUTHORIZED_FREEZE.json']),'only exact root member addition')
 for name,row in old.items():
  if name!='.':same(new[name],row,'all prior member states unchanged '+name)
 for row in after:
  if row['kind']=='file':need(stat.S_ISREG(row['identity']['state'][2]) and row['identity']['state'][3]==1 and row['identity']['symlink_chain']==[],'all retained files regular single-link')
 same(new['AUTHORIZED_FREEZE.json']['identity'],post['installed_partial'],'whole retained freeze selection');same(m.pure(post['installed_partial']),m.pure(CANDIDATE),'retained candidate exact pin')
 need(sum(r['kind']=='file' for r in after)==49 and sum(r['kind']=='directory' for r in after)==9,'retained exact file/directory counts')
 # There is no general nlink law: the pinned AFTER state is now immutable.
 return dict(E=after,source_states=old_before['source_states'],original_complete=refs['original_complete'],postflight=refs['postflight'],original_status=c['status'])

''' +s[hi:]
s=s.replace('ADMIT_INSTALL.json','ADMIT_RECONCILE.json').replace('INSTALL_BOOTSTRAP.py','RECONCILE_BOOTSTRAP.py')
s=s.replace("'ri209-root-freeze-installation-admission-v1','AUTHORIZE_ONE_EXACT_FREEZE_INSTALLATION'","'ri226-root-read-only-reconciliation-admission-v1','AUTHORIZE_ONE_READ_ONLY_RECONCILIATION'")
s=s.replace("'ri209-proposal-source-pins-v1'","'ri226-proposal-source-pins-v1'").replace("'check_installation.py','install_freeze.py'","'check_reconciliation.py','reconcile_freeze.py'")
s=s.replace("'ACCEPT_RI209_INSTALLATION_SOURCE_ONLY'","'ACCEPT_RI226_READ_ONLY_RECONCILIATION_SOURCE_ONLY'")
s=s.replace(" inputs=load(INPUT);repair=load(REPAIR);g=", " inputs=load(INPUT);repair=load(REPAIR);retained=retained_failure(repair);same(review['retained_failure'],retained['original_complete'],'root acknowledges actual failure');same(review['retained_postflight'],retained['postflight'],'root acknowledges retained custody');g=")
s=s.replace("'ri209-root-installation-preflight-v1','FRESH_EXACT_INSTALLATION_PREFLIGHT'","'ri226-root-reconciliation-preflight-v1','FRESH_EXACT_READ_ONLY_RECONCILIATION_PREFLIGHT'")
s=s.replace("before=tree();same(before,load(pre['E_before']),'fresh whole E before');same(before,sorted(load(inputs['roles']['historical_E']),key=lambda r:r['relative']),'unchanged accepted E baseline');need(len(before)==57 and not os.path.lexists(DEST),'absent destination and complete57 E');selection=source_states(g)","before=tree();same(before,load(pre['E_before']),'fresh whole E before');same(before,retained['E'],'entire retained postwrite E unchanged');need(len(before)==58,'complete58 retained E');selection=source_states(g);same(selection,retained['source_states'],'whole original48/124/30 retained');same(m.pure(m.identity(DEST)),m.pure(CANDIDATE),'existing candidate pin');need(DEST.read_bytes()==candidate,'complete existing candidate byte equality')")
s=s.replace("start=None;finish=None;elapsed=None;first=None;tails={};produced={};install=None","start=None;finish=None;elapsed=None;first=None;tails={};produced={};install=m.identity(DEST)")
s=s.replace("dict(schema='ri209-exclusive-install-attempt-v1',admission=a_ref,candidate=CANDIDATE,destination=str(DEST),no_retry=True,scientific_execution=False)","dict(schema='ri226-exclusive-read-only-reconciliation-attempt-v1',admission=a_ref,candidate=CANDIDATE,destination=str(DEST),original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True,no_retry=True,scientific_execution=False)")
lo=s.index('  # E root is pinned through');hi=s.index('\n except BaseException as exc:remember(exc)',lo)
s=s[:lo]+"  # No E mutation exists. Byte readback does not decode the candidate.\n  same(m.identity(DEST),install,'existing freeze complete selection');need(DEST.read_bytes()==candidate,'exact retained candidate bytes');same(m.identity(DEST),install,'existing freeze selection after read')\n  observations['read_only_reconciliation']=dict(original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True)"+s[hi:]
s=s.replace("after=tree();observations['E_after']=after;difference(before,after);","after=tree();observations['E_after']=after;same(after,before,'whole read-only E unchanged');")
s=s.replace("rows=tree();difference(before,rows);","rows=tree();same(rows,before,'whole final read-only E unchanged');")
s=s.replace("'installation soft wall exceeded'","'reconciliation soft wall exceeded'")
s=s.replace("schema='ri213-installation-completion-v1',status='INSTALLED_PENDING_INDEPENDENT_ROOT_REVIEW'","schema='ri226-read-only-reconciliation-completion-v1',status='RECONCILED_PENDING_INDEPENDENT_ROOT_REVIEW'")
s=s.replace("admission=a_ref,candidate=CANDIDATE,destination=str(DEST),first_error=first","admission=a_ref,candidate=CANDIDATE,destination=str(DEST),original_complete=retained['original_complete'],original_status=retained['original_status'],postflight=retained['postflight'],E_read_only=True,first_error=first")
assert 'difference(' not in s and 'os.open(E,' not in s and "dir_fd=" not in s and "os.open('AUTHORIZED_FREEZE.json'" not in s
s=s.replace("same(values,source_expected,'all source/input selection unchanged');return values","same(values,source_expected,'all source/input selection unchanged');observations['retained_failure_after']=retained_failure(repair);same(observations['retained_failure_after'],retained,'whole original failure custody retained');return values")
s=s.replace("same(g['prospective_root'],str(E),'fixed graph root');","same(sorted(load(inputs['roles']['historical_E']),key=lambda r:r['relative']),load(repair['roles']['original_before'])['E'],'complete original accepted E baseline');same(g['prospective_root'],str(E),'fixed graph root');")
emit('reconcile_freeze.py',s.encode())
# Save full exact textual delta; it is not a partial projection claim.
emit('RECONCILER_DIFF.patch',''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile=str(OW/'install_freeze.py'),tofile=str(W/'reconcile_freeze.py'))).encode())
emit('BUILD_METADATA.json',body(dict(schema='ri226-administrative-source-builder-v1',base_files=806,repair_files=len(files),base_plus_repair=len(files)+806,prospective_source_count=len(files)+814,groups={k:len(v) for k,v in groups.items()},original_installer=pin(OW/'install_freeze.py'),new_reconciler=pin(W/'reconcile_freeze.py'),subject_imported=False,subject_executed=False,scientific_body_decoded=False)))
print(json.dumps(dict(repair=repair_ref,reconciler=pin(W/'reconcile_freeze.py'),counts=dict(base=806,repair=len(files),inputs=806+len(files),prospective=814+len(files)))))
