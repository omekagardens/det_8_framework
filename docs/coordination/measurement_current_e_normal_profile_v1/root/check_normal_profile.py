"""Independent root saved-evidence arithmetic and opaque identity check only."""
import importlib.util, os, stat, hashlib
from pathlib import Path
hp=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py');hb=hp.read_bytes()
assert len(hb)==3144 and hashlib.sha256(hb).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
cardpath=m.B/'ri170-current-e-root-records-proposed-gikj2giy/ADMIT_PROFILE_NORMAL.json'
card=m.load(cardpath);out=Path(card['output']);layout=m.load(m.D/'PROFILE_NORMAL_PREFLIGHT_OBSERVATION.json')
def tree(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  row=dict(relative=p.relative_to(root).as_posix()); st=p.lstat()
  if stat.S_ISLNK(st.st_mode):row.update(kind='symlink',target=os.readlink(p))
  elif stat.S_ISDIR(st.st_mode):row['kind']='directory'
  else:assert stat.S_ISREG(st.st_mode); row.update(kind='file',**m.pure(m.ref(p)))
  rows.append(row)
 return rows
before=layout;after=[m.identity(r['path']) for r in before['sources']];assert after==before['sources']
post=m.load(m.D/'PROFILE_NORMAL_POST_CUSTODY.json');assert post['observation']==before and post['admission_and_source_review_unchanged'] is True
for key in ['admission','source_review','preflight']:
 row=m.load(m.D/'PROFILE_NORMAL_ADMISSION_CUSTODY.json')[key];assert m.identity(row['path'])==row
for row in before['copies']+before['vendor']+before['tools']:assert m.identity(row['path'])==row
genuine=dict(initial=m.load(m.D/'GENUINE_PROFILE_NORMAL_INITIAL.json'),terminal=m.load(m.D/'GENUINE_PROFILE_NORMAL_COMPLETE.json'),dispatch=m.load(m.D/'PROFILE_NORMAL_DISPATCH.json'));assert genuine['initial']['session_id']==63779 and genuine['initial']['chunk_id']=='2b5d3e' and genuine['terminal']['chunk_id']=='9aba56' and genuine['terminal']['exit_code']==0
assert genuine['initial']['output']==genuine['terminal']['output']==''
complete=m.load(out/'COMPLETE.json');card=m.load(cardpath)
assert set(complete)=={'schema','phase','status','command','environment','admission','sources','artifacts','first_error','independent_tail_errors','elapsed_seconds','scientific_targets_executed','actual_data_admitted','full32_qualified','ret_paused','runtime_acceptance_created','genuine_outer_created'}
assert set(complete['artifacts'])=={'PRE','PRE_completion','POST','POST_completion','PROFILE','PROFILE_completion','checks','namespace'}
assert complete['command']==genuine['dispatch']['outer_argv'][-6:]
assert card['environment_root']==before['E']
assert all(not list((Path(before['E'])/n).iterdir()) for n in ('tmp','runs/normal','runs/optimized'))
assert complete['status']=='CAPTURED_FOR_INDEPENDENT_REVIEW' and complete['first_error'] is None and complete['independent_tail_errors']==[]
assert complete['sources']==card['sources'] and complete['admission']==m.ref(cardpath)
assert complete['environment']==layout['environment'] and complete['phase']=='profile_normal'
assert complete['ret_paused'] is True and all(complete[k] is False for k in ['scientific_targets_executed','actual_data_admitted','full32_qualified','runtime_acceptance_created','genuine_outer_created'])
assert 0<complete['elapsed_seconds']<900
assert all(card[k] is None for k in ['normal_acceptance','profiles_acceptance','guard_admission'])
for row in complete['artifacts'].values():m.verify(row['path'],row)
namespace=m.load(out/'NAMESPACE.json');assert namespace['excluded_not_yet_written']==['NAMESPACE.json','COMPLETE.json']
expected=namespace['entries']+[dict(relative=n,kind='file',**m.pure(m.ref(out/n))) for n in ['NAMESPACE.json','COMPLETE.json']]
assert tree(out)==sorted(expected,key=lambda r:r['relative']) and len(expected)==16
checks=m.load(out/'CHECKS.json');assert set(checks)=={'post_metadata','source_and_admission_postcheck','profile'} and checks['post_metadata']==checks['source_and_admission_postcheck']=='PASS'
summaries=[]
for label in ['PRE','PROFILE','POST']:
 child=m.load(out/(label+'.COMPLETION.json'));attempt=m.load(out/(label+'.ATTEMPT.json'))
 assert child['passed'] and child['child_exit_code']==0 and child['first_error'] is None and child['stop_reason'] is None and child['tail_errors']==[]
 limit=30 if label=='PROFILE' else 180
 assert child['wall_seconds']==attempt['wall_seconds']==limit and 0<child['elapsed_seconds']<=limit
 expected_command=([str(m.B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python'),'-I','-B',str(m.B/'ri130-white-qualification-caller-source-Q4Aq7hZg/profile_observe.source-only.py')] if label=='PROFILE' else [layout['selected_interpreter_binding']['path'],'-I','-B',str(m.B/'ri141-white-bootstrap-source-h58ls076/prepare.py'),'--snapshot',str(cardpath)])
 assert child['command']==attempt['command']==expected_command
 assert child['environment']==attempt['environment']==layout['environment'] and attempt['scientific_target_entry'] is False and type(attempt['pid_owner']) is int and attempt['pid_owner']>0
 assert len(child['samples'])==len(child['monitor_attempts'])>0
 previous=0
 for sample,raw in zip(child['samples'],child['monitor_attempts']):
  assert raw['returncode']==0 and raw['stderr']=='' and raw['stdout'].strip().isdigit()
  assert sample['rss_kib']==int(raw['stdout']) and sample['elapsed_seconds']==raw['elapsed_seconds']
  assert 0<=sample['rss_kib']<=524288 and 0<=sample['gap_seconds']<=.1
  assert abs(sample['elapsed_seconds']-previous-sample['gap_seconds'])<1e-9
  previous=sample['elapsed_seconds']
 assert child['peak_sampled_rss_kib']==max(x['rss_kib'] for x in child['samples'])
 assert abs(child['elapsed_seconds']-previous-child['final_sample_to_reap_gap_seconds'])<1e-9
 assert child['final_sample_gap_passed'] and 0<=child['final_sample_to_reap_gap_seconds']<=.1
 for stream in ['stdout','stderr']:m.verify(child[stream]['path'],child[stream]);assert child[stream]['bytes']<=67108864
 assert child['stderr']['bytes']==0
 summaries.append(dict(label=label,samples=len(child['samples']),elapsed=child['elapsed_seconds'],peak_rss_kib=child['peak_sampled_rss_kib'],maximum_gap=max(x['gap_seconds'] for x in child['samples']),final_gap=child['final_sample_to_reap_gap_seconds']))
baseline=m.load(card['baseline_acceptance']['path']);m.verify(card['baseline_acceptance']['path'],card['baseline_acceptance']);base=m.load(baseline['completions']['capture']['path'])
assert (out/'PRE.stdout').read_bytes()==(out/'POST.stdout').read_bytes()==Path(base['artifacts']['POST']['path']).read_bytes()
snap=m.load(out/'PRE.stdout');deps=m.load(m.B/'ri141-white-bootstrap-source-h58ls076/DEPENDENCIES.source-only.json')
assert snap['runtime_inventory']==m.load(deps['historical_runtime']['path'])
assert snap['interpreter']==m.load(deps['historical_interpreter']['path'])
assert snap['optional_namespaces']['directories']==m.load(deps['historical_optional_namespaces']['path'])['directories']
assert snap['sources']['opaque_files']==deps['opaque_files'] and snap['sources']['packet_namespace']==deps['packet_namespace']
assert snap['host_bootstrap']['bootstrap']['named']==card['bootstrap']
assert dict(uname=snap['host_bootstrap']['uname'],system_version=snap['host_bootstrap']['system_version'])==card['host']
assert snap['scientific_execution'] is False and snap['actual_data_admission'] is False
runtime=snap['runtime_inventory'];selections={r['path']:r for r in snap['selection']['files']};runtime_rows=[]
for r in runtime['files']:
 fresh=m.verify(r['path'],r);runtime_rows.append(fresh);sel=selections[r['path']];st=fresh['state']
 for k,v in zip(['device','inode','mode','nlink','bytes','mtime_ns','ctime_ns'],st):
  if k!='nlink':assert sel[k]==v
 if Path(r['path']).suffix=='.pyc':
  with open(r['path'],'rb') as f:assert f.read(16).hex()==sel['pyc_first16_hex']
  assert sel['pyc_payload_not_parsed_or_executed'] is True
assert len(selections)==len(runtime_rows)
for p in runtime['absent_paths']+snap['preobserved_dyld_routes']['absent_paths']:assert not os.path.lexists(p)
for row in runtime['symlinks']+snap['preobserved_dyld_routes']['symlinks']:assert os.readlink(row['path'])==row['target']
for row in runtime['loader_bindings']+[snap['interpreter']]:
 fresh=m.identity(row['named_path']);assert fresh['resolved_path']==row['resolved_path'] and fresh['symlink_chain']==row['symlink_chain'] and m.pure(fresh)==row['target']

report=m.load(out/'PROFILE.stdout');pc=checks['profile']
assert set(report)=={'schema','profile_before','profile_after','uname','startup','decimal','hashlib','modules','scientific_targets_imported_or_executed','boundary'}
assert report['schema']=='ri121-installed-runtime-profile-observation-v1' and report['scientific_targets_imported_or_executed'] is False
assert report['boundary']=='Installed-runtime observation under pinned supplier, cache-selection and host premises; no scientific qualification.'
venv=str(m.B/'ri73-recovery/recovery-20260924T212511Z-2403d37c/env')
stdlib='/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/lib/python3.11'
baseprefix='/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11'
expected_profile=dict(version='3.11.6 (main, Nov  2 2023, 04:39:43) [Clang 14.0.3 (clang-1403.0.22.14.1)]',implementation='cpython',version_info=[3,11,6,'final',0],executable=venv+'/bin/python',prefix=venv,exec_prefix=venv,base_prefix=baseprefix,base_exec_prefix=baseprefix,path=[str(Path(stdlib).parent/'python311.zip'),stdlib,stdlib+'/lib-dynload',venv+'/lib/python3.11/site-packages'],byteorder='little',isolated=1,dont_write_bytecode=1,optimize=0)
assert report['profile_before']==report['profile_after']==pc['expected_runtime']==expected_profile
assert report['uname']==snap['host_bootstrap']['uname']
assert report['startup']==dict(enable_user_site=False,site_prefixes=[venv],distutils_hook_loaded=True,sitecustomize_loaded=True,usercustomize_loaded=False)
d=report['decimal'];assert set(d)=={'extension_loaded','fallback_loaded','decimal_class_is_fallback','extension_import_error','fraction_class_module'}
assert d['extension_loaded'] is False and d['fallback_loaded'] is True and d['decimal_class_is_fallback'] is True and d['fraction_class_module']=='fractions'
assert set(d['extension_import_error'])=={'type','message'} and d['extension_import_error']['type']=='ImportError'
# Full-match the complete dyld message; repeated attempts retained in order.
import re
extension=stdlib+'/lib-dynload/_decimal.cpython-311-darwin.so'
header='dlopen('+extension+', 0x0002): Library not loaded: /opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib\n'
msg=d['extension_import_error']['message'];assert msg.startswith(header)
pat=r'  Referenced from: <[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}> '+re.escape(extension)+r'\n  Reason: tried: (.+)'
mt=re.fullmatch(pat,msg[len(header):]);assert mt is not None
attempts=[]
tail=mt.group(1)
while tail:
 hit=re.match(r"'(/[^'\n]+)' \((no such file(?:, not in dyld cache)?)\)",tail);assert hit
 path,reason=hit.groups();assert str(Path(path))==path and '..' not in Path(path).parts and path in snap['preobserved_dyld_routes']['absent_paths']
 attempts.append(dict(path=path,reason=reason));tail=tail[hit.end():]
 if tail:assert tail.startswith(', ') and len(tail)>2;tail=tail[2:]
assert len(attempts)==10 and attempts==pc['ordered_actual_dyld_attempts']
h=report['hashlib'];assert set(h)=={'sha256_empty','openssl_sha256_empty','available_openssl_names'}
assert h['sha256_empty']==h['openssl_sha256_empty']=='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
assert h['available_openssl_names']==sorted(set(h['available_openssl_names'])) and all(type(x)is str for x in h['available_openssl_names'])
files={r['path']:r for r in runtime['files']};descriptors=[]
assert '__main__' in report['modules'] and not {'white_kernel','white_path','white_controls','white_fixtures','kernel_controls','white_validator','validator_controls','qualify_white_only'} & set(report['modules'])
for name,row in sorted(report['modules'].items()):
 assert set(row)=={'file','cached','origin','loader_type'} and type(row['loader_type'])is str
 for field in ('file','cached','origin'):
  path=row[field];r=dict(module=name,field=field)
  if path in (None,'built-in','frozen'):r['value']=path
  elif name=='__main__':
   assert field=='file' and path==str(m.B/'ri130-white-qualification-caller-source-Q4Aq7hZg/profile_observe.source-only.py');r['identity']=m.ref(path)
  else:
   p=Path(path);assert p.is_absolute()
   if not p.exists():
    assert field=='cached' and not p.is_symlink() and path not in files and any(path.startswith(root+'/')for root in runtime['roots']) and p.resolve()==p
    r.update(path=path,absent_from_complete_inventory=True)
   else:
    resolved=str(p.resolve(strict=True));assert resolved in files
    fresh=m.verify(resolved,files[resolved]);binding=m.identity(p)
    r['binding']=dict(named_path=path,resolved_path=binding['resolved_path'],symlink_chain=binding['symlink_chain'],target=m.pure(binding))
  descriptors.append(r)
expected_pc=dict(status='SAVED_PROFILE_FIELDS_RECONCILED_NOT_RUNTIME_ACCEPTANCE',expected_runtime=expected_profile,all_descriptors=descriptors,ordered_actual_dyld_attempts=attempts,full_dyld_error=d['extension_import_error'],preobserved_domain=snap['preobserved_dyld_routes'],hash_algorithm_names=h['available_openssl_names'],supplier_cache_and_stable_host_premises_retained=True,full_import_trace_claim=False,scientific_qualification=False)
assert pc==expected_pc and len(descriptors)==213

print(m.save('RUNTIME_POST_IDENTITIES.json',dict(identities=runtime_rows,scientific_body_decode=False,subject_execution=False)))
print(m.save('OPERATION_FINAL_IDENTITIES.json',dict(root=str(out),entries=tree(out),identities=[m.identity(p) for p in sorted(out.rglob('*')) if p.is_file()])))
outer=dict(schema='ri133-root-genuine-outer-v1',status='ACTUAL_TOOL_COMPLETION',command=complete['command'],environment=layout['environment'],exit_code=0,completion=m.ref(out/'COMPLETE.json'),raw_tool_receipt=m.ref(m.D/'GENUINE_PROFILE_NORMAL_COMPLETE.json'),external_timeout_seconds=960)
print(m.save('GENUINE_OUTER.json',outer))
print(m.save('ROOT_PROFILE_NORMAL_CHECK.json',dict(schema='ri188-root-saved-current-e-normal-profile-check-v1',status='PASS_PENDING_INDEPENDENT_REVIEW',source_files=len(after),runtime_files=len(runtime_rows),runtime_bytes=sum(x['bytes'] for x in runtime_rows),snapshots=m.ref(out/'PRE.stdout'),snapshots_byte_equal=True,monitors=summaries,parent_seconds=complete['elapsed_seconds'],output_entries=len(expected),operation_entries=len(tree(out)),source_admission_and_vendor_unchanged=True,profile_modules=len(report['modules']),profile_descriptors=len(descriptors),ordered_dyld_attempts=len(attempts),scientific_credit=False,scope='Saved complete snapshot comparison, every runtime file fresh opaque identity/selection, actual monitor arithmetic, full output namespace; independent actual review remains separate')))
