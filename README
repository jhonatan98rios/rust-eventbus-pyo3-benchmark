# EventBus Proof of Concept

This project is a proof of concept and benchmark to check the viability of an EventBus library implemented in Rust and exposed to Python using PyO3. The EventBus allows subscribing to events with callbacks and publishing events with arguments.

## Features

- Subscribe to events with callback functions
- Publish events with arguments
- Asynchronous event processing using Tokio

## Requirements

- Rust
- Python 3.6+
- PyO3
- Tokio

## Installation

1. **Install Rust**: Follow the instructions on the [official Rust website](https://www.rust-lang.org/tools/install).

2. **Install Python**: Ensure you have Python 3.6 or higher installed. You can download it from the [official Python website](https://www.python.org/downloads/).

3. **Create a virtual environment**: Run `Python -m venv .venv` to create a environment and then run `source .venv/bin/activate` (Linux and Mac) or `.\.venv\Scripts\activate` (Windows) to activate the environment.

4. **Install Python dependencies**: Run `pip install -r requirements` to install the dependencies.

5. **Install PyO3**: Add the following dependencies to your `Cargo.toml` file:

```toml
[dependencies]
pyo3 = { version = "0.15", features = ["extension-module"] }
tokio = { version = "1", features = ["full"] }
```

6. **Build the Rust project**: Run the following command to build the project:

```sh
maturin develop
```

## Usage

```python
# Example usage
from event_bus_rs import EventBus
# from python_wrapper import EventBus # For Python typings

def callback(arg1, arg2):
    print(f"Callback called with arguments: {arg1}, {arg2}")

bus = EventBus()
bus.subscribe("test_event", callback)
bus.publish("test_event", ["Hello", "World"])
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
PyO3 for providing Rust bindings for Python
Tokio for asynchronous runtime in Rust