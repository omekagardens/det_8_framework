"""Author administrative literal/opaque checker. Never imports proposed sources."""
from pathlib import Path
import hashlib,json,difflib,os,stat
W=Path(__file__).resolve().parent
P=Path('/private/tmp/ri244-preparation-proposal-3udz0imk')
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri249-normal-mode-card-preparation-y170alnf'
O=B/'ri156-operation-ri249-mode-card-y170alnf'
checks=0;pins={}
def need(ok,label):
    global checks
    if not ok:raise ValueError(label)
    checks+=1
def canonical(v):return (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def same(a,b,label):need(canonical(a)==canonical(b),label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(path):
    p=Path(path);before=p.lstat();body=p.read_bytes();after=p.lstat()
    need(state(before)==state(after),'opaque stable '+str(p))
    row={'path':str(p),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
    if str(p) in pins:same(pins[str(p)],row,'repeated opaque pin')
    pins[str(p)]=row;return row
def check_ref(row):
    need(type(row) is dict and {'path','bytes','sha256'}<=set(row),'declared reference')
    same(identity(row['path']),{k:row[k] for k in ('path','bytes','sha256')},'whole declared body pin')
def load(path):
    def pairs(rows):
        d={}
        for k,v in rows:
            need(k not in d,'duplicate administrative key');d[k]=v
        return d
    return json.loads(Path(path).read_bytes(),object_pairs_hook=pairs)
refs=load(W/'REFERENCES.json');need(len(refs)==27,'complete direct references27')
oldrefs=load(P/'REFERENCES.json');need(len(oldrefs)==18,'predecessor references18')
for key,row in oldrefs.items():same(refs[key],row,'unchanged original reference '+key)
for row in refs.values():check_ref(row)
manifest=load(refs['source_manifest']['path'])
need(len(manifest['modules'])==11 and len(manifest['dependencies'])==567,'all source cardinalities')
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:check_ref(row)
need(len({r['path'] for r in manifest['dependencies']})==567,'unique full dependency declaration')
source=(W/'prepare_unissued.py').read_text();oldsource=Path(refs['direct_preparation_predecessor']['path']).read_text()
changes=load(W/'SOURCE_CHANGES.json');same(changes['predecessor'],refs['direct_preparation_predecessor'],'exact source predecessor')
projected=oldsource
for c in changes['changes']:
    need(projected.count(c['before'])==c['occurrences'],'source literal occurrence')
    projected=projected.replace(c['before'],c['after'])
need(projected==source,'whole forward source projection')
reverse=source
for c in reversed(changes['changes']):
    need(reverse.count(c['after'])==c['occurrences'],'inverse source occurrence')
    reverse=reverse.replace(c['after'],c['before'])
need(reverse==oldsource,'whole inverse source projection')
start='    def input_tail():';end="    completion={'schema':"
need(source[source.index(start):source.index(end)]==oldsource[oldsource.index(start):oldsource.index(end)],'entire six-tail block byte equality')
for a,b in [('def canonical(value):','def main():'),('    oldroles=read(',"    def absent_authority():")]:
    need(source[source.index(a):source.index(b)]==oldsource[oldsource.index(a):oldsource.index(b)],'unchanged complete function/closure span')
bootstrap=(W/'MODE_CARD_BOOTSTRAP.proposal.txt').read_text();oldboot=(P/'PRE_MODE_BOOTSTRAP.proposal.txt').read_text()
for name,old,new,oldpath,newpath in [('SOURCE_DIFF.patch',oldsource,source,refs['direct_preparation_predecessor']['path'],str(W/'prepare_unissued.py')),
 ('BOOTSTRAP_DIFF.patch',oldboot,bootstrap,str(P/'PRE_MODE_BOOTSTRAP.proposal.txt'),str(W/'MODE_CARD_BOOTSTRAP.proposal.txt'))]:
    expected=''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile=oldpath,tofile=newpath))
    need((W/name).read_text()==expected,'whole exact diff '+name)
adref={'path':str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),'bytes':2114,'sha256':'ac86cac1f9973266d84b2a1ad1b9a34e9655d897153dc264d6b0805f437389cd'}
check_ref(adref);ad=load(adref['path']);env=dict(ad['environment'],TMPDIR=str(D/'tmp'))
base=Path(refs['bootstrap_template']['path']).read_text()
replace=[('# One root-admitted administrative adapters action; unchanged RI141 child monitor.','# UNISSUED RI249 mode-card bootstrap proposal. Separate root admission/dispatch required.'),
 (repr(ad['environment']),repr(env)),('ri204_whole_unchanged_ri141_adapters_monitor','ri249_whole_unchanged_ri141_mode_card_monitor'),
 (str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),str(D/'ADMIT_MODE_CARD.json')),
 (str(B/'ri204-root-adapters-f04k2tg9/monitor'),str(D/'monitor')),("'ADAPTERS', 180, expected_environment)","'MODE_CARD', 180, expected_environment)")]
