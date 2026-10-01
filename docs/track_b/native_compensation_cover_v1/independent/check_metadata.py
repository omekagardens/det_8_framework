"""Reviewer-owned administrative RI254 check. Never imports author sources or expands boundaries."""
import hashlib, json, os, stat
from pathlib import Path
Q=Path('/private/tmp/ri254-independent-compensation-review-hctcpep8')
W=Path('/Volumes/AI_DATA/development/det-review-evidence/ri254-native-compensation-cover-dxjpomko')
P=Path('/Volumes/AI_DATA/development/det-review-evidence/ri252-native-sigma-exchange-dz_u_bc2')
checks=[]; seen={}; bodies={}
def require(ok,label):
    if not ok: raise ValueError(label)
    checks.append(label)
def typed(x,y,label):
    require(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(y,sort_keys=True,separators=(',',':'),allow_nan=False),label)
def state(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
    p=Path(p)
    require(p.is_absolute() and p.resolve()==p,'literal resolved path '+str(p))
    require(p.name not in ('CERTIFICATE.json','check.py') and p.suffix not in ('.py','.pyc','.so','.dylib'),'no scientific or executable target '+str(p))
    before=p.lstat(); require(stat.S_ISREG(before.st_mode) and before.st_size<=64*1024*1024,'bounded regular '+str(p))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        require(state(os.fstat(fd))==state(before),'opened identity '+str(p))
        with os.fdopen(fd,'rb',closefd=False) as f: body=f.read(64*1024*1024+1)
        require(state(os.fstat(fd))==state(before),'descriptor stable '+str(p))
    finally: os.close(fd)
    require(state(p.lstat())==state(before) and len(body)==before.st_size,'path stable '+str(p))
    pin={'path':str(p),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
    return pin,body,state(before)
def verify(pin):
    require(set(pin)=={'path','bytes','sha256'} and type(pin['bytes']) is int and type(pin['sha256']) is str,'closed FilePin '+pin['path'])
    actual,body,st=read(pin['path']);typed(actual,pin,'whole pin '+pin['path'])
    if pin['path'] in seen: typed(seen[pin['path']]['pin'],pin,'repeated consistent pin '+pin['path'])
    seen[pin['path']]={'pin':pin,'state':st};bodies[pin['path']]=body
    return body
def admin(path): return json.loads(bodies[str(path)])
expected={
'COMPENSATION_COVER.md':(11066,'008024d4d4541aae8c3455afa41ec9a429fa56308af5c1675c21d08660751367'),
'PIECEWISE_REDUCTION.md':(10569,'5e60196301a398976a8eb73d2aaa65f453c5fe2a56731a088c9c8698a6ef8e82'),
'HANDOFF.md':(2175,'cf8b38298bee569c58fd744a6cd8ac4f2cbc42102a4c4dc325d5d9a28b510baf'),
'SOURCE_REFERENCES.json':(110977,'60da052ed617598855252f84973e01e80cba264b9ab40734f017429d26035588'),
'AUTHOR_VERIFICATION.json':(32591,'b9b6ec92d21515ed648574e903d7a427b03e35fc64108bde016a2e1a14c660b2'),
'HANDOFF.json':(19285,'5d56bac5238e9d8f1fa82fc912bc2ec1be66811ebb7af6f420504a898be88693')}
require(sorted(p.name for p in W.iterdir())==sorted(expected),'exact six-file packet')
for name,(n,h) in expected.items(): verify({'path':str(W/name),'bytes':n,'sha256':h})
S=admin(W/'SOURCE_REFERENCES.json');H=admin(W/'HANDOFF.json');A=admin(W/'AUTHOR_VERIFICATION.json')
require(len(H['files'])==5,'five handoff payloads')
typed(sorted(r['path'] for r in H['files']),sorted(str(W/n) for n in expected if n!='HANDOFF.json'),'full handoff payload domain')
for r in H['files']:typed(r,seen[r['path']]['pin'],'handoff binds payload '+r['path'])
require(len(A['payloads'])==4,'four author preseal payloads')
for r in A['payloads']:typed(r,seen[r['path']]['pin'],'author binds payload '+r['path'])
rows=S['direct_sources'];require(len(rows)==133 and len({r['identity']['path'] for r in rows})==133,'133 distinct direct sources')
require(sum(r['identity']['bytes'] for r in rows)==2719249,'2719249 direct source bytes')
for r in rows:
    require(set(r)=={'identity','access','role'},'closed role row '+r['identity']['path'])
    require(r['access'] in ('accepted-analytic-text','administrative-reference','opaque-historical-support') and isinstance(r['role'],str) and bool(r['role']),'retained allowed role '+r['identity']['path'])
    verify(r['identity'])
require(len(seen)==139,'139 distinct subject and direct identities')
PS=admin(P/'SOURCE_REFERENCES.json');PH=admin(P/'HANDOFF.json')
require(len(PS['direct_sources'])==123,'123 inherited direct sources')
index={r['identity']['path']:r for r in rows}
for r in PS['direct_sources']:
    typed(index[r['identity']['path']]['identity'],r['identity'],'unchanged inherited source '+r['identity']['path'])
    typed(index[r['identity']['path']]['access'],r['access'],'unchanged inherited access '+r['identity']['path'])
require(sorted(p.name for p in P.iterdir())==sorted(['AUTHOR_VERIFICATION.json','HANDOFF.json','HANDOFF.md','SIGMA_EXCHANGE.md','SIGMA_KEYS_AND_WEIGHTS.md','SOURCE_REFERENCES.json']),'complete predecessor namespace')
for r in PH['files']:typed(r,seen[r['path']]['pin'],'predecessor sealed payload '+r['path'])
keys=S['preserved_boundary_keys'];require(len(keys)==15 and len(set(keys))==15,'15 distinct boundaries')
typed(keys,PS['preserved_boundary_keys'],'exact inherited boundary order')
typed(set(keys)==set(S['preserved_boundaries']),True,'whole boundary map domain')
for k in keys:typed(S['preserved_boundaries'][k],PS['preserved_boundaries'][k],'complete preserved boundary '+k)
require(S['preserved_boundaries']['inherited_manifest_by_reference']['selected_paths']==423,'423 inherited count by reference only')
require(S['current_literal_reads']==[],'no current literal reads')
closed=S['closed_original_literal_exceptions_by_reference']
require(closed['closed'] is True and closed['new_body_read_or_hash'] is False and closed['all_older_exceptions_remain_closed'] is True,'closed all original literal authority')
typed(closed['reference'],seen[str(P/'SOURCE_REFERENCES.json')]['pin'],'exact closed authority predecessor ref')
require(closed['field']=='closed_RI250_literal_exception_by_reference' and closed['field'] in PS,'exact inherited closed field')
for key in ('assignment','assignment_text','accepted_predecessor'):
    typed(S[key],H[key],'handoff '+key);typed(S[key],A[key],'author '+key)
    typed(S[key],seen[S[key]['path']]['pin'],'authenticated '+key)
typed(S['current_scope'],H['current_scope'],'complete handoff scope');typed(S['current_scope'],A['current_scope'],'complete author scope')
true_keys={'manual_mathematical_reasoning','manually_derived_history_weights_and_prices'}
for k,v in S['current_scope'].items():
    typed(v,0 if k=='qualification_credit' else k in true_keys,'scope boundary '+k)
require(A['independent_acceptance'] is False and A['scientific_execution'] is False,'author self-review scope')
typed(S['diagnostics'],A['diagnostics'],'full author diagnostics');typed(S['diagnostics'],H['diagnostics'],'full handoff diagnostics')
typed(S['diagnostics']['predecessor_diagnostics'],PS['diagnostics'],'all historical diagnostics retained')
G=json.loads((Q/'GENUINE_AUTHOR_CHECKS.json').read_bytes());require(len(G['items'])==2,'two genuine retrieved compact command records')
actual=[]
for i,item in enumerate(G['items']):
    require(item['status']=='completed' and type(item['exitCode']) is int and item['exitCode']==0,'completed genuine author command '+item['id'])
    require(item['output']['truncated'] is False,'complete API output '+item['id'])
    r=json.loads(item['output']['text']);mode=['preseal','final6'][i]
    require(r['mode']==mode,'genuine mode '+mode)
    for k,v in [('direct_sources',133),('direct_bytes',2719249),('whole_identities',137 if i==0 else 139),('preserved_boundaries',15),('inherited_manifest_sources_by_reference',423),('exit_intent',0)]:typed(r[k],v,'actual author '+mode+' '+k)
    for k in ['original_scientific_body_read','original_scientific_body_hash','scientific_JSON_decoded','scientific_arithmetic','scientific_execution']:require(r[k] is False,'author scope '+mode+' '+k)
    expected_names=sorted(expected if i else [p.name for p in map(Path,[v['path'] for v in A['payloads']])])
    typed(r['current_namespace'],expected_names,'genuine namespace '+mode)
    require(len(r['current_identities'])==(4 if i==0 else 6),'complete genuine pin count '+mode)
    for p in r['current_identities']:typed(p,seen[p['path']]['pin'],'genuine current pin '+p['path'])
    if i==0:typed(r,H['actual_preseal_receipt']['result'],'full preserved preseal result');typed(r,A['preseal']['result'],'full author preseal result')
    actual.append({'id':item['id'],'status':item['status'],'exit_code':item['exitCode'],'mode':mode,'truncated':False})
# Fresh whole-file re-read, never follow nested references. No source state is changed.
for path,row in list(seen.items()):
    actualpin,body,st=read(path);typed(actualpin,row['pin'],'final whole identity '+path);typed(st,row['state'],'final stable state '+path)
require(sorted(p.name for p in W.iterdir())==sorted(expected),'final exact packet namespace')
result={'schema':'ri254-independent-admin-review-v1','passed':True,'predicates':len(checks),'source_domain':{'packet':6,'direct_sources':133,'direct_bytes':2719249,'whole_identities':139,'inherited_direct':123,'new_direct':10,'preserved_boundaries':15,'manifest_entries_unexpanded':423},'actual_author_commands':actual,'source_observations':[seen[p] for p in sorted(seen)],'predicate_labels':checks,'scope':{'scientific_body_read_or_hash':False,'scientific_json_decoded':False,'mathematical_engine':False,'subject_executed':False,'boundary_descendants_followed':False,'manual_math_is_separate':True}}
body=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode();out=Q/'CHECK.json'
with out.open('xb') as f:f.write(body)
require(out.read_bytes()==body,'exact reviewer report readback')
print(json.dumps({'passed':True,'predicates_saved':result['predicates'],'additional_report_readback':1,'domain':result['source_domain'],'CHECK':{'path':str(out),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}}))
