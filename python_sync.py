from collections import defaultdict
from typing import Callable, Any

class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

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
        """Trigger an event and notify all subscribers."""
        for callback in self._subscribers.get(event_name, []):
            callback(*args, **kwargs)

# Example usage:
bus = EventBus()

def on_custom_event(data):
    print(f"Received event with data: {data}")

bus.subscribe("custom_event", on_custom_event)
bus.emit("custom_event", {"key": "value"})  # Output: Received event with data: {'key': 'value'}
