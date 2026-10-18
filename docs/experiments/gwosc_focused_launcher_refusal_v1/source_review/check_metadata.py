"""Independent RI137 administrative/opaque identity and literal-text review only."""
from pathlib import Path
from hashlib import sha256
import json, stat, os, re
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
Q=B/'ri137-focused-control-launcher-source-nykv2tsg'
P=B/'ri135-white-preparation-repair-source-lski1ize'
V=B/'ri135-preparation-repair-independent-review-0ysy6sdb'
R=B/'ri137-launcher-independent-review-5q_931ea'
def need(ok,msg):
    if not ok: raise ValueError(msg)
def pairs(rows):
    out={}
    for k,v in rows: need(k not in out,'duplicate admin key'); out[k]=v
    return out
def read(p): return json.loads(p.read_text(),object_pairs_hook=pairs)
def pin(p):
    p=Path(p); need(p.is_absolute() and os.path.normpath(str(p))==str(p),'literal metadata path')
    cur=Path(p.anchor)
    for part in p.parts[1:]:
        cur=cur/part; need(not stat.S_ISLNK(cur.lstat().st_mode),'symlink '+str(cur))
    b=p.stat(); need(stat.S_ISREG(b.st_mode),'regular file')
    digest=sha256(); count=0
    with p.open('rb') as f:
        for x in iter(lambda:f.read(1048576),b''): digest.update(x); count+=len(x)
    a=p.stat(); state=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    need(state(a)==state(b) and count==b.st_size,'read drift')
    return {'path':str(p),'bytes':count,'sha256':digest.hexdigest()}
def verify(row):
    actual=pin(row['path']); need(actual==row,'pin differs '+row['path']); return actual
def typed(v):
    if type(v) is dict:
        if set(v)=={'path','bytes','sha256'}: yield v
        for x in v.values(): yield from typed(x)
    elif type(v) is list:
        for x in v: yield from typed(x)
h=read(Q/'HANDOFF.json')
need(pin(Q/'HANDOFF.json')=={'path':str(Q/'HANDOFF.json'),'bytes':4642,'sha256':'95112c29b0448f7f48810fb34d9510b6d7b6079826054383795758e3f70b2cbd'},'input handoff')
files=[verify(x) for x in h['files']]
need(sorted(p.name for p in Q.iterdir())==h['closed_namespace'],'closed six namespace')
need(len(files)==5,'five payloads')
d=read(Q/'DEPENDENCIES.source-only.json'); prior=read(P/'DEPENDENCIES.source-only.json')
rows=d['opaque_files']; old=prior['opaque_files']
need(len(rows)==276 and len(old)==253,'dep counts')
need([x['path'] for x in rows]==sorted(set(x['path'] for x in rows)),'ordered unique paths')
observed=[verify(x) for x in rows]; index={x['path']:x for x in rows}; oldindex={x['path']:x for x in old}
need(all(index[p]==x for p,x in oldindex.items()),'inherited identity changed')
add=[x for x in rows if x['path'] not in oldindex]
need(len(add)==23,'new count')
for directory,n in ((P,12),(V,6)):
    namespace=sorted(str(p) for p in directory.iterdir())
    expected=sorted(x['path'] for x in add if Path(x['path']).parent==directory)
    need(len(namespace)==n and namespace==expected,'predecessor whole namespace '+str(directory))
root=[x for x in add if Path(x['path']).parent not in (P,V)]
need(len(root)==5,'five root support')
need(sum(x['bytes'] for x in rows)==16850995==d['counts']['opaque_bytes'],'opaque byte count')
roots=d['sealed_namespace_roots']
need(len(roots)==378 and roots==sorted(set(roots)),'namespace exclusion roots')
need(str(Q) in roots and '/Volumes/AI_DATA/development/det_8_framework-ret' in roots,'source and repo excluded')
need(all(any(Path(x['path'])==Path(r) or Path(r) in Path(x['path']).parents for r in roots) for x in rows),'dependency root not excluded')
# Observe only the declared exclusion roots; do not inventory any runtime or all evidence directories.
root_checks=[]
for value in roots:
    p=Path(value); need(p.is_absolute() and p.resolve(strict=True)==p and p.is_dir() and not p.is_symlink(),'declared namespace root')
    root_checks.append({'path':value,'canonical_directory':True})
