"""Same-run isolated C compilation. No cached files or serialized match credit.

Each child runs the existing source capability guard. The parent owns private
pipes and live processes, verifies exact task/result identities and consumes each
result once. All children must close before the existing SOURCE seal is minted.
"""
import json,multiprocessing,os,time,uuid
from multiprocessing.connection import wait
from pathlib import Path
from cohort import need,sha


def eligible(row):
    # COMMON providers, Actor70, and packet literals require parent-local scopes.
    # Preserve their real compiler invocation; do not replace it with a receipt.
    return row['kind']=='c-whole-omf' and row['source'] not in ('src/data/actors_05e0.c','src/packet_literal_context_match.c')


def _worker(connection, project, descriptor_hash):
    import sys,traceback
    project=Path(project)
    sys.path[:0]=[str(project),str(project/'build_pipeline/engine_v1')]
    try:
        import build_game,check,source_inputs
        from source_phase import SourceObserver
        _,descriptor=build_game.validate_inputs(project)
        need(sha(json.dumps(descriptor,sort_keys=True).encode())==descriptor_hash,'child descriptor identity')
        connection.send({'kind':'ready','pid':os.getpid()})
        while True:
            task=connection.recv()
            if task is None:break
            slot=task['slot'];row=descriptor['rows'][slot]
            need(eligible(row),'parallel ordinary C only')
            started=time.time();connection.send({'kind':'started','slot':slot,'nonce':task['nonce'],'at':started,'pid':os.getpid()})
            observer=SourceObserver(project,descriptor)
            with observer.install(check,source_inputs):
                kw={'compiler':row['compiler'],'source_name':row['source_name']}
                if row.get('dosbox_keyword')is not None:kw['dosbox']=row['dosbox_keyword']
                result=check.compile_c(project/row['source'],row['compiler_flags'],**kw)
            need(not observer.poisoned and observer.current is None and not observer.roots and len(observer.events)==1,'closed child source guard')
            connection.send({'kind':'result','slot':slot,'nonce':task['nonce'],'pid':os.getpid(),
                             'result':result,'event':observer.events[0],'started':started,'ended':time.time()})
        connection.close()
    except BaseException as exc:
        try:connection.send({'kind':'error','pid':os.getpid(),'error':str(exc),'traceback':traceback.format_exc()})
        except Exception:pass
        raise


