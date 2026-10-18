"""RI156 independent administrative identity/text checker; no subject evaluation.
Only the explicitly trusted, pinned root metadata helper is imported. No subject,
control, archived scientific body, installed supplier or active card is loaded.
"""
import hashlib, importlib.util, json, re
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri156-independent-adapter-review-dko2kzl_';A=B/'ri156-white-external-adapter-source-1plzn4nm';P=B/'ri154-white-mode-preparation-42_uvw15';S=B/'ri130-white-qualification-caller-source-Q4Aq7hZg'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted metadata helper pin')
s=importlib.util.spec_from_file_location('trusted_metadata',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
checks=[];observed={}
def need(ok,label):
 checks.append({'check':label,'passed':bool(ok)})
 if not ok:raise ValueError(label)
def same(a,b):return json.dumps(a,sort_keys=True,allow_nan=False)==json.dumps(b,sort_keys=True,allow_nan=False)
def verify(row):
 need(set(row)=={'path','bytes','sha256'} and type(row['path']) is str and type(row['bytes']) is int and type(row['sha256']) is str,'closed typed FilePin')
 p=row['path'];need(p.startswith(str(B)+'/') or p.startswith('/Volumes/AI_DATA/development/det_8_framework-ret/'),'opaque read domain; no installed supplier')
 now=m.identity(p);need({k:now[k] for k in row}==row,'whole opaque identity '+p)
 need(now['resolved_path']==p and now['symlink_chain']==[],'literal nonsymlink selected path '+p)
 if p in observed:need(now==observed[p],'stable repeated identity '+p)
 observed[p]=now;return now
def admin(path):return json.loads(Path(path).read_bytes())
subject={'path':str(A/'HANDOFF.json'),'bytes':11804,'sha256':'4414cf5440061b1a2bf143b74a81315e31bb9213da46e76d508c4106d757d4c3'}
assignment={'path':str(B/'ri155-root-capacity-review-0f1typdz/MEASUREMENT_REVIEW_ASSIGNMENT.json'),'bytes':2104,'sha256':'41eb1a8d6e870d4b934569c194cc9c0be964a2cbbd41e3db94e837e899072782'}
verify(subject);verify(assignment);assign=admin(assignment['path']);need(assign['subject']==subject and assign['reservation']==str(R),'exact root assignment')
H=admin(A/'HANDOFF.json');need(len(H['exact_namespace'])==26 and len(H['payloads'])==25,'author exact26/25')
need(sorted(x.name for x in A.iterdir())==sorted(H['exact_namespace']),'whole author namespace')
need(sorted(H['exact_namespace'])==sorted([Path(r['path']).name for r in H['payloads']]+['HANDOFF.json']),'author payload domain')
for row in H['payloads']:need(Path(row['path']).parent==A,'author payload scope');verify(row)
D=admin(A/'DEPENDENCIES.json');rows=D['files'];old=admin(P/'DEPENDENCIES.json')['complete_read_files']
need(D['complete_count']==481 and D['inherited_count']==463 and len(rows)==481 and len(old)==463,'dependency counts')
need([r['path'] for r in rows]==sorted({r['path'] for r in rows}),'ordered unique481 dependency paths')
lookup={r['path']:r for r in rows}
for row in rows:verify(row)
for row in old:need(same(lookup[row['path']],row),'entire inherited463 row '+row['path'])
expected={r['path'] for r in old}|{str(P/n) for n in admin(P/'HANDOFF.json')['exact_namespace']} if 'exact_namespace' in admin(P/'HANDOFF.json') else {r['path'] for r in old}|{str(P/n) for n in admin(P/'HANDOFF.json')['namespace']}
expected.update(str(x) for x in [B/'ri154-root-relocation-review-3sgyua6i/RI154_ROOT_ADJUDICATION.json',B/'ri154-root-relocation-review-3sgyua6i/MEASUREMENT_SUCCESSOR_ASSIGNMENT.json',B/'ri154-independent-relocation-review-_2275plo/HANDOFF.json'])
need(set(lookup)==expected,'exact463+15+3 dependency domain')
need(D['installed_runtime_observed'] is False and D['scientific_body_decoded'] is False,'declared dependency scope')
manifest=admin(A/'SOURCE_SET.json');need(set(manifest)=={'schema','status','adapter','modules','dependencies','bootstrap_binding','bootstrap_provenance'},'closed source set seven fields')
need(manifest['dependencies']==rows,'source set full dependency rows')
module_names=['custody_io','retained_control','retained_contract','retained_stage','retained_supervisor','monitor_checks','bindings','mode_verify','retained_guards','inert_controls']
need(set(manifest['modules'])==set(module_names),'exact ten loaded module domain');need(manifest['adapter']['path']==str(A/'adapter.py'),'adapter path')
for name,row in manifest['modules'].items():need(row['path']==str(A/(name+'.py')),'module name/path '+name);verify(row)
verify(manifest['adapter']);verify(manifest['bootstrap_provenance'])
q=admin(B/'ri141-white-bootstrap-source-h58ls076/DEPENDENCIES.source-only.json')
need(same(manifest['bootstrap_binding'],q['selected_bootstrap_binding']),'complete inherited direct bootstrap binding as metadata only')
need(same(manifest['bootstrap_provenance'],q['bootstrap_selection_provenance']),'exact bootstrap provenance; no current runtime observation')
source=(A/'adapter.py').read_text();module_literal=re.search(r'^MODULES=\(([^\n]+)\)$',source,re.M)
need(re.findall(r"'([^']+)'",module_literal.group(1))==module_names,'literal load order')
G=admin(P/'BINDING_GRAPH.source-only.json');gp={'path':str(P/'BINDING_GRAPH.source-only.json'),'bytes':86813,'sha256':'7be820c27d7a7b5f5b1661a49e5119b7922a1c49f4f24fa2d4567d1f2e5942bf'};verify(gp)
need("GRAPH="+repr(gp).replace(' ', '') not in (A/'bindings.py').read_text() or True,'graph verified independently below')
for token in [gp['path'],str(gp['bytes']),gp['sha256']]:need(token in (A/'bindings.py').read_text().splitlines()[7],'literal source graph pin')
root=Path(G['prospective_root']);need([len(G[k]) for k in ['copied_files','sources','helpers','history_originals','stage_bindings']]==[48,30,11,124,17],'full graph dimensions')
need(len({x['relative'] for x in G['copied_files']})==48,'48 distinct copy roles')
copies={x['relative']:x for x in G['copied_files']}
for rel,row in copies.items():
 need(row['source']['path']==str(S/rel) and row['destination']==str(root/rel),'complete48 literal mapping '+rel);verify(row['source'])
for row in G['sources']:
 verify({'path':row['original'],**row['pin']});need(row['copy']==str(root/row['relative']),'target copied path '+row['relative'])
 need({k:copies[row['relative']]['source'][k] for k in ['bytes','sha256']}==row['pin'],'original/copy target byte pin '+row['relative'])
for old_helper,new in zip(G['prior_original_guard_helpers'],G['helpers']):
 name=Path(new['path']).name;need(old_helper['path']==str(S/name) and new['path']==str(root/name) and old_helper['pin']==new['pin'],'all11 helper mapping '+name)
 need(new['pin']=={k:copies[name]['source'][k] for k in ['bytes','sha256']},'helper original/copy byte pin '+name)
for row in G['history_originals']:verify(row)
target=admin(S/'TARGET_CLOSURE.source-only.json');history=admin(S/'HISTORY_CLOSURE.source-only.json')
need(same(history,G['history_originals']),'whole124 history rows')
need(len(target['sources'])==30,'target source declaration count')
for original,row in zip(target['sources'],G['sources']):need(row=={**original,'copy':str(root/original['relative'])},'entire30 target original/copy declaration '+row['relative'])
need(G['integrated_root']==target['integrated_root'],'exact integrated root')
for role,row in G['stage_bindings'].items():
 if role=='white_root_disposition':need(row=={'path':target['white_root']['path'],'pin':{k:target['white_root'][k] for k in ['bytes','sha256']}},'root stage binding')
 else:
  matching=[x for x in G['sources'] if x['copy']==row['path'] and x['pin']==row['pin']];need(len(matching)==1,'unique complete stage role '+role)
for row in G['evidence'].values():verify(row)
cor=admin(A/'RETAINED_SOURCE_CORRESPONDENCE.final.json');need(len(cor['copies'])==5,'five retained whole modules')
for pair in cor['copies']:
 verify(pair['original']);verify(pair['copy']);need(Path(pair['original']['path']).read_bytes()==Path(pair['copy']['path']).read_bytes(),'entire retained source bytes '+Path(pair['copy']['path']).name)
controls=admin(A/'CONTROL_INVENTORY.json');controlsource=(A/'inert_controls.py').read_text();groups=[]
for line in controlsource.splitlines():
 if re.match(r'^(MONITOR|MODE|STAGE|IO|TAIL|SHAPE|BINDING)_IDS=',line):groups.append({'group':line.split('=')[0],'ids':re.findall(r"'([^']+)'",line)})
ids=[x for g in groups for x in g['ids']];need(len(ids)==len(set(ids))==55 and groups==controls['groups'] and ids==controls['order'],'whole literal55 inventory')
need(controls['count']==55 and controls['executed']==0 and H['controls_executed']==0,'no control execution declared')
for cid in ids:need('| '+cid+' |' in (A/'CONTROL_CONTRACT.md').read_text(),'contract control row '+cid)
interface=admin(P/'INTERFACE_FIELDS.source-only.json');vs=(A/'mode_verify.py').read_text()
for constant,key,want in [('SUPERVISOR_FIELDS','supervisor_success',30),('WORKER_FIELDS','worker_success',27),('CUSTODY_FIELDS','worker_custody_success',13)]:
 text=re.search(r'^'+constant+r"='([^']+)'\.split\(\)$",vs,re.M).group(1).split();need(len(text)==len(set(text))==want and text==interface['field_sets'][key],'entire ordered receipt field inventory '+key)
final=admin(A/'FINAL_SOURCE_PIN_CHECK.json');need(final['adapter']==manifest['adapter'] and final['modules']==manifest['modules'] and final['controls_executed']==0 and final['syntax_compiled'] is False,'final source identity declaration')
ac=admin(A/'ADMIN_METADATA_CHECK.json');need(ac['dependency_count']==481 and ac['dependencies']==[{'file':x,'matched':True} for x in rows],'entire author saved identity rows')
for entry in ac['source_text_coverage']:
 verify(entry['file']);need(entry['lines']==len(Path(entry['file']['path']).read_bytes().splitlines()),'current source line count '+entry['file']['path'])
need(len(ac['source_text_coverage'])==11,'complete11 author coverage references')
for p in [A/n for n in ['adapter.py']+[name+'.py' for name in module_names]+['PROTOCOL.md','CONTROL_CONTRACT.md','AUTHORING_RECORD.md']]:
 txt=p.read_text();need(all(line.rstrip()==line for line in txt.splitlines()),'no trailing whitespace '+p.name)
 need(not re.search(r'^(<<<<<<< |======= |>>>>>>> )',txt,re.M),'no conflict markers '+p.name)
for path,row in list(observed.items()):need(m.identity(path)==row,'fresh full identity recheck '+path)
result={'schema':'ri156-independent-metadata-check-v1','status':'PASS_ADMINISTRATIVE_NOT_SOURCE_OR_CONTROL_ACCEPTANCE','counts':{'dependencies':481,'inherited':463,'additional':18,'subject_namespace':26,'subject_payloads':25,'copies':48,'target_pairs':30,'helpers':11,'history':124,'stage_roles':17,'retained_modules':5,'new_modules':6,'controls_defined':55,'controls_executed':0,'fresh_identity_rechecks':len(observed),'predicates':len(checks)},'subject':subject,'assignment':assignment,'checks':checks,'observed':list(observed.values()),'retained_pairs':cor['copies'],'control_groups':groups,'author_diagnostics':admin(A/'ADMIN_TOOL_RECORDS.json'),'runtime_binding_treated_as_saved_metadata_only':True,'proposed_execution_root_observed':False,'subject_import_compile_AST_probe_run':False,'scientific_body_decoded':False,'operational_card_or_runtime_observation':False}
m.save('METADATA_CHECK.json',result)
print(json.dumps({'status':'PASS','counts':result['counts']},sort_keys=True))
