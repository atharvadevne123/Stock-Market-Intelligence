"""Tests for scheduler package — PeriodicTask, RetryableTask, TaskRegistry."""

from __future__ import annotations

import threading
import time
from unittest.mock import MagicMock

import pytest

from scheduler import PeriodicTask, RetryableTask, TaskRegistry


class TestPeriodicTask:
    def test_start_and_stop(self):
        func = MagicMock()
        task = PeriodicTask(func, interval_seconds=60, name="test_task")
        task.start()
        assert task._thread is not None
        assert task._thread.is_alive()
        task.stop()
        assert not task._thread.is_alive()

    def test_func_called_on_run(self):
        called = threading.Event()

        def target():
            called.set()

        task = PeriodicTask(target, interval_seconds=60, name="caller")
        task.start()
        assert called.wait(timeout=2), "Function was not called within 2s"
        task.stop()

    def test_stop_without_start(self):
        task = PeriodicTask(MagicMock(), interval_seconds=60)
        task.stop()

    def test_exception_in_func_does_not_kill_thread(self):
        def bad_func():
            raise ValueError("simulated error")

        task = PeriodicTask(bad_func, interval_seconds=60, name="bad")
        task.start()
        time.sleep(0.1)
        assert task._thread.is_alive()
        task.stop()

    @pytest.mark.parametrize("interval", [1, 30, 3600])
    def test_interval_stored(self, interval: int):
        task = PeriodicTask(MagicMock(), interval_seconds=interval)
        assert task.interval == interval


class TestRetryableTask:
    def test_retries_on_failure(self):
        call_count = 0

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("not yet")

        task = RetryableTask(flaky, interval_seconds=60, max_retries=3, retry_delay=0.01)
        task.start()
        time.sleep(0.3)
        task.stop()
        assert call_count >= 3

    def test_max_retries_exhausted(self):
        call_count = 0

        def always_fails():
            nonlocal call_count
            call_count += 1
            raise RuntimeError("always")

        task = RetryableTask(always_fails, interval_seconds=60, max_retries=2, retry_delay=0.01)
        task.start()
        time.sleep(0.2)
        task.stop()
        assert call_count >= 2


class TestTaskRegistry:
    def test_register_starts_task(self):
        func = MagicMock()
        registry = TaskRegistry()
        task = PeriodicTask(func, interval_seconds=60, name="reg_task")
        registry.register(task)
        assert "reg_task" in registry.status()
        registry.stop_all()

    def test_stop_all_clears_tasks(self):
        registry = TaskRegistry()
        t1 = PeriodicTask(MagicMock(), interval_seconds=60, name="t1")
        t2 = PeriodicTask(MagicMock(), interval_seconds=60, name="t2")
        registry.register(t1)
        registry.register(t2)
        registry.stop_all()
        assert len(registry.status()) == 0

    def test_status_returns_running_state(self):
        func = MagicMock()
        registry = TaskRegistry()
        task = PeriodicTask(func, interval_seconds=60, name="status_task")
        registry.register(task)
        status = registry.status()
        assert status["status_task"] is True
        registry.stop_all()
