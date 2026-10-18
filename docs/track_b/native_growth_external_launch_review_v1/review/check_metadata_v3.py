"""Reviewer metadata/text checker only. Never imports or parses subject Python."""
from pathlib import Path
import collections
import hashlib
import json
import os
import stat
import sys

B = Path('/Volumes/AI_DATA/development/det-review-evidence')
Q = B/'ri138-native-external-launch-source-92pbd52w'
R = B/'ri138-launch-independent-review-6xGu5oak'
OLD = B/'ri136-native-policy-dispatch-source-g_z472z7'
CAP = 67108864
REPORT = {'schema':'ri138-independent-metadata-text-check-v1','scope':'Opaque hashes and plain text; new administrative references checked against direct396 closure, inherited external reference pins retained without dereference.', 'errors':[],'checks':{}}

def canonical(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True)

def need(ok,message):
    if not ok: raise ValueError(message)

def opaque(p):
    p=Path(p); need(p.is_absolute() and os.path.normpath(str(p))==str(p),'literal path')
    current=Path('/')
    for part in p.parts[1:]:
        current/=part;need(not stat.S_ISLNK(current.lstat().st_mode),'symlink '+str(current))
    s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_size<=CAP,'file type/cap')
    signature=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    h=hashlib.sha256();size=0
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        need(signature(s)==signature(os.fstat(f.fileno())),'open drift')
        for block in iter(lambda:f.read(1048576),b''):
            h.update(block);size+=len(block);need(size<=CAP,'read cap')
        need(signature(s)==signature(os.fstat(f.fileno())),'descriptor drift')
    need(signature(s)==signature(p.lstat()) and size==s.st_size,'path drift')
    return {'path':str(p),'resolved_path':str(p),'bytes':size,'sha256':h.hexdigest(),'symlinks':[]}

def ordinary(row):
    return {k:row[k] for k in ('path','bytes','sha256')}

def load(p):
    def pairs(items):
        result={}
        for k,v in items:need(k not in result,'duplicate metadata key');result[k]=v
        return result
    def bad(x):raise ValueError('nonfinite metadata')
    return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=bad)

def attempt(name,fn):
    try:REPORT['checks'][name]=fn()
    except Exception as e:REPORT['errors'].append({'check':name,'type':type(e).__name__,'message':str(e)})

def all_dependencies():
    results=[]
    for x in D['protected_files']:
        try:
            got=opaque(x['path']);need(canonical(got)==canonical(x['identity']),'whole identity mismatch '+x['path'])
            results.append({'role':x['role'],'identity':got})
        except Exception as e:REPORT['errors'].append({'check':'dependency','path':x['path'],'type':type(e).__name__,'message':str(e)})
    return {'count':len(results),'bytes':sum(x['identity']['bytes'] for x in results),'identities':results}

def source_packet():
    h=load(Q/'HANDOFF.json')
    need(ordinary(opaque(Q/'HANDOFF.json'))=={'path':str(Q/'HANDOFF.json'),'bytes':5173,'sha256':'6ee043592352d35048bb31a34aa8b550bb830a9af2afc99170db14b3806510e0'},'root-provided source handoff pin')
    for row in h['files']:need(ordinary(opaque(row['path']))==row,'source payload '+row['path'])
    need(sorted(x.name for x in Q.iterdir())==sorted([Path(x['path']).name for x in h['files']]+['HANDOFF.json']),'source namespace')
    return {'handoff':ordinary(opaque(Q/'HANDOFF.json')),'files':h['files'],'names':sorted(x.name for x in Q.iterdir())}

def lineage():
    old=load(OLD/'SOURCE_DEPENDENCIES.json');oldmap={x['path']:x for x in old['protected_files']}
    need(len(D['protected_files'])==396 and len(oldmap)==373,'closure counts')
    need([x['path'] for x in D['protected_files']]==sorted(set(x['path'] for x in D['protected_files'])),'unique sorted paths')
    for i,x in enumerate(D['protected_files'],1):need(x['role']=='dep_'+str(i).zfill(4),'role sequence')
    for p,x in oldmap.items():
        need(canonical({k:v for k,v in x.items() if k!='role'})==canonical({k:v for k,v in LOOKUP[p].items() if k!='role'}),'old entry changed '+p)
    subject=load(Q/'SOURCE_IDENTITIES.json');prior=load(OLD/'SOURCE_IDENTITIES.json')
    need(canonical(subject['subjects'])==canonical(prior['subjects']),'subject contract change')
    return {'inherited':373,'added':[x['path'] for x in D['protected_files'] if x['path'] not in oldmap],
            'case_counts':{k:len(v['ordered_cases']) for k,v in subject['subjects'].items()},
            'authorship_overlap_identity_only':[x['path'] for x in D['protected_files'] if any(y in x['path'] for y in ('ri125-independent-white-validator-source-i00kkece','ri125-white-qualifier-independent-review-qmRAU0M6'))],
            'direct_native_subjects':[subject['dispatcher']]+[v[k] for v in subject['subjects'].values() for k in ('caller','controls')]}

