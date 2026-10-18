"""Reviewer-owned opaque identity, administrative JSON and literal-text checks.
Never import/parse/compile/evaluate target source or decode scientific bodies.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json, re, stat, os
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
Q=B/'ri136-native-policy-dispatch-source-g_z472z7'
A=B/'ri134-native-validator-extraction-source-y8kwkcde'
P=B/'ri132-native-caller-qualification-source-0ZmB3R5I'
V=B/'ri134-native-extraction-independent-review-mcwy0ya3'
R=B/'ri136-dispatch-independent-review-s5t7rk5z'
def check(ok,message):
    if not ok: raise ValueError(message)
def pairs(items):
    out={}
    for k,v in items:
        check(k not in out,'duplicate admin key'); out[k]=v
    return out
def admin(p): return json.loads(p.read_text(),object_pairs_hook=pairs)
def pin(p):
    p=Path(p); check(p.is_absolute() and os.path.normpath(str(p))==str(p),'noncanonical metadata path')
    cur=Path(p.anchor)
    for part in p.parts[1:]:
        cur=cur/part; check(not stat.S_ISLNK(cur.lstat().st_mode),'symlink '+str(cur))
    before=p.stat(); check(stat.S_ISREG(before.st_mode),'not regular')
    h=sha256(); n=0
    with p.open('rb') as f:
        for raw in iter(lambda:f.read(1048576),b''): h.update(raw); n+=len(raw)
    after=p.stat()
    check((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'changed while read')
    check(n==before.st_size,'wrong byte count')
    return {'path':str(p),'bytes':n,'sha256':h.hexdigest()}
def verify(ref):
    obs=pin(ref['path']); exp={k:ref[k] for k in ('path','bytes','sha256')}
    check(obs==exp,'identity mismatch '+str(ref['path']))
    if 'resolved_path' in ref: check(ref['resolved_path']==ref['path'] and ref['symlinks']==[],'alias identity')
    return obs
def refs(v,loc='$'):
    if type(v) is dict:
        if {'path','bytes','sha256'}<=v.keys() and type(v['path']) is str and type(v['bytes']) is int and type(v['sha256']) is str: yield loc,v
        for k,x in v.items(): yield from refs(x,loc+'.'+k)
    elif type(v) is list:
        for i,x in enumerate(v): yield from refs(x,loc+'.'+str(i))
h=admin(Q/'HANDOFF.json')
check(pin(Q/'HANDOFF.json')=={'path':str(Q/'HANDOFF.json'),'bytes':11534,'sha256':'748b0e5e7b309705d5a6daf0aaaf6b89dce071f95af4fe3f4b9cb572a6f9ae18'},'handoff pin')
packet=[verify(x) for x in h['files']]
check(sorted(x['path'] for x in packet)==sorted(str(x) for x in Q.iterdir() if x.name!='HANDOFF.json'),'RI136 exact namespace')
check(len(packet)==11,'payload count')
d=admin(Q/'SOURCE_DEPENDENCIES.json'); old=admin(A/'SOURCE_DEPENDENCIES.json')
entries=d['protected_files']; olds=old['protected_files']
check(len(entries)==373 and len(olds)==343,'closure sizes')
check(d['schema']==old['schema'] and d['status']==old['status'] and d['scope']==old['scope'],'dependency envelope changed')
check([x['path'] for x in entries]==sorted(set(x['path'] for x in entries)),'dependency path order')
index={x['path']:x for x in entries}; prior={x['path']:x for x in olds}
observed=[]
for i,e in enumerate(entries,1):
    check(e['role']=='dep_%04d'%i and e['path']==e['identity']['path'],'role/path')
    observed.append(verify(e['identity']))
for path,e in prior.items(): check({k:v for k,v in e.items() if k!='role'}=={k:v for k,v in index[path].items() if k!='role'},'inherited changed '+path)
adds=[e for e in entries if e['path'] not in prior]
check(len(adds)==30,'addition count')
for directory,n in ((A,17),(V,8)):
    expected=sorted(e['path'] for e in adds if Path(e['path']).parent==directory)
    actual=sorted(str(p) for p in directory.iterdir())
    check(len(expected)==n and expected==actual,'predecessor exact namespace '+str(directory))
root_add=[e for e in adds if Path(e['path']).parent not in (A,V)]
check(len(root_add)==5,'selected root count')
new_admin=[e for e in adds if e['access_policy']=='metadata-identities-only-no-scientific-body-decoding']
check(len(new_admin)==11,'new administrative body count')
refrows=[]
for e in new_admin:
    rr=[]
    for loc,v in refs(admin(Path(e['path']))):
        check(v['path'] in index,'new unclosed reference '+e['path']+loc+' '+v['path'])
        exp=index[v['path']]['identity']
        check(all(v[k]==exp[k] for k in ('path','bytes','sha256')),'new mismatched reference '+loc)
        rr.append({'location':loc,'reference':{k:v[k] for k in ('path','bytes','sha256')}})
    refrows.append({'source':e['path'],'typed_references':len(rr),'rows':rr})
check(sum(x['typed_references'] for x in refrows)==785,'new refcount')
m=admin(Q/'SOURCE_IDENTITIES.json'); mr=[]
for loc,v in refs(m): mr.append({'location':loc,'observed':verify(v)})
check(len(mr)==14,'manifest refs')
casechecks={}
for which in ('native','audit'):
    p=Path(m['subjects'][which]['controls']['path']); text=p.read_text()
    triples=[dict(zip(('id','family','mutation'),t)) for t in re.findall(r"^    _case\('([^']+)', '([^']+)', '([^']+)'",text,re.M)]
    check(triples==m['subjects'][which]['ordered_cases'],'literal tuples '+which)
    check(len(triples)==m['subjects'][which]['case_count'],'case count '+which)
    check(len(set(x['id'] for x in triples))==len(triples),'case uniqueness '+which)
    casechecks[which]={'count':len(triples),'families':dict(Counter(x['family'] for x in triples)),'ordered_triples':triples,'exact':True}
cor=admin(Q/'SOURCE_CORRESPONDENCE.json')
oldtext=(P/'qualify_callers.py').read_text(); newtext=(Q/'qualify_policies.py').read_text()
patch=(Q/'DISPATCHER_DELTA.patch').read_text().splitlines(keepends=True)
oldlines=oldtext.splitlines(keepends=True); projected=[]; cursor=0; i=2; hunks=0
while i<len(patch):
    match=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n',patch[i]); check(match is not None,'unified header')
    start=int(match[1])-1; oldn=int(match[2] or 1); newn=int(match[4] or 1)
    projected.extend(oldlines[cursor:start]); cursor=start; i+=1; oldcount=newcount=0
    while i<len(patch) and not patch[i].startswith('@@ '):
        line=patch[i]; check(line[0] in ' +-','diff record')
        if line[0] in ' -': check(oldlines[cursor]==line[1:],'diff old line'); cursor+=1; oldcount+=1
        if line[0] in ' +': projected.append(line[1:]); newcount+=1
        i+=1
    check(oldcount==oldn and newcount==newn,'hunk lengths'); hunks+=1
projected.extend(oldlines[cursor:]); check(''.join(projected)==newtext,'whole projection')
def span(text,name):
    match=re.search(r'^def '+re.escape(name)+r'\(',text,re.M)
    if not match: return None
    tail=text[match.start():]; nxt=re.search(r'\n(?=def |class |if __name__)',tail)
    chunk=tail[:nxt.start()+1] if nxt else tail
    return {'start_line':text[:match.start()].count('\n')+1,'bytes':len(chunk.encode()),'sha256':sha256(chunk.encode()).hexdigest()}
spans=[]
for row in cor['functions']:
    oo=span(oldtext,row['name']); nn=span(newtext,row['name'])
    check(oo==row['old'] and nn==row['new'],'span '+row['name'])
    klass='NEW_FUNCTION' if oo is None else ('EXACT_RETAINED_TEXT' if oo['sha256']==nn['sha256'] else 'ADAPTED_FUNCTION')
    check(klass==row['classification'],'classification '+row['name']); spans.append({'name':row['name'],'old':oo,'new':nn,'classification':klass})
imports=lambda text: '\n'.join(x for x in text.splitlines() if x.startswith('import ') or x.startswith('from '))
check(imports(oldtext)==imports(newtext),'imports changed')
check(sorted(re.findall(r'^def (\w+)\(',newtext,re.M))==sorted(x['name'] for x in spans),'function inventory')
check(newtext.count('helper.run_case(caller, case_id)')==1,'call count text')
check(newtext.index("'authorized case triple differs'")<newtext.index("helper, control_id = load_exact_module")<newtext.index("caller, caller_id = load_exact_module")<newtext.index('helper.run_case(caller, case_id)'),'static selection/load/call order')
refusals=admin(Q/'DISPATCHER_REFUSALS.json')
check([len(refusals[k]) for k in ('operational_first_refusals','source_defense_boundaries','lifecycle_and_collection_failures')]==[13,5,3],'refusal inventories')
for row in refusals['operational_first_refusals']: check(row['first_message'] in newtext,'operational first message missing '+row['id'])
result={'schema':'ri136-independent-opaque-text-review-v1','status':'PASS_METADATA_AND_LITERAL_TEXT_ONLY',
 'method':'Reviewer-owned Python standard library; no target import/AST/compile/evaluation and no scientific JSON body decoding.',
 'source_handoff':pin(Q/'HANDOFF.json'),'source_packet':packet,'exact_source_namespace':12,
 'dependencies_checked':observed,'dependency_count':373,'inherited_entries_unchanged_except_role':343,
 'additions':adds,'additions_count':30,'complete_predecessor_namespaces':{'source':17,'review':8},'selected_root_support_count':5,
 'access_policy_counts':dict(Counter(x['access_policy'] for x in entries)),
 'new_administrative_bodies':11,'new_reference_count':785,'new_admin_reference_checks':refrows,
 'inherited_145_body_traversal_repeated':False,'mixed_lane_root_support_bodies_decoded':False,
 'manifest_reference_count':14,'manifest_references':mr,'literal_case_inventory_checks':casechecks,
 'source_correspondence':{'full_patch_reconstruction':True,'hunks':hunks,'exact_import_block':True,'functions':spans,'classes':dict(Counter(x['classification'] for x in spans))},
 'dispatch_order_literal_check':True,'run_case_callsite_count':1,'prospective_first_refusal_message_literals':13,
 'unexecuted_refusal_map_counts':[13,5,3],
 'execution':{'subject':False,'fixtures_controls':False,'scientific_body_decode':False,'runtime_inventory':False,'active_cards_or_admissions':False,'repository_or_git':False}}
out=R/'OPAQUE_TEXT_REVIEW.json'
with out.open('x') as f: json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
print(json.dumps({'output':pin(out),'summary':{'dependencies':373,'new_admin':11,'new_refs':785,'manifest_refs':14,'cases':139,'patch_hunks':hunks,'functions':result['source_correspondence']['classes']}}))
