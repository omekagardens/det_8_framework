"""Additional source-decision and inert positive relational metadata checks only."""
import json,hashlib,pathlib,time
E=pathlib.Path('/Volumes/AI_DATA/development/det-review-evidence');R=E/'ri162-inert106-root-records-proposed-wb69vu5s';O=E/'ri156-operation-ri162-inert106-wb69vu5s';H=pathlib.Path(__file__).parent
checks=0
def c(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode()
def q(a,b,label):
 global checks
 checks+=1
 if c(a)!=c(b):raise ValueError(label)
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def pin(p):
 b=pathlib.Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
p=load(R/'BOOTSTRAP_PREFLIGHT.json');a=load(R/'ADAPTER_ADMISSION.json');d=load(p['source_acceptance']['path']);q(d['source_manifest'],a['source_manifest'],'D160 accepted exact manifest');q(d['controls'],{'defined':106,'executed':0,'new':22,'retained':84},'source-only historical controls')
r=load(O/'RESULT.json');by={x['id']:x['evidence'] for x in r['controls']}
for role,g in [('inert-fixtures','retained55'),('integration-fixtures','integration51')]:q(r['fixture_trees'][role],r['groups'][g]['fixture_tree'],'identical entire group fixture rows')
f=by['copy_positive'];z=f['result'];q(z['tree'],f['entire_tree'],'complete copied namespace');q(z['cards'],{},'copy no invented cards');q(z['stage'],'copied','exact stage');q(z['scientific_body_decoded'],False,'no numerical decode');q(z['source_acceptance_created'],False,'no source decision');q(z['tmp_empty'],True,'inert tmp empty')
q(z['source_states']['history'],[],'empty reduced history');q(z['source_states']['target_originals'],[],'empty reduced target originals');q(len(z['source_states']['copies']),1,'one copied inert source')
copy=z['source_states']['copies'][0];q(copy['relative'],'inert-source','one exact copied name');q(pathlib.Path(copy['copy']['path']).read_bytes(),pathlib.Path(copy['original']['path']).read_bytes(),'entire inert copy bytes') if False else q(pin(copy['copy']['path']),pin(copy['original']['path']),'entire inert copy identity')
g=by['guard_path_positive'];q(g['trace'],[['read','INERT_DECISION'],['read','INERT_OLD'],['read','INERT_REPORT'],['body','INERT_SOURCE_REVIEW'],['body','INERT_REVIEW'],['body','INERT_OUTER'],['body','INERT_REVIEW'],['body','INERT_REPORT']],'complete positive path-policy trace');q(g['result'],{'genuine_outer':'INERT_OUTER','helpers':[{'path':'INERT_NEW/helper.py','pin':{'inert_identity':'same'}}],'independent_review':'INERT_REVIEW','report':'INERT_REPORT'},'positive substituted policy output')
relation=by['relation_positive'];A=O/'inert-fixtures/relation_positive/normal';B=O/'inert-fixtures/relation_positive/optimized'
fixed=[f'W{i:02d}-{suffix}.json' for i in range(1,16) for suffix in ('operand','primary','independent')]+['W09-complete-capture.json','W09-primary-assembly.json','W09-independent-assembly.json','PRIMARY_KERNEL_CONTROLS.json','PRIMARY_WRAPPER_CONTROLS.json','PRIMARY_ALL_CONTROLS.json','INDEPENDENT_ALL_CONTROLS.json','FRESH_SAVED_COMPARISON.json'];q(relation['byte_identical_artifacts'],fixed,'all53 exact literal artifact names')
for name in fixed:
 if (A/name).read_bytes()!=(B/name).read_bytes():raise ValueError('entire inert relation bytes '+name)
 checks+=1
changes={};link_count=0
for name,tree in [('PRIMARY-KERNEL-CONTROLS_TREE.json','primary-kernel-controls'),('PRIMARY-WRAPPER-CONTROLS_TREE.json','primary-wrapper-controls'),('INDEPENDENT-CONTROLS_TREE.json','independent-controls')]:
 left=load(A/name);right=load(B/name)
 for row in left['records']:
  if row['kind']=='symlink':
   q(row['name'],'WC19-link.fabricated','only declared seed link');q(row['target'],str(A/tree/'WC19-seed.fabricated'),'entire normal seed target');row['target']=str(B/tree/'WC19-seed.fabricated');link_count+=1
 q(left,right,'all inert tree fields with only declared link relocation');q(pin(B/name),{'bytes':len(c(left)),'sha256':hashlib.sha256(c(left)).hexdigest()},'canonical propagated tree body');changes[name]=(pin(A/name),pin(B/name))
q(link_count,2,'exactly two target relocations')
def replace(x):
 if type(x) is dict:
  if set(x)=={'name','pin'} and x['name'] in changes:
   old,new=changes[x['name']];q(x['pin'],old,'authentic prior tree pin');return {'name':x['name'],'pin':new}
  return {k:replace(v) for k,v in x.items()}
 if type(x) is list:return [replace(v) for v in x]
 return x
q(replace(load(A/'WHITE_ONLY_QUALIFICATION.json')),load(B/'WHITE_ONLY_QUALIFICATION.json'),'entire inert qualifier metadata relation under only tree pins')
result={'status':'PASS_ADDITIVE_SOURCE_AND_INERT_RELATION_REVIEW','checks':checks,'source_decision_matches_manifest':True,'positive_copy_and_policy_complete':True,'inert_relation_full53_bytes_and3tree_records_and_report':True,'only_literal_seed_links_relocated':2,'scientific_or_genuine_fixture_credit':False,'checker':{'path':str(pathlib.Path(__file__)),**pin(__file__)},'completed_at_unix_ns':time.time_ns()}
p=H/'SUPPLEMENT_RESULT.json'
with p.open('xb') as f:f.write(c(result))
print({'path':str(p),**pin(p),'checks':checks})