def references(value,where):
    out=[]
    def walk(v,trail):
        if isinstance(v,dict):
            if type(v.get('path')) is str and type(v.get('bytes')) is int and type(v.get('sha256')) is str and len(v['sha256'])==64:
                p=v['path']
                if p not in IDS:
                    out.append({'at':trail,'outside_direct_closure':True,'declared_identity':{k:v[k] for k in ('path','bytes','sha256','resolved_path','symlinks') if k in v}})
                else:
                    target=IDS[p]
                    for k in ('path','bytes','sha256','resolved_path','symlinks'):
                        if k in v:need(canonical(v[k])==canonical(target[k]),'reference mismatch '+p+' '+k+' at '+where+trail)
                    out.append({'at':trail,'outside_direct_closure':False,'identity':ordinary(target)})
            for k,item in v.items():walk(item,trail+'.'+k)
        elif isinstance(v,list):
            for i,item in enumerate(v):walk(item,trail+'['+str(i)+']')
    walk(value,'$');return out

def admin_closure():
    results=[]
    inherited={x['path'] for x in load(OLD/'SOURCE_DEPENDENCIES.json')['protected_files']}
    for entry in D['protected_files']:
        if entry['access_policy']=='metadata-identities-only-no-scientific-body-decoding':
            try:
                need(ordinary(opaque(entry['path']))==ordinary(entry['identity']),'admin before drift')
                refs=references(load(entry['path']),entry['path'])
                need(ordinary(opaque(entry['path']))==ordinary(entry['identity']),'admin after drift')
                if entry['path'] not in inherited:need(not any(x['outside_direct_closure'] for x in refs),'new administrative reference outside closure')
                results.append({'path':entry['path'],'inherited':entry['path'] in inherited,'references':refs})
            except Exception as e:REPORT['errors'].append({'check':'administrative references','path':entry['path'],'type':type(e).__name__,'message':str(e)})
    subject_refs=references(load(Q/'SOURCE_IDENTITIES.json'),str(Q/'SOURCE_IDENTITIES.json'))
    need(not any(x['outside_direct_closure'] for x in subject_refs),'subject reference outside closure')
    summary = {'bodies':len(results),'reference_count':sum(len(x['references']) for x in results),'new_bodies':sum(not x['inherited'] for x in results),'new_references':sum(len(x['references']) for x in results if not x['inherited']),'external_inherited_reference_occurrences':sum(sum(v['outside_direct_closure'] for v in x['references']) for x in results),'external_referents_opened':False,'bodies_and_references':results,'subject_references':subject_refs,
            'opaque_bodies_decoded':0,'own_retained_WHITE_semantic_review':False}
    compact=[]
    for row in results:
        refs=row['references']
        compact.append({'path':row['path'],'inherited':row['inherited'],'reference_count':len(refs),'external_reference_count':sum(x['outside_direct_closure'] for x in refs),'canonical_references_sha256':hashlib.sha256(canonical(refs).encode()).hexdigest()})
    summary['bodies_and_references']=compact
    summary['full_occurrences_retained_in']='OPAQUE_TEXT_CHECK_V2.json'
    return summary

def correspondence():
    c=load(Q/'SOURCE_CORRESPONDENCE.json');results=[]
    for group,oldrole,newrole in (('custody','ri134_native','custody'),('launcher','ri136_dispatcher','launcher')):
        before=Path(c['sources'][oldrole]['path']).read_text().splitlines(keepends=True)
        after=Path(c['sources'][newrole]['path']).read_text().splitlines(keepends=True)
        for row in c['exact_unchanged_definitions'][group]:
            a=''.join(before[row['old_start']-1:row['old_end']]).encode();b=''.join(after[row['new_start']-1:row['new_end']]).encode()
            need(a==b,'definition text changed '+row['name'])
            need(len(b)==row.get('bytes',row.get('whole_definition_bytes')) and hashlib.sha256(b).hexdigest()==row['sha256'],'definition pin '+row['name'])
            results.append({'component':group,'name':row['name'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    return {'literal_definition_checks':results,'source_lines':{x:len((Q/x).read_text().splitlines()) for x in ('custody.py','owned_process.py','launch_policy_case.py')},'subject_syntax_or_AST_parsed':False}

try:
    D=load(Q/'SOURCE_DEPENDENCIES.json');LOOKUP={x['path']:x for x in D['protected_files']};IDS={p:x['identity'] for p,x in LOOKUP.items()}
    IDS[str(Q/'SOURCE_DEPENDENCIES.json')]=opaque(Q/'SOURCE_DEPENDENCIES.json')
    for name,fn in [('source_packet',source_packet),('dependencies',all_dependencies),('lineage',lineage),('administrative_closure',admin_closure),('literal_correspondence',correspondence)]:attempt(name,fn)
except Exception as e:REPORT['errors'].append({'check':'checker startup','type':type(e).__name__,'message':str(e)})
REPORT['success']=not REPORT['errors'];REPORT['source_execution']=False;REPORT['runtime_inventory']=False;REPORT['scientific_body_decode']=False
p=R/'OPAQUE_TEXT_CHECK_V3.json'
with p.open('x') as f:json.dump(REPORT,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'success':REPORT['success'],'error_count':len(REPORT['errors']),'report':ordinary(opaque(p)),
                  'dependency_count':REPORT['checks'].get('dependencies',{}).get('count'),
                  'administrative_bodies':REPORT['checks'].get('administrative_closure',{}).get('bodies'),
                  'reference_count':REPORT['checks'].get('administrative_closure',{}).get('reference_count')},sort_keys=True))
sys.exit(0 if REPORT['success'] else 1)
