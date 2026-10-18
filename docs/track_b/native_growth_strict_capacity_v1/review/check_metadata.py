"""Independent administrative RI155 closure verification; no subject execution.
Only root's authenticated metadata helper is imported; scientific bodies opaque.
"""
import hashlib,importlib.util,json,re,collections
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri155-independent-capacity-review-3gu50gvs';A=B/'ri155-strict-capacity-proof-jv0xliup';P=B/'ri153-fixed-prefix-weighted-margin-7_73jtl5';V=B/'ri153-independent-margin-review-FciZqSiY'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted metadata helper drift')
s=importlib.util.spec_from_file_location('trusted_metadata',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
checks=[];identities={};refs=[];extended=[]
def need(value,label):
 checks.append({'check':label,'passed':bool(value)})
 if not value:raise ValueError(label)
def typed_equal(a,b):return json.dumps(a,sort_keys=True,ensure_ascii=True,allow_nan=False)==json.dumps(b,sort_keys=True,ensure_ascii=True,allow_nan=False)
def verify(row):
 p=row['path'];now=m.identity(p)
 need(now['path']==p and m.pure(now)=={k:row[k] for k in ('bytes','sha256')},'opaque identity '+p)
 if 'resolved_path' in row:need(now['resolved_path']==row['resolved_path'],'resolved identity '+p)
 for k in ('symlinks','symlink_chain'):
  if k in row:need(typed_equal(now['symlink_chain'],row[k]),'selection chain '+p)
 if p in identities:need(now==identities[p],'unchanged fresh identity '+p)
 identities[p]=now
 return now
def admin(path):return json.loads(Path(path).read_bytes())
assignment={'path':str(B/'ri154-root-relocation-review-3sgyua6i/NATIVE_REVIEW_ASSIGNMENT.json'),'bytes':1372,'sha256':'88292622081b1e6bbd14d4614df6496b5536e1b28b5b6833458198343bbe9056'}
verify(assignment);assign=admin(assignment['path'])
subject={'path':str(A/'HANDOFF.json'),'bytes':8064,'sha256':'d4fd15fd5236990227bf1c059df960a3e0e53d01559c2bf1fee5422d7f059690'}
need(assign['subject']==subject and assign['reservation']==str(R),'exact assigned subject/reservation')
verify(subject);H=admin(subject['path'])
need(len(H['namespace'])==10 and len(H['payloads'])==9,'exact author counts')
need(sorted(p.name for p in A.iterdir())==sorted(H['namespace']),'exact author namespace')
need(sorted(H['namespace'])==sorted([Path(x['path']).name for x in H['payloads']]+['HANDOFF.json']),'complete payload name coverage')
for row in H['payloads']:
 need(Path(row['path']).parent==A and not Path(row['path']).is_symlink(),'author payload scope')
 verify(row)
D=admin(A/'SOURCE_DEPENDENCIES.json');S=admin(A/'SOURCE_IDENTITIES.json');rows=D['protected_files'];lookup={r['path']:r for r in rows}
need(len(rows)==193 and len(lookup)==193 and [r['path'] for r in rows]==sorted(lookup),'193 unique sorted dependency paths')
for i,row in enumerate(rows,1):
 need(row['role']=='dep_'+str(i).zfill(4) and row['path']==row['identity']['path'],'sorted role and path '+row['role'])
 need(set(row['identity'])=={'path','resolved_path','bytes','sha256','symlinks'},'closed five-field selected identity')
 verify(row['identity'])
old=admin(P/'SOURCE_DEPENDENCIES.json')['protected_files'];need(len(old)==171,'171 inherited rows')
without=lambda x:{k:v for k,v in x.items() if k!='role'}
for row in old:need(typed_equal(without(row),without(lookup[row['path']])),'entire inherited row except role '+row['path'])
added=[r for r in rows if r['path'] not in {o['path'] for o in old}]
need(len(added)==22,'22 additional paths')
expected_added={str(P/n) for n in ['ANALYTIC_RESULT.json','AUTHOR_CHECKS.json','FIXED_PREFIX_MARGIN_SYNTHESIS.md','HANDOFF.json','HANDOFF.md','PREFIX_STRUCTURE.md','SOURCE_DEPENDENCIES.json','SOURCE_IDENTITIES.json','WEIGHTED_PREFIX_COMPARISON.md','DEPENDENCY_NOTES.md']}
# The complete declared predecessor namespaces are authoritative for exact names.
expected_added=set()
namespace_checks=[]
for directory,want in [(P,10),(V,7)]:
 ph=admin(directory/'HANDOFF.json');names=sorted(p.name for p in directory.iterdir())
 need(names==sorted(ph['namespace']) and len(names)==want,'complete predecessor namespace '+str(directory))
 need(names==sorted([Path(r['path']).name for r in ph['payloads']]+['HANDOFF.json']),'predecessor payload domain '+str(directory))
 for row in ph['payloads']:verify(row)
 expected_added.update(str(directory/n) for n in names)
 namespace_checks.append({'root':str(directory),'names':names})
root=B/'ri153-root-margin-review-sflbzpwj'
expected_added.update(str(root/n) for n in ['NATIVE_SUCCESSOR_RESERVATION.json','RI153_ROOT_ADJUDICATION.json','ROOT_MANUAL_REVIEW.md','METADATA_CHECK.json','RI155_UNIFORM_MARGIN_SCOPE_CLARIFICATION.json'])
need({r['path'] for r in added}==expected_added,'exact disjoint 10+7+5 additions')
classes=collections.Counter(r['classification'] for r in rows)
need(dict(classes)=={'selected-administrative-proof-provenance':65,'analytic-source-text-or-review':75,'opaque-historical-acceptance-or-source-support':52,'opaque-scientific-historical-premise':1},'closed permitted access classification counts')
allowed={r['path'] for r in rows if r['classification']=='selected-administrative-proof-provenance'}
current_manifest=str(A/'SOURCE_DEPENDENCIES.json')
def walk(value,origin,position=''):
 if type(value) is dict:
  if type(value.get('path')) is str and type(value.get('bytes')) is int and type(value.get('sha256')) is str:
   need(value['path'] in lookup or value['path']==current_manifest,'closed typed reference '+value['path'])
   verify(value)
   refs.append({'origin':origin,'position':position,'path':value['path'],'bytes':value['bytes'],'sha256':value['sha256']})
   if 'state' in value and 'symlink_chain' in value:
    # Do not equate historical stat arrays with fresh observations.
    extended.append({'origin':origin,'position':position,'historical_identity':value,'historical_state_compared_to_current':False})
  for k,v in value.items():walk(v,origin,position+'/'+k)
 elif type(value) is list:
  for i,v in enumerate(value):walk(v,origin,position+'/'+str(i))
for path in sorted(allowed):walk(admin(path),path)
historical_count=len(refs);historical_extended=len(extended)
need(historical_count==1294 and historical_extended==17,'1294 historical typed references and 17 extended identities')
walk(S,str(A/'SOURCE_IDENTITIES.json'));current_count=len(refs)-historical_count
need(current_count==79 and len(extended)==17,'79 current refs without new historical stat claims')
for x in extended:
 need(x['historical_identity']['symlink_chain']==[],'historical no-link route retained')
 need(type(x['historical_identity']['state']) is list,'original historical state array retained opaquely in parent')
pairs=[]
for key,right in S['source_text_counterparts']['published'].items():
 left=S['premise_texts'][key];verify(left);verify(right)
 need(Path(left['path']).read_bytes()==Path(right['path']).read_bytes(),'complete source text counterpart '+key)
 pairs.append({'role':key,'left':left,'right':right})
need(len(pairs)==4,'four complete distinct-path counterparts')
literal=[]
for name in ['STRICT_CAPACITY_SYNTHESIS.md','CAPACITY_STRUCTURE.md','CAPACITY_COMPARISON.md']:
 text=(A/name).read_text()
 need(re.search(r'^(<{7}|={7}|>{7})( |$)',text,re.M) is None,'no conflict marker '+name)
 need(re.search(r'[ \t]+$',text,re.M) is None,'no trailing whitespace '+name)
 for match in re.finditer(r'`(/Volumes/[^` \n]+\.(?:md|json|py))`',text):
  path=match.group(1);need(path in lookup or Path(path).parent==A,'selected literal manuscript reference '+path)
  literal.append({'manuscript':name,'path':path})
need(len(literal)==6,'six literal manuscript reference occurrences')
author=admin(A/'AUTHOR_CHECKS.json');a=author['administrative_check'];actual=a['result']
need(a['tool_chunk']=='8565bf' and a['exit_code']==0 and actual['stage']=='preseal8','recorded author check is preseal8 only')
need(actual['dependencies']==193 and actual['selected_bytes']==5432055 and actual['historical_typed_refs']==1294 and actual['premise_refs']==79 and actual['extended_historical_identity_occurrences']==17 and actual['final_fresh_identity_rechecks']==201,'recorded author administrative counts reconciled')
for row in actual['current_payloads']:verify(row)
need(len(actual['current_payloads'])==8 and 'AUTHOR_CHECKS.json' not in [Path(x['path']).name for x in actual['current_payloads']],'no self-future author check identity claim')
need(H['actual_author_check']['tool_chunk']==a['tool_chunk'] and H['actual_author_check']['exit_code']==0,'handoff exact recorded author check')
need({x['tool_chunk']:x['exit_code'] for x in author['diagnostics'] if 'tool_chunk' in x}=={'fd819e':1,'bec2f5':2,'5715a2':1},'three actual author read errors preserved')
result=admin(A/'ANALYTIC_RESULT.json')
for k in ['actual_v_greater_than_B_proved','actual_joint_capacities_proved','actual_adequate_q_v_joint_budget_proved','actual_branch_or_root_order_decided','actual_W_C2_C3_signs_decided','actual_rho_in_delta0_proved','full_H30_decided']:
 need(result[k] is False,'unresolved boundary '+k)
need(result['actual_YE_less_than_one_proved'] is True and result['extra_capacity_multiplier_proved_one'] is True,'claimed new manual result fields separated')
need(S['excluded_historical_inferences']['withdrawn_numeric_seed_order_is_premise'] is False and S['excluded_historical_inferences']['withdrawn_numeric_seed_order_has_branch_or_sign_credit'] is False,'withdrawn seed order excluded')
# A fresh identity pass, independent of cached bodies and historical state arrays.
for path,oldrow in list(identities.items()):need(m.identity(path)==oldrow,'fresh final identity '+path)
report={'schema':'ri155-independent-administrative-review-v1','status':'PASS_NOT_MATHEMATICAL_PROOF','counts':{'dependencies':193,'dependency_bytes':sum(x['identity']['bytes'] for x in rows),'inherited':171,'added':22,'administrative_bodies':65,'historical_typed_refs':historical_count,'current_typed_refs':current_count,'historical_extended_identity_occurrences':17,'source_pairs':4,'literal_manuscript_references':6,'author_namespace':10,'author_payloads':9,'fresh_identity_rechecks':len(identities),'reviewer_predicates':len(checks)},'subject':subject,'assignment':assignment,'additional_rows':added,'classifications':dict(classes),'typed_references':refs,'extended_historical_identities':extended,'historical_state_compared_to_current':False,'predecessor_namespaces':namespace_checks,'source_pairs':pairs,'literal_references':literal,'author_diagnostics_verbatim':author['diagnostics'],'checks':checks,'observed':list(identities.values()),'scope':{'scientific_body_decode':False,'numerical_theorem_evaluation':False,'source_subject_import_compile_AST_probe_run':False,'runtime_observation':False,'new_cards_or_admissions':False,'repository_Git_write':False}}
m.save('METADATA_CHECK.json',report)
print(json.dumps({'status':'PASS','counts':report['counts']},sort_keys=True))
