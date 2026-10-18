"""Administrative source-text builder only. It never imports proposed code."""
from pathlib import Path
import hashlib,json,difflib,os
W=Path(__file__).resolve().parent
P=Path('/private/tmp/ri244-preparation-proposal-3udz0imk')
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,value):
 b=value.encode('ascii') if isinstance(value,str) else (json.dumps(value,sort_keys=True,indent=2)+'\n').encode('ascii')
 with (W/name).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 if (W/name).read_bytes()!=b:raise ValueError('readback '+name)
 return pin(W/name)
assert pin(W/'REFERENCES.json')['sha256']=='15745efc9d6fc4b50fdefc8877fa2d3dd976c3f26e86b57ff3cea25a38d97e1d'
assert pin(W/'MODE_CARD_REQUEST.proposal.json')['sha256']=='0ff48797216ca57b070e63ff2e3081add9421e77947c9864d9599155a4eae091'
old=(P/'prepare_unissued.py').read_text()
assert pin(P/'prepare_unissued.py')['sha256']=='02d5e3c3d617ea3c0299e313a63569d97121d6c16b57c3ce290544896ef1cfce'
s=old;changes=[]
def replace(a,b):
 global s
 n=s.count(a)
 if n==0:raise ValueError('missing marker '+repr(a))
 changes.append({'before':a,'after':b,'occurrences':n});s=s.replace(a,b)
for a,b in [
 ('UNEXECUTED RI244 administrative preparation proposal','UNEXECUTED RI249 mode-card administrative preparation proposal'),
 ("D = B/'ri244-current-normal-premode-2kfsmiea'","D = B/'ri249-normal-mode-card-preparation-y170alnf'"),
 ("O = B/'ri156-operation-ri244-premode-2kfsmiea'","O = B/'ri156-operation-ri249-mode-card-y170alnf'"),
 ('ADMIT_PRE_MODE.json','ADMIT_MODE_CARD.json'),('No ADMIT_PRE_MODE,','No ADMIT_MODE_CARD,'),
 ('PRE_MODE_BOOTSTRAP','MODE_CARD_BOOTSTRAP'),('RI244_PREPARATION:','RI249_MODE_CARD_PREPARATION:'),
 ('ri244-root-unissued-preparation-decision-v1','ri249-root-unissued-mode-card-preparation-decision-v1'),
 ('ri244_administrative_metadata_only','ri249_mode_card_administrative_metadata_only'),
 ('ri244-unissued-preparation-attempt-v1','ri249-unissued-mode-card-preparation-attempt-v1'),
 ('ri244-complete-preparation-custody-v1','ri249-complete-mode-card-preparation-custody-v1'),
 ('ri244-root-unissued-premode-preflight-v1','ri249-root-unissued-mode-card-preflight-v1'),
 ('# UNISSUED RI244 bootstrap proposal.','# UNISSUED RI249 mode-card bootstrap proposal.'),
 ('ri244_whole_unchanged_ri141_premode_monitor','ri249_whole_unchanged_ri141_mode_card_monitor'),
 ('''"'PRE_MODE', 180, expected_environment)"''','''"'MODE_CARD', 180, expected_environment)"'''),
 ("'action':'pre_mode'","'action':'mode_card'"),
 ('ri244-wrapped-unissued-admission-v1','ri249-wrapped-unissued-mode-card-admission-v1'),
 ('ri244-unissued-preparation-completion-v1','ri249-unissued-mode-card-preparation-completion-v1'),
 ("'BOOTSTRAP_PREFLIGHT.json','MODE_CARD_BOOTSTRAP.proposal.py'","'BOOTSTRAP_PREFLIGHT.json','MODE_CARD_REQUEST.json','MODE_CARD_BOOTSTRAP.proposal.py'"),
 ("str(W/'REFERENCES.json'),'bytes':4500","str(W/'REFERENCES.json'),'bytes':6775"),
 ('e1043bed3183088b4718a6dbfd3ea563b93d8875075fb60a148f71294b3c0b70','15745efc9d6fc4b50fdefc8877fa2d3dd976c3f26e86b57ff3cea25a38d97e1d')]:replace(a,b)
