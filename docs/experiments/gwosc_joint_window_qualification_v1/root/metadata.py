"""Root metadata custody only; never imports or runs a scientific target."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

D = Path(__file__).resolve().parent
B = D.parent
REPO = Path('/Volumes/AI_DATA/development/det_8_framework-ret')

def canonical(v):
    return (json.dumps(v, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()

def pin(body):
    return dict(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())

def identity(path):
    p=Path(path)
    if not p.is_absolute(): raise ValueError('nonabsolute path')
    pending=list(p.parts[1:]); current=Path('/'); links=[]
    while pending:
        part=pending.pop(0)
        if part in ('','.'): continue
        if part=='..': current=current.parent; continue
        q=current/part; st=q.lstat()
        if stat.S_ISLNK(st.st_mode):
            if len(links)>=64: raise ValueError('link loop')
            target=os.readlink(q); links.append(dict(path=str(q),target=target))
            t=Path(target)
            if t.is_absolute(): current=Path('/'); pending=list(t.parts[1:])+pending
            else: pending=list(t.parts)+pending
        else: current=q
    a=current.lstat()
    if not stat.S_ISREG(a.st_mode): raise ValueError('not regular')
    key=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    h=hashlib.sha256(); n=0
    fd=os.open(current,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        if key(a)!=key(os.fstat(f.fileno())): raise ValueError('open changed')
        for body in iter(lambda:f.read(1024*1024),b''): h.update(body); n+=len(body)
        z=os.fstat(f.fileno())
    if key(a)!=key(z) or key(z)!=key(current.lstat()) or n!=a.st_size or p.resolve()!=current:
        raise ValueError('changed during hash')
    for link in links:
        if os.readlink(link['path'])!=link['target']: raise ValueError('changed link')
    return dict(path=str(p),resolved_path=str(current),symlink_chain=links,bytes=n,sha256=h.hexdigest(),state=key(z))

def pure(row): return {k:row[k] for k in ('bytes','sha256')}
def ref(path): return {k:identity(path)[k] for k in ('path','bytes','sha256')}
def verify(path,expected):
    row=identity(path)
    if pure(row)!=pure(expected): raise ValueError('pin differs: '+str(path))
    return row
def load(path): return json.loads(Path(path).read_bytes())
def save(name,v):
    p=D/name
    with p.open('xb') as f: f.write(canonical(v)); f.flush(); os.fsync(f.fileno())
    return ref(p)
def git(*args): return subprocess.check_output(['git',*args],cwd=REPO)
def snapshot():
    names=git('ls-files','--cached','--others','--exclude-standard','-z').split(b'\0')
    files=[identity(REPO/os.fsdecode(n)) for n in sorted(set(names)) if n]
    return dict(head=git('rev-parse','HEAD').decode().strip(),branch=git('branch','--show-current').decode().strip(),
                upstream=git('rev-parse','--abbrev-ref','@{upstream}').decode().strip(),
                index=git('diff','--cached','--name-only','-z').decode(),files=files)

if __name__=='__main__':
    print(json.dumps(save('REPO_ENTRY.json',snapshot())))
