from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from typing import Callable, Any

class MultiThreadEventBus:
    def __init__(self, max_workers: int = 10):
        self._subscribers = defaultdict(list)
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def subscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        """Subscribe a callback to an event."""
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        """Unsubscribe a callback from an event."""
        if event_name in self._subscribers:
            self._subscribers[event_name].remove(callback)
            if not self._subscribers[event_name]:
                del self._subscribers[event_name]

    def emit(self, event_name: str, *args, **kwargs) -> None:
        """Trigger an event asynchronously using threads."""
        for callback in self._subscribers.get(event_name, []):
            self._executor.submit(callback, *args, **kwargs)