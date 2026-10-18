#!/usr/bin/env python3
"""Independent tests of the NEW archive metadata verifier only."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

D=Path(__file__).resolve().parent
REPO=Path('/Volumes/AI_DATA/development/det_8_framework-ret')
SRC=REPO/'docs/track_b/native_growth_connected_sensitivity_archive_check_v1'
ORIGINAL=REPO/'docs/track_b/native_growth_connected_sensitivity_result_v1'
RELOCATED=D/'relocated'/'track_b'
CHECK=RELOCATED/SRC.name
ARCHIVE=RELOCATED/ORIGINAL.name
RELOCATED.mkdir(parents=True,exist_ok=False)
shutil.copytree(SRC,CHECK)
shutil.copytree(ORIGINAL,ARCHIVE)
CASE=D/'cases'
CASE.mkdir()
results=[]

def pin(path):
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def run(name,expected,archive=None,optimized=False,default=False,checker=None):
    case=CASE/name;case.mkdir(exist_ok=True)
    cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str((checker or CHECK)/'verify_archive.py')]
    if not default:cmd+=['--archive',str(archive or ARCHIVE)]
    p=subprocess.run(cmd,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
    (case/'stdout.log').write_bytes(p.stdout);(case/'stderr.log').write_bytes(p.stderr)
    parsed=json.loads(p.stdout if expected==0 else p.stderr)
    assert p.returncode==expected,(name,p.returncode,p.stdout,p.stderr)
    assert parsed['status']==('PUBLISHED_ARCHIVE_INTEGRITY_AND_SAVED_AGREEMENT_PASS' if expected==0 else 'FAIL')
    if expected==0:
        assert parsed['files_checked']==117 and parsed['complete_certificate_sections']==19
        for k in ('archived_code_executed','independent_arithmetic_rerun','external_provenance_paths_traversed','execution_custody_readjudicated','new_scientific_or_physical_claim'):
            assert parsed[k] is False
    row={'name':name,'argv':cmd,'returncode':p.returncode,'parsed_result':parsed,'stdout':pin(case/'stdout.log'),'stderr':pin(case/'stderr.log')}
    (case/'RESULT.json').write_text(json.dumps(row,sort_keys=True,indent=2)+'\n')
    results.append(row)

run('relocated_default',0,default=True)
run('relocated_explicit',0)
run('relocated_optimized',0,optimized=True)

# One ordinary archive copy; each sequential mutation is retained outside it.
def mutate(name,relative,transform,expected_error):
    p=ARCHIVE/relative;original=p.read_bytes();case=CASE/name;case.mkdir()
    changed=transform(original);p.write_bytes(changed)
    (case/'MUTATED_ARTIFACT.bin').write_bytes(changed)
    try:
        run(name,1)
        assert expected_error in results[-1]['parsed_result']['error']
    finally:p.write_bytes(original)

mutate('changed_same_length','NORMAL_SUMMARY.json',lambda b:b.replace(b'PASS',b'FAIL',1),'content digest differs')
mutate('changed_length','NORMAL_SUMMARY.json',lambda b:b+b'\n','file size differs')
name='missing_artifact';case=CASE/name;case.mkdir();target=ARCHIVE/'NORMAL_SUMMARY.json';saved=case/'ABSENT_ARTIFACT.json';shutil.copy2(target,saved);target.rename(case/'temporary_original')
try:run(name,1)
finally:(case/'temporary_original').rename(target)
name='extra_artifact';case=CASE/name;case.mkdir();target=ARCHIVE/'unlisted.json';target.write_text('{}\n')
try:run(name,1)
finally:target.rename(case/'UNEXPECTED_ARTIFACT.json')
name='symlink_artifact';case=CASE/name;case.mkdir();target=ARCHIVE/'NORMAL_SUMMARY.json';original=case/'original.json';target.rename(original);target.symlink_to(original)
try:run(name,1)
finally:target.rename(case/'REFUSED_SYMLINK');shutil.copy2(original,target)
name='symlink_directory';case=CASE/name;case.mkdir();target=ARCHIVE/'caller';original=case/'original_caller';target.rename(original);target.symlink_to(original,target_is_directory=True)
try:run(name,1)
finally:target.rename(case/'REFUSED_SYMLINK');original.rename(target)
name='symlink_archive_root';case=CASE/name;case.mkdir();target=case/'LINK';target.symlink_to(ARCHIVE,target_is_directory=True);run(name,1,archive=target)
name='fifo_artifact';case=CASE/name;case.mkdir();target=ARCHIVE/'NORMAL_SUMMARY.json';original=case/'original.json';target.rename(original);os.mkfifo(target)
try:run(name,1)
finally:target.rename(case/'REFUSED_FIFO');shutil.copy2(original,target)
name='manifest_tamper';case=CASE/name;case.mkdir();p=CHECK/'MANIFEST.json';old=p.read_bytes();changed=old.replace(b'3027dc6813b95cc57e8637c6598a6b07325074f0',b'4027dc6813b95cc57e8637c6598a6b07325074f0',1);assert changed!=old;p.write_bytes(changed);(case/'MUTATED_MANIFEST.json').write_bytes(changed)
try:
    run(name,1)
    assert results[-1]['parsed_result']['error']=='pinned manifest differs'
finally:p.write_bytes(old)
run('restored_archive',0)

# Import only the new metadata verifier for focused saved-object unit cases.
spec=importlib.util.spec_from_file_location('new_archive_verifier_under_review',CHECK/'verify_archive.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
bodies={n:(ARCHIVE/n).read_bytes() for n in ['CERTIFICATE.json','AUDIT_REPORT.json','NORMAL_SUMMARY.json','OPTIMIZED_SUMMARY.json','ROOT_ADJUDICATION.json']}
unit=[]
def refuse(name,fn,artifact=None):
    c=CASE/name;c.mkdir()
    if artifact is not None:(c/'FABRICATED_OBJECT.json').write_bytes(artifact)
    try:fn()
    except (v.InvalidArchive,ValueError,KeyError,TypeError) as e:
        row={'name':name,'status':'EXPECTED_REFUSAL','exception':type(e).__name__,'error':str(e)}
    else:raise RuntimeError(name+' did not refuse')
    (c/'RESULT.json').write_text(json.dumps(row,sort_keys=True,indent=2)+'\n');unit.append(row)

def report_case(name,edit):
    b=dict(bodies);r=v.decode(b['AUDIT_REPORT.json']);edit(r['reconstructed_certificate']);b['AUDIT_REPORT.json']=v.canonical(r)
    refuse(name,lambda:v.verify_science(b),b['AUDIT_REPORT.json'])

report_case('nested_audit_mismatch',lambda x:x['decision'].__setitem__('actual_scale_computed',True))
report_case('nested_bool_integer_confusion',lambda x:x['decision'].__setitem__('actual_scale_computed',0))
report_case('extra_nested_audit_key',lambda x:x['decision'].__setitem__('unreviewed_extra',False))
refuse('duplicate_json_keys',lambda:v.decode(b'{"outer":{"x":1,"x":2}}'),b'{"outer":{"x":1,"x":2}}')
refuse('nonfinite_json_constant',lambda:v.decode(b'{"x":NaN}'),b'{"x":NaN}')
refuse('nonfinite_exponent_canonical',lambda:v.canonical(v.decode(b'{"x":1e999}')),b'{"x":1e999}')
b=dict(bodies);b['CERTIFICATE.json']+=b'\n';refuse('noncanonical_certificate',lambda:v.verify_science(b),b['CERTIFICATE.json'])
b=dict(bodies);b['OPTIMIZED_SUMMARY.json']+=b'\n';refuse('summary_byte_difference',lambda:v.verify_science(b),b['OPTIMIZED_SUMMARY.json'])
b=dict(bodies);root=v.decode(b['ROOT_ADJUDICATION.json']);root['programme_complete']=0;b['ROOT_ADJUDICATION.json']=v.canonical(root);refuse('root_claim_bool_integer_confusion',lambda:v.verify_science(b),b['ROOT_ADJUDICATION.json'])
assert v.same({'x':[1,False]},{'x':[1,False]}) and not v.same({'x':[1,False]},{'x':[True,0]}) and not v.same([1,2],[2,1])
unit.append({'name':'nested_type_and_array_order','status':'PASS'})

# A runtime open trace covers only verify() after the module/standard library import.
# It never traverses any referenced absolute provenance pathname.
opened=[]
def audit(event,args):
    if event=='open':opened.append(str(args[0]))
sys.addaudithook(audit)
result=v.verify(ARCHIVE)
expected={str(CHECK/'MANIFEST.json')}|{str(ARCHIVE/r['path']) for r in json.loads((CHECK/'MANIFEST.json').read_bytes())['files']}
# The read above adds one repeated manifest open, permitted and disclosed.
assert set(opened)==expected,(set(opened)-expected,expected-set(opened))
assert len(opened)==119,len(opened)
trace={'status':'PASS','open_events':opened,'distinct_open_paths':len(set(opened)),'verifier_expected_distinct_open_paths':118,'extra_review_manifest_read':1}
(D/'OPEN_TRACE.json').write_text(json.dumps(trace,sort_keys=True,indent=2)+'\n')
summary={'status':'ALL_INDEPENDENT_ARCHIVE_TESTS_PASS','python':sys.version,'cli_cases':results,'saved_object_cases':unit,'scope':'Only NEW metadata verifier imported/executed; archived code never executed; no scientific arithmetic rerun, external custody authentication, or provenance traversal.','open_trace':str(D/'OPEN_TRACE.json')}
(D/'TEST_RESULTS.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':summary['status'],'cli_cases':len(results),'saved_object_cases':len(unit),'python':sys.version,'distinct_verified_open_paths':118,'review_directory':str(D)}))
