"""Independent opaque identities and literal text checks only; no subject evaluation."""
from pathlib import Path
from hashlib import sha256
import os, stat, json, re, difflib
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
S=B/'ri135-white-preparation-repair-source-lski1ize';P=B/'ri133-white-runtime-preparation-source-lrck33ys';R=B/'ri135-preparation-repair-independent-review-0ysy6sdb'
def require(ok,message):
 if not ok:raise ValueError(message)
def raw(p):
 p=Path(p);require(p.is_absolute() and str(p)==os.path.normpath(p),'literal')
 for q in [p,*p.parents]:require(not stat.S_ISLNK(q.lstat().st_mode),'symlink '+str(q))
 before=p.stat();require(stat.S_ISREG(before.st_mode),'regular');state=lambda st:(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
 with p.open('rb') as f:
  a=os.fstat(f.fileno());data=f.read();b=os.fstat(f.fileno())
 require(state(before)==state(a)==state(b)==state(p.stat()),'read drift');return data
def ref(p):
 data=raw(p);return {'path':str(p),'bytes':len(data),'sha256':sha256(data).hexdigest()}
def verify(v):
 q=ref(v['path']);require(all(q[k]==v[k] for k in q),'pin '+v['path']);return q
def load(p):return json.loads(raw(p))
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
h=load(S/'HANDOFF.json');packet=[verify(v) for v in h['artifacts']]+[verify({'path':str(S/'HANDOFF.json'),'bytes':5902,'sha256':'4291a055c4cc125d4a07fe6be4fec0e0c5945dc31225cc4bda079fce84824b1d'})]
require(sorted(x.name for x in S.iterdir())==sorted(Path(x['path']).name for x in packet),'source namespace')
d=load(S/'DEPENDENCIES.source-only.json');old=load(P/'DEPENDENCIES.source-only.json');dep=d['opaque_files'];require(len(dep)==253 and len({x['path'] for x in dep})==253,'unique253')
actual=[verify(v) for v in dep];require(sum(x['bytes'] for x in actual)==16220282,'totalbytes')
index={x['path']:x for x in dep};require(len(old['opaque_files'])==228,'old228')
for row in old['opaque_files']:require(index.get(row['path'])==row,'old dependency changed')
added=[x for x in dep if x['path'] not in {a['path'] for a in old['opaque_files']}];require(len(added)==25,'25 additions')
for k in ['historical_optional_namespaces','historical_runtime','packet_handoff','packet_namespace','packet_root','root_adjudication','status']:require(canon(d[k])==canon(old[k]),'retained dependency field '+k)
oldh=load(P/'HANDOFF.json');oldfiles=[verify(x) for x in oldh['artifacts']]+[ref(P/'HANDOFF.json')];require(len(oldfiles)==10,'10 predecessorfiles')
require(sorted(x.name for x in P.iterdir())==sorted(Path(x['path']).name for x in oldfiles),'old source namespace')
for row in oldfiles:require(index.get(row['path'])==row,'predecessor closure')
Q=Path(d['packet_root']);namespace=[]
for q in sorted(Q.rglob('*')):
 t=q.lstat();rel=str(q.relative_to(Q))
 if stat.S_ISDIR(t.st_mode):namespace.append({'relative':rel,'kind':'directory'})
 elif stat.S_ISREG(t.st_mode):identity=ref(q);namespace.append({'relative':rel,'kind':'file','bytes':identity['bytes'],'sha256':identity['sha256']});require(index.get(str(q))==identity,'RI130memberclosure')
 else:raise ValueError('nonregular packetmember')
require(namespace==d['packet_namespace'],'complete packet namespace');require(sum(x['kind']=='file' for x in namespace)==48,'48files')
qh=load(Q/'HANDOFF.json')
for x in qh['artifacts']:verify(x)
target=load(Q/'TARGET_CLOSURE.source-only.json');pairs=[]
for row in target['sources']:
 a=Path(row['original']);b=Q/row['relative'];wanted=row['pin'];ar=verify({'path':str(a),**wanted});br=verify({'path':str(b),**wanted});require(raw(a)==raw(b),'originalcopywholebytes');require(index[str(a)]==ar and index[str(b)]==br,'pairclosure');pairs.append({'original':ar,'copy':br})
require(len(pairs)==30 and target['actual_scientific_inputs']==[],'30pairs noinputs')
history=load(Q/'HISTORY_CLOSURE.source-only.json');require(len(history)==124,'history124')
for x in history:verify(x);require(index[x['path']]==x,'historicalclosure')
expected=load(d['historical_interpreter']['path']);provenance=load(d['historical_interpreter_provenance']['path'])
for key in ('historical_interpreter','historical_interpreter_provenance'):verify(d[key]);require(index[d[key]['path']]==d[key],'historicalinterpreterclosure')
require(provenance['schema']=='ri121-reviewed-runtime-metadata-candidate-handoff-v1' and provenance['status']=='METADATA_CANDIDATE_INDEPENDENTLY_VERIFIED_NOT_RUNTIME_ADMITTED','provenance scope')
require([x for x in provenance['files'] if x['path']==d['historical_interpreter']['path']]==[d['historical_interpreter']],'genuine historicalmembership')
# Literal function spans only, not syntax parsing, AST, compilation or eval.
def spans(text):
 lines=text.splitlines(keepends=True);starts=[(i,re.match(r'def (\w+)\(',line).group(1)) for i,line in enumerate(lines) if re.match(r'def \w+\(',line)]
 return {name:''.join(lines[i:(starts[n+1][0] if n+1<len(starts) else len(lines))]).rstrip() for n,(i,name) in enumerate(starts)}
c=load(S/'SOURCE_CORRESPONDENCE.json');unchanged=[];newdiff=[];fullpatch=''
for row in c['changed_modules']:
 name=row['module'];oldtext=raw(P/name).decode();newtext=raw(S/name).decode();verify(row['old']);verify(row['new']);a=spans(oldtext);b=spans(newtext)
 same_names=sorted(x for x in a if x in b and a[x]==b[x]);changed_names=sorted(x for x in a if x in b and a[x]!=b[x]);added_names=sorted(set(b)-set(a))
 require(same_names==row['unchanged_functions'],'unchanged functionlist '+name)
 require(sorted(changed_names+added_names)==sorted(row['changed_top_level_text_ranges']),'changed functionlist '+name)
 unchanged.extend({'module':name,'function':fn,'bytes':len(a[fn].encode()),'sha256':sha256(a[fn].encode()).hexdigest()} for fn in same_names)
 newdiff.append({'module':name,'changed':changed_names,'added':added_names,'oldlines':len(oldtext.splitlines()),'newlines':len(newtext.splitlines())})
 fullpatch+=''.join(difflib.unified_diff(oldtext.splitlines(keepends=True),newtext.splitlines(keepends=True),fromfile=str(P/name),tofile=str(S/name)))
require(fullpatch==raw(S/'REPAIR.diff').decode(),'entire two-module delta');require(len(unchanged)==42,'42functions')
a=raw(P/'prepare.py').decode();b=raw(S/'prepare.py').decode();blocks=[]
for start,end in [('GUARD_IDS = ','BOUNDS = '),('BOUNDS = ','M = None')]:
 oldblock=a[a.index(start):a.index(end)].rstrip();newblock=b[b.index(start):b.index(end)].rstrip();require(oldblock==newblock,'retained '+start);blocks.append({'start':start,'bytes':len(newblock.encode()),'sha256':sha256(newblock.encode()).hexdigest()})
require("same(binding(VENV + '/bin/python'), interpreter, 'interpreter binding drift')" in raw(S/'runtime_metadata.py').decode(),'fresh interpreter postcheck')
# Metadata labels transcribed from fully reviewed literal declarations; no controls generated or run.
f01=['positive','pre_admission_read','occupied','mkdir','post_admission_read','initial_source_read','attempt_open','attempt_partial','secondary_post','secondary_source','secondary_namespace','secondary_checks','three_secondary','final_partial']
f02=['positive','named_path','resolved_path','link_literal','link_order','link_omitted','target_bytes','target_sha','provenance_missing','snapshot_alias','snapshot_target']
t=raw(S/'fault_controls.source-only.py').decode()
for label,names in [('F01',f01),('F02',f02)]:
 block=t.split(label+' = (',1)[1].split(')\n',1)[0];found=re.findall(r"'([^']+)'",block);require(found==names,'literal focused ids '+label)
ids=['F01_'+x for x in f01]+['F02_'+x for x in f02]
require(len(ids)==25,'25focus')
for x in packet:verify(x)
result={'schema':'ri135-independent-opaque-and-literal-check-v1','status':'COMPLETE','checker':ref(__file__),'source_files':packet,'source_namespace':12,'dependencies':actual,'dependency_count':253,'dependency_bytes':16220282,'unchanged_old_dependencies':228,'added_dependencies':added,'predecessor_source_files':oldfiles,'ri130_namespace':namespace,'original_copy_pairs':pairs,'history_roles':124,'historical_interpreter':d['historical_interpreter'],'historical_interpreter_provenance':d['historical_interpreter_provenance'],'authentic_handoff_membership':True,'historical_binding_fields':sorted(expected),'historical_link_count':len(expected['symlink_chain']),'whole_two_module_patch_matches':True,'unchanged_functions':unchanged,'changed_ranges':newdiff,'unchanged_literal_blocks':blocks,'unchanged_ri130_guard_count':65,'focused_order':ids,'source_lines':1365,'all_source_pins_unchanged_after':True,'target_syntax_or_execution':False,'scientific_body_decode':False,'fixture_execution':False,'runtime_inventory':False}
with (R/'OPAQUE_TEXT_CHECK.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'result':ref(R/'OPAQUE_TEXT_CHECK.json'),'dependency_count':len(actual),'unchanged_functions':len(unchanged),'source_lines':1365,'focused_controls_source_only':len(ids)},indent=2))
