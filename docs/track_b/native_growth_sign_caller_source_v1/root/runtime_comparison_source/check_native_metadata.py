"""External root custody: opaque files and administrative metadata only."""
from metadata import *
import errno
import plistlib
import sys

E=B/'ri122-native-caller-source-jgehvvxx'
PINS={
 'HANDOFF.json':(23450,'28acf383f4d70d08a9d2965b8665e2969e4e91e817f0edf3699acaf16b0df474'),
 'RUNTIME_CLOSURE.json':(2862854,'35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920'),
 'HISTORY_RECONCILIATION.json':(2170307,'b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c')}

def need(value,reason):
    if not value: raise ValueError(reason)

def full(path):
    row=identity(path)
    return dict(path=row['path'],resolved_path=row['resolved_path'],symlinks=row['symlink_chain'],bytes=row['bytes'],sha256=row['sha256'])

def resolve_any(path):
    pending=list(Path(path).parts[1:]);current=Path('/');links=[]
    while pending:
        part=pending.pop(0)
        if part in ('','.'):continue
        if part=='..':current=current.parent;continue
        candidate=current/part;value=candidate.lstat()
        if stat.S_ISLNK(value.st_mode):
            need(len(links)<64,'link loop')
            target=os.readlink(candidate);links.append(dict(path=str(candidate),target=target))
            t=Path(target)
            if t.is_absolute():current=Path('/');pending=list(t.parts[1:])+pending
            else:pending=list(t.parts)+pending
        else:current=candidate
    return current,links

def directory(path):
    resolved,links=resolve_any(path);before=resolved.lstat()
    need(stat.S_ISDIR(before.st_mode),'not directory')
    def members():
        rows=[]
        with os.scandir(resolved) as iterator:
            for entry in iterator:
                st=entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(st.st_mode):row=dict(name=entry.name,kind='symlink',target=os.readlink(entry.path))
                elif stat.S_ISREG(st.st_mode):row=dict(name=entry.name,kind='file')
                elif stat.S_ISDIR(st.st_mode):row=dict(name=entry.name,kind='dir')
                else:raise ValueError('unexpected object')
                rows.append(row)
        return sorted(rows,key=lambda x:x['name'])
    rows=members();again=members();after=resolved.lstat()
    sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)
    need(rows==again and sig(before)==sig(after) and resolve_any(path)==(resolved,links),'directory changed')
    return dict(path=str(path),resolved_path=str(resolved),symlinks=links,entries=rows)

def location(path):
    try:value=Path(path).lstat()
    except FileNotFoundError as error:
        need(error.errno==errno.ENOENT,'wrong missing status');return 'absent'
    if stat.S_ISLNK(value.st_mode):return 'symlink'
    need(stat.S_ISREG(value.st_mode),'unsupported system object');return 'regular_file'

def check():
    for name,(count,digest) in PINS.items():verify(E/name,dict(bytes=count,sha256=digest))
    runtime=load(E/'RUNTIME_CLOSURE.json');history=load(E/'HISTORY_RECONCILIATION.json');handoff=load(E/'HANDOFF.json')
    records=[];errors=[]
    def record(group,path,fn,expected):
        try:
            actual=fn();need(actual==expected,'identity differs')
            records.append(dict(group=group,path=str(path),ok=True,observed=actual))
        except Exception as error:
            errors.append(dict(group=group,path=str(path),error=type(error).__name__+': '+str(error)))
    for group,rows in [('sealed',handoff['artifacts']),('runtime',runtime['files']),('history',history['protected_files'])]:
        for row in rows:
            expected=row['identity'] if 'identity' in row else {k:row[k]for k in ('path','resolved_path','symlinks','bytes','sha256')}
            record(group,row['path'],lambda p=row['path']:full(p),expected)
    for row in runtime['directories']:record('directory',row['path'],lambda p=row['path']:directory(p),row)
    def absent(path):
        try:Path(path).lstat()
        except FileNotFoundError as error:
            need(error.errno==errno.ENOENT,'not ENOENT');return True
        return False
    for path in runtime['absences']:record('absence',path,lambda p=path:absent(p),True)
    host=runtime['host_platform']
    record('host','uname',lambda:{k:getattr(os.uname(),k)for k in host['expected_uname']},host['expected_uname'])
    def version():
        p=Path(host['system_version_plist']['path']);expected=next(r['identity']for r in runtime['files']if r['path']==str(p))
        need(full(p)==expected,'plist preidentity');raw=p.read_bytes();need(pin(raw)==pure(expected),'plist body')
        values=plistlib.loads(raw);need(full(p)==expected,'plist postidentity')
        return {k:values[k]for k in host['system_version_plist']['expected_values']}
    record('host',host['system_version_plist']['path'],version,host['system_version_plist']['expected_values'])
    for row in host['system_dependencies']:record('system_location',row['install_name'],lambda p=row['install_name']:location(p),row['location_status'])
    for name,(count,digest) in PINS.items():verify(E/name,dict(bytes=count,sha256=digest))
    result=dict(schema='ri122-root-external-metadata-custody-v1',all_match=not errors,errors=errors,
                counts=dict(sealed=len(handoff['artifacts']),runtime=len(runtime['files']),history=len(history['protected_files']),directories=len(runtime['directories']),absences=len(runtime['absences']),system_locations=len(host['system_dependencies'])),
                manifests={name:ref(E/name) for name in PINS},records=records,
                trust_boundary=host['trust_boundary'],native_target_invoked=False,actual_runtime_profile_measured=False)
    return result

if __name__=='__main__':
    result=check();print(save(sys.argv[1],result));print(json.dumps({'all_match':result['all_match'],'counts':result['counts'],'errors':result['errors']}))
    if not result['all_match']:raise SystemExit(1)
