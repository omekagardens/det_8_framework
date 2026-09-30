"""Reviewer-owned opaque/admin/literal-text checks only; never import subject code."""
import difflib, hashlib, json, os, re, shlex, stat
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
Q=B/'ri139-focused-bootstrap-repair-source-XP8iNwMw'
O=B/'ri137-focused-control-launcher-source-nykv2tsg'
D=B/'ri137-root-launch-adjudication-ie1m0jc_'
R=B/'ri139-bootstrap-independent-review-VMq4RmI9'

def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p); a=p.lstat(); assert stat.S_ISREG(a.st_mode) and p.resolve()==p
 with p.open('rb') as f:
  assert state(os.fstat(f.fileno()))==state(a)
  data=f.read(); assert state(os.fstat(f.fileno()))==state(a)
 assert state(p.lstat())==state(a)
 return {'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def j(p):return json.loads(Path(p).read_bytes()) # Only explicit administrative paths below.
def digest(t):
 b=t.encode();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(row):
 actual=pin(row['path']); assert actual==row,(row,actual);return actual
h=j(Q/'HANDOFF.json'); d=j(Q/'DEPENDENCIES.source-only.json'); m=j(Q/'METADATA_CHECK.json'); c=j(Q/'SOURCE_CORRESPONDENCE.json')
assert pin(Q/'HANDOFF.json')=={'path':str(Q/'HANDOFF.json'),'bytes':7035,'sha256':'24e6815b31bd47b543211f4f51156d1c0c67d96dac88db65db48f85d3be898d0'}
packet=[verify(r) for r in h['files']]+[pin(Q/'HANDOFF.json')]
assert len(packet)==8 and sorted(p.name for p in Q.iterdir())==sorted(Path(r['path']).name for r in packet)
checked=[verify(r) for r in d['opaque_files']]
assert len(checked)==len({r['path'] for r in checked})==310
assert sum(r['bytes'] for r in checked)==21106955
old=j(O/'DEPENDENCIES.source-only.json'); oldmap={x['path']:x for x in old['opaque_files']}; newmap={x['path']:x for x in checked}
assert len(oldmap)==276 and all(newmap[k]==v for k,v in oldmap.items())
added=[r for r in checked if r['path'] not in oldmap]; assert len(added)==34
roots=d['sealed_namespace_roots']; assert len(roots)==len(set(roots))==385
assert set(old['sealed_namespace_roots'])<=set(roots) and all(Path(p).is_absolute() for p in roots)
# Inspect recorded roots as strings only, not a new filesystem/runtime inventory.
assert d['counts']=={'opaque_bytes':21106955,'opaque_files':310,'sealed_namespace_roots':385}
assert m['all_opaque_dependencies_authenticated']==checked and m['counts']==d['counts']
for row in m['payloads_before_this_record']:verify(row)
for role,value in d.items():
 if type(value) is dict and set(value)=={'path','bytes','sha256'}: assert newmap[value['path']]==value,role
oldtext=(O/'launch_controls.source-only.py').read_text(); newtext=(Q/'launch_controls.source-only.py').read_text()
delta=''.join(difflib.unified_diff(oldtext.splitlines(True),newtext.splitlines(True),fromfile=str(O/'launch_controls.source-only.py'),tofile=str(Q/'launch_controls.source-only.py')))
assert delta==(Q/'REPAIR.diff').read_text()
assert len(newtext.splitlines())==390 and len(oldtext.splitlines())==373
# Literal top-level def-line spans; no Python syntax parser, AST, compile or import.
def spans(text):
 matches=list(re.finditer(r'^def ([A-Za-z_]\w*)\(',text,re.M)); out={}
 for i,x in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else text.index("if __name__ == '__main__':",x.start())
  body=text[x.start():end].rstrip('\n')+'\n';out[x.group(1)]={'text':body,'start':text[:x.start()].count('\n')+1,'end':text[:x.start()].count('\n')+len(body.splitlines()),**digest(body)}
 return out
a=spans(oldtext);z=spans(newtext)
assert len(a)==19 and len(z)==20 and set(z)-set(a)=={'selected_bootstrap'}
unchanged=[k for k in a if a[k]['text']==z[k]['text']]; changed=[k for k in a if a[k]['text']!=z[k]['text']]
assert len(unchanged)==17 and changed==['prepare_launch','run']
assert len(z['selected_bootstrap']['text'].splitlines())==12 and z['selected_bootstrap']['start']==255
correspondence=[]
for row in c['unchanged_functions']:
 name=row['name']
 oldspan=oldtext[oldtext.index('def '+name+'('):oldtext.index('def inspect_controls(')] if name=='environment' else a[name]['text']
 newsp=newtext[newtext.index('def '+name+'('):newtext.index('def inspect_controls(')] if name=='environment' else z[name]['text']
 oldspan=oldspan.rstrip('\n')+'\n';newsp=newsp.rstrip('\n')+'\n'
 assert oldspan==newsp and digest(oldspan)=={'bytes':row['utf8_bytes'],'sha256':row['sha256']}
 correspondence.append({'name':name,'validated':True,'covers': ['environment','inspect_f01','inspect_f02'] if name=='environment' else [name]})
control_old=oldtext[oldtext.index('F01 = '):oldtext.index('\n\ndef need')].rstrip('\n')+'\n'
control_new=newtext[newtext.index('F01 = '):newtext.index('\n\ndef need')].rstrip('\n')+'\n'
assert control_old==control_new and digest(control_new)==c['unchanged_control_limit_premise_block']
assert oldtext[oldtext.index('import argparse'):oldtext.index('HERE =')]==newtext[newtext.index('import argparse'):newtext.index('HERE =')]
assert newtext.count("P.child_run(card['child_command'], out, 'FOCUSED25', 180, env)")==1
assert 'P.run(' not in newtext and 'P.authenticate(' not in newtext and 'patch.object' not in newtext
assert newtext.count("selected_bootstrap(read(card['bootstrap_host_preflight']), deps)")==2
assert "command = [BOOTSTRAP,'-I','-B',deps['ri135_control']['path']" in newtext
assert "launcher = [BOOTSTRAP,'-I','-B',str(HERE/'launch_controls.source-only.py')" in newtext
assert newtext.index("selected_bootstrap(read(card['bootstrap_host_preflight']), deps)")<newtext.index("exec(compile(module_bytes")<newtext.index('    out.mkdir(mode=0o700)')
pre=j(D/'BOOTSTRAP_PRE.json');post=j(D/'BOOTSTRAP_POST.json')
assert (D/'BOOTSTRAP_PRE.json').read_bytes()==(D/'BOOTSTRAP_POST.json').read_bytes()
selected=d['selected_bootstrap_binding']; path=selected['path']
rows=[r for r in pre['framework_namespace'] if r['path']==path]
assert len(rows)==1 and rows[0]['kind']=='file' and rows[0]['identity']==selected
assert selected['resolved_path']==path and selected['symlink_chain']==[]
alias=[r for r in pre['bindings'] if r['path']=='/Applications/Xcode.app/Contents/Developer/usr/bin/python3'][0]
assert alias['resolved_path']==path and len(alias['symlink_chain'])==2
for k in ['bytes','sha256','state']:assert alias[k]==selected[k]
assert "BOOTSTRAP = "+repr(path) in newtext
# Saved diagnostics and original actual refusal; never invoke their command text.
direct=j(D/'DIRECT_VENDOR_ENV_DIAGNOSTIC.json');indirect=j(D/'BOOTSTRAP_ENV_DIAGNOSTIC.json');failure=j(D/'GENUINE_TOOL_INITIAL.json')
card=j(B/'ri137-focused25-run-musr4qw9/cards/launcher.json'); expected=card['environment']
assert len(expected)==10 and json.loads(direct['result']['output'])==expected
indirect_env=json.loads(indirect['result']['output']); assert all(indirect_env[k]==v for k,v in expected.items())
extras=sorted(set(indirect_env)-set(expected));assert extras==['CPATH','LIBRARY_PATH','MANPATH','SDKROOT']
assert direct['result']['exit_code']==0 and direct['result']['chunk_id']=='a34537'
assert path in shlex.split(direct['invocation']['cmd'])
assert failure['result']['exit_code']==1 and failure['result']['chunk_id']=='feff2a'
assert failure['result']['output'].endswith('ValueError: actual complete environment\n')
assert '    same(dict(os.environ), env, \'actual complete environment\')' in failure['result']['output']
# No current executable access: selection is compared only to saved administrative rows.
report={'schema':'ri139-independent-opaque-text-review-v1','reviewer':'/root/ri116_complete_caller_review','source_packet':packet,
 'opaque_dependencies':checked,'counts':d['counts'],'old276_exactly_preserved':True,'added34':added,
 'protected_root_strings_checked':roots,'root_check_scope':'Recorded absolute strings and inherited subset only; no current directory or runtime scan.',
 'source_delta_exact':True,'old_source_lines':373,'new_source_lines':390,'all_actual_literal_functions':[{'name':k,'old':{x:v for x,v in a[k].items() if x!='text'} if k in a else None,'new':{x:v for x,v in z[k].items() if x!='text'},'status':'unchanged' if k in unchanged else 'changed' if k in changed else 'new'} for k in z],
 'unchanged_function_count':17,'changed_existing_functions':changed,'new_function':'selected_bootstrap','author15_spans_reconciled':correspondence,
 'author_span_count_note':'The named environment span includes environment, inspect_f01 and inspect_f02. Fifteen unchanged spans represent seventeen unchanged actual top-level functions.',
 'control_limit_premise_block':digest(control_new),'imports_unchanged':True,'one_exact_monitor_call':True,'both_commands_use_selected_bootstrap':True,
 'selected_check_before_load_and_in_independent_card_tail':True,'selected_binding_exact_saved_PRE_framework_row':selected,
 'saved_PRE_POST_byte_equality':True,'saved_alias_provenance':alias,'saved_direct_diagnostic_exact_ten_fields':True,'saved_indirect_four_extras':extras,
 'saved_failure_exit':1,'saved_failure_chunk':'feff2a','saved_direct_diagnostic_chunk':'a34537',
 'saved_evidence_pins':[pin(D/n) for n in ['BOOTSTRAP_PRE.json','BOOTSTRAP_POST.json','GENUINE_TOOL_INITIAL.json','BOOTSTRAP_ENV_DIAGNOSTIC.json','DIRECT_VENDOR_ENV_DIAGNOSTIC.json']],
 'genuine_origin_limit':'Retained tool records reconcile parent actual tool history; no JSON record self-authenticates its origin.',
 'current_runtime_inventory':False,'selected_actual_executable_read':False,'source_target_import_compile_ast_probe_run':False,'scientific_decode':False,'controls_executed':0,'admissions_or_attempts_created':False,'repository_or_git_operations':False,'all_checks_passed':True}
with (R/'OPAQUE_TEXT_CHECK.json').open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'result':pin(R/'OPAQUE_TEXT_CHECK.json'),'counts':d['counts'],'unchanged_functions':unchanged,'added_function_lines':[255,266],'all_checks_passed':True},indent=2))
