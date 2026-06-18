"""Scheduler package for periodic analysis tasks."""

from __future__ import annotations

import logging
import threading
from typing import Callable

logger = logging.getLogger(__name__)


class PeriodicTask:
    """Runs a callable on a fixed interval in a background thread."""

    def __init__(self, func: Callable, interval_seconds: int, name: str = "task") -> None:
        """Initialise the periodic task.

        Args:
            func: The callable to execute periodically.
            interval_seconds: How often (in seconds) to call *func*.
            name: Human-readable name for logging.
        """
        self.func = func
        self.interval = interval_seconds
        self.name = name
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the background scheduler thread."""
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True, name=self.name)
        self._thread.start()
        logger.info("Scheduler started: %s (every %ds)", self.name, self.interval)

    def stop(self) -> None:
        """Signal the scheduler thread to stop."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=10)
        logger.info("Scheduler stopped: %s", self.name)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                self.func()
            except Exception:
                logger.exception("Error in scheduled task %s", self.name)
            self._stop_event.wait(timeout=self.interval)


class RetryableTask(PeriodicTask):
    """PeriodicTask that retries the callable up to *max_retries* times on failure."""

    def __init__(
        self,
        func: Callable,
        interval_seconds: int,
        name: str = "task",
        max_retries: int = 3,
        retry_delay: float = 5.0,
    ) -> None:
        """Initialise a retryable periodic task.

        Args:
            func: The callable to execute periodically.
            interval_seconds: How often (in seconds) to call *func*.
            name: Human-readable name for logging.
            max_retries: Maximum consecutive failure retries before giving up.
            retry_delay: Seconds to wait between retry attempts.
        """
        super().__init__(func, interval_seconds, name)
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _run(self) -> None:
        while not self._stop_event.is_set():
            for attempt in range(1, self.max_retries + 1):
                try:
                    self.func()
                    break
                except Exception:
                    logger.exception(
                        "Error in %s (attempt %d/%d)", self.name, attempt, self.max_retries
                    )
                    if attempt < self.max_retries:
                        self._stop_event.wait(timeout=self.retry_delay)
                    else:
                        logger.error("%s: all %d retries exhausted", self.name, self.max_retries)
            self._stop_event.wait(timeout=self.interval)


class TaskRegistry:
    """A registry that tracks and controls multiple named PeriodicTask instances."""

    def __init__(self) -> None:
        self._tasks: dict[str, PeriodicTask] = {}

    def register(self, task: PeriodicTask) -> None:
        """Add a task to the registry and start it immediately."""
        if task.name in self._tasks:
            logger.warning("Overwriting existing task: %s", task.name)
        self._tasks[task.name] = task
        task.start()

    def stop_all(self) -> None:
        """Stop every registered task."""
        for task in self._tasks.values():
            task.stop()
        self._tasks.clear()
        logger.info("All scheduled tasks stopped")

    def status(self) -> dict[str, bool]:
        """Return a mapping of task names to their running state."""
        return {name: (t._thread is not None and t._thread.is_alive()) for name, t in self._tasks.items()}


__all__ = ["PeriodicTask", "RetryableTask", "TaskRegistry"]
