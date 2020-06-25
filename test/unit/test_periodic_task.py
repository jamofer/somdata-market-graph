import time
import unittest

import monotonic
import periodic_task


class TestPeriodicTask(unittest.TestCase):
    def _task_callback(self):
        self.callback_times.append(monotonic.monotonic())

    def setUp(self):
        self.callback_times = []
        self.task = periodic_task.PeriodicTask(0.1, self._task_callback)

    def tearDown(self):
        self.task.stop()

    def test_should_start_periodic_task(self):
        self.task.start()
        time.sleep(0.05)

        assert self.callback_times

    def test_should_stop_periodic_task(self):
        self.task.start()

        self.task.stop()
        self.callback_times = []
        time.sleep(0.1)

        assert self.callback_times == []

    def test_should_execute_periodic_task_many_times_periodically(self):
        self.task.start()
        time.sleep(0.45)

        self.assert_time_delta(0.1)

    def assert_time_delta(self, delta):
        tolerance = 0.01
        intervals = [current - last for current, last in zip(self.callback_times[1:], self.callback_times[:-1])]
        mean_interval = sum(intervals) / len(intervals)

        assert (delta + tolerance) > mean_interval > (delta - tolerance)