block="""    # The earlier action is accepted externally; never substitute a pass label
    # for the whole pinned pre result, prior custody, original outputs or sources.
    pre_review=read(refs['pre_mode_acceptance']);keep_refs(pre_review)
    same([pre_review['status'],pre_review['scientific_execution'],pre_review['mode_card_created'],
          pre_review['qualification_credit'],pre_review['RET_paused']],
         ['ACCEPT_ONE_NORMAL_PRE_MODE_METADATA_OPERATION_ONLY',False,False,0,True],'accepted metadata predecessor only')
    same([pre_review['result'],pre_review['root_custody'],pre_review['root_check']],
         [refs['pre_result'],refs['pre_mode_postflight'],refs['pre_mode_root_check']],'exact predecessor bindings')
    pre_result=read(refs['pre_result']);keep_refs(pre_result)
    same(pre_result,{'schema':'ri130-root-pre-mode-runtime-custody-v1','mode':'normal',
         'freeze':runtime['freeze'],'runtime_acceptance':runtime['runtime_acceptance'],
         'selection_unchanged':True,'optional_namespaces_unchanged':True,'host_identity_unchanged':True,
         'observed_dyld_routes':runtime['observed_dyld_routes'],'metadata_record':refs['runtime']},'whole accepted pre result9')
    previous=read(refs['pre_mode_postflight']);keep_refs(previous)
    same([previous['schema'],previous['phase'],previous['status'],previous['immutable_preparation_input_rows'],
          previous['E_files'],previous['E_directories'],previous['E_unchanged'],previous['subject_executed_by_this_script']],
         ['ri249-whole-premode-custody-v1','postflight','PASS_METADATA_CUSTODY',2854,49,9,True,False],'whole accepted previous custody domain')
    need(len(previous['input_identities'])==2883,'all previous operation custody identities')
    for row in previous['input_identities']:fresh(row)
    prior_check=read(refs['pre_mode_root_check']);keep_refs(prior_check)
    same(prior_check['full_result'],pre_result,'complete actual pre reconstruction')
    same([prior_check['status'],prior_check['scientific_execution'],prior_check['mode_card_created']],
         ['PASS_COMPLETE_METADATA_OPERATION_RECONSTRUCTION',False,False],'root predecessor scope')
    need(len(prior_check['output_identities'])==3 and len(prior_check['monitor_identities'])==4,'prior output/monitor domains')
    for row in prior_check['output_identities']+prior_check['monitor_identities']:fresh(row)
    prior_output=Path(refs['pre_result']['path']).parent
    prior_monitor=Path(prior_check['monitor_identities'][0]['path']).parent
    prior_D=prior_monitor.parent
    same(str(prior_output),str(B/'ri156-operation-ri244-premode-2kfsmiea'),'exact completed prior output')
    same(str(prior_D),str(B/'ri244-current-normal-premode-2kfsmiea'),'exact completed prior preparation')
    mode_request={'freeze':request['freeze'],'mode':'normal','pre':refs['pre_result'],'normal_acceptance':None}
    sealed_request=next(row for row in handoff['files'] if row['path']==str(W/'MODE_CARD_REQUEST.proposal.json'))
    need(canonical(mode_request)==initial_body(sealed_request['path'],sealed_request['sha256']),'whole sealed request4 source')
"""
marker="    oldroles=read(refs['old_roles']);need(len(oldroles['observed_identities'])==2811,'all retained custody identities')"
replace(marker,block+marker)
marker="             ['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json'],'preserved RI241 namespace')"
addition="""
        same(sorted(p.name for p in prior_output.iterdir()),['ATTEMPT.json','COMPLETE.json','RESULT.json'],'prior pre-mode output namespace')
        same(sorted(p.name for p in prior_monitor.iterdir()),
             ['PRE_MODE.ATTEMPT.json','PRE_MODE.COMPLETION.json','PRE_MODE.stderr','PRE_MODE.stdout'],'prior monitor namespace')
        same(sorted(p.name for p in prior_D.iterdir()),previous['D_namespace'],'whole prior preparation namespace')
        same(sorted(p.name for p in (prior_D/'tmp').iterdir()),[],'prior operation tmp empty')"""
replace(marker,marker+addition)
marker="        vendor=emit('SUPPLIER_BEFORE.json',before_supplier);e_ref=emit('E_BEFORE.json',before_E)"
replace(marker,marker+"\n        request_ref=emit('MODE_CARD_REQUEST.json',mode_request)")
replace("'input_acceptance':refs['input_review']","'input_acceptance':refs['pre_mode_acceptance']")
replace("'request':refs['request']","'request':request_ref")
replace("'root_input_acceptance':refs['input_review']","'root_input_acceptance':refs['pre_mode_acceptance']")
reverse=s
for c in reversed(changes):
 if reverse.count(c['after'])!=c['occurrences']:raise ValueError('inverse count '+repr(c['after']))
 reverse=reverse.replace(c['after'],c['before'])
if reverse!=old:raise ValueError('entire source reversal')
boot=(P/'PRE_MODE_BOOTSTRAP.proposal.txt').read_text()
newboot=boot
for a,b in [('# UNISSUED RI244 bootstrap proposal.','# UNISSUED RI249 mode-card bootstrap proposal.'),
 ('ri244_whole_unchanged_ri141_premode_monitor','ri249_whole_unchanged_ri141_mode_card_monitor'),
 ('ri244-current-normal-premode-2kfsmiea','ri249-normal-mode-card-preparation-y170alnf'),
 ('ADMIT_PRE_MODE.json','ADMIT_MODE_CARD.json'),("'PRE_MODE', 180, expected_environment)","'MODE_CARD', 180, expected_environment)")]:
 if a not in newboot:raise ValueError('bootstrap marker '+a)
 newboot=newboot.replace(a,b)
rows=[write('prepare_unissued.py',s),write('MODE_CARD_BOOTSTRAP.proposal.txt',newboot),
 write('SOURCE_CHANGES.json',{'schema':'ri249-mode-card-source-changes-v1','predecessor':pin(P/'prepare_unissued.py'),'changes':changes,'whole_reverse_exact':True}),
 write('SOURCE_DIFF.patch',''.join(difflib.unified_diff(old.splitlines(keepends=True),s.splitlines(keepends=True),fromfile=str(P/'prepare_unissued.py'),tofile=str(W/'prepare_unissued.py')))),
 write('BOOTSTRAP_DIFF.patch',''.join(difflib.unified_diff(boot.splitlines(keepends=True),newboot.splitlines(keepends=True),fromfile=str(P/'PRE_MODE_BOOTSTRAP.proposal.txt'),tofile=str(W/'MODE_CARD_BOOTSTRAP.proposal.txt'))))]
print(json.dumps({'source_text_only':True,'whole_reverse_exact':True,'files':rows}))
