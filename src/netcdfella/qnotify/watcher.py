"""
Creates a watcher for a directory.
"""
import asyncio

from pyinotify import ALL_EVENTS, AsyncioNotifier, WatchManager

from netcdfella.qnotify.event_processor import EventHandler
from netcdfella.qnotify.queues import Consumer


# A Watcher is a thing that watches a directory.
class Watcher:
    "Watcher is watching for changes in directory."

    def __init__(self, name, directory, target_fn=None):
        self.name = name
        self.directory = directory
        self.new_files = set()
        self.manager = WatchManager()
        self.timeout = None
        self.notifier = None
        self.target_fn = target_fn

    def set_notifier(self):
        "set_notifier instantiates and configures the EventHandler notifier."
        EventHandler.create()
        self.notifier = AsyncioNotifier(
            self.manager,
            loop=asyncio.get_event_loop(),
            default_proc_fun=EventHandler(loop=asyncio.get_event_loop()),
        )

    def start(self):
        """
        Starts a watcher in a loop.
        """
        consumer = Consumer(self.notifier.loop, self.target_fn)
        consumer.start()
        self.manager.add_watch(self.directory, ALL_EVENTS)
        try:
            self.notifier.loop.run_forever()
        except KeyboardInterrupt:
            print(
                """\n >> Caught keyboard interrupt.
 >> Canceling notify tasks..."""
            )
            consumer.event.set()
            self.notifier.loop.stop()
        finally:
            self.notifier.loop.close()
