from pathlib import Path
import json, hashlib
R=Path('/Volumes/AI_DATA/development/det_8_framework-ret/docs/experiments')
O=Path('/Volumes/AI_DATA/development/det-review-evidence/ri123-independent-design-review-ou3oo3fq')
def load(name):return json.loads((R/name/'RESULT.json').read_bytes())
def pin(v):
 b=(json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
a=load('gwosc_mode_weighted_trace_result_v1')
b=load('gwosc_frequency_resolved_proxy_result_v1')
c=load('gwosc_noise_operator_covariance_v1')
d=load('gwosc_off_event_context_benchmark_result_v1')
print('RI73 gate entry keys',list(c['gates'][0]))
print('RI116 scenario keys',list(d['scenarios'][0]))
print('RI96 gate keys',list(b['gates']) if isinstance(b['gates'],dict) else list(b['gates'][0]))
print('RI73 integration gram',next(x.keys() for x in c['gates'] if x['id']=='integration:gram'))
assert len(a['mode_terms'])==8192
assert [x['k'] for x in a['mode_terms']]==list(range(1,8193))
assert all(x['pair_weight']==(1 if x['k']==8192 else 2) for x in a['mode_terms'])
assert len(b['row_proofs'])==8 and all(len(x['midpoint_modes'])==8193 for x in b['row_proofs'])
assert len(c['gates'])==92
assert c['gate_inventory']==[x['id'] for x in c['gates']]
assert all(x['passed'] is True for x in c['gates'])
scenario_order=['H1:left','H1:right','L1:left','L1:right']
assert [x['id'] for x in a['scenarios']]==[x['id'] for x in b['scenarios']]==[x['id'] for x in d['scenarios']]==scenario_order
source_pins=[]
for x,y in zip(a['scenarios'],b['scenarios']):
 s=y['source_record'];assert set(s)=={'dtype','shape','values_hex','sha256'}
 assert s['dtype']=='<f8' and s['shape']==[8193] and len(s['values_hex'])==8193
 assert pin(s)==x['source_identity']
 source_pins.append({'id':x['id'],'canonical_source_identity_matches':True,'identity':x['source_identity']})
out={'schema':'ri123-independent-retained-schema-review-v1','scope':'Keys, order, lengths, fixed method/header text, exact historical source-record identities only; no rational or PSD numerical decoding, capture parsing, target import, contraction or empirical processing.', 'ri100':{'top_keys':list(a),'schema':a['schema'],'phase':a['phase'],'status':a['status'],'mode_count':len(a['mode_terms']),'all_mode_keys':sorted(set(tuple(sorted(x)) for x in a['mode_terms'])),'mode_order_and_pair_weights_match':True,'scenario_keys':list(a['scenarios'][0]),'checks':a['checks']},'ri96':{'top_keys':list(b),'schema':b['schema'],'phase':b['phase'],'status':b['status'],'row_proof_keys':list(b['row_proofs'][0]),'row_count':len(b['row_proofs']),'rectangles_per_row':8193,'source_record_keys':list(b['scenarios'][0]['source_record']),'complete_psd_counts':[len(x['source_record']['values_hex']) for x in b['scenarios']],'source_identities':source_pins},'ri73':{'top_keys':list(c),'schema_version':c['schema_version'],'mode':c['mode'],'status':c['status'],'gate_counts':c['gate_counts'],'gate_inventory':c['gate_inventory'],'full_inventory_and_successes_match':True,'integration_gram_record_keys':list(next(x for x in c['gates'] if x['id']=='integration:gram'))},'ri116':{'top_keys':list(d),'schema':d['schema'],'phase':d['phase'],'status':d['status'],'method':d['method'],'scenario_order':scenario_order,'scenario_keys':list(d['scenarios'][0]),'energy_keys':list(d['scenarios'][0]['energy']),'artifact_count':len(d['inputs']['artifacts']),'window_starts':[[w['start'] for w in x['windows']] for x in d['scenarios']]}}
(O/'SCHEMA_REVIEW.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('metadata checks pass')
