"""Independent administrative byte/text checks only. No subject interpretation."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import stat
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
Q=B/'ri144-bootstrap-guard-source-oaj1jvyt'
R=B/'ri144-independent-guard-review-qytlt8l3'
ARCHIVE=Path('/Volumes/AI_DATA/development/det_8_framework-ret/docs/experiments/gwosc_joint_window_covariance_v1')
ARCHIVE_NAMES={'DESIGN.md','INDEPENDENT_PROOF_REVIEW.json','REVIEW.md','ROOT_ADJUDICATION.json'}
read_pins={}
def need(ok,msg):
    if not ok: raise ValueError(msg)
def enc(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def pure(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def body(p):
    p=Path(p);need(p.is_absolute() and (B in p.parents or (p.parent==ARCHIVE and p.name in ARCHIVE_NAMES)),'only saved external evidence/four pinned archive paths')
    need(p.resolve(strict=True)==p,'literal evidence path')
    s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_size<=67108864,'bounded regular evidence')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        need(state(os.fstat(f.fileno()))==state(s),'open drift');b=f.read(67108865);need(state(os.fstat(f.fileno()))==state(s),'descriptor drift')
    need(state(p.lstat())==state(s) and len(b)==s.st_size,'final drift')
    row={'path':str(p),**pure(b)}
    if str(p) in read_pins:need(read_pins[str(p)]==row,'repeat identity drift')
    read_pins[str(p)]=row;return b
def pin(p):return {'path':str(p),**pure(body(p))}
def check(row):
    need(set(row)=={'path','bytes','sha256'},'closed FilePin')
    need(pin(row['path'])==row,'pin mismatch '+row['path']);return row
def admin(p):
    b=body(p)
    def pairs(items):
        x={}
        for k,v in items:need(k not in x,'duplicate metadata');x[k]=v
        return x
    x=json.loads(b,object_pairs_hook=pairs);need(enc(x)==b,'canonical metadata '+str(p));return x
hpin=pin(Q/'HANDOFF.json');need(hpin['bytes']==9005 and hpin['sha256']=='2c0da438ab15490d4f3c5ac4c557ef2ddedc879d8f97def7f77537fbd5588796','root exact handoff')
h=admin(Q/'HANDOFF.json');need(len(h['files'])==9 and len(h['exact_namespace'])==10,'10 packet files')
need(sorted(p.name for p in Q.iterdir())==h['exact_namespace'],'exact packet namespace')
for x in h['files']:check(x)
packet=[pin(Q/n) for n in h['exact_namespace']]
d=admin(Q/'DEPENDENCIES.source-only.json');c=admin(Q/'SOURCE_CORRESPONDENCE.json');a=admin(Q/'METADATA_CHECK.json');diagnostics=admin(Q/'AUTHOR_DIAGNOSTICS.json')
rows=d['opaque_files'];need(len(rows)==472 and len({x['path'] for x in rows})==472,'472 unique')
for x in rows:check(x)
need(sum(x['bytes'] for x in rows)==26701752,'26701752 opaque bytes')
lookup={x['path']:x for x in rows}
old=admin(d['target_dependencies']['path']);prior={x['path']:x for x in old['opaque_files']}
need(len(prior)==442 and all(lookup.get(k)==v for k,v in prior.items()),'all442 inherited')
added=sorted((x for k,x in lookup.items() if k not in prior),key=lambda x:x['path'])
need(len(added)==30 and added==a['dependencies']['additions'],'30 exact additions')
old139=admin(d['bootstrap_selection_provenance']['path'])
need(len(old139['opaque_files'])==310 and all(lookup.get(x['path'])==x for x in old139['opaque_files']),'old310 subset')
for k,x in d.items():
    if isinstance(x,dict) and set(x)=={'path','bytes','sha256'}:need(lookup.get(x['path'])==x,'direct role '+k)
need(d['selected_bootstrap_binding']==old['selected_bootstrap_binding']==old139['selected_bootstrap_binding'],'whole selected historical row')
ns=[]
for role,expected in [('target_handoff',15),('target_review',10)]:
    ph=admin(d[role]['path']);root=Path(d[role]['path']).parent;names=ph['exact_namespace']
    need(sorted(p.name for p in root.iterdir())==names and len(names)==expected,'complete predecessor namespace '+role)
    for name in names:need(lookup.get(str(root/name))==pin(root/name),'complete predecessor pin '+role)
    for x in ph['files']:check(x)
    ns.append({'role':role,'directory':str(root),'names':names})
roots=d['sealed_namespace_roots'];need(len(roots)==393 and roots==sorted(set(roots)),'393 unique sorted protected roots')
for root in roots:need(Path(root).is_absolute() and str(Path(root))==root and '..' not in Path(root).parts,'literal protected root spelling')
for row in rows:need(any(Path(x) in Path(row['path']).parents for x in roots),'dependency protected by root domain '+row['path'])
need(str(Q) in roots,'new source namespace protected')
# No protected-root or current supplier enumeration is performed.
decision=admin(d['target_adjudication']['path'])
need(decision['status']=='ACCEPT_EXACT_SOURCE_WITH_EXECUTION_PREREQUISITES' and decision['execution_admitted'] is False and decision['source_handoff']==d['target_handoff'],'historical target source-only decision')
monitor_decision=admin(d['ri135_root_adjudication']['path']);need(monitor_decision['source_accepted'] is True and monitor_decision['execution_admitted'] is False,'monitor source decision')
actual25=admin(d['ri139_actual_acceptance']['path']);need(actual25['counts']=={'total':25,'passed':25,'positives':2,'expected_refusals':23} and actual25['future_execution_admitted'] is False,'old25 scoped acceptance')
oldpath=Path(d['ri139_launcher']['path']);oldbody=body(oldpath)
newbody=body(Q/'launch_controls.source-only.py');harness=body(Q/'bootstrap_controls.source-only.py')
monitor=body(d['ri135_module']['path']);target=body(d['target_module']['path'])
need(c['before']==pin(oldpath) and c['after']==pin(Q/'launch_controls.source-only.py'),'full wrapper identities')
need(c['new_control_source']==pin(Q/'bootstrap_controls.source-only.py'),'full child identity')
need(c['qualified_monitor_whole_source']==d['ri135_module'] and c['exact_target_module']==d['target_module'],'exact selected whole operands')
def slices(data):
    lines=data.splitlines(True);starts=[]
    for i,line in enumerate(lines):
        m=re.match(rb'^def ([A-Za-z_][A-Za-z_0-9]*)\(',line)
        if m:starts.append((i,m[1].decode('ascii')))
    result={}
    for index,(i,name) in enumerate(starts):
        end=starts[index+1][0] if index+1<len(starts) else len(lines)
        for k in range(i+1,end):
            if lines[k].startswith(b'if __name__'):end=k;break
        span=b''.join(lines[i:end]);result[name]={'start':i+1,'end':end,'body':span,**pure(span)}
    return result
oslices=slices(oldbody);nslices=slices(newbody);hslices=slices(harness);tslices=slices(target);mslices=slices(monitor)
unchanged=sorted(k for k in oslices.keys()&nslices.keys() if oslices[k]['body']==nslices[k]['body'])
changed=sorted(k for k in oslices.keys()&nslices.keys() if oslices[k]['body']!=nslices[k]['body'])
need(len(unchanged)==14 and unchanged==[x['name'] for x in c['unchanged_existing_definition_spans']],'14 unchanged literal spans')
need(changed==sorted(x['name'] for x in c['changed_existing_definition_spans']) and len(changed)==4,'4 changed literal spans')
need(sorted(oslices.keys()-nslices.keys())==c['removed_existing_definitions']==['inspect_f01','inspect_f02'],'2 old inspector removals')
need(sorted(nslices.keys()-oslices.keys())==c['added_definitions']==['recipe'],'only recipe addition')
for row in c['unchanged_existing_definition_spans']+c['changed_existing_definition_spans']:
    n=row['name'];need([oslices[n]['start'],oslices[n]['end']]==row['before_lines'],'old span endpoints '+n)
    need([nslices[n]['start'],nslices[n]['end']]==row['after_lines'],'new span endpoints '+n)
    if 'sha256' in row:need({k:nslices[n][k] for k in ('bytes','sha256')}=={k:row[k] for k in ('bytes','sha256')},'span pin '+n)
helpers=c['same_13_copied_helper_spans_in_control_and_launcher'];need(len(helpers)==13,'13 helper spans')
for k in helpers:need(oslices[k]['body']==nslices[k]['body']==hslices[k]['body'],'copied helper '+k)
need(nslices['recipe']['body']==hslices['recipe']['body'],'complete recipe source equality only, never evaluated')
need(c['exact_target_selected_bootstrap']=={k:v for k,v in tslices['selected_bootstrap'].items() if k!='body'},'target full span pin')
need(c['qualified_monitor_unchanged_function']=={k:v for k,v in mslices['child_run'].items() if k!='body'},'monitor full span pin')
# Environment function body excludes later top-level ID declarations.
def envbody(x):return x['environment']['body'].split(b'\n\n',1)[0]
need(envbody(oslices)==envbody(nslices)==envbody(hslices)==envbody(mslices),'exact inherited environment body')
for marker,end in [(b'LIMITS = ',b'\nPREMISES ='),(b'PREMISES = ',b'\n\n')]:
    need(oldbody.split(marker,1)[1].split(end,1)[0]==newbody.split(marker,1)[1].split(end,1)[0],'unchanged literal global '+marker.decode())
exactdiff=(''.join(difflib.unified_diff(oldbody.decode().splitlines(True),newbody.decode().splitlines(True),fromfile=str(oldpath),tofile=str(Q/'launch_controls.source-only.py')))+''.join(difflib.unified_diff([],harness.decode().splitlines(True),fromfile='/dev/null',tofile=str(Q/'bootstrap_controls.source-only.py')))).encode()
need(exactdiff==body(Q/'REPAIR.diff'),'entire two-part delta exact')
for source in (newbody,harness):
    need(d['selected_bootstrap_binding']['path'].encode() in source,'direct supplier literal')
    need(str(len(body(Q/'DEPENDENCIES.source-only.json'))).encode() in source and pure(body(Q/'DEPENDENCIES.source-only.json'))['sha256'].encode() in source,'literal dependency identity')
ids=['B01','B02','B03','B04','B05','B06','B07_path','B07_resolved_path','B07_symlink_chain','B07_bytes','B07_sha256','B07_state','B08','B09','B10']
need(h['declared_controls']==ids and h['declared_positive_expectations']==1 and h['declared_refusal_expectations']==14,'closed source handoff case domain')
need(h['declared_success_namespace_entries']=={'child':33,'parent_with_child':43},'namespace source declaration arithmetic')
need(len(newbody.splitlines())==397 and len(harness.splitlines())==339,'complete736 lines')
for x in packet:check(x)
need(sorted(p.name for p in Q.iterdir())==h['exact_namespace'],'final source namespace unchanged')
result={'schema':'ri144-independent-opaque-text-check-v1','status':'PASS_METADATA_AND_LITERAL_TEXT_ONLY','source_handoff':hpin,'source_packet':packet,'opaque_dependencies':rows,
 'counts':{'opaque_files':472,'opaque_bytes':26701752,'preserved_ri141':442,'additions':30,'preserved_ri139_subset':310,'protected_roots':393},'additions':added,'predecessor_namespaces':ns,
 'correspondence':{'unchanged':unchanged,'changed':changed,'removed':c['removed_existing_definitions'],'added':['recipe'],'same_helpers':helpers,'same_recipe_text':True,'whole_monitor_source':d['ri135_module'],'monitor_span':c['qualified_monitor_unchanged_function'],'target_span':c['exact_target_selected_bootstrap'],'diff':pin(Q/'REPAIR.diff'),'same_limits_premises_environment':True},
 'declared_control_ids':ids,'source_lines':{'launcher':397,'harness':339},'historical_source_decision':d['target_adjudication'],'reviewer_checker':pin(Path(__file__)),
 'method':'Independent standard-library saved evidence hashing, administrative JSON and regex-delimited literal slices. No subject parser/compiler/evaluator/import or recipe execution.',
 'no_current_supplier_or_runtime_referents':True,'scientific_body_decode':False,'controls_executed':0,'execution_admitted':False,'repo_index_git':False,'errors':[]}
with (R/'OPAQUE_TEXT_CHECK.json').open('xb') as f:f.write(enc(result))
print(json.dumps({'status':result['status'],'result':pin(R/'OPAQUE_TEXT_CHECK.json'),'counts':result['counts']},sort_keys=True))
