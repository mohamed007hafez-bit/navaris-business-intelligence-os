"""Health monitoring with bounded retries; upgrades are never downloaded automatically."""
import time
from core.master import health
def retry_operation(operation, attempts=10, delay_seconds=0.1):
    if not 1 <= attempts <= 10: raise ValueError("attempts must be between 1 and 10")
    last=None
    for i in range(attempts):
        try: return operation()
        except Exception as exc:
            last=exc
            if i+1<attempts: time.sleep(max(0,delay_seconds))
    raise RuntimeError(f"Operation failed after {attempts} attempts") from last
def health_check(): return retry_operation(health,10,0.1)
def run_health_loop(interval_seconds=60,max_cycles=None):
    n=0
    while max_cycles is None or n<max_cycles:
        try: print(health_check())
        except Exception as exc: print({"status":"degraded","error":str(exc)})
        n+=1
        if max_cycles is None or n<max_cycles: time.sleep(max(5,interval_seconds))
if __name__=="__main__": run_health_loop()
