import time
import datetime
import threading
from distributed_lock import single, FuncAlreadyRunning

@single(max_processing_time=datetime.timedelta(seconds=8))
def some_func(thread):
    print(f"Thread {thread} started...")
    time.sleep(2)
    print(f"Thread {thread} finished...")
    return f"Thread {thread} completed"

def worker_thread(thread_id, results):
    try:
        result = some_func(thread_id)
        results[thread_id] = f"SUCCESS: {result}"
    except FuncAlreadyRunning:
        results[thread_id] = f"BLOCKED: Function already running"
    except Exception as e:
        results[thread_id] = f"ERROR: {e}"

if __name__ == "__main__":
    results = {}
    threads = []
    
    for i in range(4):
        t = threading.Thread(target=worker_thread, args=(i+1, results))
        threads.append(t)
    
    start_time = time.time()
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    
    print(f"\nРезультаты (время выполнения: {end_time - start_time:.2f}s):")
    for thread_id, result in results.items():
        print(f"Thread {thread_id}: {result}")
