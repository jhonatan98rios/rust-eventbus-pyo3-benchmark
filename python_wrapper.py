from typing import Callable
from event_bus_rs import EventBus as RustEventBus

class EventBus:
    def __init__(self):
        self._event_bus = RustEventBus()

    def subscribe(self, event: str, callback: Callable[..., None]) -> None:
        self._event_bus.subscribe(event, callback)

    def publish(self, event: str, data: dict) -> None:
        self._event_bus.publish(event, data)

# Example usage
if __name__ == "__main__":
    def callback(data):
        print(f"Callback called with arguments: {data}")

    bus = EventBus()
    bus.subscribe("test_event", callback)
    bus.publish("test_event", {"msg": "Hello, World!"})