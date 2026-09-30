"""RI130 complete saved WHITE evidence relation; UNEXECUTED source.

Metadata/custody checks are not mathematical reruns. Optional reconstruct_saved
calls are separate actual independent reconstruction inside a reviewed budget.
No target is imported here. The caller supplies separately captured modules.
"""
import hashlib
import json
import os
from pathlib import Path
import stat

CAP=67108864
CONTEXT='RI125_FABRICATED_ONLY_NOT_HISTORICAL'
CASE_IDS=('W01_single_white_two','W02_single_white_three','W03_oriented_two','W04_negative_scale',
 'W05_double_scale','W06_interval_mixed','W07_interval_crosses_zero','W08_zero_shift',
 'W09_production_boundary_sparse','W10_usefulness_boundaries','W11_asymmetric_rational_radii',
 'W12_sparse_lifted_denominators','W13_full_response_below','W14_full_response_equal','W15_full_response_above')
CONTROLS=([f'WK{i:02d}' for i in range(1,39)]+[f'WC{i:02d}' for i in range(1,27)]
 +[f'WG{i:02d}' for i in range(1,93)]+[f'WC{i:02d}' for i in range(27,47)]+['WT01','WT02','WT03'])
TREES=('primary-kernel-controls','primary-wrapper-controls','independent-controls')
TREE_FILES=tuple(x.upper()+'_TREE.json' for x in TREES)
CASE_FILES=tuple(f'W{i:02d}-{kind}.json' for i in range(1,16) for kind in ('operand','primary','independent'))
ASSEMBLY_FILES=('W09-complete-capture.json','W09-primary-assembly.json','W09-independent-assembly.json')
CONTROL_FILES=('PRIMARY_KERNEL_CONTROLS.json','PRIMARY_WRAPPER_CONTROLS.json','PRIMARY_ALL_CONTROLS.json','INDEPENDENT_ALL_CONTROLS.json')
FIXED_FILES=CASE_FILES+ASSEMBLY_FILES+CONTROL_FILES+('FRESH_SAVED_COMPARISON.json',)
ARTIFACT_NAMES=CASE_FILES+ASSEMBLY_FILES+(TREE_FILES[0],CONTROL_FILES[0],TREE_FILES[1],CONTROL_FILES[1],CONTROL_FILES[2],TREE_FILES[2],CONTROL_FILES[3],'FRESH_SAVED_COMPARISON.json','WHITE_ONLY_QUALIFICATION.json')


def need(ok,message):
    if not ok:raise ValueError(message)


def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')


def same(a,b,message):
    need(canonical(a)==canonical(b),message)


def keys(value,names,message):
    need(type(value) is dict and set(value)==set(names),message)


