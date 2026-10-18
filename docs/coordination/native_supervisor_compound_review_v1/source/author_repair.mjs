// Administrative literal source editing only; never imports/parses/runs Python.
import fs from 'node:fs';
const D='/Volumes/AI_DATA/development/det-review-evidence/ri176-supervisor-qualification-repair-3ausb2jo';
function edit(name, fn){let t=fs.readFileSync(D+'/'+name,'utf8');const replace=(a,b)=>{if(t.split(a).length!==2)throw Error(name+' nonunique/missing literal '+a.slice(0,80));t=t.replace(a,b)};fn(replace,()=>t);fs.writeFileSync(D+'/'+name,t);}
edit('protocol.py',r=>r("SOURCE_DIRECTORY = BASE + '/ri171-supervisor-qualification-source-zksymhs1'","SOURCE_DIRECTORY = BASE + '/ri176-supervisor-qualification-repair-3ausb2jo'"));
edit('case_worker.py',r=>{
r("        self.target_stream = case.get('stream') or ('stderr' if '.stderr.' in self.fault else 'stdout')", "        self.target_stream = case.get('stream') or ('stderr' if '.stderr.' in self.fault else 'stdout')\n        self.target_input_tag = ('ps' if case['kind'] == 'observer' else 'caller') + ':' + self.target_stream");
r("selected = tag is not None and tag.endswith(':'+self.target_stream)","selected = tag == self.target_input_tag");
r("self.tag.endswith(':'+self.i.target_stream)","self.tag == self.i.target_input_tag");
// Two distinct literal selector sites, each replaced once.
r("pipe.tag.endswith(':'+self.i.target_stream) and self.i.once_at('register_fault')", "pipe.tag == self.i.target_input_tag and self.i.once_at('register_fault')");
r("pipe.tag.endswith(':'+self.i.target_stream) and self.i.once_at('unregister_fault')", "pipe.tag == self.i.target_input_tag and self.i.once_at('unregister_fault')");
r("            if self.fault == 'late_replacement':", "            before_raw, before_pin, _ = self.P.capture(path, 67108864)\n            if self.fault == 'late_replacement':");
r("            self.event('file_mutation', tag=tag, fault=self.fault)\n        return os.fsync(fd)", "            after_raw, after_pin, _ = self.P.capture(path, 67108864)\n            self.event('file_mutation', tag=tag, fault=self.fault, before=before_pin, after=after_pin,\n                       before_first_byte=before_raw[0] if before_raw else None)\n        result = os.fsync(fd)\n        if tag:\n            self.event('fsync_complete', tag=tag)\n        return result");
r("        result = os.close(fd)\n        if tag ==", "        result = os.close(fd)\n        if tag:\n            self.event('close_complete', tag=tag)\n        if tag ==");
r("        self.event('fixture_directory_sync', path=self.D)\n        if n ==", "        self.event('fixture_directory_sync', path=self.D)\n        self.event('sync_base_complete', ordinal=n)\n        if n ==");
r("        self.handles.append((kind, p))\n        self.event('popen_acquired', kind=kind, pid=p.pid)", "        handle_id = len(self.handles) + 1\n        self.handles.append((handle_id, kind, p))\n        self.event('popen_acquired', handle_id=handle_id, kind=kind, pid=p.pid)");
r("        for kind, p in self.handles:", "        for handle_id, kind, p in self.handles:");
r("result.append({'kind': kind, 'pid': p.pid, 'returncode': p.returncode,", "result.append({'handle_id': handle_id, 'kind': kind, 'pid': p.pid, 'returncode': p.returncode,");
r("result.append({'kind': kind, 'pid': p.pid, 'error': type(exc).__name__+': '+str(exc)})", "result.append({'handle_id': handle_id, 'kind': kind, 'pid': p.pid, 'error': type(exc).__name__+': '+str(exc)})");
r("                os.killpg(now['pgid'], signal.SIGKILL)\n                result.append", "                os.killpg(now['pgid'], signal.SIGKILL)\n                self.event('leaf_recovery_signal', identity=now, signal=int(signal.SIGKILL))\n                result.append");
});
edit('inert_payload.py',r=>{
r("CAP = 8 * 1024 * 1024", "CAP = 8 * 1024 * 1024\nLATE_FILES = ('late_fsync', 'late_close', 'late_replacement', 'late_descriptor', 'late_drift', 'late_size')");
r("        if both or fault == 'stderr':", "        if both or fault == 'stderr' or fault in LATE_FILES:");
r("return 7 if fault == 'nonzero' or fault.startswith('late_') else 0", "return 7 if fault == 'nonzero' or fault in LATE_FILES else 0");
});
