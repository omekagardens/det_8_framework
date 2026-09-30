"""Classify saved file/cache descriptors without observing a current runtime."""
from pathlib import Path
import json,hashlib
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri139-focused25-independent-review-FQU9u14Y';D=B/'ri139-root-bootstrap-adjudication-goau3dIc'
p=json.loads((D/'BOOTSTRAP_PRE.json').read_bytes());x=json.loads((R/'SAVED_EVIDENCE_CHECK.json').read_bytes());framework={z['path']:z for z in p['framework_namespace']};out=[]
for m in p['bootstrap_descriptor']['modules']:
 assert set(m)=={'name','file','origin','cached','loader_type'} | ({'identity'} if 'identity' in m else set())
 if 'identity' in m:
  assert m['file']==m['identity']['path'];assert m['origin'] in (m['file'],None)
 cached=m['cached'];classification='no_cache_descriptor'
 if cached:
  if cached in framework:classification='present_in_saved_framework'
  elif Path(cached).is_relative_to(p['prefix']):
   assert not any(z['kind']=='symlink' and Path(z['path']) in Path(cached).parents for z in framework.values())
   classification='absent_from_complete_saved_framework'
  else:
   assert m['name']=='m' and m['file']==p['metadata_helper']['path']
   classification='external_root_metadata_helper_cache_not_in_framework_scope'
 out.append({'name':m['name'],'file':m['file'],'origin':m['origin'],'cached':cached,'loader_type':m['loader_type'],'file_identity_present':'identity' in m,'cache_classification':classification})
assert len({z['name'] for z in out})==len(out)==92
v={'schema':'ri139-saved-module-complete-field-check-v1','source_pre':{'path':str(D/'BOOTSTRAP_PRE.json'),'bytes':len((D/'BOOTSTRAP_PRE.json').read_bytes()),'sha256':hashlib.sha256((D/'BOOTSTRAP_PRE.json').read_bytes()).hexdigest()},'module_rows':out,'module_count':92,'file_identity_count':sum(z['file_identity_present'] for z in out),'cache_classifications':{k:sum(z['cache_classification']==k for z in out) for k in sorted({z['cache_classification'] for z in out})},'scope':'All descriptors compared only to saved inventory. A cached filename need not exist and is not evidence of loaded bytecode or source/cache equivalence; external helper cache remains covered only by the declared trusted supplier/cache premise. No live runtime files read.','reviewer_diagnostic':{'tool_chunk':'99cb56','exit_code':1,'source_kind':'reviewer metadata-only inline check','error':'AssertionError at line10: if m[\'cached\']:assert m[\'cached\'] in framework','cause':'Reviewer initially demanded actual presence for every cache descriptor, which is not the accepted contract or Python cached-descriptor semantics. Main saved-evidence check already recorded presence booleans without this false requirement.','correction':'Classify recorded presence/absence and external-helper scope; do not replace observation with invented cached-file identity. No subject source/output/threshold changed.'},'control_namespace_kind_counts':{k:sum(z['kind']==k for z in x['control_namespace']) for k in ['file','directory','symlink']},'output_namespace_kind_counts':{k:sum(z['kind']==k for z in x['full_output_namespace']) for k in ['file','directory','symlink']},'all_checks_passed':True}
with (R/'SAVED_MODULE_FIELD_CHECK.json').open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({k:v[k] for k in ['module_count','file_identity_count','cache_classifications','control_namespace_kind_counts','output_namespace_kind_counts','all_checks_passed']},indent=2))
