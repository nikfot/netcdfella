"""
The event_processor module instantiates an event processor and configurates it.
"""
import asyncio

from pyinotify import ProcessEvent

from qnotify.queues import q as queue


class EventHandler(ProcessEvent):
    """EventHandler is a subclass of the pyinotify.ProcessEvent class."""

    _methods = [
        "IN_CREATE",
    ]

    def my_init(self, loop=None, extension=".nc", **kargs):
        self.loop = loop if loop else asyncio.get_event_loop()
        self.extension = extension

    @classmethod
    def process_generator(cls, method):
        "process_generator generate process info for events."
        # pylint: disable=unused-argument
        def _method_name(self, event):
            print(f" ===> Event: {event.maskname} | Path: {event.pathname}")
            if event.pathname.endswith(self.extension):
                queue.put(event.pathname)

        _method_name.__name__ = f"process_{method}"
        setattr(cls, _method_name.__name__, _method_name)

    @classmethod
    def create(cls):
        "create instantiates the processes for an event handler."
        for method in cls._methods:
            cls.process_generator(method)
