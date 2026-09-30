"""Reviewer-only opaque identities/source text. No target code evaluation/import."""
from pathlib import Path
import hashlib,json,re,stat
S=Path('/Volumes/AI_DATA/development/det-review-evidence/ri130-white-qualification-caller-source-Q4Aq7hZg')
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri130-caller-independent-review-GpeTxmLW')
B=S.parent
checks=[]
def require(ok,n):
 checks.append({'check':n,'passed':bool(ok)})
 if not ok: raise ValueError(n)
def pin(p):
 p=Path(p); b=p.read_bytes()
 require(stat.S_ISREG(p.lstat().st_mode),'regular file '+str(p))
 return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p,expected):
 actual=pin(p);require(all(actual[k]==expected[k] for k in ('bytes','sha256')),'opaque pin '+str(p));return actual
def digest(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
hp=check(S/'HANDOFF.json',{'bytes':26684,'sha256':'1e478b0db8fcda22daedc77bce20c59a1f142b09d61e64d2f4a29a813f1152e8'})
h=json.loads((S/'HANDOFF.json').read_bytes())
a=h['artifacts'];require(len(a)==47==h['artifact_count'],'47 handoff artifacts')
artifact_checks=[]
for row in a:
 require(str(S/row['relative'])==row['path'],'artifact path '+row['relative'])
 artifact_checks.append(check(S/row['relative'],row))
require(len({r['relative'] for r in a})==47,'artifact uniqueness')
require({str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}=={r['relative'] for r in a}|{'HANDOFF.json'},'exact48 packet file namespace')
t=json.loads((S/'TARGET_CLOSURE.source-only.json').read_bytes());require(len(t['sources'])==30,'30 target pairs');require(t['actual_scientific_inputs']==[],'no actual scientific inputs')
pairs=[]
for row in t['sources']:
 x=check(row['original'],row['pin']);y=check(S/row['relative'],row['pin']);same=Path(row['original']).read_bytes()==(S/row['relative']).read_bytes();require(same,'whole pair equality '+row['relative']);pairs.append({'original':x,'copy':y,'whole_bytes_equal':same})
require({k:sum(r['relative'].startswith('science/'+k+'/') for r in t['sources']) for k in ('primary','validator','qualifier')}=={'primary':13,'validator':8,'qualifier':9}==t['packet_counts'],'13primary8validator9qualifier')
for n in ('white_root','integrated_root'):check(t[n]['path'],t[n])
history=json.loads((S/'HISTORY_CLOSURE.source-only.json').read_bytes());require(len(history)==124,'124 history rows');require(len({r['path'] for r in history})==124,'unique history paths')
hi=[check(row['path'],row) for row in history]
require(sum(x['bytes'] for x in hi)==10625600,'history10625600bytes')
require(len([x for x in hi if x['bytes']==0])==2,'two valid empty history stderr files')
support=[]
for src,dst in [(B/'ri121-synthetic-caller-repair-7ys8vsc3/control.py',S/'control.py'),(B/'ri121-synthetic-caller-repair-7ys8vsc3/runtime_support.py',S/'runtime_support.py'),(B/'ri121-root-runtime-qualification-jsf0o3_x/runtime_profile_probe.py',S/'profile_observe.source-only.py')]:
 require(src.read_bytes()==dst.read_bytes(),'whole retained support '+dst.name);support.append({'original':pin(src),'copy':pin(dst)})
old=(B/'ri121-synthetic-caller-repair-7ys8vsc3/launch.py').read_bytes();new=(S/'monitor.py').read_bytes()
oldfunc=old[old.index(b'def monitor_text('):old.index(b'def admit_command(')].rstrip()+b'\n'
newfunc=new[new.index(b'def monitor_text('):new.index(b'def supervise(')].rstrip()+b'\n'
require(oldfunc==newfunc,'monitor_text and reap whole retained text')
oldloop=b''.join(old.splitlines(keepends=True)[335:377]);newloop=b''.join(new.splitlines(keepends=True)[44:86])
require(all(not x.strip() or x.startswith(b'        ') for x in oldloop.splitlines(keepends=True)),'loop removable indentation')
reindented=b''.join(x[8:] if x.strip() else x for x in oldloop.splitlines(keepends=True))
require(reindented==newloop,'whole monitor loop after exact8spaces removal')
corr=json.loads((S/'BLOCK_CORRESPONDENCE.source-only.json').read_bytes());require(digest(oldloop)['sha256']==corr['retained_loop_sha256_before_indentation'],'declared original newline-inclusive block');require(digest(newloop)['sha256']==corr['current_loop_sha256'],'declared new newline-inclusive block')
gold=(B/'ri121-synthetic-caller-repair-7ys8vsc3/guard_controls.source-only.py').read_bytes();gnew=(S/'guard_controls.source-only.py').read_bytes()
oldruntime=gold[gold.index(b'def runtime_case('):gold.index(b'def main(')].rstrip()+b'\n';newruntime=gnew[gnew.index(b'def runtime_case('):gnew.index(b'def static_case(')].rstrip()+b'\n'
require(oldruntime==newruntime,'legacy runtime_case unchanged text')
coverage=[]
for name,decl in h['source_declaration_locations_not_syntax_validation'].items():
 lines=(S/name).read_text().splitlines();require(len(lines)==decl['lines'],'source line count '+name)
 found=[{'line':i,'name':re.match(r'def ([A-Za-z_][A-Za-z0-9_]*)',v).group(1)} for i,v in enumerate(lines,1) if re.match(r'def ([A-Za-z_][A-Za-z0-9_]*)',v)]
 require(found==decl['declarations'],'plain text declared functions '+name);coverage.append({'file':name,'lines':len(lines),'declarations':found})
# Extract ONLY literal words from author-declared tuple text, never evaluate source.
gtext=gnew.decode();ctext=(S/'caller_contract.py').read_text();groups={}
for key,prefix in [('FAILURE','failure'),('CAPTURE','capture'),('MONITOR','monitor'),('RUNTIME','runtime'),('STATIC','static'),('ACCEPTANCE','acceptance'),('MODE','mode'),('RELATION','relation')]:
 line=next(v for v in gtext.splitlines() if v.startswith(key+'_KINDS='));words=re.findall(r"'([a-z_]+)'",line);groups[prefix]=words
 for word in words:require("'"+word+"'" in ctext[ctext.index('GUARD_IDS ='):ctext.index('def need(')],'guard id literal '+prefix+':'+word)
ids=[side+'_'+x for side in ('parent','worker') for x in groups['failure']]+[k+'_'+x for k in ('capture','monitor','runtime','static','acceptance','mode','relation') for x in groups[k]]
require(len(ids)==len(set(ids))==65,'65 unique manually matched prospective control IDs')
absent=[]
for name in ('AUTHORIZED_FREEZE.json','ADMIT_NORMAL.json','ADMIT_OPTIMIZED.json','runs','controls','RUNTIME_INVENTORY.json'):
 p=S/name;require(not p.exists() and not p.is_symlink(),'no active packet path '+name);absent.append(str(p))
# No scientific result decoded: only packet and historical source-metadata identity lists.
result={'schema':'ri130-independent-opaque-metadata-review-v1','status':'PASS_SOURCE_IDENTITIES_ONLY','source_handoff':hp,'artifact_checks':artifact_checks,'target_pairs':pairs,'historical_pins':hi,'retained_support':support,'text_correspondence':{'monitor_text_reap':digest(oldfunc),'original_loop_including_final_newline':digest(oldloop),'reindented_loop_including_final_newline':digest(newloop),'legacy_runtime_case':digest(oldruntime)},'plain_source_declarations':coverage,'prospective_guard_ids':ids,'absent_paths':absent,'checks':checks,'target_execution':False,'target_import_compile_ast_probe':False,'scientific_body_decode':False,'qualification':False}
(R/'OPAQUE_METADATA_REVIEW.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'artifacts':len(a),'target_pairs':len(pairs),'history':len(hi),'output':pin(R/'OPAQUE_METADATA_REVIEW.json')},indent=2))
