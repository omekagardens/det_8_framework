"""Independent Homebrew-only opaque/admin checker; subjects remain inert text."""
from pathlib import Path
import hashlib,json,os,re,shlex,stat,sys
D=Path(__file__).resolve().parent;B=D.parent;S=B/'ri165-native-external-supervision-krvtol4v';P=B/'ri163-native-qualification-preflight-fqexul5v';R=B/'ri163-root-preflight-review-u80slv0b'
count=0;observations={};trail=[]
def need(ok,label):
 global count
 count+=1
 if not ok:raise ValueError(label)
def canonical(o):return (json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def equal(a,b,label):need(canonical(a)==canonical(b),label)
def pure(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def observe(path):
 p=Path(path);need(p.is_absolute(),'absolute '+str(p));z=p.lstat();need(stat.S_ISREG(z.st_mode) and not p.is_symlink(),'regular '+str(p))
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 with os.fdopen(fd,'rb') as f:
  equal(state(os.fstat(f.fileno())),state(z),'opened state '+str(p))
  for raw in iter(lambda:f.read(1024*1024),b''):h.update(raw);n+=len(raw)
  equal(state(os.fstat(f.fileno())),state(z),'descriptor stable '+str(p))
 equal(state(p.lstat()),state(z),'named stable '+str(p));need(n==z.st_size,'bytecount '+str(p))
 return {'path':str(p),'bytes':n,'sha256':h.hexdigest(),'resolved':str(p.resolve(strict=True)),'state':state(z)}
def pin(path):
 p=str(path)
 if p not in observations:observations[p]=observe(p)
 return {k:observations[p][k] for k in ('path','bytes','sha256')}
def verify(row,label):
 q={k:row[k] for k in ('path','bytes','sha256')};equal(pin(row['path']),q,label);return q
def read(path):return json.loads(Path(path).read_bytes())
def save(name,value):
 with (D/name).open('xb') as f:f.write(canonical(value));f.flush();os.fsync(f.fileno())
try:
 need(sys.executable.startswith('/opt/homebrew/'),'Homebrew administrative interpreter only')
 verify({'path':str(S/'HANDOFF.json'),'bytes':8490,'sha256':'5ea6624c7aa52e72ab1810a9446f720f849d9b2ebff5bfee338efe313ec4a6da'},'given handoff pin')
 h=read(S/'HANDOFF.json');equal(sorted(p.name for p in S.iterdir()),h['namespace'],'exact subject namespace');need(len(h['namespace'])==16 and len(h['payloads'])==15,'16/15 subject seal')
 equal(sorted(Path(x['path']).name for x in h['payloads']),sorted(set(h['namespace'])-{'HANDOFF.json'}),'complete unique payload domain')
 for row in h['payloads']:verify(row,'sealed payload '+row['path'])
 verify(h['assignment'],'assignment');a=read(h['assignment']['path']);equal(a['reservation'],str(S),'author reservation')
 bindings=read(S/'DEPENDENCY_BINDINGS.json');deps=read(P/'SOURCE_DEPENDENCIES.json');facts=read(S/'AUTHENTICATION_AND_FIXED_FACTS.json');older=read(P/'HANDOFF.json');req=read(P/'REQUEST_PROPOSAL.json');dispatch=read(P/'DISPATCH_PROPOSAL.json');proposal=read(S/'COMMAND_PROPOSAL.json')
 equal(len(deps['protected_files']),307,'307 source dependencies');derived={}
 for role in deps['protected_files']:
  row=verify(role['identity'],'inherited source '+role['identity']['path']);derived[row['path']]=row
 need(len(derived)==307,'307 distinct inherited paths')
 for row in older['payloads']+facts['assignment_and_predecessors']+facts['fixed_files']:
  q=verify(row,'selected predecessor/fixed '+row['path']);derived[q['path']]=q
 row=pin(R/'ROOT_MANUAL_REVIEW.md');derived[row['path']]=row
 equal(len(derived),325,'325 independently reconstructed distinct external identities')
 equal({row['path']:row for row in bindings['files']},derived,'exact external identity set, not count alone')
 need(len(bindings['files'])==325,'no duplicate dependency rows')
 equal(sum(row['identity']['bytes'] for row in deps['protected_files']),33312952,'inherited source bytes')
 for row in bindings['files']:verify(row,'bound external file '+row['path'])
 raw=req['exact_proposed_request_utf8'].encode('utf8');equal(pure(raw),{k:req['prospective_request_identity'][k] for k in ('bytes','sha256')},'exact proposed request raw bytes')
 equal(len(raw),2304,'request2304');equal(json.loads(raw),req['proposed_request'],'request is administrative exact fields')
 equal(proposal['unchanged_request'],req['prospective_request_identity'],'unchanged request pin')
 equal(proposal['unchanged_five_sources'],req['proposed_request']['sources'],'all five role bindings')
 for role,row in req['proposed_request']['sources'].items():verify(row,'original source role '+role)
 equal(proposal['unchanged_native_argv'],dispatch['parent_argv'],'unchanged native argv')
 equal(proposal['environment'],{'LANG':'C','LC_ALL':'C','PATH':'/usr/bin:/bin'},'exact environment')
 outer=['/usr/bin/env','-i','LC_ALL=C','LANG=C','PATH=/usr/bin:/bin',dispatch['parent_argv'][0],'-I','-S','-B',str(S/'supervise_native.py')]
 equal(proposal['argv'],outer,'fixed outer argv')
 equal(shlex.split(proposal['command_utf8']),['exec']+outer,'literal shell command token relation')
 equal(proposal['command_pin'],pure(proposal['command_utf8'].encode()),'command bytes pin')
 equal(proposal['tool_fields'],dict(dispatch['tool_parameters_proposed'],cmd=proposal['command_utf8']),'whole proposed tool parameters')
 verify(proposal['supervisor_source'],'final supervisor pin');equal(proposal['supervisor_source'],h['supervisor'],'handoff supervisor binding')
 paths={k:v for k,v in dispatch['evidence_paths_proposed'].items() if k!='nonce'};paths['outer_processes']=paths['outer_completion'].replace('.completion.json','.processes.jsonl')
 equal(proposal['proposed_paths'],paths,'exact seven prospective paths');need(len(set(paths.values()))==7,'distinct path roles')
 absences={k:not os.path.lexists(p) for k,p in paths.items()};need(all(absences.values()),'all proposed paths still absent')
 for p in paths.values():need(Path(p).parent==B and Path(p).resolve()==Path(p),'literal immediate external path')
 src=(S/'supervise_native.py').read_text();lines=src.splitlines();equal(len(lines),488,'488 full source lines')
 headers=[(i+1,re.match(r'^def (\w+)\(',line).group(1)) for i,line in enumerate(lines) if re.match(r'^def (\w+)\(',line)]
 equal(len(headers),13,'13 top-level function headers')
 constants=["OUTER_SECONDS, TERM_SECONDS, KILL_SECONDS = 315, 310, 312","CAP = 8 * 1024 * 1024","JOURNAL_CAP = 64 * 1024 * 1024","PS_CAP = 262144","RECEIPT_CAP = 262144","PS_SECONDS, PS_CLEANUP_SECONDS, SCAN_PERIOD = 0.2, 0.2, 0.5","signal.setitimer(signal.ITIMER_REAL, 0.0)","if process is not None and process.returncode is None and (hard or errors):","'complete_fork_coverage': False","'scientific_acceptance': False"]
 for text in constants:need(text in src,'exact selected literal '+text)
 equal(src.count('preexec_fn=clear_child_timer'),2,'both actual Popen sources clear timer')
 for i in (0,4,6,8):
  text=dispatch['parent_argv'][i];need(text in src or (text.startswith(str(B)) and "BASE + '"+text[len(str(B)):]+"'" in src),'exact composed argv operand '+str(i))
 checks=(S/'SUPERVISOR_CHECKS.md').read_text();ids=re.findall(r'^\| (S\d\d) \|',checks,re.M);equal(ids,['S%02d'%i for i in range(1,14)],'all 13 prospective groups exactly once')
 for f in facts['fixed_files']:
  observed=observations[f['path']];equal(observed['resolved'],f['resolved'],'fixed resolution '+f['path']);equal(observed['state'],f['state'],'fixed full state '+f['path'])
 header=Path(facts['fixed_files'][-1]['path']).read_text();need('NOTE_TRACK, NOTE_TRACKERR, and NOTE_CHILD are no longer supported as of 10.5' in header,'SDK unsupported note source only')
 before=read(S/'AUTHOR_METADATA_CHECK.json');delta=read(S/'FINAL_SOURCE_DELTA.json');final=read(S/'FINAL_METADATA_CHECK.json');diagnostic=read(S/'ADMIN_DIAGNOSTICS.json')
 equal(before['source_bytes'],22198,'retained earlier22198 source check not relabelled final');equal(before['source_lines'],486,'retained earlier486 lines')
 equal(delta['source'],proposal['supervisor_source'],'explicit final source delta');equal(final['supervisor'],proposal['supervisor_source'],'final metadata binds actual source')
 equal(diagnostic['boundary_exception']['tool_chunks'],['8cab54','7fee95','34a049','21a995','929699','2697e6'],'six disclosed system Python uses retained')
 equal(diagnostic['boundary_exception']['no_bootstrap_runtime_or_qualification_credit'],True,'no vendor qualification credited')
 old_failure=read(S/'FAILED_ADMIN_TOOL.json');need(old_failure['exit_code']==1 and 'AssertionError' in old_failure['output'],'preserved real author failure')
 for row in h['payloads']:equal({k:observe(row['path'])[k] for k in ('path','bytes','sha256')},row,'subject payload unchanged after checks')
 equal(sorted(p.name for p in S.iterdir()),h['namespace'],'subject namespace unchanged after check')
 result={'schema':'ri165-independent-finite-admin-check-v1','status':'ALL_OPAQUE_AND_ADMINISTRATIVE_CHECKS_PASSED_NOT_SOURCE_ACCEPTANCE','predicate_count':count,'source_dependency_count':307,'source_dependency_bytes':33312952,'exact_external_identity_count':325,'fresh_unique_identity_count':len(observations),'subject_files':16,'subject_payloads':15,'all_five_sources_unchanged':True,'request_bytes':2304,'source_lines':488,'source_function_headers':headers,'prospective_group_ids':ids,'prospective_paths_absent':absences,'author_boundary_exception_retained':True,'author_checks_not_qualification':True,'source_or_supervisor_or_vendor_or_ps_executed':False,'science_decoded':False,'operational_objects_created':False,'administrative_interpreter':sys.executable,'opaque_observations':[observations[k] for k in sorted(observations)],'whole_external_set_canonical_pin':pure(canonical([derived[k] for k in sorted(derived)]))}
 save('METADATA_CHECK.json',result)
 print(json.dumps({k:v for k,v in result.items() if k not in ('opaque_observations','source_function_headers')},sort_keys=True));print(json.dumps({'result':pin(D/'METADATA_CHECK.json')},sort_keys=True))
except BaseException as exc:
 save('FAILED_ADMIN_ATTEMPT.json',{'predicate_count':count,'type':type(exc).__name__,'message':str(exc),'observed_paths':list(observations),'subject_executed':False});raise
