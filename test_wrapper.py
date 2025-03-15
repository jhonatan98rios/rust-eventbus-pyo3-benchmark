import time
import unittest
from python_wrapper import EventBus

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()

    def test_subscribe_and_publish(self):
        self.callback_called = False

        def callback(data):
            self.callback_called = True
            self.assertEqual(data["msg"], "Hello, World!")

        self.bus.subscribe("test_event", callback)
        self.bus.publish("test_event", {"msg": "Hello, World!"})
        
        time.sleep(0.0001)

        self.assertTrue(self.callback_called)

if __name__ == "__main__":
    unittest.main()