expected=base
for a,b in replace:need(expected.count(a)==1,'one template literal substitution');expected=expected.replace(a,b)
need(expected==bootstrap,'six-change whole RI204 bootstrap')
for a,b in reversed(replace):expected=expected.replace(b,a)
need(expected==base,'whole RI204 bootstrap inverse')
request=load(W/'MODE_CARD_REQUEST.proposal.json');oldreq=load(refs['request']['path']);runtime=load(refs['runtime']['path'])
same(request,{'freeze':oldreq['freeze'],'mode':'normal','normal_acceptance':None,'pre':refs['pre_result']},'entire request4 value')
need(canonical(request)==(W/'MODE_CARD_REQUEST.proposal.json').read_bytes(),'request canonical body')
need(len(request)==4 and request['normal_acceptance'] is None,'closed normal request4')
pre=load(refs['pre_result']['path'])
same(pre,{'schema':'ri130-root-pre-mode-runtime-custody-v1','mode':'normal','freeze':runtime['freeze'],
 'runtime_acceptance':runtime['runtime_acceptance'],'selection_unchanged':True,'optional_namespaces_unchanged':True,
 'host_identity_unchanged':True,'observed_dyld_routes':runtime['observed_dyld_routes'],'metadata_record':refs['runtime']},'whole accepted pre9 derived independently')
review=load(refs['pre_mode_acceptance']['path']);previous=load(refs['pre_mode_postflight']['path']);prior=load(refs['pre_mode_root_check']['path'])
same([review['result'],review['root_custody'],review['root_check']],[refs['pre_result'],refs['pre_mode_postflight'],refs['pre_mode_root_check']],'exact independent predecessor bindings')
same([review['status'],review['scientific_execution'],review['mode_card_created'],review['qualification_credit'],review['RET_paused']],['ACCEPT_ONE_NORMAL_PRE_MODE_METADATA_OPERATION_ONLY',False,False,0,True],'accepted scope')
same([previous['schema'],previous['phase'],previous['status'],previous['immutable_preparation_input_rows'],previous['E_files'],previous['E_directories'],previous['E_unchanged'],previous['subject_executed_by_this_script']],['ri249-whole-premode-custody-v1','postflight','PASS_METADATA_CUSTODY',2854,49,9,True,False],'saved predecessor custody domain')
need(len(previous['input_identities'])==2883,'saved full custody count, not current inventory')
need(len({x['path'] for x in previous['input_identities']})==2883,'saved full custody distinct')
for row in previous['input_identities']:
    need(set(row)=={'path','resolved_path','symlink_chain','bytes','sha256','state'} and len(row['state'])==7,'saved full identity shape')
