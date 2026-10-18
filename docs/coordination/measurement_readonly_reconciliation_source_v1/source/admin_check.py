"""Metadata and literal source checks ONLY. No subject/helper import/AST/compile/run.
Opens declared source/history bodies only as opaque bytes; decodes only named
administrative manifests and saved custody records. Does not inventory runtime/E.
"""
from pathlib import Path
import json,hashlib,re,difflib,stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence');W=B/'ri226-directory-custody-recovery-yvfg_p1b/worker_proposal';OW=B/'ri222-freeze-cwd-repair-ypiy2jqw/worker_proposal';O=B/'ri222-freeze-install-operation-ypiy2jqw';R=B/'ri224-root-cwd-review-nyvru347'
checks=[];seen={}
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def verify(ok,label):
 checks.append(label)
 if not ok:raise ValueError(label)
def eq(a,b,label):verify(canonical(a)==canonical(b),label)
def pin(p):
 p=Path(p);before=p.stat();data=p.read_bytes();after=p.stat();verify(before==after,'opaque read stable '+str(p));v=dict(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest());seen[str(p)]=v;return v
def checkpin(r):eq(pin(r['path']),{k:r[k] for k in ('path','bytes','sha256')},'full opaque pin '+r['path'])
def load(p):return json.loads(Path(p).read_bytes())
def span(s,name):
 match=re.search(r'^def '+re.escape(name)+r'\(',s,re.M);verify(match is not None,'function present '+name);start=match.start();nxt=re.search(r'^def |^if __name__',s[match.end():],re.M);return s[start:match.end()+nxt.start() if nxt else len(s)].rstrip()
base=load(W/'INPUT_PINS.json');repair=load(W/'REPAIR_PROVENANCE.json');manifest=load(W/'SOURCE_PINS.json')
eq((W/'INPUT_PINS.json').read_text(),(OW/'INPUT_PINS.json').read_text(),'original base byte text unchanged');eq([len(base['files']),len(repair['files']),base['prior_role_count']],[806,157,810],'closure declared sizes')
allrefs={}
for row in base['files']+repair['files']+manifest['files']:
 verify(row['path'] not in allrefs or allrefs[row['path']]==row,'compatible duplicate');allrefs[row['path']]=row
for row in allrefs.values():checkpin(row)
eq(len(allrefs),968,'all current963inputs plus5payloads');eq(len(allrefs)+3,971,'future manifest review bootstrap union')
for row in repair['roles'].values():checkpin(row)
# Sets are compared directly for membership; canonical JSON only handles JSON values.
verify(set(repair['groups'])=={'inherited_repair','ri222_seal','retained_root_operation','retained_monitor','retained_operation','actual_failure_and_diagnostics'},'explicit exact group names')
grouprefs={r['path']:r for rows in repair['groups'].values() for r in rows};eq([grouprefs[k] for k in sorted(grouprefs)],repair['files'],'complete group union');eq([len(repair['groups'][k]) for k in ['inherited_repair','ri222_seal','retained_root_operation','retained_monitor','retained_operation','actual_failure_and_diagnostics']],[90,16,12,4,4,31],'group counts')
old_sources=load(repair['roles']['original_sources']['path']);verify(len(old_sources)==904,'old source rows904');verify(all(r['path'] in allrefs for r in old_sources),'all904 original source paths retained')
for row in old_sources:eq({k:row[k] for k in ('path','bytes','sha256')},allrefs[row['path']],'old source pin retained')
original=load(O/'BEFORE.json');obs=load(O/'OBSERVATIONS.json');complete=load(O/'COMPLETE.json');post=load(R/'POST_FAILURE_CUSTODY.json')
eq(sorted(p.name for p in O.iterdir()),['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json'],'actual original four-file namespace');eq(post['operation_files'],[pin(O/n) for n in ['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json']],'recorded operation order and pins')
eq(complete['status'],'REFUSED_RETAIN_ALL_PARTIALS','original refused');eq(complete['first_error'],dict(type='ValueError',message='RI209: root device inode mode links',secondary=[]),'original error');eq([n for n,t in complete['independent_tails'].items() if t['error'] is not None],['E_and_frozen','final_E'],'two failures')
eq(obs['sources_actual'],old_sources,'all old saved source observations');eq(original['source_observations'],old_sources,'old saved preselection');eq(obs['binding_actual'],original['bindings'],'old saved bindings');eq(obs['installation_write'],dict(error=None,cleanup_errors=[]),'old write/close observed')
old={r['relative']:r for r in original['E']};new={r['relative']:r for r in obs['E_after']};verify(len(old)==57 and len(new)==58 and set(new)==set(old)|{'AUTHORIZED_FREEZE.json'},'saved sole addition');eq(old['.'],post['root_before'],'whole saved before root');eq({k:new['.'][k] for k in ['state','entries']},post['root_after'],'whole saved after root');eq(old['.']['state'][:3],new['.']['state'][:3],'recorded stable dev ino mode');eq([old['.']['state'][3],new['.']['state'][3]],[23,24],'recorded links transition');eq(new['.']['entries'],sorted(old['.']['entries']+['AUTHORIZED_FREEZE.json']),'exact saved membership addition')
for n,row in old.items():
 if n!='.':eq(new[n],row,'saved whole old member '+n)
