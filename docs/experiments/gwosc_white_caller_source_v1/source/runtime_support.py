"""RI121 explicit stdlib closure support; source only until root admission.

Expands the historical package-only byte inventory to whole stdlib/site trees.
Does not discover-and-accept a runtime inside the active child: every entry is
compared to a separately root-admitted existing-file inventory and profile.
"""
import os
from pathlib import Path
import stat
import sys

STDLIB = '/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/lib/python3.11'
VENV_SITE = '/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/lib/python3.11/site-packages'
SYSTEM_SITE = '/opt/homebrew/lib/python3.11/site-packages'
ROOTS = [STDLIB, VENV_SITE, SYSTEM_SITE]
REQUIRED_FILES = [
 '/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/pyvenv.cfg',
 '/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/Python',
 '/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/bin/python3.11',
 '/bin/ps',
 '/opt/homebrew/etc/openssl@3/openssl.cnf',
 '/opt/homebrew/Cellar/openssl@3/3.6.0/lib/libcrypto.3.dylib',
]
ABSENT_ZIP = '/opt/homebrew/Cellar/python@3.11/3.11.6_1/Frameworks/Python.framework/Versions/3.11/lib/python311.zip'
ABSENT_PATHS = [
 ABSENT_ZIP,
 '/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/pyvenv.cfg',
 '/opt/homebrew/opt/python-tk@3.11',
 '/opt/homebrew/opt/python-gdbm@3.11',
 '/opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib',
 '/opt/homebrew/lib/libmpdec.3.dylib',
 '/usr/local/lib/libmpdec.3.dylib',
 '/usr/lib/libmpdec.3.dylib',
]
REQUIRED_LOADER_BINDINGS = [{
 'named_path':'/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib',
 'resolved_path':'/opt/homebrew/Cellar/openssl@3/3.6.0/lib/libcrypto.3.dylib',
 'symlink_chain':[{'path':'/opt/homebrew/opt/openssl@3','target':'../Cellar/openssl@3/3.6.0'}],
 'target':{'bytes':4874704,'sha256':'e7731484e003229df06b3945b198a557110ba5bbbf7d735a79130540c6fb2480'},
}]
ALLOWED_LINKS = [
 {'path': STDLIB + '/config-3.11-darwin/libpython3.11.a', 'target': '../../../Python'},
 {'path': STDLIB + '/config-3.11-darwin/libpython3.11.dylib', 'target': '../../../Python'},
 {'path': STDLIB + '/site-packages', 'target': '../../../../../../../../../lib/python3.11/site-packages'},
]


def scan(inventory, control):
    control.require(type(inventory) is dict and set(inventory) ==
                    {'schema','roots','extra_files','files','symlinks','absent_paths','loader_bindings','scope'}, 'runtime inventory keys')
    control.require(inventory['schema'] == 'ri121-complete-stdlib-runtime-inventory-v2' and
                    inventory['roots'] == ROOTS and inventory['symlinks'] == ALLOWED_LINKS and
                    inventory['absent_paths'] == ABSENT_PATHS, 'complete declared stdlib domain differs')
    extras = inventory['extra_files']
    control.require(type(extras) is list and extras == sorted(set(extras)) and
                    set(REQUIRED_FILES) <= set(extras), 'interpreter/framework/monitor/config runtime files omitted')
    bindings = inventory['loader_bindings']
    control.require(type(bindings) is list and all(type(row) is dict and set(row) ==
                    {'named_path','resolved_path','symlink_chain','target'} for row in bindings), 'loader binding inventory differs')
    names = [row['named_path'] for row in bindings]
    control.require(names == sorted(set(names)) and all(row in bindings for row in REQUIRED_LOADER_BINDINGS),
                    'mandatory loader binding omitted or changed')
    for row in bindings:
        control.require(control.binding(row['named_path']) == row, 'non-OS loader binding changed')
        control.require(row['resolved_path'] in extras, 'resolved non-OS loader bytes omitted')
    paths = set(extras)
    links = []
    def walk_error(error):
        raise error
    for directory in ROOTS:
        root = Path(directory)
        control.require(root.is_dir() and root == root.resolve(), 'runtime root changed')
        for parent, directories, names in os.walk(root, onerror=walk_error):
            for name in list(directories):
                path = Path(parent)/name
                if path.is_symlink():
                    links.append({'path':str(path),'target':os.readlink(path)})
                    directories.remove(name)
            for name in names:
                path=Path(parent)/name
                if path.is_symlink():
                    links.append({'path':str(path),'target':os.readlink(path)})
                    # The permitted framework aliases must resolve to an
                    # independently inventoried regular file, never an omission.
                    paths.add(str(path.resolve(strict=True)))
                else:
                    control.require(stat.S_ISREG(path.lstat().st_mode), 'nonregular runtime member')
                    paths.add(str(path))
    links.sort(key=lambda row:row['path'])
    control.require(links == ALLOWED_LINKS, 'runtime symlink membership changed')
    for path in inventory['absent_paths']:
        control.require(not Path(path).exists() and not Path(path).is_symlink(), 'previously absent startup/import/loader path appeared')
    return [{'path':name, **control.file_pin(name)} for name in sorted(paths)]


