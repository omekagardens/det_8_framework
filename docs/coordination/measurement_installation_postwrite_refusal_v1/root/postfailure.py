"""Record the refused outcome and exact custody; no success acceptance or repair."""
import hashlib,importlib.util,json,os,stat
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri224-root-cwd-review-nyvru347';D=B/'ri222-freeze-cwd-repair-ypiy2jqw';E=B/'ri154-white-execution-proposed-42_uvw15';O=B/'ri222-freeze-install-operation-ypiy2jqw'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
def eq(a,b):assert m.canonical(a)==m.canonical(b)
genuine=m.load('/private/tmp/ri224_actual_installation.json');assert genuine['initial_result']['chunk_id']=='8081b8' and genuine['terminal_result']['chunk_id']=='17185d' and genuine['terminal_result']['exit_code']==1
transcript=m.save('GENUINE_INSTALLATION_TOOL.json',genuine)
host=m.load('/private/tmp/ri224_post_host.json');assert host['result']['exit_code']==0 and host['result']['chunk_id']=='e67a20';host['observation']=json.loads(host['result']['output']);host_ref=m.save('GENUINE_POST_HOST_TOOL.json',host)
eq(host['observation'],m.load(D/'HOST_GENUINE_TOOL.json')['observation'])
source=m.load(D/'SOURCES_BEFORE.json');supplier=m.load(D/'SUPPLIER_BEFORE.json');old=m.load(D/'E_BEFORE.json')
assert len(source)==904 and len(supplier['vendor'])==1810 and len(supplier['tools'])==4 and len(supplier['namespace'])==195 and len(supplier['absent'])==2
for row in source+supplier['vendor']+supplier['tools']:eq(m.identity(row['path']),row)
state=lambda z:[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
for row in supplier['namespace']:
 p=Path(row['path']);eq(state(p.lstat()),row['state'])
 if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'])
 else:eq(os.readlink(p),row['target'])
assert all(not os.path.lexists(p) for p in supplier['absent']);eq(list(os.uname()),supplier['host']['uname'])
assert len(old)==57 and sum(r['kind']=='file' for r in old)==48
root=next(r for r in old if r['relative']=='.');root_after=state(E.lstat())
eq(root_after[:3],root['state'][:3]);eq(sorted(p.name for p in E.iterdir()),sorted(root['entries']+['AUTHORIZED_FREEZE.json']))
assert root['state'][3]==23 and root_after[3]==24
for row in old:
 if row['relative']=='.':continue
 p=E/row['relative'];eq(state(p.lstat()),row['state'])
 if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'])
 else:eq(m.identity(p),row['identity'])
candidate=B/'ri156-operation-ri206-freeze-5e_n5lj_/RESULT.json';expected=dict(bytes=26214,sha256='9e0c0e4953c7213a76fea291d5f799984422de8628f039eac4e0d7b3c5758b14')
m.verify(candidate,expected);installed=m.verify(E/'AUTHORIZED_FREEZE.json',expected);assert (E/'AUTHORIZED_FREEZE.json').read_bytes()==candidate.read_bytes() and installed['state'][3]==1 and installed['symlink_chain']==[]
assert not (E/'ADMIT_NORMAL.json').exists() and not (E/'ADMIT_OPTIMIZED.json').exists()
assert list((D/'tmp').iterdir())==[]
eq(sorted(p.name for p in O.iterdir()),['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json'])
eq(sorted(p.name for p in (D/'monitor').iterdir()),['INSTALL.ATTEMPT.json','INSTALL.COMPLETION.json','INSTALL.stderr','INSTALL.stdout'])
c=m.load(O/'COMPLETE.json');mon=m.load(D/'monitor/INSTALL.COMPLETION.json')
assert c['status']=='REFUSED_RETAIN_ALL_PARTIALS' and c['first_error']['message']=='RI209: root device inode mode links'
assert [k for k,v in c['independent_tails'].items() if v['error'] is not None]==['E_and_frozen','final_E']
assert mon['passed'] is False and mon['child_exit_code']==1 and mon['first_error'] is None and mon['tail_errors']==[] and mon['stop_reason'] is None
assert len(mon['samples'])==42 and mon['peak_sampled_rss_kib']==49040
for row in c['produced_outputs'].values():m.verify(row['path'],row)
for name in ('stdout','stderr'):m.verify(mon[name]['path'],mon[name]);assert mon[name]['bytes']==0
eq(m.snapshot(),m.load(R/'REPO_ENTRY.json'))
report=m.save('POST_FAILURE_CUSTODY.json',dict(schema='ri224-postwrite-refusal-custody-v1',status='REFUSAL_AND_RETAINED_PARTIALS_CONFIRMED_NOT_INSTALLATION_ACCEPTANCE',genuine_tool=transcript,genuine_post_host=host_ref,sources=904,vendor_files=1810,vendor_bytes=48024515,tools=4,namespace_rows=195,absences=2,old_E_files=48,old_E_directories=9,all_prior_E_members_unchanged=True,root_before=root,root_after=dict(state=root_after,entries=sorted(p.name for p in E.iterdir())),installed_partial=installed,candidate=m.ref(candidate),exact_candidate_byte_equality=True,operation_files=[m.ref(p) for p in sorted(O.iterdir())],monitor_files=[m.ref(p) for p in sorted((D/'monitor').iterdir())],first_error=c['first_error'],failed_tails=['E_and_frozen','final_E'],passed_tail_count=6,monitor_summary={k:mon[k] for k in ('child_exit_code','passed','elapsed_seconds','peak_sampled_rss_kib','final_sample_to_reap_gap_seconds','first_error','tail_errors','stop_reason')},samples=42,whole_repository_unchanged=True,no_mode_cards=True,no_retry=True,success_checker_not_run=True,qualification_credit=0,RET_paused=True))
print(json.dumps(dict(report=report,status='PASS_FAILURE_CUSTODY_ONLY',sources=904,old_E_unchanged=48,installed_partial_bytes=26214,root_link_count_transition=[23,24])))