def identity(body):
    return {'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}


def file_body(path,pin,C,canonical_json=True):
    need(type(pin) is dict and set(pin)=={'bytes','sha256'} and type(pin['bytes']) is int
         and 0<pin['bytes']<=CAP,'positive bounded artifact pin')
    body=C.verified_body(path,pin)
    if not canonical_json:return body
    value=C.parse_json(body);same(identity(canonical(value)),pin,'canonical saved metadata body')
    return value


def tree_snapshot(root,C):
    root=Path(root);need(root==root.resolve() and root.is_dir(),'owned tree root literal')
    records=[]
    def visit(path,depth):
        need(depth<=8 and len(records)<1024,'owned tree resource limit')
        st=path.lstat();before=(st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
        name=str(path.relative_to(root))
        if stat.S_ISLNK(st.st_mode):
            target=os.readlink(path);need(len(target)<=4096,'bounded link target')
            records.append({'name':name,'kind':'symlink','pin':None,'target':target})
        elif stat.S_ISDIR(st.st_mode):
            records.append({'name':name,'kind':'directory','pin':None,'target':None})
            with os.scandir(path) as scan:children=sorted(x.name for x in scan)
            for child in children:visit(path/child,depth+1)
        else:
            need(stat.S_ISREG(st.st_mode) and 0<=st.st_size<=CAP,'bounded regular owned artifact')
            records.append({'name':name,'kind':'file','pin':C.file_pin(path),'target':None})
        after=path.lstat()
        need(before==(after.st_dev,after.st_ino,after.st_mode,after.st_nlink,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'tree entry changed during inspection')
    visit(root,0)
    return {'schema':'ri125-fabricated-control-tree-v1','records':records}


def good_tail(rows):
    need(type(rows) is list and len(rows)==2,'two full independent postchecks')
    for row in rows:keys(row,('role','pin','unchanged','error'),'complete tail fields')
    need(rows[0]['role']=='first' and rows[0]['unchanged'] is False and rows[0]['pin'] is None
         and type(rows[0]['error']) is str and 0<len(rows[0]['error'])<=1024,'first tail failure')
    need(rows[1]['role']=='second' and rows[1]['unchanged'] is True and rows[1]['error'] is None
         and type(rows[1]['pin']) is dict and set(rows[1]['pin'])=={'bytes','sha256'}
         and type(rows[1]['pin']['bytes']) is int and rows[1]['pin']['bytes']>0,'second tail independently attempted')


def control_report(value,spec,independent):
    keys(value,('schema','phase','context','actual_scientific_input_opened','independent_validator_run','controls','counts','status'),'complete control envelope')
    same({k:value[k] for k in value if k!='controls'},
         {'schema':'ri125-independent-white-controls-v1' if independent else 'ri125-primary-complete-white-controls-v1',
          'phase':'fabricated_qualification','context':CONTEXT,'actual_scientific_input_opened':False,
          'independent_validator_run':independent,'counts':{'total':179,'passed':179,'failed':0},'status':'all_declared_controls_passed'},'exact saved control header')
    need(type(value['controls']) is list and len(value['controls'])==179,'179 complete control records')
    same([r['id'] for r in value['controls']],CONTROLS,'full control order')
    for row,want in zip(value['controls'][:-3],spec['refusals']):
        same(row,{'id':want['id'],'expected_code':want['code'],'expected_message':want['message'],
             'observed_code':want['code'],'observed_message':want['message'],'passed':True},'literal first refusal '+want['id'])
    a,b,c=value['controls'][-3:]
    keys(a,('id','passed','postchecks'),'WT01 closed fields');need(a['passed'] is True,'WT01 passed');good_tail(a['postchecks'])
    for row,code,message in ((b,'EXACT','first-error'),(c,'CUSTODY','one or more final source/input postchecks failed')):
        keys(row,('id','passed','refusal'),'WT closed fields');need(row['passed'] is True,'tail passed')
        r=row['refusal'];keys(r,('schema','status','phase','stage','code','message','scientific_disposition_emitted','postchecks'),'full tail refusal')
        same({k:v for k,v in r.items() if k not in ('message','postchecks')},
             {'schema':'ri125-application-refusal-v1','status':'REFUSED','phase':'fixed_saved_application',
              'stage':'white','code':code,'scientific_disposition_emitted':False},'tail first-error semantics')
        need(type(r['message']) is str and len(r['message'])<=1024 and r['message'].split(': ',2)[-1]==message,'tail first message')
        same(r['postchecks'],a['postchecks'],'all tail records retained');good_tail(r['postchecks'])


def inspect_success(envelope,stage,bindings,C):
    """Complete retained evidence/custody checks; does not recompute arithmetic."""
    keys(envelope,('result','report_pin','artifacts','postchecks','tree_postchecks','namespace','refusal'),'closed qualifier return envelope')
    need(envelope['refusal'] is None and type(envelope['result']) is dict,'qualifier returned success')
    stage=Path(stage)
    artifacts=envelope['artifacts'];need(type(artifacts) is list and len(artifacts)==57,'all57 artifact files')
    same([x['name'] for x in artifacts],list(ARTIFACT_NAMES),'complete ordered artifact inventory')
    pins={}
    for item in artifacts:
        keys(item,('name','pin'),'artifact fields');keys(item['pin'],('bytes','sha256'),'artifact pin fields')
        need(type(item['pin']['bytes']) is int and 0<item['pin']['bytes']<=CAP and type(item['pin']['sha256']) is str
             and len(item['pin']['sha256'])==64 and all(c in '0123456789abcdef' for c in item['pin']['sha256']),'positive bounded artifact identity')
        same(C.file_pin(stage/item['name']),item['pin'],'entire saved artifact '+item['name']);pins[item['name']]=item['pin']
    report=file_body(stage/'WHITE_ONLY_QUALIFICATION.json',envelope['report_pin'],C)
    same(envelope['report_pin'],pins['WHITE_ONLY_QUALIFICATION.json'],'saved report identity')
    same(report,envelope['result'],'entire saved report equals returned object')
    keys(report,('schema','phase','status','context','scope','limits','source_bindings','cases','complete_capture_assembly','controls','fresh_saved_comparison','artifacts','limitations'),'complete stage report fields')
    same([report[k] for k in ('schema','phase','status','context')],['ri125-white-only-qualification-v1','fabricated_qualification','all_white_only_gates_passed',CONTEXT],'WHITE-only stage header')
    same(report['scope'],{'white_case_ids':list(CASE_IDS),'white_case_count':15,'full_application_case_count':32,
         'full_application_qualified':False,'actual_data_admitted':False,'periodic_mean_or_join_executed':False,'physical_claim':False},'no full32 or actual promotion')
    same(report['source_bindings'],bindings,'complete17 direct bindings')
    same(report['limits'],{'seconds':180,'sampled_rss_kib':524288,'poll_ms':25,'max_gap_ms':100,'ps_timeout_ms':50,
         'file_bytes':CAP,'capture_row_bytes':8388608,'completed_integer_bits':262144},'unchanged stage limits')
    same(report['artifacts'],artifacts[:-1],'self-excluding56 report artifacts')
    need(type(report['cases']) is list and len(report['cases'])==15,'complete15 case records')
    def artifact(name):return {'name':name,'pin':pins[name]}
    six=['fixed_operand_schema_and_recipe','complete_result_shape','literal_case_anchor','full_directed_shift_consistency','correct_gram_presence_and_inherited_gate','correct_response_presence_and_new_gate']
    four=['fixed_bound_operand_recipe','complete_bound_result_shape','literal_predicate_results','fabricated_identity_only']
    for index,(row,cid) in enumerate(zip(report['cases'],CASE_IDS),1):
        ids=four if index==10 else six
        same(row,{'id':cid,'kind':'bound_predicate_only' if index==10 else 'white_primitive',
             'operand':artifact(f'W{index:02d}-operand.json'),'primary':artifact(f'W{index:02d}-primary.json'),
             'independent':artifact(f'W{index:02d}-independent.json'),'full_fields_match':True,
             'expected_checks':{'inventory':ids,'counts':{'total':len(ids),'passed':len(ids),'failed':0},'results':[{'id':x,'passed':True} for x in ids]}},'complete case record '+cid)
    assembly=report['complete_capture_assembly']
    keys(assembly,('id','capture','gram_pin','primary','independent','full_fields_match'),'complete assembly record')
    same({k:v for k,v in assembly.items() if k!='gram_pin'}, {'id':CASE_IDS[8],'capture':artifact(ASSEMBLY_FILES[0]),
         'primary':artifact(ASSEMBLY_FILES[1]),'independent':artifact(ASSEMBLY_FILES[2]),'full_fields_match':True},'full W09 assembly references')
    w09=file_body(stage/'W09-operand.json',pins['W09-operand.json'],C)
    same(assembly['gram_pin'],identity(canonical(w09['gram'])),'saved W09 Gram identity')
    spec_ref=bindings['control_expectations'];spec=file_body(spec_ref['path'],spec_ref['pin'],C)
    same(spec['order'],CONTROLS,'full literal control specification order');need(len(spec['refusals'])==176,'176 first refusal specifications')
    primary=file_body(stage/CONTROL_FILES[2],pins[CONTROL_FILES[2]],C);independent=file_body(stage/CONTROL_FILES[3],pins[CONTROL_FILES[3]],C)
    control_report(primary,spec,False);control_report(independent,spec,True)
    kernel=file_body(stage/CONTROL_FILES[0],pins[CONTROL_FILES[0]],C);wrapper=file_body(stage/CONTROL_FILES[1],pins[CONTROL_FILES[1]],C)
    for value,schema,n,rows in [(kernel,'ri125-primary-kernel-controls-v1',37,primary['controls'][:37]),
                                (wrapper,'ri125-primary-white-controls-v1',142,primary['controls'][37:])]:
        same(value,{'schema':schema,'phase':'fabricated_qualification','context':CONTEXT,'actual_scientific_input_opened':False,
             'independent_validator_run':False,'controls':rows,'counts':{'total':n,'passed':n,'failed':0},'status':'all_declared_controls_passed'},'complete original control report')
    same(report['controls'],{'order':CONTROLS,'per_implementation':179,'kernel_per_implementation':38,'wrapper_and_tail_per_implementation':141,
         'primary_kernel':artifact(CONTROL_FILES[0]),'primary_wrapper':artifact(CONTROL_FILES[1]),'primary_complete':artifact(CONTROL_FILES[2]),
         'independent_complete':artifact(CONTROL_FILES[3]),'both_exact_inventories_and_first_refusals_passed':True,
         'trees':[{'name':name,'inventory':artifact(file)} for name,file in zip(TREES,TREE_FILES)]},'complete control report references')
    fresh=file_body(stage/'FRESH_SAVED_COMPARISON.json',pins['FRESH_SAVED_COMPARISON.json'],C)
    same(fresh,{'schema':'ri125-white-only-fresh-saved-comparison-v1','phase':'fabricated_qualification',
         'cases':[{'id':cid,'fresh_result_pin':pins[f'W{i:02d}-independent.json'],'all_fields_match':True} for i,cid in enumerate(CASE_IDS,1)],
         'assembly':{'id':CASE_IDS[8],'fresh_result_pin':pins[ASSEMBLY_FILES[2]],'all_fields_match':True},
         'saved_control_envelopes_fully_checked':True,'controls_rerun_by_comparator':False,'actual_data_evaluated':False,'full_application_qualified':False},'full fresh-saved comparison witness')
    same(report['fresh_saved_comparison'],artifact('FRESH_SAVED_COMPARISON.json'),'fresh comparison reference')
    same(report['limitations'],['Only W01-W15 and their white controls are covered.',
         'The full 32-case application, periodic/mean/join paths and actual-data admission remain pending.',
         'Separate root source/runtime/history/caller custody and genuine completion remain required.',
         'Exact fabricated arithmetic is not detector covariance, calibration, native geometry/gravity or physical validation.',
         'Original precision, domain, resource and protected-validation boundaries remain; RET is paused.'],'all stage limitations')
    # Pin/type equality of full scientific files; arithmetic is a separately identified reconstruction operation below.
    for i in range(1,16):same(pins[f'W{i:02d}-primary.json'],pins[f'W{i:02d}-independent.json'],'full result file identity')
    same(pins[ASSEMBLY_FILES[1]],pins[ASSEMBLY_FILES[2]],'full assembly identity')
    # Source map insertion order differs from the fixed qualifier roles; use its literal order.
    order=('white_kernel','white_path','wrapper_controls','white_contract','cases','kernel_refusals','fabricated_interfaces','white_refusals_text',
           'white_source_handoff','white_root_disposition','fixtures','kernel_controls','orchestrator','stage_contract','control_expectations','validator','validator_controls')
    wanted_posts=[{'role':'source:'+role,'pin':bindings[role]['pin'],'unchanged':True,'error':None} for role in order]
    wanted_posts += [{'role':'artifact:'+x['name'],'pin':x['pin'],'unchanged':True,'error':None} for x in artifacts]
    same(envelope['postchecks'],wanted_posts,'all74 exact source/artifact postchecks')
    same(envelope['tree_postchecks'],[{'name':x,'unchanged':True,'error':None} for x in TREES],'all3 exact tree postchecks')
    for name,file in zip(TREES,TREE_FILES):same(tree_snapshot(stage/name,C),file_body(stage/file,pins[file],C),'entire control tree '+name)
    namespace=tree_snapshot(stage,C)
    same(envelope['namespace'],{'inventory':namespace,'error':None},'complete final namespace custody')
    top=sorted(x['name'] for x in namespace['records'] if x['name']!='.' and '/' not in x['name'])
    same(top,sorted(list(ARTIFACT_NAMES)+list(TREES)),'closed57 files and3 directories')
    return {'schema':'ri130-white-saved-custody-check-v1','status':'complete_saved_WHITE_evidence_matches',
            'artifact_count':57,'source_artifact_postchecks':74,'tree_postchecks':3,
            'report_pin':envelope['report_pin'],'namespace_pin':identity(canonical(namespace)),
            'arithmetic_recomputed_by_this_check':False,'full32_qualified':False,'actual_data_admitted':False}


def reconstruct_saved(envelope,stage,bindings,C,validator):
    """Prospective fresh independent reviewer entry; requires its own admission/budget.

    Never called automatically by metadata/parent checks. Reconstructs every field
    from saved operands, without giving the independent validator primary outputs.
    """
    custody=inspect_success(envelope,stage,bindings,C);stage=Path(stage);rows=[]
    for i,row in enumerate(envelope['result']['cases'],1):
        operand=file_body(stage/row['operand']['name'],row['operand']['pin'],C,False)
        fresh=validator.validate_fixture_bytes(operand)
        for role in ('primary','independent'):
            same(fresh,file_body(stage/row[role]['name'],row[role]['pin'],C),'fresh entire saved result '+row['id'])
        rows.append({'id':row['id'],'pin':identity(canonical(fresh))})
    operand=file_body(stage/'W09-operand.json',envelope['result']['cases'][8]['operand']['pin'],C)
    row=envelope['result']['complete_capture_assembly'];ref={'path':str(stage/row['capture']['name']),'pin':row['capture']['pin']}
    same(row['gram_pin'],identity(canonical(operand['gram'])),'saved W09 Gram identity')
    fresh=validator.validate_fabricated_assembly(ref,operand['gram'],CASE_IDS[8],CONTEXT)
    for role in ('primary','independent'):same(fresh,file_body(stage/row[role]['name'],row[role]['pin'],C),'fresh entire saved assembly')
    after=inspect_success(envelope,stage,bindings,C);same(after,custody,'review custody before/after')
    return {'schema':'ri130-independent-saved-WHITE-reconstruction-v1','custody':custody,'cases':rows,
            'assembly_pin':identity(canonical(fresh)),'complete_independent_reconstruction':True,
            'controls_reexecuted':False,'actual_data_evaluated':False,'full32_qualified':False}


def compare_modes(normal,optimized,normal_stage,optimized_stage,bindings,C):
    """Closed full-envelope relation; only named link targets and propagated pins differ."""
    a=Path(normal_stage);b=Path(optimized_stage)
    inspect_success(normal,a,bindings,C);inspect_success(optimized,b,bindings,C)
    ap={x['name']:x['pin'] for x in normal['artifacts']};bp={x['name']:x['pin'] for x in optimized['artifacts']}
    for name in FIXED_FILES:
        same(ap[name],bp[name],'exact mode file identity '+name)
        # Opaque bounded streaming equality; no doubled hex/string allocation.
        with (a/name).open('rb') as left,(b/name).open('rb') as right:
            while True:
                x,y=left.read(65536),right.read(65536)
                need(x==y,'exact mode file bytes '+name)
                if not x:break
        same(C.file_pin(a/name),ap[name],'normal after byte comparison '+name)
        same(C.file_pin(b/name),bp[name],'optimized after byte comparison '+name)
    # Only the intentional WC19 links have mode-specific target strings.
    changes={}
    for tree,name in zip(TREES,TREE_FILES):
        left=file_body(a/name,ap[name],C);right=file_body(b/name,bp[name],C)
        for record in left['records']:
            if record['kind']=='symlink':
                need(tree in TREES[1:] and record['name']=='WC19-link.fabricated','only declared WC19 links may differ')
                same(record['target'],str(a/tree/'WC19-seed.fabricated'),'normal literal WC19 target')
                record['target']=str(b/tree/'WC19-seed.fabricated')
        same(left,right,'every control-tree field under exact link relation')
        same(identity(canonical(left)),bp[name],'propagated complete tree pin')
        changes[name]=(ap[name],bp[name])
    def replace_artifact_refs(value):
        if type(value) is dict:
            if set(value)=={'name','pin'} and value['name'] in changes:
                old,new=changes[value['name']];same(value['pin'],old,'old bound artifact pin')
                return {'name':value['name'],'pin':new}
            return {k:replace_artifact_refs(v) for k,v in value.items()}
        if type(value) is list:return [replace_artifact_refs(v) for v in value]
        return value
    transformed=replace_artifact_refs(normal['result'])
    same(transformed,optimized['result'],'entire mode report with only3 tree-pin propagation')
    same(identity(canonical(transformed)),bp['WHITE_ONLY_QUALIFICATION.json'],'propagated report identity')
    changes['WHITE_ONLY_QUALIFICATION.json']=(ap['WHITE_ONLY_QUALIFICATION.json'],bp['WHITE_ONLY_QUALIFICATION.json'])
    transformed=replace_artifact_refs(normal)
    transformed['result']=replace_artifact_refs(normal['result'])
    transformed['report_pin']=bp['WHITE_ONLY_QUALIFICATION.json']
    for row in transformed['postchecks']:
        name=row['role'].removeprefix('artifact:')
        if row['role'].startswith('artifact:') and name in changes:
            same(row['pin'],changes[name][0],'old artifact postcheck pin');row['pin']=changes[name][1]
    for record in transformed['namespace']['inventory']['records']:
        if record['name'] in changes and record['kind']=='file':
            same(record['pin'],changes[record['name']][0],'old namespace artifact pin');record['pin']=changes[record['name']][1]
        if record['kind']=='symlink':
            need(record['name'] in [x+'/WC19-link.fabricated' for x in TREES[1:]],'only2 declared namespace links')
            tree=record['name'].split('/')[0]
            same(record['target'],str(a/tree/'WC19-seed.fabricated'),'normal namespace link target')
            record['target']=str(b/tree/'WC19-seed.fabricated')
    same(transformed,optimized,'entire return envelope under closed mode relation')
    return {'schema':'ri130-complete-WHITE-mode-relation-v1','status':'all_fields_match_under_exact_custody_path_relation',
            'byte_identical_artifacts':list(FIXED_FILES),'tree_link_relation':'only2 literal WC19 absolute seed targets',
            'propagated_pin_artifacts':list(TREE_FILES)+['WHITE_ONLY_QUALIFICATION.json'],
            'complete_envelopes_compared':True,'scientific_fields_omitted':False,'full32_qualified':False}