roles={}
for name in ('historical_interpreter','historical_interpreter_provenance','historical_optional_namespaces',
             'ri135_control','ri135_independent_review','ri135_module','ri135_root_adjudication','ri135_source_handoff'):
    need(d[name]==index[d[name]['path']],'direct role outside closure '+name); roles[name]=verify(d[name])
for name in ('historical_interpreter','historical_interpreter_provenance','historical_optional_namespaces'):
    need(d[name]==prior[name],'historic role drift '+name)
source=(Q/'launch_controls.source-only.py').read_text(); controls=(P/'fault_controls.source-only.py').read_text(); monitor=(P/'prepare.py').read_text()
def tuple_text(text,key):
    match=re.search(r'^'+key+r' = \((.*?)\)\n',text,re.M|re.S)
    need(match is not None,'literal tuple '+key)
    return re.findall(r"'([^']*)'",match[1])
families={k:tuple_text(source,k) for k in ('F01','F02')}
need(all(families[k]==tuple_text(controls,k) for k in families),'literal25 tuple relation')
need(len(families['F01'])==14 and len(families['F02'])==11,'25 count')
need(source.count('P.child_run(')==1 and "P.child_run(card['child_command'], out, 'FOCUSED25', 180, env)" in source,'one exact inherited monitor call')
need('P.run(' not in source and 'P.authenticate(' not in source and 'patch.object' not in source,'forbidden direct call or patch')
need("module_bytes = captured(deps['ri135_module'])" in source and "exec(compile(module_bytes, deps['ri135_module']['path'], 'exec'), module.__dict__)" in source,'whole captured load')
need(source.index("module_bytes = captured(deps['ri135_module'])")<source.index("exec(compile(module_bytes")<source.index('    out.mkdir(mode=0o700)'),'capture/load/ownership order')
need(source.index('first = None; tails = []')<source.index('    out.mkdir(mode=0o700)')<source.index("same(ref(path), admission_pin, 'admission drift after ownership')"),'safe state before ownership')
need('def child_run(' not in source and 'def authenticate(' not in source,'no cloned monitor or authentication')
meta=read(Q/'METADATA_CHECK.json')
for row in meta['payloads_before_this_record']: verify(row)
need(meta['opaque_dependencies_authenticated']==rows,'author opaque actual identity records')
need(meta['literal_control_inventory']=={**families,'total':25},'author literal control records')
need(source.count('\n')==373,'whole launcher line count')
for name,line in meta['source_line_locations'].items():
    need(source.splitlines()[line-1].startswith('def '+name+'('),'function literal line '+name)
need(str(d['counts']['opaque_files']) in (Q/'PROTOCOL.md').read_text(),'protocol count')
# Verify direct references as administrative identities, not the content/authority of historic scientific outputs.
refchecks=[]
for location in (Q/'HANDOFF.json',Q/'METADATA_CHECK.json'):
    refs=list(typed(read(location)))
    refchecks.append({'administrative_file':str(location),'reference_count':len(refs),'identities':[verify(x) for x in refs]})
result={'schema':'ri137-independent-opaque-literal-check-v1','status':'PASS_METADATA_AND_TEXT_ONLY','source_handoff':pin(Q/'HANDOFF.json'),
 'packet_files':files,'exact_packet_namespace':h['closed_namespace'],'dependencies':observed,'dependency_count':276,'dependency_bytes':16850995,
 'prior_dependency_count':253,'inherited_unchanged':True,'additions':add,'addition_count':23,'whole_predecessor_namespaces':{'source':12,'review':6},'selected_root_support_count':5,
 'declared_exclusion_roots_checked':root_checks,'declared_exclusion_count':378,'later_namespace_exclusion_still_root_owned':True,'direct_roles':roles,
 'literal_controls':families,'controls_count':25,'source_text_checks':{'all373lines':True,'one_inherited_monitor_call':True,'whole_authenticated_capture_before_load':True,'capture_before_ownership':True,'safe_state_before_ownership':True,'no_production_entry_or_patch':True,'no_monitor_clone':True},
 'administrative_reference_checks':refchecks,
 'scope':{'target_import_compile_AST_probe_run':False,'controls_generated_or_evaluated':False,'scientific_json_body_decode':False,'current_runtime_inventory':False,'active_cards_or_admission':False,'repository_or_git':False}}
out=R/'OPAQUE_TEXT_CHECK.json'
with out.open('x') as f: json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
print(json.dumps({'output':pin(out),'counts':{'dependencies':276,'bytes':16850995,'inherited':253,'additions':23,'controls':25,'exclusion_roots':378}}))
