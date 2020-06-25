import threading

import monotonic


class PeriodicTask(object):
    def __init__(self, interval, func, *args, **kwargs):
        self.interval = interval
        self.running = False
        self.event = None
        self.thread = None
        self._run = lambda: func(*args, **kwargs)

    def start(self):
        if self.running:
            self.stop()

        self.running = True
        self.event = threading.Event()
        self.thread = threading.Thread(target=self.__task)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.event.set()
        self.thread.join()

    def __task(self):
        next_time = monotonic.monotonic()

        while self.running:
            self._run()
            next_time += self.interval
            self.event.wait(next_time - monotonic.monotonic())
