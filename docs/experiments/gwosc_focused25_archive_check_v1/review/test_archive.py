"""Nonauthor administrative utility tests. Never execute archived subjects."""
import hashlib,json,os,shutil,stat,subprocess,time
from pathlib import Path
S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri142-portable-focused25-net0j999')
R=S/'review';A=Path('/Volumes/AI_DATA/development/det_8_framework-ret/docs/experiments/gwosc_focused25_result_v1')
PYTHON='/usr/bin/python3'
def pin(p):
 b=Path(p).read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def inv(root):
 out=[]
 for d,dirs,files in os.walk(root,followlinks=False):
  for name in sorted(dirs+files):
   p=Path(d)/name;s=p.lstat();x={'relative':str(p.relative_to(root))}
   if stat.S_ISDIR(s.st_mode):x['kind']='directory'
   elif stat.S_ISREG(s.st_mode):x.update(kind='file',**{k:v for k,v in pin(p).items() if k!='path'})
   elif stat.S_ISLNK(s.st_mode):x.update(kind='symlink',target=os.readlink(p))
   else:x['kind']='special'
   out.append(x)
 return sorted(out,key=lambda x:x['relative'])
def save(p,v):
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n')
source_before=pin(S/'verify_archive.py');readme_before=pin(S/'README.md');archive_before=inv(A)
assert source_before['sha256']=='660e41bb8615b86145b12f7a161ac532886fb6405949b4197e7f164d48ef798d'
assert sum(x['kind']=='file' for x in archive_before)==135
(R/'fixtures').mkdir();(R/'different-cwd').mkdir();(R/'records').mkdir();(R/'portable').mkdir();(R/'portable/utility').mkdir()
portable=R/'portable/gwosc_focused25_result_v1';shutil.copytree(A,portable)
checker=R/'portable/utility/verify_archive.py';shutil.copy2(S/'verify_archive.py',checker);assert checker.read_bytes()==(S/'verify_archive.py').read_bytes()
# Known archived streams and deliberate partial JSON are read as bytes, never executed or normalized.
byte_specials=[]
for p in sorted(A.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes()
 if len(b)==0 or b in [b'{"CONTROL_PARTIAL_ATTEMPT":',b'{"CONTROL_PARTIAL_COMPLETE":']:
  byte_specials.append({'relative':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'kind':'zero_byte_stream' if not b else 'deliberately_partial_json'})
assert sum(x['kind']=='zero_byte_stream' for x in byte_specials)==2
assert sum(x['kind']=='deliberately_partial_json' for x in byte_specials)==8
results=[]
def execute(name,archive=None,expected_exit=0,error_contains=None,script=checker,extra=None):
 args=[PYTHON,'-I','-B',str(script)]+([] if archive is None else ['--archive',str(archive)])
 began=time.monotonic();p=subprocess.run(args,cwd=R/'different-cwd',capture_output=True,timeout=30,check=False);elapsed=time.monotonic()-began
 stdout=p.stdout.decode();stderr=p.stderr.decode();passed=p.returncode==expected_exit
 body=json.loads(stdout if expected_exit==0 else stderr)
 if expected_exit==0:
  passed=passed and stderr=='' and body=={'status':'PUBLISHED_BYTES_AND_SAVED_AGREEMENT_PASS','published_commit':'878ef6041d937abd4ecdc7b0d4fa9adbc81a5005','archived_files':135,'exact_copies':132,'operation_files':89,'saved_control_outcomes':25,'saved_monitor_samples':30,'historical_empty_directories_required_on_disk':False,'archived_code_executed':False,'external_paths_opened':False,'current_runtime_qualified':False,'historical_tool_origin_independently_authenticated':False,'scientific_claim_established':False}
 else:passed=passed and stdout=='' and body['status']=='REFUSED' and error_contains in body['error']
 result={'case':name,'command':args,'cwd':str(R/'different-cwd'),'timeout_seconds':30,'exit_code':p.returncode,'stdout':stdout,'stderr':stderr,'elapsed_seconds':elapsed,'expected_exit':expected_exit,'expected_refusal_substring':error_contains,'passed':passed,'checker':pin(script),'scope_note':extra}
 save(R/'records'/('case_'+name+'.json'),result);results.append(result);assert passed,result

def fixture(name):
 p=R/'fixtures'/name;shutil.copytree(A,p);return p
execute('01_original_archive',A,script=S/'verify_archive.py',extra='Original public archive, explicit path, unrelated working directory; read only.')
execute('02_relocated_archive',portable,extra='Identical checker and archive both relocated under review reservation; unrelated working directory.')
execute('03_default_layout',extra='Default sibling-archive path works in relocated checkout-like layout; historical empty directories are absent on disk.')
assert not (portable/'operation/environment').exists()
p=fixture('04_missing_payload');(p/'README.md').unlink();execute('04_missing_payload',p,1,'complete archive file inventory differs')
p=fixture('05_same_size_tamper');f=p/'README.md';b=f.read_bytes();f.write_bytes(b'!'+b[1:]);execute('05_same_size_tamper',p,1,'payload bytes differ: README.md')
p=fixture('06_extra_file');(p/'EXTRA.txt').write_text('extra\n');execute('06_extra_file',p,1,'complete archive file inventory differs')
p=fixture('07_extra_empty_directory');(p/'EMPTY_EXTRA').mkdir();execute('07_extra_empty_directory',p,1,'unexpected empty or other directory')
sentinel=R/'fixtures/OUTSIDE_SENTINEL';sentinel.write_text('review-owned symlink target; must not be opened by archive checker\n');sentinel_pin=pin(sentinel)
p=fixture('08_symlink_file');(p/'README.md').unlink();(p/'README.md').symlink_to(sentinel);execute('08_symlink_file',p,1,'nonregular archive member',extra='Static symlink rejected by inventory before payload open; target is reviewer-owned.')
p=fixture('09_symlink_directory');(p/'directory_link').symlink_to(R/'different-cwd',target_is_directory=True);execute('09_symlink_directory',p,1,'nonregular archive directory')
p=R/'fixtures/10_symlink_root';p.symlink_to(portable,target_is_directory=True);execute('10_symlink_root',p,1,'archive root must be a real directory')
p=fixture('11_mutated_manifest');f=p/'PUBLICATION_MANIFEST.json';b=f.read_bytes();assert b.count(b'"exact_copies": 132')==1;f.write_bytes(b.replace(b'"exact_copies": 132',b'"exact_copies": 133'));execute('11_mutated_manifest',p,1,'pinned publication manifest differs',extra='Immutable manifest pin refusal; does not exercise later count parser.')
p=fixture('12_unsafe_manifest_path');f=p/'PUBLICATION_MANIFEST.json';b=f.read_bytes();assert b.count(b'"path": "README.md"')==1;f.write_bytes(b.replace(b'"path": "README.md"',b'"path": "/EADME.md"'));execute('12_unsafe_manifest_path',p,1,'pinned publication manifest differs',extra='Same-length absolute path mutation refuses at immutable manifest hash, not a claimed execution of relative().')
p=fixture('13_nonempty_stream');(p/'operation/output/FOCUSED25.stdout').write_bytes(b'x');execute('13_nonempty_stream',p,1,'nonregular or changed-size file',extra='Baseline preserved both zero-byte streams; added byte rejects before content decoding.')
p=fixture('14_partial_json_repaired');f=p/'operation/output/controls/F01_attempt_partial/owned-output/ATTEMPT.json';assert f.read_bytes()==b'{"CONTROL_PARTIAL_ATTEMPT":';f.write_bytes(b'{"CONTROL_PARTIAL_ATTEMPT": null}\n');execute('14_partial_json_repaired',p,1,'nonregular or changed-size file',extra='Baseline accepts exact deliberately partial receipt bytes; changing them to valid JSON is tampering, not repair.')
p=fixture('15_saved_outcome_tamper');f=p/'operation/output/controls/REPORT.json';b=f.read_bytes();assert b.count(b'"passed": 25')==1;f.write_bytes(b.replace(b'"passed": 25',b'"passed": 24'));execute('15_saved_outcome_tamper',p,1,'payload bytes differ',extra='Outcome tamper detected at payload hash; does not independently qualify deeper saved-outcome branches.')
p=fixture('16_missing_manifest');(p/'PUBLICATION_MANIFEST.json').unlink();execute('16_missing_manifest',p,1,'No such file or directory')
p=R/'fixtures/17_regular_file_root';p.write_text('not an archive');execute('17_regular_file_root',p,1,'archive root must be a real directory')
assert pin(sentinel)==sentinel_pin
assert inv(A)==archive_before and inv(portable)==archive_before
assert pin(S/'verify_archive.py')==source_before and pin(S/'README.md')==readme_before and checker.read_bytes()==(S/'verify_archive.py').read_bytes()
assert not list((R/'portable/utility').glob('__pycache__'))
summary={'schema':'ri142-nonauthor-portable-archive-test-results-v1','source':source_before,'readme':readme_before,'original_archive':str(A),'archive_before_and_after':archive_before,'checker_copy':pin(checker),'result_records':[pin(R/'records'/('case_'+x['case']+'.json')) for x in results],'results':results,'counts':{'total':len(results),'passed':sum(x['passed'] for x in results),'positive':3,'negative':14},'zero_and_partial_bytes':byte_specials,'original_archive_unchanged':True,'source_and_readme_unchanged':True,'portable_copy_unchanged':True,'no_cache_files_created':True,'archived_subjects_executed':False,'current_runtime_inventory':False,'external_dependency_paths_opened_by_checker_source':False,'deep_parser_or_outcome_negative_branches_executed':False,'fixture_trees_external_only':True,'read_only_operational_scope':True}
save(R/'TEST_RESULTS.json',summary)
print(json.dumps({'record':pin(R/'TEST_RESULTS.json'),'counts':summary['counts'],'preserved_zero_streams':2,'preserved_partial_receipts':8,'all_passed':True},indent=2))
