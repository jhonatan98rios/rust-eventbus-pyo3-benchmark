import time
import concurrent.futures
from python_multithread import MultiThreadEventBus
from python_sync import EventBus

EVENTS = 5000
SUBSCRIBERS = 300
MAX_WORKERS = 2

def cpu_bound_task(data):
    sum(i * i for i in range(1000))  # Fake CPU work

# Sync Benchmark
def benchmark_sync(event_bus, events=EVENTS, subscribers=SUBSCRIBERS):
    event_name = "test_event"
    
    for _ in range(subscribers):
        event_bus.subscribe(event_name, cpu_bound_task)

    start_time = time.time()
    
    for _ in range(events):
        event_bus.emit(event_name, {"test": "data"})

    elapsed = time.time() - start_time
    print(f"Sync EventBus: {events} events in {elapsed:.4f} sec ({events/elapsed:.2f} events/sec)")

# ThreadPool Benchmark
def benchmark_threadpool(event_bus, events=EVENTS, subscribers=SUBSCRIBERS):
    event_name = "test_event"
    event_bus._executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)  # Adjust worker count
    
    for _ in range(subscribers):
        event_bus.subscribe(event_name, cpu_bound_task)

    start_time = time.time()

    futures = [event_bus._executor.submit(event_bus.emit, event_name, {"test": "data"}) for _ in range(events)]
    concurrent.futures.wait(futures)  # Ensure all complete

    elapsed = time.time() - start_time
    print(f"ThreadPool EventBus: {events} events in {elapsed:.4f} sec ({events/elapsed:.2f} events/sec)")


# Run all benchmarks
if __name__ == "__main__":
    print("\n[1] Testing Sync EventBus")
    sync_bus = EventBus()
    benchmark_sync(sync_bus)

    print(f"\n[2] Testing ThreadPool EventBus with {MAX_WORKERS} worker(s)")
    threadpool_bus = MultiThreadEventBus()
    benchmark_threadpool(threadpool_bus)