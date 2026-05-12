"""Scheduler package for periodic analysis tasks."""
from __future__ import annotations

import logging
import threading
import time
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


__all__ = ["PeriodicTask"]
