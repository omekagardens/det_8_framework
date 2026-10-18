"""RI156 bounded administrative byte/namespace I/O. Unexecuted source."""
import hashlib
import json
import math
import os
from pathlib import Path
import stat

CAP=67108864
TREE_CAP=25000
TREE_BYTES=536870912

def need(ok,message):
    if not ok:raise ValueError('RI156_IO: '+message)

def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')

def same(left,right,message):need(canonical(left)==canonical(right),message)

def keys(value,names,message):need(type(value) is dict and set(value)==set(names),message)

def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def literal(name):
    need(type(name) is str,'path type')
    p=Path(name)
    need(p.is_absolute() and str(p)==name and p.resolve()==p,'literal resolved path')
    return p

def identity(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def pin_shape(p,empty=False):
    keys(p,('bytes','sha256'),'pin fields')
    need(type(p['bytes']) is int and (0 if empty else 1)<=p['bytes']<=CAP,'bounded pin bytes')
    need(type(p['sha256']) is str and len(p['sha256'])==64 and all(x in '0123456789abcdef' for x in p['sha256']),'sha256')

def observe(name,empty=True):
    p=literal(str(name));before=p.lstat()
    need(stat.S_ISREG(before.st_mode) and (0 if empty else 1)<=before.st_size<=CAP,'bounded regular nonsymlink file')
    digest=hashlib.sha256();n=0
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        same(state(os.fstat(f.fileno())),state(before),'opened state drift')
        while True:
            part=f.read(65536)
            if not part:break
            n+=len(part);need(n<=CAP,'stream cap');digest.update(part)
        same(state(os.fstat(f.fileno())),state(before),'descriptor state drift')
    same(state(p.lstat()),state(before),'final state drift');need(n==before.st_size,'length drift')
    return {'path':str(p),'bytes':n,'sha256':digest.hexdigest(),'state':state(before)}

def ref(name,empty=True):
    return {k:v for k,v in observe(name,empty).items() if k!='state'}

def file_pin(name):return {k:v for k,v in ref(name).items() if k!='path'}

def body(row,empty=False):
    keys(row,('path','bytes','sha256'),'FilePin fields');pin_shape({k:row[k] for k in ('bytes','sha256')},empty)
    before=observe(row['path'],empty);same({k:v for k,v in before.items() if k!='state'},row,'FilePin drift')
    with literal(row['path']).open('rb') as stream:data=stream.read(CAP+1)
    need(len(data)<=CAP,'bounded body read');same(identity(data),{k:row[k] for k in ('bytes','sha256')},'body drift')
    same(observe(row['path'],empty),before,'body final state drift');return data

def parse(data):
    def pairs(rows):
        out={}
        for key,value in rows:
            need(key not in out,'duplicate metadata key');out[key]=value
        return out
    def bad(_):raise ValueError('RI156_IO: nonfinite JSON')
    value=json.loads(data.decode('ascii'),object_pairs_hook=pairs,parse_constant=bad)
    same(data.decode('ascii'),canonical(value).decode('ascii'),'canonical metadata body');return value

def read(row,empty=False):return parse(body(row,empty))

def verified_body(path,pin):return body({'path':str(path),**pin},empty=pin.get('bytes')==0)

def write(path,value):
    p=literal(str(path));data=canonical(value);need(len(data)<=CAP,'emitted file cap')
    with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    return ref(p)

def tree(root):
    root=literal(str(root));need(root.is_dir(),'owned tree directory')
    rows=[];total=0
    def visit(path,depth):
        nonlocal total
        need(depth<=16 and len(rows)<TREE_CAP,'owned tree bound')
        before=path.lstat();relative=str(path.relative_to(root));row={'relative':relative}
        if stat.S_ISLNK(before.st_mode):
            target=os.readlink(path);need(len(target)<=4096,'bounded link target');row.update(kind='symlink',target=target)
        elif stat.S_ISDIR(before.st_mode):row['kind']='directory'
        else:
            need(stat.S_ISREG(before.st_mode),'special owned member');p=ref(path);total+=p['bytes'];need(total<=TREE_BYTES,'owned aggregate bytes')
            row.update(kind='file',bytes=p['bytes'],sha256=p['sha256'])
        rows.append(row)
        if row['kind']=='directory':
            with os.scandir(path) as scan:names=sorted(x.name for x in scan)
            for name in names:visit(path/name,depth+1)
            with os.scandir(path) as scan:same(sorted(x.name for x in scan),names,'directory membership drift')
        same(state(path.lstat()),state(before),'tree entry state drift')
    visit(root,0);return sorted(rows,key=lambda x:x['relative'])

def tails(actions,first=None):
    results={}
    for name,fn in actions:
        try:results[name]={'value':fn(),'error':None}
        except BaseException as exc:
            error={'type':type(exc).__name__,'message':str(exc)[:2048]}
            results[name]={'value':None,'error':error}
            if first is None:first=error
    return results,first

# Explicit compatibility surface for unchanged retained metadata predicates.
# No import/load/launch entry is provided here.
def require(condition,message):need(condition,message)
def parse_json(data):return parse(data)
