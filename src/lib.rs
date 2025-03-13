use pyo3::prelude::*;
use pyo3::types::PyTuple;
use tokio::sync::{mpsc, RwLock};
use tokio::runtime::Runtime;
use std::collections::HashMap;
use std::sync::Arc;

/// Struct for event bus
/// This struct represents an event bus that allows subscribing to events
/// with callbacks and publishing events with arguments.
#[pyclass]
struct EventBus {
    /// A map of event names to lists of callback functions
    subscribers: Arc<RwLock<HashMap<String, Vec<PyObject>>>>,
    /// A sender for publishing events
    sender: mpsc::Sender<(String, Vec<PyObject>)>,
    /// A Tokio runtime for managing asynchronous tasks
    runtime: Arc<Runtime>,
}

#[pymethods]
impl EventBus {
    /// Creates a new EventBus instance
    /// This function initializes the event bus, sets up the Tokio runtime,
    /// and spawns an asynchronous task to process events.
    #[new]
    fn new(_py: Python) -> PyResult<Self> {
        
        let subscribers = Arc::new(RwLock::new(HashMap::new()));
        let (sender, mut receiver) = mpsc::channel(1024);

        // Clone subscribers for async task
        let subs_clone = subscribers.clone();

        // Create a new Tokio runtime
        let runtime = Runtime::new().expect("Failed to create Tokio runtime");
        let runtime_handle = runtime.handle().clone();

        // Spawn the async event processing task
        runtime_handle.spawn(async move {
            // Process events as they arrive
            while let Some((event, args)) = receiver.recv().await {
                // Get the subscribers for the event
                let subs = subs_clone.read().await;
                // Call each callback with the arguments
                if let Some(callbacks) = subs.get(&event) {
                    let callbacks: &Vec<PyObject> = callbacks;
                    Python::with_gil(|py| {
                        for callback in callbacks {
                            let callback: &PyAny = callback.as_ref(py);
                            let _ = callback.call1(PyTuple::new(py, &args));
                        }
                    });
                }
            }
        });

        Ok(Self { subscribers, sender, runtime: Arc::new(runtime) })
    }

    /// Subscribe to an event with a callback
    /// This function allows you to subscribe to a specific event by providing
    /// an event name and a callback function. The callback will be called
    /// whenever the event is published.
    ///
    /// # Arguments
    /// * `event` - The name of the event to subscribe to
    /// * `callback` - The callback function to be called when the event is published
    fn subscribe(&self, event: String, callback: PyObject) -> PyResult<()> {
        // Clone the subscribers map to use it in the async task
        let subs = self.subscribers.clone();
        // Clone the runtime handle to use it in the async task
        let runtime_handle = self.runtime.handle().clone();
        // Spawn an async task to add the callback to the subscribers map
        runtime_handle.spawn(async move {
            let mut subs = subs.write().await;
            subs.entry(event).or_insert_with(Vec::new).push(callback);
        });
        Ok(())
    }

    /// Publish an event with arguments3
    /// This function allows you to publish an event by providing an event name
    /// and a list of arguments. All subscribed callbacks for the event will be
    /// called with the provided arguments.
    /// 
    /// # Arguments
    ///
    /// * `event` - The name of the event to publish
    /// * `args` - The list of arguments to pass to the callbacks
    fn publish(&self, event: String, args: Vec<PyObject>) -> PyResult<()> {
        // Clone the sender to use it in the async task
        let sender = self.sender.clone();
        // Clone the runtime handle to use it in the async task
        let runtime_handle = self.runtime.handle().clone();
        // Spawn an async task to send the event and arguments to the receiver
        runtime_handle.spawn(async move {
            let _ = sender.send((event, args)).await;
        });
        Ok(())
    }
}

/// Register Rust module in Python
/// This function registers the `EventBus` class in the Python module.
#[pymodule]
fn event_bus_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<EventBus>()?;
    Ok(())
}