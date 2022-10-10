""" 
queues module creates a producer and a consumer thread for queueing events.
"""
import queue
import sys
import time
from threading import Event, Thread

BUF_SIZE = 100
q = queue.Queue(BUF_SIZE)


class Consumer(Thread):
    "Consumer reads from the buffer queue"

    def __init__(self, loop=None, target=None, name="consumer"):
        super(Consumer, self).__init__()
        self.name = name
        self.target = target
        self.event = Event()
        self.restart = 0
        self.notify_loop = loop
        return

    def run(self):
        while not self.event.is_set():
            while not q.empty():
                item = q.get()
                print(" *** consumer: getting item " + item)
                try:
                    self.target(item)
                except TypeError as type_ex:
                    print("[FATAL] error in target function: " + type_ex)
                    self.event.is_set()
                    self.notify_loop.stop()
                    sys.exit(1)
            time.sleep(1)
        print(" >> finalizing consumer thread...")
        return
