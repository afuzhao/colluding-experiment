"""Bounded operational monitor; never starts/restarts study inference."""
import fcntl,json,subprocess,sys,time,urllib.request
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def main():
 lock=(ROOT/'work/runtime_memory_watch.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 active=ROOT/'results/final_16';initial=json.loads((active/'live_status.json').read_text());pid=initial['pid'];last=initial['completed_scenarios'];resets=0;last_reset=time.monotonic()
 while True:
  time.sleep(10)
  s=json.loads((active/'live_status.json').read_text())
  if s['pid']!=pid or s['state']not in ['running_markets','running_assessments']:break
  os_state=subprocess.check_output(['ps','-o','stat=','-p',str(pid)],text=True).strip()
  # Never resume a user-paused/stopped controller.
  if 'T'in os_state:continue
  completed=s['completed_scenarios']
  if completed<=last:continue
  last=completed
  with urllib.request.urlopen('http://127.0.0.1:11434/api/ps',timeout=10)as f:m=json.load(f)
  size=max([x.get('size_vram',0)for x in m['models']]+[0])
  if size<=12_000_000_000 or time.monotonic()-last_reset<600 or resets>=5:continue
  code=subprocess.run([sys.executable,str(ROOT/'tools/runtime_cache_reset.py')],cwd=ROOT).returncode
  print(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'scenario_boundary':completed,'allocation_bytes':size,'reset_exit_code':code}),flush=True)
  if code:break
  resets+=1;last_reset=time.monotonic()
 print('Memory maintenance monitor finished; study not restarted or altered',flush=True)
if __name__=='__main__':main()