class ParallelCompiler:
    def __init__(self,observer,workers,slots=None):
        need(type(workers)is int and 1<=workers<=8,'bounded compile workers')
        self.observer=observer;self.project=observer.project;self.descriptor=observer.descriptor
        self.run_id=uuid.uuid4().hex;self.closed=False;self.poisoned=False;self.ready={};self.consumed=set();self.clients=[]
        rows=[r for r in self.descriptor['rows']if eligible(r)]
        if slots is not None:rows=[r for r in rows if r['order_slot']in slots]
        self.rows={r['order_slot']:r for r in rows}
        self.queue=sorted(self.rows)
        self.progress_fd=None
        progress=os.environ.get('REWORKBENCH_SUBJOB_EVENTS')
        if progress:self.progress_fd=os.open(progress,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
        for slot in self.queue:self.emit(slot,'queued')
        context=multiprocessing.get_context('spawn')
        descriptor_hash=sha(json.dumps(self.descriptor,sort_keys=True).encode())
        try:
            for _ in range(min(workers,len(rows))):
                parent,child=context.Pipe();process=context.Process(target=_worker,args=(child,str(self.project),descriptor_hash))
                process.start();child.close();self.clients.append({'pipe':parent,'process':process,'task':None})
            for client in self.clients:
                need(client['pipe'].poll(60),'child ready timeout')
                response=client['pipe'].recv();need(response=={'kind':'ready','pid':client['process'].pid},'child failed initialization: '+str(response))
        except BaseException:self.close(False);raise

    def emit(self,slot,status,**extra):
        if self.progress_fd is not None:
            row=self.rows[slot]
            record={'id':'compile-'+str(slot),'label':row['source'],'kind':'compile','status':status,
                    'at':time.time(),'run_id':self.run_id,**extra}
            os.write(self.progress_fd,(json.dumps(record)+'\n').encode())

    def dispatch(self,client):
        if not self.queue:return
        slot=self.queue.pop(0);task={'slot':slot,'nonce':uuid.uuid4().hex}
        client['task']=task;client['pipe'].send(task)

    def receive(self,client,message,refill=True):
        task=client['task'];need(task is not None,'unsolicited worker result')
        need(message.get('pid')==client['process'].pid,'live child PID identity')
        if message.get('kind')=='error':raise ValueError('parallel compiler failed: '+message.get('error','unknown'))
        need(message.get('slot')==task['slot']and message.get('nonce')==task['nonce'],'wrong/replayed source task identity')
        slot=task['slot'];row=self.rows[slot]
        if message['kind']=='started':
            need(not task.get('started'),'duplicate child start');task['started']=True
            self.emit(slot,'running',pid=message['pid'],started_at=message['at']);return
        need(message['kind']=='result'and task.get('started')and slot not in self.ready and slot not in self.consumed,'one result per issued source task')
        from msc import CompileResult
        result=message['result'];event=message['event']
        need(type(result)is CompileResult,'real compiler result type')
        need(result.source_sha256==row['source_sha256']and list(result.flags)==row['compiler_flags']and result.compiler==row['compiler']and result.source_name==row['source_name'],'complete source/compiler identity')
        from msc import validate_toolchain
        manifest_hash,tool_hashes=validate_toolchain(compiler=row['compiler'])
        need(result.toolchain_manifest_sha256==manifest_hash and result.tool_hashes==tool_hashes,'parent independently pinned compiler distribution')
        raw_hash=sha(result.object_bytes)
        need(raw_hash==row['comparison_expected_raw_sha256']==event['raw_sha256']and raw_hash in event['raw_reads'],'whole fresh raw object identity')
        need(event['slot']==slot and event['fresh_witness']is True and not event['denials']and event['roots']and event['processes'],'complete guarded generation witness')
        need(all(p['host_returncode']==0 for p in event['processes']),'actual compiler processes closed successfully')
        need(any(Path(p).name==row['source_name']and v['sha256']==row['source_sha256']for p,v in event['submitted'].items()),'actual submitted source identity')
        event=dict(event,parallel_run_id=self.run_id,worker_pid=message['pid'],task_nonce=task['nonce'])
        self.ready[slot]=(result,event);client['task']=None
        self.emit(slot,'finished',pid=message['pid'],started_at=message['started'],finished_at=message['ended'],seconds=message['ended']-message['started'])
        if refill:self.dispatch(client)

    def quiesce(self):
        # Finish in-flight compilers before a parent-local guarded generator.
        deadline=time.monotonic()+600
        while any(c["task"]is not None for c in self.clients):
            need(time.monotonic()<deadline,"parallel drain timeout")
            pending=[c for c in self.clients if c["task"]is not None]
            available=wait([c["pipe"]for c in pending],timeout=1)
            for client in pending:
                if client["pipe"]in available:self.receive(client,client["pipe"].recv(),False)
                elif not client["process"].is_alive():raise ValueError("parallel compiler exited during drain")

    def consume(self,row):
        slot=row['order_slot'];need(not self.closed and not self.poisoned and self.rows.get(slot)==row and slot not in self.consumed,'same-run source result consumed once')
        deadline=time.monotonic()+600
        try:
            for client in self.clients:
                if client["task"]is None:self.dispatch(client)
            while slot not in self.ready:
                pending=[c for c in self.clients if c['task']is not None]
                need(pending and time.monotonic()<deadline,'parallel source timeout/no pending task')
                available=wait([c['pipe']for c in pending],timeout=1)
                for client in pending:
                    if client['pipe']in available:self.receive(client,client['pipe'].recv())
                    elif not client['process'].is_alive():raise ValueError('parallel compiler exited without a result')
            value=self.ready.pop(slot);self.consumed.add(slot);return value
        except BaseException:self.poisoned=True;raise

    def close(self,success=True):
        if self.closed:
            need(not success or not self.poisoned,'poisoned compiler pool');return
        if success:
            need(not self.poisoned and not self.queue and not self.ready and self.consumed==set(self.rows)and all(c['task']is None for c in self.clients),'all fresh compile tasks consumed before SOURCE seal')
        self.poisoned=not success
        try:
            for client in self.clients:
                if success:client['pipe'].send(None)
                else:
                    if client['task']:self.emit(client['task']['slot'],'cancelled')
                    client['process'].terminate()
            for client in self.clients:
                client['process'].join(10)
                if client['process'].is_alive():client['process'].kill();client['process'].join();self.poisoned=True
                client['pipe'].close()
                if success:need(client['process'].exitcode==0,'compiler worker did not close cleanly')
        except BaseException:
            self.poisoned=True
            for client in self.clients:
                if client['process'].is_alive():client['process'].terminate();client['process'].join(2)
                if client['process'].is_alive():client['process'].kill();client['process'].join()
            raise
        finally:
            self.closed=True
            if self.progress_fd is not None:os.close(self.progress_fd);self.progress_fd=None
