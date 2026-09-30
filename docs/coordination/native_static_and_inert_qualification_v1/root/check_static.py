"""Independent finite metadata and Mach-O header audit; no target evaluation."""
import base64, hashlib, importlib.util, json, os, re, struct
from pathlib import Path
HP=Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
hb=HP.read_bytes()
assert len(hb)==3144 and hashlib.sha256(hb).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
sp=importlib.util.spec_from_file_location('metadata',HP);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
m.D=Path(__file__).resolve().parent
S=m.B/'ri164-native-supplier-closure-ddcuy7rz'
m.verify(S/'HANDOFF.json',dict(bytes=8680,sha256='436565be87bab883a0fa1894afe4ffa903443e6541240c4d1400e054349cfb9d'))
h=m.load(S/'HANDOFF.json');assert sorted(p.name for p in S.iterdir())==sorted(h['namespace'])
packet=[m.verify(r['path'],r) for r in h['payloads']]
o=m.load(S/'NATIVE_OBJECTS.json')['objects'];t=m.load(S/'TOOL_OBSERVATIONS.json');g=m.load(S/'NATIVE_GRAPH.json');policy=m.load(S/'INSPECTION_POLICY.json')
deps=[m.verify(r['path'],r['identity']) for r in m.load(S/'SOURCE_DEPENDENCIES.json')['protected_files']]
assert len(deps)==322 and sum(r['bytes'] for r in deps)==37108627
sdk=Path('/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/mach-o')
header_refs=[m.identity(sdk/n) for n in ('loader.h','fat.h')]
# Values read from the installed Apple loader.h. Unsupported command kinds refuse.
codes={0x19:'LC_SEGMENT_64',2:'LC_SYMTAB',0xb:'LC_DYSYMTAB',0x1b:'LC_UUID',0x32:'LC_BUILD_VERSION',0x2a:'LC_SOURCE_VERSION',0x80000028:'LC_MAIN',0x26:'LC_FUNCTION_STARTS',0x29:'LC_DATA_IN_CODE',0x1d:'LC_CODE_SIGNATURE',0x80000022:'LC_DYLD_INFO_ONLY',0x80000034:'LC_DYLD_CHAINED_FIXUPS',0x80000033:'LC_DYLD_EXPORTS_TRIE',0xc:'LC_LOAD_DYLIB',0xd:'LC_ID_DYLIB',0xe:'LC_LOAD_DYLINKER',0x80000018:'LC_LOAD_WEAK_DYLIB',0x20:'LC_LAZY_LOAD_DYLIB',0x8000001f:'LC_REEXPORT_DYLIB',0x80000023:'LC_LOAD_UPWARD_DYLIB',0x8000001c:'LC_RPATH',0x27:'LC_DYLD_ENVIRONMENT'}
named={'LC_ID_DYLIB','LC_LOAD_DYLIB','LC_LOAD_DYLINKER','LC_LOAD_WEAK_DYLIB','LC_LAZY_LOAD_DYLIB','LC_REEXPORT_DYLIB','LC_LOAD_UPWARD_DYLIB','LC_RPATH','LC_DYLD_ENVIRONMENT'}
dylib=named-{'LC_LOAD_DYLINKER','LC_RPATH','LC_DYLD_ENVIRONMENT'}
edgekinds=dylib-{'LC_ID_DYLIB'}|{'LC_LOAD_DYLINKER'}
statekeys=['dev','ino','mode','nlink','size','mtimeNs','ctimeNs']
def state(d):return [int(d[k]) for k in statekeys]
def capture(c):
 b=c['utf8'].encode() if c['utf8'] is not None else base64.b64decode(c['base64'],validate=True)
 assert m.pin(b)==m.pure(c)
 return b
def callcheck(c):
 assert c['status']==0 and c['error'] is None and c['signal'] is None and c['complete'] is True
 assert c['environment']==policy['tool_environment'] and 0<=c['elapsed_ms']<15000
 assert len(capture(c['stdout']))+len(capture(c['stderr']))<=2097152
def version(v):
 a=[v>>16,(v>>8)&255,v&255]
 return '.'.join(map(str,a if a[2] else a[:2]))
