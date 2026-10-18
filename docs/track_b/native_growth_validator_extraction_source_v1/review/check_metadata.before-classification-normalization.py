"""Reviewer-owned text/opaque metadata checks. Never imports or evaluates target source."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json, os, stat, difflib, re
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
S=B/'ri134-native-validator-extraction-source-y8kwkcde'
R=B/'ri134-native-extraction-independent-review-mcwy0ya3'
P=B/'ri129-native-sign-caller-source-8TksBLo0'
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def require(ok,msg):
 if not ok: raise ValueError(msg)
def raw(p):
 p=Path(p); require(p.is_absolute() and os.path.normpath(str(p))==str(p),'literal path '+str(p))
 for q in [p,*p.parents]:require(not stat.S_ISLNK(q.lstat().st_mode),'symlink '+str(q))
 before=p.stat(); require(stat.S_ISREG(before.st_mode),'regular '+str(p))
 with p.open('rb') as f:
  fd0=os.fstat(f.fileno()); body=f.read();fd1=os.fstat(f.fileno())
 after=p.stat()
 keys=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 require(keys(before)==keys(fd0)==keys(fd1)==keys(after),'read drift '+str(p))
 require(len(body)==before.st_size,'length '+str(p));return body

def pin(p):
 b=raw(p);return {'path':str(p),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def checkpin(v):
 got=pin(v['path']); require(got=={k:v[k] for k in got},'pin '+v['path']);return got

def load(p):return json.loads(raw(p))
H=load(S/'HANDOFF.json');require(pin(S/'HANDOFF.json')=={'path':str(S/'HANDOFF.json'),'bytes':14101,'sha256':'3dd25f629fffe6bf23491bfb98987df75870f180ccd2733d5011fde6abf882ac'},'handoff')
packet=[checkpin(v) for v in H['files']]+[pin(S/'HANDOFF.json')]
require(sorted(p.name for p in S.iterdir())==sorted(Path(x['path']).name for x in packet),'packet namespace')
D=load(S/'SOURCE_DEPENDENCIES.json'); oldD=load(P/'SOURCE_DEPENDENCIES.json'); A=load(S/'AUTHOR_METADATA_CHECK.json')
rows=D['protected_files']; oldrows=oldD['protected_files'];require(len(rows)==343 and len(oldrows)==299,'dependency counts')
require(canon({k:v for k,v in D.items() if k!='protected_files'})==canon({k:v for k,v in oldD.items() if k!='protected_files'}),'retained protocol')
index={r['path']:r for r in rows}; require(len(index)==343,'duplicate dependency')
for i,r in enumerate(rows,1):
 require(r['role']=='dep_%04d'%i,'role');require(r['path']==sorted(index)[i-1],'path order')
 require(r['identity']['resolved_path']==r['path'] and r['identity']['symlinks']==[],'dep literal')
dep_pins=[checkpin(r['identity']) for r in rows]
for r in oldrows:
 require(canon({k:v for k,v in r.items() if k!='role'})==canon({k:v for k,v in index[r['path']].items() if k!='role'}),'inherited entry '+r['path'])
added=[r['path'] for r in rows if r['path'] not in {x['path'] for x in oldrows}];require(len(added)==44,'44 additions')
ns=[]
for expected in A['complete_predecessor_namespaces']:
 p=Path(expected['path']); observed=sorted(str(x) for x in p.iterdir()); wanted=sorted(x for x in index if Path(x).parent==p)
 require(observed==wanted and len(wanted)==expected['complete_file_count'],'predecessor namespace '+str(p));ns.append({'path':str(p),'count':len(wanted),'members':wanted})
C=load(S/'SOURCE_CORRESPONDENCE.json');projections=[]
for caller in C['callers']:
 old=raw(caller['old_source']['path']).decode();new=raw(caller['new_source']['path']).decode(); ol=old.splitlines(keepends=True);nl=new.splitlines(keepends=True)
 checkpin(caller['old_source']);checkpin(caller['new_source']);replacements={};removed=set();bchecks=[]
 for item in caller['four_moved_blocks']:
  a=item['old_block'];b=item['new_function'];ob=''.join(ol[a['start_line']-1:a['end_line']]);nb=''.join(nl[b['start_line']-1:b['end_line']])
  require(len(ob.encode())==a['bytes'] and sha256(ob.encode()).hexdigest()==a['sha256'],'old moved pin')
  require(len(nb.encode())==b['bytes'] and sha256(nb.encode()).hexdigest()==b['sha256'],'new moved pin')
  lines=nb.splitlines(keepends=True); require(lines[0].startswith('def '+item['function']+'('),'function declaration');lines=lines[1:]
  if item['one_line_docstring_excluded'] is not None:
   require(lines[0].rstrip('\n')==item['one_line_docstring_excluded'],'docstring');lines=lines[1:]
  while lines and not lines[-1].strip(): lines.pop()
  if item['dependency_return_entries_added']:
   require(lines[-1]=='    return entries\n','return');lines.pop()
  before=ob.splitlines(keepends=True)
  while before and not before[-1].strip(): before.pop()
  indent=item['common_indent_removed_from_old']; before=[x[indent:] if x.strip() else x for x in before]
  require(before==lines,'moved body '+item['function'])
  line=item['production_call_line']; require(nl[line-1].strip()==item['production_call'],'production call')
  replacements[line]=ob; removed.update(range(b['start_line'],b['end_line']+1));bchecks.append({'function':item['function'],'old_block':a,'new_function':b,'production_call_line':line,'exact_policy_body':True})
 projected=''.join(replacements.get(n,x) for n,x in enumerate(nl,1) if n not in removed)
 pl=projected.splitlines(keepends=True)
 for i,line in enumerate(pl):
  if i==1 or line.startswith(('E = Path(', 'DEPENDENCIES_BYTES = ', 'DEPENDENCIES_SHA256 = ')):
   if i==1:pl[i]=ol[1]
   else:
    prefix=line.split('=')[0]+'=';matches=[x for x in ol if x.startswith(prefix)];require(len(matches)==1,'single allowed old line');pl[i]=matches[0]
 require(''.join(pl)==old,'whole source projection '+caller['caller'])
 patch=S/('NATIVE_CALLER_DELTA.patch' if caller['caller']=='native' else 'AUDIT_CALLER_DELTA.patch')
 # Check the stored unified patch by literal in-memory hunk reconstruction.
 # Valid diff algorithms can choose different repeated-blank-line alignments.
 saved=raw(patch).decode().splitlines(keepends=True); rebuilt=[];cursor=0;pos=2
 while pos<len(saved):
  match=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',saved[pos]);require(match is not None,'hunk header')
  begin=int(match[1])-1;require(begin>=cursor,'hunk order');rebuilt.extend(ol[cursor:begin]);cursor=begin;pos+=1;oldn=newn=0
  while pos<len(saved) and not saved[pos].startswith('@@ '):
   line=saved[pos];tag=line[0];require(tag in ' +-','hunk tag')
   if tag in ' -':require(ol[cursor]==line[1:],'hunk old context');cursor+=1;oldn+=1
   if tag in ' +':rebuilt.append(line[1:]);newn+=1
   pos+=1
  require(oldn==int(match[2] or 1) and newn==int(match[4] or 1),'hunk counts')
 rebuilt.extend(ol[cursor:]);require(rebuilt==nl,'whole source delta '+caller['caller'])
 projections.append({'caller':caller['caller'],'old_source':caller['old_source'],'new_source':caller['new_source'],'moved_blocks':bchecks,'whole_projected_identity':{'bytes':len(old.encode()),'sha256':sha256(old.encode()).hexdigest()},'complete_delta_exact':True})
prior=load(B/'ri132-native-qualification-independent-review-ye271mv3/OPAQUE_SOURCE_REVIEW.json')['declaration_coverage'];coverage=[]
for who,fn,cf,controlname,rowkey,casekey,idkey,prior_key in [('native','supervise.py','native_coverage.json','native_policy_controls.py','declarations','direct_case_inventory','current_case_ids','ri132_classification'),('audit','launch_audit.py','audit_coverage.json','audit_policy_controls.py','rows','ordered_case_inventory','implemented_case_ids','prior_ri132_classification')]:
 v=load(S/cf); text=raw(S/fn).decode(); oldtext=raw(P/fn).decode()
 block=text.split('CONTROL_DECLARATIONS = (\n',1)[1].split('\n)\n',1)[0];oldblock=oldtext.split('CONTROL_DECLARATIONS = (\n',1)[1].split('\n)\n',1)[0];require(block==oldblock,'old declarations')
 source_lines=block.splitlines(); rr=v[rowkey];require(len(source_lines)==len(rr),'declaration count')
 for line,r in zip(source_lines,rr):
  d=r['declaration'];expected='    ('+', '.join(repr(d[k]) for k in ['name','function','code','condition'])+'),';require(line==expected,'declaration literal '+d['name'])
 priorrows=[x for x in prior if x['caller']==who]; require([x['declaration'] for x in priorrows]==[x['declaration'] for x in rr],'prior tuple order')
 normalization={'blocked':'BLOCKED_DEEPER','retained':'RETAINED_ENGINE_SOURCE_APPLICABILITY_UNEXECUTED','direct':'RETAINED_DIRECT_SOURCE_APPLICABILITY_UNEXECUTED','whole_entry_specification':'PRIOR_ENTRY_SPECIFICATION_NOT_ADAPTED_OR_EXECUTED'}
 for r,pr in zip(rr,priorrows):
  want=normalization[pr['classification']] if who=='native' else pr['classification'];require(r[prior_key]==want,'prior class '+r['declaration']['name'])
 controltext=raw(S/controlname).decode()
 triples=re.findall(r"^    _case\('([^']*)', '([^']*)', '([^']*)'",controltext,re.M)
 require([dict(zip(('id','family','mutation'),tr)) for tr in triples]==v[casekey],'complete literal case inventory')
 ids={x[0] for x in triples};require(len(ids)==len(triples),'unique cases')
 for r in rr:require(set(r[idkey])<=ids,'linked case ids')
 coverage.append({'caller':who,'ordered_declarations':len(rr),'source_case_inventory':len(triples),'current_partition':dict(Counter(r['current_support'] for r in rr)),'literal_source_declarations_and_prior_classifications_match':True,'case_inventory_exact_and_linked':True})
# Expected historical/runtime boundaries only; do not touch their named objects.
history_path=B/'ri122-native-caller-source-jgehvvxx/HISTORY_RECONCILIATION.json';runtime_path=B/'ri122-native-caller-source-jgehvvxx/RUNTIME_CLOSURE.json'
history_pin=checkpin({'path':str(history_path),'bytes':2170307,'sha256':'b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c'})
runtime_pin=checkpin({'path':str(runtime_path),'bytes':2862854,'sha256':'35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920'})
history=load(history_path);runtime=load(runtime_path)
boundaries=[('dependency',{x['path']:x['identity'] for x in rows}),('history',{x['path']:x['identity'] for x in history['protected_files']}),('runtime',{x['path']:x['identity'] for x in runtime['files']})]
require([len(x[1]) for x in boundaries]==[343,699,2988],'boundary counts')
counts=Counter();admin=[];failures=[]
for r in rows:
 if r['access_policy']!='metadata-identities-only-no-scientific-body-decoding':continue
 p=Path(r['path']);v=load(p);stack=[('$',v)];local=Counter()
 while stack:
  where,x=stack.pop()
  if isinstance(x,dict):
   if {'path','bytes','sha256'}<=set(x) and isinstance(x['path'],str) and type(x['bytes']) is int and isinstance(x['sha256'],str):
    found=[(name,inventory[x['path']]) for name,inventory in boundaries if x['path'] in inventory]
    if not found: failures.append({'body':str(p),'field':where,'reason':'unclosed','reference':x})
    else:
     name,wanted=found[0];local[name]+=1;counts[name]+=1
     for k in ['path','bytes','sha256','resolved_path','symlinks']:
      if k in x and canon(x[k])!=canon(wanted[k]):failures.append({'body':str(p),'field':where,'reason':'mismatch','key':k})
   stack.extend((where+'.'+k,y) for k,y in x.items())
  elif isinstance(x,list):stack.extend((where+'['+str(i)+']',y) for i,y in enumerate(x))
 admin.append({'path':str(p),'reference_counts':dict(local),'references':sum(local.values())})
result={'schema':'ri134-independent-text-and-opaque-metadata-review-v1','status':'COMPLETE_METADATA_CHECKS','reviewer_source':pin(__file__),'source_handoff':pin(S/'HANDOFF.json'),'packet_files':packet,'namespace_count':len(packet),'dependency_pins':dep_pins,'inherited_entries_unchanged':299,'added_entries':added,'predecessor_namespaces':ns,'reverse_projections':projections,'coverage':coverage,'administrative_closure':{'bodies':len(admin),'reference_occurrences':sum(counts.values()),'reference_boundary_counts':dict(counts),'per_body':admin,'failures':failures,'history_manifest':history_pin,'runtime_manifest':runtime_pin,'history_expected_entries':699,'runtime_expected_files':2988,'runtime_expected_directories':258,'runtime_expected_absences':40,'current_history_runtime_files_observed':False},'scientific_json_decoded':False,'targets_imported_compiled_parsed_executed':False,'fixtures_evaluated':False}
require(not failures,'closure failures '+str(len(failures)));require(len(admin)==145,'admin count')
require(dict(counts)=={'dependency':3394,'history':16738,'runtime':95538},'reference counts '+str(counts))
for v in packet:checkpin(v)
result['postcheck_packet_identity_unchanged']=True
out=R/'OPAQUE_TEXT_REVIEW.json'
with out.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'result':pin(out),'dependencies':len(rows),'references':sum(counts.values()),'projections':len(projections),'coverage':coverage},indent=2))
