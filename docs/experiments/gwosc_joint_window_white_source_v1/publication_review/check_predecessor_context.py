"""Opaque identity checks for predecessor's historical source/design references."""
import hashlib
import json
from pathlib import Path
O=Path('/Volumes/AI_DATA/development/det-review-evidence/ri125-white-publication-closure-xjTxsfe6')
R=Path('/Volumes/AI_DATA/development/det_8_framework-ret')
P=Path('/Volumes/AI_DATA/development/det-review-evidence/ri125-joint-window-application-source-fsra3wcw/PREDECESSOR_PINS.json')
D=R/'docs/experiments/gwosc_joint_window_application_v1'
relocations={
 'ri123-joint-window-application-design-e0qwhenu/DESIGN.md':D/'DESIGN.md',
 'ri123-joint-window-application-design-e0qwhenu/HANDOFF.json':D/'HANDOFF.json',
 'ri123-joint-window-application-design-e0qwhenu/PREDECESSOR_PINS.json':D/'PREDECESSOR_PINS.json',
 'ri122-root-execution-review-6whn_vky/RI123_ROOT_DESIGN_ADJUDICATION.json':D/'ROOT_ADJUDICATION.json',
 'ri123-independent-design-review-ou3oo3fq/INDEPENDENT_DESIGN_REVIEW.md':D/'independent/INDEPENDENT_DESIGN_REVIEW.md',
 'ri123-independent-design-review-ou3oo3fq/INDEPENDENT_DESIGN_REVIEW.json':D/'independent/INDEPENDENT_DESIGN_REVIEW.json',
}
rows=[]
for x in json.loads(P.read_text())['records']:
 p=Path(x['path']); key='/'.join(p.parts[-2:]); q=relocations.get(key,p)
 def identity(z):
  b=z.read_bytes();return {'path':str(z),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 a=identity(p); b=identity(q)
 ok=all(y['bytes']==x['bytes'] and y['sha256']==x['sha256'] for y in (a,b))
 rows.append({'declared':x,'current_original':a,'existing_repository_copy':b,
              'relative_repository_path':str(q.relative_to(R)),'matches':ok})
v={'schema':'ri125-predecessor-context-copy-check-v1','status':'PASS' if all(x['matches'] for x in rows) else 'FAIL',
 'record_count':len(rows),'records':rows,'scope':'Metadata only. No referenced scientific or target source body decoded, parsed as code or executed. No recursive runtime closure claim.'}
with (O/'PREDECESSOR_CONTEXT_CHECK.json').open('x') as f: json.dump(v,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'status':v['status'],'record_count':len(rows)}))
