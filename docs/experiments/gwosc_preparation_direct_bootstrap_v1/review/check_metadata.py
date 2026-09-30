"""Reviewer-owned opaque metadata and literal text check; no target interpretation."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import stat

B = Path('/Volumes/AI_DATA/development/det-review-evidence')
Q = B/'ri141-white-bootstrap-source-h58ls076'
R = B/'ri141-bootstrap-independent-review-k5bss5xp'
P = B/'ri135-white-preparation-repair-source-lski1ize'
reads = {}
ARCHIVE = Path('/Volumes/AI_DATA/development/det_8_framework-ret/docs/experiments/gwosc_joint_window_covariance_v1')
ARCHIVE_NAMES = {'DESIGN.md','INDEPENDENT_PROOF_REVIEW.json','REVIEW.md','ROOT_ADJUDICATION.json'}

def need(value, reason):
    if not value:
        raise ValueError(reason)

def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')

def pure(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def state(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read(path):
    path=Path(path)
    need(path.is_absolute() and (B in path.parents or (path.parent == ARCHIVE and path.name in ARCHIVE_NAMES)), 'external evidence only, no vendor/current-runtime referent')
    need(path.resolve(strict=True)==path, 'no linked component')
    a=path.lstat(); need(stat.S_ISREG(a.st_mode) and a.st_size<=67108864,'bounded regular evidence')
    with os.fdopen(os.open(path,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        need(state(os.fstat(f.fileno()))==state(a),'opened evidence drift')
        body=f.read(67108865)
        need(state(os.fstat(f.fileno()))==state(a),'read evidence drift')
    need(state(path.lstat())==state(a) and len(body)==a.st_size,'final evidence drift')
    row={'path':str(path),**pure(body)}
    if str(path) in reads: need(reads[str(path)]==row,'repeated evidence drift')
    reads[str(path)]=row
    return body

def pin(path):
    return {'path':str(path),**pure(read(path))}

def check(row):
    need(set(row)=={'path','bytes','sha256'},'exact FilePin')
    need(pin(row['path'])==row,'opaque pin mismatch '+row['path'])
    return row

def admin(path):
    data=read(path)
    def pairs(items):
        result={}
        for key,value in items:
            need(key not in result,'duplicate administrative key');result[key]=value
        return result
    value=json.loads(data,object_pairs_hook=pairs)
    need(canonical(value)==data,'administrative canonical JSON '+str(path))
    return value

def namespace(root):
    rows=[]; stack=[root]
    while stack:
        at=stack.pop()
        for path in sorted(at.iterdir()):
            s=path.lstat(); rel=str(path.relative_to(root))
            if stat.S_ISDIR(s.st_mode): rows.append({'relative':rel,'kind':'directory'});stack.append(path)
            else:
                need(stat.S_ISREG(s.st_mode),'unexpected namespace link/special '+str(path))
                rows.append({'relative':rel,'kind':'file',**pure(read(path))})
    return sorted(rows,key=lambda x:x['relative'])

handoff_pin=pin(Q/'HANDOFF.json')
need(handoff_pin['bytes']==9366 and handoff_pin['sha256']=='40effed085b2b79cd8933d675ec627e51c2910d95ea1f2e02ea75d2927c40f65','root selected handoff')
h=admin(Q/'HANDOFF.json')
need(sorted(p.name for p in Q.iterdir())==h['exact_namespace'],'exact15 source namespace')
need(len(h['files'])==14 and len(h['exact_namespace'])==15,'packet count')
for row in h['files']: check(row)
packet=[pin(Q/name) for name in h['exact_namespace']]
d=admin(Q/'DEPENDENCIES.source-only.json'); old=admin(P/'DEPENDENCIES.source-only.json')
a=admin(Q/'DEPENDENCY_ADDITIONS.json'); claimed=admin(Q/'METADATA_CHECK.json')
opaque=d['opaque_files']; need(len(opaque)==442 and len({x['path'] for x in opaque})==442,'unique442')
for row in opaque:check(row)
need(sum(x['bytes'] for x in opaque)==25947539,'25,947,539 total opaque bytes')
lookup={x['path']:x for x in opaque}; prior={x['path']:x for x in old['opaque_files']}
need(len(prior)==253 and all(lookup.get(k)==v for k,v in prior.items()),'all253 prior exact')
added=sorted((v for k,v in lookup.items() if k not in prior),key=lambda x:x['path'])
need(len(added)==189 and added==a['added'],'exact189 additions')
need(a['predecessor']==pin(P/'DEPENDENCIES.source-only.json'),'dependency predecessor')
for key in ('packet_root','packet_handoff','packet_namespace','historical_runtime','historical_optional_namespaces','historical_interpreter','historical_interpreter_provenance','root_adjudication','predecessor_source','repair_adjudication'):
    need(d[key]==old[key],'retained role '+key)
need(d['counts']=={'historical_file_roles':124,'opaque_unique_bytes':25947539,'opaque_unique_dependencies':442,'sealed_ri130_files':48,'target_original_copy_pairs':30},'all declaredcounts')
for k,v in d.items():
    if isinstance(v,dict) and set(v)=={'path','bytes','sha256'}:need(lookup.get(v['path'])==v,'complete direct dependency role '+k)
need(claimed['opaque_dependencies']==opaque,'author opaque table correspondence only')
need(claimed['all_checks_passed'] is True and claimed['errors']==[],'author result status (not independent proof)')

packet_root=Path(d['packet_root']); packet_rows=namespace(packet_root)
need(packet_rows==d['packet_namespace'] and len(packet_rows)==52,'exact RI130 namespace52')
need(sum(x['kind']=='file' for x in packet_rows)==48,'RI13048 files')
targets=admin(packet_root/'TARGET_CLOSURE.source-only.json')
history=admin(packet_root/'HISTORY_CLOSURE.source-only.json')
need(len(targets['sources'])==30 and len(history)==124,'30 pairs and124 historical roles')
pairs=[]
for row in targets['sources']:
    o=pin(row['original']); c=pin(packet_root/row['relative'])
    need({k:o[k] for k in ('bytes','sha256')}==row['pin']=={k:c[k] for k in ('bytes','sha256')},'original/copy exact')
    need(lookup.get(o['path'])==o and lookup.get(c['path'])==c,'pair both in closure')
    pairs.append({'original':o,'copy':c})
for row in history:need(lookup.get(row['path'])==row,'all124 historical roles in closure')

historical_namespaces=[]
for record in claimed['historical_namespaces']:
    root=Path(record['directory']); check(record['handoff'])
    need(sorted(p.name for p in root.iterdir())==record['names'],'complete historical namespace')
    for name in record['names']:need(lookup.get(str(root/name))==pin(root/name),'historical namespace file in closure')
    historical_namespaces.append({'directory':str(root),'files':len(record['names']),'exact_names':record['names']})
need([x['files'] for x in historical_namespaces]==[12,8,7,8],'four namespaces sizes')
operation=B/'ri139-focused25-run-6_wa8gqh'; op_rows=namespace(operation)
opfiles=[{'path':str(operation/x['relative']),'bytes':x['bytes'],'sha256':x['sha256']} for x in op_rows if x['kind']=='file']
need(sorted(opfiles,key=lambda x:x['path'])==a['actual_operation_files'] and len(opfiles)==89,'all89 retained operation files')
for row in opfiles:need(lookup.get(row['path'])==row,'complete operation closure')
need(len(a['selected_root_names'])==20,'selected20 root records')
root139=B/'ri139-root-bootstrap-adjudication-goau3dIc'
for name in a['selected_root_names']:need(lookup.get(str(root139/name))==pin(root139/name),'selected root record')

provenance=admin(d['bootstrap_selection_provenance']['path'])
need(provenance['selected_bootstrap_binding']==d['selected_bootstrap_binding'],'selected provenance fullbinding')
need(provenance['historical_bootstrap_observation']==d['historical_bootstrap_observation'],'selected observation provenance')
historical=admin(d['historical_bootstrap_observation']['path']); selected=d['selected_bootstrap_binding']
matching=[x for x in historical['framework_namespace'] if x['path']==selected['path']]
need(len(matching)==1,'historical framework target row')
row=matching[0]
need(row['kind']=='file' and row['identity']==selected,'selected bytes/state from saved genuine framework evidence')
need(selected['resolved_path']==selected['path'] and selected['symlink_chain']==[],'literal direct historical binding')

corr=admin(Q/'SOURCE_CORRESPONDENCE.json')
newb={name:read(Q/name) for name in ('prepare.py','runtime_metadata.py','fault_controls.source-only.py')}
oldb={name:read(P/name) for name in newb}
for role,root,bodies in [('new',Q,newb),('old',P,oldb)]:
    need(corr['sources'][role]=={n:{'path':str(root/n),**pure(b)} for n,b in bodies.items()},'source declaration '+role)
def intervals(data):
    lines=data.splitlines(keepends=True); starts=[]
    for i,line in enumerate(lines):
        match=re.match(rb'^def ([A-Za-z_][A-Za-z_0-9]*)\(',line)
        if match:starts.append((i,match[1].decode('ascii')))
    result={}
    for n,(i,name) in enumerate(starts):
        end=starts[n+1][0] if n+1<len(starts) else len(lines)
        for k in range(i+1,end):
            if lines[k].startswith(b'if __name__'):end=k;break
        while end>i and not lines[end-1].strip():end-=1
        data=b''.join(lines[i:end]);result[name]={'start':i+1,'end':end,**pure(data),'body':data}
    return result
newsp={n:intervals(newb[n]) for n in ('prepare.py','runtime_metadata.py')}
oldsp={n:intervals(oldb[n]) for n in ('prepare.py','runtime_metadata.py')}
need(sum(len(x) for x in newsp.values())==46 and sum(len(x) for x in oldsp.values())==45,'function definition counts')
need({(x['file'],x['name']) for x in corr['functions']}=={(n,k) for n,rows in newsp.items() for k in rows},'whole correspondence domain')
checked=[]
for item in corr['functions']:
    n=item['file']; k=item['name']; now=newsp[n][k]; need(item['new']=={a:b for a,b in now.items() if a!='body'},'new literal span '+k)
    if 'old' in item:
        before=oldsp[n][k]; need(item['old']=={a:b for a,b in before.items() if a!='body'},'old literal span '+k)
        equal=before['body']==now['body']; need(equal==item['identical'],'span comparison '+k)
    else:need(k=='selected_bootstrap' and item['added'] is True,'only one addition');equal=None
    checked.append({'file':n,'name':k,'identical':equal,'new':item['new'],'old':item.get('old')})
need(sum(x['identical'] is True for x in checked)==43 and sum(x['identical'] is False for x in checked)==2,'43unchanged2changed')
need(oldb['fault_controls.source-only.py']==newb['fault_controls.source-only.py'],'complete297line focusedharness exact')
complete_diff=''.join(''.join(difflib.unified_diff(oldb[n].decode().splitlines(True),newb[n].decode().splitlines(True),fromfile=str(P/n),tofile=str(Q/n))) for n in ('prepare.py','runtime_metadata.py','fault_controls.source-only.py')).encode()
need(complete_diff==read(Q/'REPAIR.diff'),'complete exact delta')
need(newb['prepare.py'].count(b"[BOOTSTRAP, '-I', '-B'")==oldb['prepare.py'].count(b"[BOOTSTRAP, '-I', '-B'")==4,'four command sites')
need(b"'/usr/bin/python3'" not in newb['prepare.py']+newb['runtime_metadata.py'],'old bootstrap literal removed')
need(newb['prepare.py'].split(b'BOUNDS = ',1)[1].split(b'\nM =',1)[0]==oldb['prepare.py'].split(b'BOUNDS = ',1)[1].split(b'\nM =',1)[0],'whole BOUNDS text exact')
need(newb['prepare.py'].split(b'GUARD_IDS = ',1)[1].split(b'\nBOUNDS =',1)[0]==oldb['prepare.py'].split(b'GUARD_IDS = ',1)[1].split(b'\nBOUNDS =',1)[0],'whole65ID construction exact')
for n in ('prepare.py','runtime_metadata.py'):
    match=re.search(rb"^BOOTSTRAP = '([^']+)'$",newb[n],re.M);need(match and match[1].decode()==selected['path'],'shared exact supplier '+n)

design=admin(Q/'BOOTSTRAP_VERIFICATION_DESIGN.json')
need([x['id'] for x in design['isolated_cases']]==['B%02d'%i for i in range(1,11)],'ten prospective categories')
need(design['single_value_variants_B07']==['path','resolved_path','symlink_chain','bytes','sha256','state'],'six B07 variants')
need(design['inherited_actual25']['changed_source_controls_executed']==0,'no new control claim')
for row in packet:check(row)
need(sorted(p.name for p in Q.iterdir())==h['exact_namespace'],'unchanged final packet namespace')
result={'schema':'ri141-independent-opaque-source-check-v1','status':'PASS_METADATA_AND_LITERAL_TEXT_ONLY','source_handoff':handoff_pin,
 'source_packet':packet,'dependency_counts':{'total':442,'bytes':25947539,'preserved':253,'added':189},'opaque_dependencies':opaque,
 'ri130_namespace':packet_rows,'original_copy_pairs':pairs,'history_role_count':124,'historical_namespaces':historical_namespaces,
 'operation_counts':{'files':len(opfiles),'directories':sum(x['kind']=='directory' for x in op_rows)},'selected_root_records':a['selected_root_names'],
 'source_spans':checked,'source_lines':{n:len(b.splitlines()) for n,b in newb.items()},'exact_full_diff':pin(Q/'REPAIR.diff'),
 'bootstrap_historical_binding':selected,'prospective_categories':10,'B07_variants':6,'expanded_prospective_expectations':15,
 'metadata_source':pin(Path(__file__)),'read_unique_evidence_files':len(reads),
 'limits':{'target_import_compile_AST_probe_run':False,'target_syntax_validated':False,'scientific_body_decode':False,'current_vendor_runtime_observation':False,'fixtures_controls_executed':False,'repo_git_mutations':False},
 'errors':[]}
with (R/'OPAQUE_SOURCE_CHECK.json').open('xb') as f:f.write(canonical(result))
print(json.dumps({'status':result['status'],'result':pin(R/'OPAQUE_SOURCE_CHECK.json'),'counts':result['dependency_counts'],'read_evidence_files':len(reads)},sort_keys=True))