def verify(manifest, control):
    row=manifest['runtime_inventory']
    body=control.verified_body(row['path'],row['pin'])
    inventory=control.parse_json(body)
    control.require(body == control.canonical(inventory), 'noncanonical runtime inventory')
    actual_binding=control.binding(manifest['interpreter']['named_path'])
    control.require(actual_binding == manifest['interpreter'], 'interpreter chain changed')
    actual=scan(inventory,control)
    control.require(actual == inventory['files'], 'whole stdlib/interpreter support bytes changed')
    return {'interpreter':actual_binding,'runtime_files_count':len(actual),
            'runtime_files_identity':control.identity(control.canonical(actual)),
            'inventory_pin':row['pin']}


def profile(manifest, mode, control):
    actual={'version':sys.version,'implementation':sys.implementation.name,
            'version_info':list(sys.version_info),'executable':sys.executable,
            'prefix':sys.prefix,'base_prefix':sys.base_prefix,'exec_prefix':sys.exec_prefix,
            'base_exec_prefix':sys.base_exec_prefix,'path':list(sys.path),'byteorder':sys.byteorder,
            'isolated':sys.flags.isolated,'dont_write_bytecode':sys.flags.dont_write_bytecode,
            'optimize':sys.flags.optimize}
    expected=dict(manifest['expected_runtime'])
    expected['optimize']=0 if mode=='normal' else 1
    control.require(actual == expected and actual['isolated']==1 and actual['dont_write_bytecode']==1,
                    'fresh runtime/profile not equal to root-admitted profile')
    return actual


def loaded_files(manifest, control):
    """Check loaded file origins against frozen runtime or captured source paths."""
    row=manifest['runtime_inventory']
    inventory=control.parse_json(control.verified_body(row['path'],row['pin']))
    allowed={item['path']:{k:item[k] for k in ('bytes','sha256')} for item in inventory['files']}
    allowed.update({item['path']:item['pin'] for item in manifest['helpers']})
    allowed.update({item['copy']:item['pin'] for item in manifest['sources']})
    observed={}
    for name,module in sorted(sys.modules.items()):
        if module is None: continue
        path=getattr(module,'__file__',None)
        spec=getattr(module,'__spec__',None)
        origin=getattr(spec,'origin',None)
        if path is None:
            control.require(origin in (None,'built-in','frozen') or name=='__main__', 'untracked nonfile module origin')
            continue
        path=str(Path(path).resolve(strict=True))
        control.require(path in allowed, 'loaded module outside admitted stdlib/source closure: '+name)
        pin=control.file_pin(path)
        control.require(pin==allowed[path], 'loaded module bytes drift: '+name)
        observed[name]={'path':path,**pin}
    return observed