same(prior['full_result'],pre,'whole root reconstruction result')
need(len(prior['output_identities'])==3 and len(prior['monitor_identities'])==4,'complete retained operation references')
for row in prior['output_identities']+prior['monitor_identities']:check_ref(row)
recipe=load(W/'ROOT_RECIPES.json');check_ref(recipe['actual_command_predecessor'])
genuine=load(recipe['actual_command_predecessor']['path']);oldD=str(B/'ri244-current-normal-premode-2kfsmiea')
expectedcmd=genuine['operation']['arguments']['cmd'].replace(oldD,str(D)).replace('PRE_MODE_BOOTSTRAP.proposal.py','MODE_CARD_BOOTSTRAP.proposal.py')
same(recipe['operation_arguments_if_separately_admitted'],{'cmd':expectedcmd,'workdir':str(D),'login':False,'yield_time_ms':1000,'max_output_tokens':2000},'entire actual predecessor command/cwd adaptation')
same(recipe['operation_environment'],env,'complete ten-field environment')
need(recipe['operational_authorization'] is False and recipe['prepared_request_filepin'] is None,'no fake future authority/ref')
for key in ('preparation_source','bootstrap_source','request_source'):check_ref(recipe[key])
same(recipe['operation_bounds'],{'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864},'all unchanged metadata bounds')
need(recipe['outer_alarm_seconds']==960,'retained external alarm')
for literal in ["decision_raw=initial_body(a.root_decision,a.root_decision_sha256)","exec(compile(helper,str(hp),'exec'),m.__dict__)",
 "same(descriptor_state(f),before,'initial opened descriptor')","same(descriptor_state(f),before,'initial final descriptor')",
 "same(sorted(p.name for p in prior_D.iterdir()),previous['D_namespace']", "for row in previous['input_identities']:fresh(row)",
 "request_ref=emit('MODE_CARD_REQUEST.json',mode_request)","'qualification':refs['qualification'],'request':request_ref", "'action':'mode_card'",
 "need(canonical(mode_request)==initial_body(sealed_request['path'],sealed_request['sha256'])", "snapshot=list(seen.values())", "'UNISSUED_NOT_OPERATIONAL_AUTHORITY'",
 "need((D/name).read_bytes()==body", "'input_acceptance':refs['pre_mode_acceptance']", "'root_input_acceptance':refs['pre_mode_acceptance']",
 "'MODE_CARD_REQUEST.json','MODE_CARD_BOOTSTRAP.proposal.py'", "'ADMIT_MODE_CARD.json'", "len(candidate)==12", "[1810,48024515,4,195,2]", "len(rows)==58 and sum(x['kind']=='file' for x in rows)==49"]:
    need(literal in source,'required exact source check '+literal)
need(source.index("need(len(helper)==3144")<source.index('exec(compile(helper'),'authenticate helper before load')
need(source.index('first=None;artifacts={}')<source.index("(D/'tmp').mkdir"),'safe state before ownership')
need("(D/'tmp').mkdir(mode=0o700)  # Failure here is genuine preownership refusal.\n    try:\n        (D/'monitor').mkdir" in source,'immediate owned protection')
need(source.index("for row in previous['input_identities']:fresh(row)")<source.index('snapshot=list(seen.values())'),'extended inputs retained in snapshot')
need(source.index("request_ref=emit('MODE_CARD_REQUEST.json'")>source.index("        (D/'monitor').mkdir"),'request in protected body')
for forbidden in ["emit('ADMIT_MODE_CARD.json'","emit('DISPATCH.json'","subprocess.run(","subprocess.Popen(","m.git(","m.snapshot(","read(request['freeze'])","O.mkdir","os.chdir(","unlink("]:
    need(forbidden not in source,'forbidden action absent '+forbidden)
need(source.count('exec(compile(')==1,'sole future admin helper load')
need(not os.path.lexists(D) and not os.path.lexists(O),'prospective D/O remain uncreated')
for name in ['prepare_unissued.py','REFERENCES.json','MODE_CARD_REQUEST.proposal.json','MODE_CARD_BOOTSTRAP.proposal.txt','SOURCE_CHANGES.json','SOURCE_DIFF.patch','BOOTSTRAP_DIFF.patch','PROTOCOL.md','ROOT_RECIPES.json','AUTHOR_DESIGN_AUDIT.md','build_source.py','AUTHORING_FAILURE_02e746.json','check_source_metadata.py']:identity(W/name)
result={'schema':'ri249-mode-card-author-metadata-check-v1','status':'AUTHOR_TEXT_METADATA_PASS_NOT_QUALIFICATION','saved_predicates':checks,'opaque_distinct_files':len(pins),'identities':list(pins.values()),'original_references':18,'current_references':27,'source_dependencies':567,'saved_previous_custody_rows':2883,'source_inverse_exact':True,'whole_two_diffs_exact':True,'six_tail_block_byte_identical':True,'whole_bootstrap_six_substitutions_reversed':True,'subject_import_compile_AST_probe_execution':False,'scientific_body_decoded':False,'fresh_vendor_or_E_inventory':False,'independent_acceptance':False}
body=canonical(result)
with (W/'AUTHOR_CHECK.json').open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
need((W/'AUTHOR_CHECK.json').read_bytes()==body,'author report raw-byte readback')
print(json.dumps({'saved_predicates':result['saved_predicates'],'readback_predicates':1,'opaque_distinct_files':len(pins),'report':{'path':str(W/'AUTHOR_CHECK.json'),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}}))
