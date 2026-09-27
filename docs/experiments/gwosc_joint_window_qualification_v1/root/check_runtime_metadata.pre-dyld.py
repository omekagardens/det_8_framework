"""Root independent metadata checks; never loads a candidate module."""
import sys
import os
import stat
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('metadata', HERE/'metadata.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
C = m.B/'ri121-runtime-candidate-rIMnamYh'
S = m.B/'ri121-synthetic-caller-repair-7ys8vsc3'


def require(value, message):
    if not value:
        raise ValueError(message)


def binding(name):
    row = m.identity(name)
    return {'named_path': str(name), 'resolved_path': row['resolved_path'],
            'symlink_chain': row['symlink_chain'], 'target': m.pure(row)}


def main(label):
    inventory = m.load(C/'RUNTIME_INVENTORY.candidate.json')
    require(m.pin((C/'RUNTIME_INVENTORY.candidate.json').read_bytes()) ==
            {'bytes':2806092,'sha256':'b6f0fd3244cef06c16da19922db212695387926e2f94012d1857c7c8793f7edc'}, 'inventory changed')
    files = {r['path']: r for r in inventory['files']}
    require(len(files) == len(inventory['files']) == 9923, 'membership duplicates/count')
    paths = set(inventory['extra_files'])
    links = []
    def failed(error):
        raise error
    for root in inventory['roots']:
        require(Path(root).resolve(strict=True) == Path(root), 'root resolution')
        for parent, dirs, names in os.walk(root, followlinks=False, onerror=failed):
            for name in list(dirs):
                p = Path(parent)/name
                if p.is_symlink():
                    links.append({'path':str(p), 'target':os.readlink(p)})
                    dirs.remove(name)
            for name in names:
                p = Path(parent)/name
                if p.is_symlink():
                    links.append({'path':str(p),'target':os.readlink(p)})
                    paths.add(str(p.resolve(strict=True)))
                else:
                    require(stat.S_ISREG(p.lstat().st_mode), 'nonregular member')
                    paths.add(str(p))
    require(sorted(paths) == list(files), 'complete membership mismatch')
    require(sorted(links,key=lambda r:r['path']) == inventory['symlinks'], 'links mismatch')
    selection = m.load(C/'FILE_SELECTION_METADATA.candidate.json')
    selection_rows = selection if type(selection) is list else selection['files']
    expected_selection = {r['path']:r for r in selection_rows}
    identities = []
    for name in sorted(paths):
        row = m.verify(name, files[name])
        require(not row['symlink_chain'] and row['resolved_path'] == name, 'regular file resolution changed')
        expected = expected_selection[name]
        s = row['state']
        actual = dict(device=s[0], inode=s[1], mode=s[2], bytes=s[4], mtime_ns=s[5], ctime_ns=s[6])
        require(all(expected[k] == v for k,v in actual.items()), 'selection metadata changed: '+name)
        identities.append(row)
    for path in inventory['absent_paths']:
        try:
            Path(path).lstat()
        except FileNotFoundError:
            continue
        raise ValueError('declared absence appeared: '+path)
    for row in inventory['loader_bindings']:
        require(binding(row['named_path']) == row, 'loader alias changed')
    namespaces = m.load(C/'OPTIONAL_NATIVE_NAMESPACES.candidate.json')
    for namespace in namespaces['directories']:
        root = Path(namespace['root'])
        actual = []
        def visit(parent):
            for p in sorted(parent.iterdir()):
                relative = str(p.relative_to(root))
                info = p.lstat()
                if stat.S_ISLNK(info.st_mode):
                    actual.append({'kind':'symlink','relative_path':relative,'literal_target':os.readlink(p)})
                elif stat.S_ISDIR(info.st_mode):
                    actual.append({'kind':'directory','relative_path':relative})
                    visit(p)
                elif stat.S_ISREG(info.st_mode):
                    actual.append({'kind':'regular','relative_path':relative})
                else:
                    raise ValueError('namespace special file')
        visit(root)
        require(actual == namespace['recursive_members_no_symlink_traversal'], 'optional namespace changed')
    interpreter = m.load(C/'INTERPRETER_BINDING.candidate.json')
    require(binding(interpreter['named_path']) == interpreter, 'interpreter changed')
    manifest = m.load(S/'MANIFEST.source-only-template.json')
    for r in manifest['helpers']:
        m.verify(r['path'], r['pin'])
    for r in manifest['sources']:
        m.verify(r['original'], r['pin']); m.verify(r['copy'], r['pin'])
    history = m.load(S/'HISTORY_CLOSURE.source-only.json')
    for r in history:
        m.verify(r['path'],r)
    value = {'status':'ALL_METADATA_CHECKS_PASS','candidate_inventory':m.ref(C/'RUNTIME_INVENTORY.candidate.json'),
             'selection_metadata':m.ref(C/'FILE_SELECTION_METADATA.candidate.json'),
             'file_count':len(paths),'file_bytes':sum(r['bytes'] for r in identities),
             'full_identities_pin':m.pin(m.canonical(identities)),
             'optional_namespaces':m.ref(C/'OPTIONAL_NATIVE_NAMESPACES.candidate.json'),
             'optional_namespace_check':'separate root metadata check; not an in-process v2 guard',
             'roots':inventory['roots'],'symlinks':links,'absent_paths':inventory['absent_paths'],
             'loader_bindings':inventory['loader_bindings'],'interpreter':interpreter,
             'helpers':manifest['helpers'],'science':manifest['sources'],'history_count':len(history),
             'uname':list(os.uname()),'system_version':m.ref('/System/Library/CoreServices/SystemVersion.plist'),
             'candidate_execution':False,'scientific_execution':False}
    print(m.save(label+'.json',value))


if __name__ == '__main__':
    main(sys.argv[1])