for row in new.values():
 if row['kind']=='file':verify(stat.S_ISREG(row['identity']['state'][2]) and row['identity']['state'][3]==1,'saved regular single-link '+row['relative'])
eq(new['AUTHORIZED_FREEZE.json']['identity'],post['installed_partial'],'whole saved freeze identity');eq([sum(r['kind']=='file' for r in new.values()),sum(r['kind']=='directory' for r in new.values())],[49,9],'saved domain')
primary=(W/'reconcile_freeze.py').read_text();checker=(W/'check_reconciliation.py').read_text();oldp=(OW/'install_freeze.py').read_text();oldc=(OW/'check_installation.py').read_text()
unchanged=['need','same','keys','st','literal','read','parse','load','error','save','tree','source_states','frozen']
for name in unchanged:eq(span(primary,name),span(oldp,name),'whole retained primary function '+name)
unchanged_checker=['check','eq','fields','load','selection','state','full_tree']
for name in unchanged_checker:eq(span(checker,name),span(oldc,name),'whole retained checker function '+name)
for tag in ['CAP=','LIMITS=','ENV=','VENDOR=']:
 line=next(l for l in oldp.splitlines() if l.startswith(tag));verify(line in primary,'unchanged primary literal '+tag)
for tag in ['LIMITS=','ENV=','VENDOR=']:
 line=next(l for l in oldc.splitlines() if l.startswith(tag));verify(line in checker,'unchanged checker literal '+tag)
verify("Path.cwd()==literal(D/'monitor')" in primary and "eq(dispatch['cwd'],str(D),'outer cwd')" in checker,'exact separate child and outer cwd')
verify("need(Path(path).parent==OUT,'only fresh external output writes')" in primary,'fixed external writer')
for forbidden in ["os.open(E,",'dir_fd=',"os.open('AUTHORIZED_FREEZE.json'",'os.rename(','.unlink(','.replace(','.chmod(', 'subprocess.', 'Popen(']:verify(forbidden not in primary,'no E mutation/child launch primitive '+forbidden)
verify(primary.count('os.open(')==1,'only generic confined writer open');verify(primary.count('OUT.mkdir(')==1,'single fresh output ownership')
for required in ["same(after,before,'whole read-only E unchanged')","same(rows,before,'whole final read-only E unchanged')","same(before,retained['E'],'entire retained postwrite E unchanged')","[23,24]","'original_status'","retained_failure(repair)"]:
 verify(required in primary,'primary exact recovery guard '+required)
for required in ["eq(current,before['E']","eq(current,retained['E']","[23,24]","REFUSED_RETAIN_ALL_PARTIALS","RECONCILED_PENDING_INDEPENDENT_ROOT_REVIEW"]:verify(required in checker,'checker exact recovery guard '+required)
for source in [primary,checker]:verify("state'][:4]" not in source,'incorrect root links equality removed');verify('INSTALLED_PENDING_INDEPENDENT_ROOT_REVIEW' not in source,'no retroactive installation success')
start='  # All eight ordinary tails above were attempted before final timing.';end='  completion=dict('
eq(primary[primary.index(start):primary.index(end)],oldp[oldp.index(start):oldp.index(end)].replace('installation soft wall exceeded','reconciliation soft wall exceeded'),'whole final protected clock span')
start='  # The first fallible post-mkdir operation is protected.';end="  same(m.ref(args.admission),a_ref,'admission after ownership')"
eq(primary[primary.index(start):primary.index(end)],oldp[oldp.index(start):oldp.index(end)],'whole initial clock span')
for old,new,patch in [(oldp,primary,'RECONCILER_DIFF.patch'),(oldc,checker,'CHECKER_DIFF.patch')]:
 original_name='install_freeze.py' if patch.startswith('RECONCILER') else 'check_installation.py';new_name='reconcile_freeze.py' if patch.startswith('RECONCILER') else 'check_reconciliation.py';expected=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(OW/original_name),tofile=str(W/new_name)));eq((W/patch).read_text(),expected,'whole exact source delta '+patch)
# Literal functions are never imported or evaluated. No old/new FROZEN is generated.
result=dict(schema='ri226-nonexecuting-administrative-check-v1',status='PASS_SOURCE_TEXT_AND_SAVED_METADATA_ONLY',checks=len(checks),opaque_files=len(seen),source_inputs=963,prospective_source_count=971,preserved_original_source_paths=904,base_role_count=810,unchanged_primary_function_spans=unchanged,unchanged_checker_function_spans=unchanged_checker,saved_root_before=original['E'][0],saved_root_after=obs['E_after'][0],predicate_labels=checks,opaque_identities=[seen[k] for k in sorted(seen)],no_subject_import_compile_AST_probe_execution=True,no_fixtures_runtime_observation_or_admission=True,no_new_current_E_scan=True,no_scientific_body_decode=True,qualification_credit=0)
with (W/'ADMIN_CHECK.json').open('xb') as f:f.write(canonical(result))
print(json.dumps(dict(report=pin(W/'ADMIN_CHECK.json'),checks=len(checks),status=result['status'])))