def binary_slices(b):
 magic,n=struct.unpack_from('>II',b);assert magic==0xcafebabe and n==2
 result=[];ends=[]
 for i in range(n):
  cpu,sub,start,size,align=struct.unpack_from('>IIIII',b,8+20*i)
  assert start>=8+20*n and start+size<=len(b) and start%(1<<align)==0
  ends.append((start,start+size));v=memoryview(b)[start:start+size]
  magic,cpu2,sub2,typ,ncmds,sz,flags,res=struct.unpack_from('<8I',v)
  assert magic==0xfeedfacf and (cpu,sub)==(cpu2,sub2) and res==0 and 32+sz<=size
  arch={16777223:'x86_64',16777228:'arm64'}[cpu]
  hdr=dict(magic=hex(magic),cpu_type=cpu,cpu_subtype=sub&0xffffff,caps=f'0x{sub>>24:02x}',filetype=typ,ncmds=ncmds,sizeofcmds=sz,flags=f'0x{flags:08x}')
  pos=32;commands=[]
  for j in range(ncmds):
   cmd,length=struct.unpack_from('<II',v,pos);kind=codes[cmd]
   assert length>=8 and length%8==0 and pos+length<=32+sz
   row=dict(index=j,kind=kind,bytes=length)
   if kind in named:
    no=struct.unpack_from('<I',v,pos+8)[0];assert 12<=no<length
    raw=bytes(v[pos+no:pos+length]);assert b'\0' in raw
    row.update(name=raw.split(b'\0',1)[0].decode('utf-8'),name_offset=no)
   if kind=='LC_BUILD_VERSION':
    platform,minimum,sdkv,ntools=struct.unpack_from('<4I',v,pos+8)
    assert length==24+ntools*8
    row.update(minimum_os=version(minimum),sdk=version(sdkv))
   commands.append(row);pos+=length
  assert pos==32+sz
  result.append(dict(architecture=arch,header=hdr,commands=commands,listing=[r['name'] for r in commands if r['kind'] in dylib],unknown_commands=[]))
 assert ends[0][1]<=ends[1][0]
 assert [r['architecture'] for r in result]==['x86_64','arm64']
 return result
initial=t['initial']['outcome']
assert json.loads(t['initial']['receipt']['output'])==initial and t['initial']['receipt']['exit_code']==0
for c in initial['calls']:callcheck(c)
rawobjects=[]
for batch in t['batches']:
 assert batch['receipt']['exit_code']==0 and batch['outcome']['errors']==[] and batch['outcome']['target_invocations']==0
 rawobjects.extend(batch['outcome']['objects'])
assert [r['path'] for r in rawobjects]==[r['path'] for r in o]==policy['selected_roots']==g['selection']['roots']['roots']
assert len(o)==76
native=[];edges=[];kinds={};commands_total=0;captures=0
otool='/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/llvm-otool'
for obj,raw in zip(o,rawobjects):
 p=Path(obj['path']);ident=m.verify(p,obj['identity'])
 assert ident['symlink_chain']==[] and ident['resolved_path']==str(p)
 assert ident['state']==state(obj['state_before'])==state(obj['state_after'])==state(raw['state_before'])==state(raw['state_after'])
 assert raw['identity']==obj['identity'] and raw['stable_bytes_and_state'] is True and obj['stable_bytes_and_state'] is True
 b=p.read_bytes();assert m.pin(b)==m.pure(ident);assert m.identity(p)==ident
 slices=binary_slices(b);assert slices==obj['slices'];native.append(ident)
 expected=[['/usr/bin/file',str(p)],[otool,'-arch','all','-h','-L','-l',str(p)],['/usr/bin/codesign','--display','--verbose=4',str(p)],['/usr/bin/codesign','--verify','--strict','--verbose=2',str(p)]]
 assert [c['argv'] for c in raw['tool_calls']]==expected
 for c in raw['tool_calls']:callcheck(c);captures+=2
 text=capture(raw['tool_calls'][1]['stdout']).decode();assert capture(raw['tool_calls'][1]['stderr'])==b''
 for i,s in enumerate(slices):
  delimiter=str(p)+' (architecture '+s['architecture']+'):\n'
  assert text.count(delimiter)==1
  piece=text.split(delimiter)[1].split(str(p)+' (architecture ')[0]
  matches=list(re.finditer(r'^Load command (\d+)\n\s*cmd (\w+)\n\s*cmdsize (\d+)\n',piece,re.M))
  assert len(matches)==s['header']['ncmds']
  assert [x.group(1,2,3) for x in matches]==[(str(r['index']),r['kind'],str(r['bytes'])) for r in s['commands']]
  listing=re.findall(r'^\t(.+) \(compatibility version [^\n]+\)$',piece,re.M);assert listing==s['listing']
  for j,(match,r) in enumerate(zip(matches,s['commands'])):
   block=piece[match.end():matches[j+1].start() if j+1<len(matches) else len(piece)]
   if r['kind'] in named:
    mm=re.search(r'^\s*(?:name|path) (.+) \(offset (\d+)\)$',block,re.M)
    assert mm and (mm[1],int(mm[2]))==(r['name'],r['name_offset'])
   kinds[r['kind']]=kinds.get(r['kind'],0)+1;commands_total+=1
   if r['kind'] in edgekinds:edges.append((str(p),s['architecture'],r['index'],r['kind'],r['name']))
