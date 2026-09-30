"""Root external metadata collector; never loads a target/control/launcher."""
import importlib.util, os, stat, subprocess, sys, time
from pathlib import Path
s=importlib.util.spec_from_file_location('m','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=Path(__file__).resolve().parent
phase=sys.argv[1];assert phase in ('PRE','POST')
layout=m.load(m.D/'OPERATION_LAYOUT.json');assert dict(os.environ)==layout['environment']
selected=m.identity(layout['selected_interpreter_binding']['path']);assert selected==layout['selected_interpreter_binding']
assert sys.executable==selected['path']
started=time.monotonic()
prefix=Path('/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9')
env={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
commands=[]
for argv in [['/usr/bin/xcode-select','-p'],['/usr/bin/xcrun','--find','python3']]:
 p=subprocess.run(argv,env=env,capture_output=True,timeout=10,check=True)
 assert not p.stderr
 commands.append(dict(command=argv,stdout=p.stdout.decode(),stderr=p.stderr.decode(),exit_code=p.returncode))
assert commands[0]['stdout'].strip()=='/Applications/Xcode.app/Contents/Developer'
assert commands[1]['stdout'].strip()=='/Applications/Xcode.app/Contents/Developer/usr/bin/python3'
names=['/usr/bin/env','/usr/bin/perl','/usr/bin/python3','/bin/ps','/usr/bin/xcode-select','/usr/bin/xcrun',
 '/System/Library/CoreServices/SystemVersion.plist',commands[1]['stdout'].strip(),str(prefix/'Python3')]
bindings=[m.identity(p) for p in names]
assert Path(sys.executable).resolve()==Path(bindings[-2]['resolved_path'])
assert Path(sys.prefix)==prefix
rows=[];stack=[prefix];total=0
while stack:
 parent=stack.pop()
 for p in sorted(parent.iterdir()):
  st=p.lstat();row=dict(path=str(p))
  if stat.S_ISLNK(st.st_mode):row.update(kind='symlink',target=os.readlink(p))
  elif stat.S_ISDIR(st.st_mode):row['kind']='directory';stack.append(p)
  else:
   assert stat.S_ISREG(st.st_mode);identity=m.identity(p);assert identity['bytes']<=67108864
   row.update(kind='file',identity=identity);total+=identity['bytes']
  rows.append(row);assert len(rows)<=25000 and time.monotonic()-started<180
rows.sort(key=lambda x:x['path'])
paths=list(sys.path)
assert all(Path(p)==prefix/'lib/python39.zip' or Path(p).is_relative_to(prefix) for p in paths)
absences=[]
for p in [prefix/'lib/python39.zip',Path('/Library/Python/3.9/site-packages')]:
 if not os.path.lexists(p):absences.append(str(p))
 else:assert p.is_relative_to(prefix),'unexpected external system site-packages'
modules=[]
for name,mod in sorted(sys.modules.items()):
 if mod is None:continue
 spec=getattr(mod,'__spec__',None);f=getattr(mod,'__file__',None)
 row=dict(name=name,file=f,origin=getattr(spec,'origin',None),cached=getattr(mod,'__cached__',None),loader_type=type(getattr(spec,'loader',None)).__name__)
 if f and Path(f).is_absolute():row['identity']=m.identity(f)
 modules.append(row)
observation=dict(schema='ri152-root-direct-vendor-bootstrap-observation-v1',actual_environment=dict(os.environ),selected_interpreter_binding=selected,collector=m.ref(__file__),metadata_helper=m.ref(m.B/'ri122-root-execution-review-6whn_vky/metadata.py'),
 host=list(os.uname()),commands=commands,bindings=bindings,prefix=str(prefix),framework_namespace=rows,framework_file_bytes=total,
 bootstrap_descriptor=dict(executable=sys.executable,prefix=sys.prefix,version=sys.version,path=paths,isolated=sys.flags.isolated,dont_write_bytecode=sys.flags.dont_write_bytecode,optimize=sys.flags.optimize,modules=modules),
 absences=absences,scope='Opaque vendor-bootstrap selection and full installed framework metadata; no candidate science runtime or target entry.',
 trusted_premises=['Root tool and Apple vendor bootstrap collector','Darwin kernel and Apple loader/shared cache','Stable host and supplier; opaque byte equality is not an instruction trace or source/cache equivalence'],
 target_or_launcher_execution=False)
if phase=='POST':
 before=m.load(m.D/'BOOTSTRAP_PRE.json')
 for key in ('host','commands','bindings','prefix','framework_namespace','framework_file_bytes','absences','actual_environment','selected_interpreter_binding'):
  assert observation[key]==before[key],key+' drift'
 assert observation['bootstrap_descriptor']==before['bootstrap_descriptor'],'descriptor drift'
print(m.save('BOOTSTRAP_'+phase+'.json',observation))
print({'entries':len(rows),'file_bytes':total,'elapsed_seconds':time.monotonic()-started})
