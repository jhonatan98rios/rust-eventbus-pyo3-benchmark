from typing import Callable, List
from event_bus_rs import EventBus as RustEventBus

class EventBus:
    def __init__(self):
        self._event_bus = RustEventBus()

    def subscribe(self, event: str, callback: Callable[..., None]) -> None:
        self._event_bus.subscribe(event, callback)

    def publish(self, event: str, args: List) -> None:
        self._event_bus.publish(event, args)

# Example usage
if __name__ == "__main__":
    def callback(arg1, arg2):
        print(f"Callback called with arguments: {arg1}, {arg2}")

    bus = EventBus()
    bus.subscribe("test_event", callback)
    bus.publish("test_event", ["Hello", "World"])