assert edges==[(r['origin'],r['architecture'],r['load_command_index'],r['kind'],r['install_name']) for r in g['edges']]
assert len(edges)==200 and sum(r['bytes'] for r in native)==22985616
non=[r for r in g['edges'] if not r['install_name'].startswith('/')]
assert len(non)==2
for r in non:
 assert r['origin']==o[0]['path'] and r['install_name']=='@executable_path/../Python3'
 assert len(r['candidates'])==1
 c=r['candidates'][0];assert c['path']==os.path.normpath(str(Path(r['origin']).parent/'../Python3'))==o[1]['path']
 assert c['identity']==o[1]['identity'] and c['slice_present'] is True and c['status']=='RESOLVED_SELECTED_NON_SYSTEM'
systemnames=sorted({r[4] for r in edges if r[4].startswith('/')});assert len(systemnames)==17
assert systemnames==sorted(r['path'] for r in g['system_boundary']['rows'])
system=[]
for r in g['system_boundary']['rows']:
 p=Path(r['path']);cur=Path('/');missing=None
 for part in p.parts[1:]:
  cur/=part
  try:st=cur.lstat()
  except FileNotFoundError:missing=str(cur);break
  assert not cur.is_symlink()
 assert (missing is None)==(r['status']=='REGULAR_AT_EXPLICIT_PATH')
 if missing is None:assert p.is_file()
 system.append(dict(path=str(p),first_missing=missing))
tools={r['path']:r for r in initial['tool_pins']}
tools[otool]=t['tool_resolution']['resolved_target']['identity'] if 'identity' in t['tool_resolution']['resolved_target'] else t['tool_resolution']['resolved_target']
toolstates=[]
for p,r in tools.items():
 q=m.verify(p,r)
 if 'state' in r:assert q['state']==state(r['state'])
 toolstates.append(q)
totalms=max(initial['aggregate_tool_ms'],sum(c['elapsed_ms'] for c in initial['calls']))+sum(c['elapsed_ms'] for r in rawobjects for c in r['tool_calls'])
assert totalms<300000
assert all(k not in kinds for k in ('LC_LOAD_WEAK_DYLIB','LC_LAZY_LOAD_DYLIB','LC_REEXPORT_DYLIB','LC_LOAD_UPWARD_DYLIB','LC_RPATH','LC_DYLD_ENVIRONMENT'))
summary=dict(schema='ri164-root-independent-binary-review-v1',status='PASS_FINITE_STATIC_CLOSURE_ONLY',seal=m.ref(S/'HANDOFF.json'),native_objects=len(native),native_bytes=sum(r['bytes'] for r in native),slices=152,load_commands=commands_total,edges=len(edges),non_system_edges=2,system_edges=198,system_names=systemnames,capture_streams_checked=captures+6,tool_calls=307,conservative_tool_ms=totalms,historical_paths=len(deps),historical_bytes=sum(r['bytes'] for r in deps),historical_reference_expansion_replayed=False,tool_executables=len(toolstates),commands_by_kind=kinds,primary_layout_headers=header_refs,scientific_decoding=False,target_execution=False,system_trust_proved=False,runtime_closure_proved=False)
print(m.save('INDEPENDENT_STATIC_CHECK.json',dict(summary=summary,packet=packet,historical=deps,native=native,tools=toolstates,system_path_observations=system)))
print(m.save('STATIC_CHECK_SUMMARY.json',summary))
