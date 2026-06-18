"""Thread-safe in-memory cache with per-entry TTL expiry."""

from __future__ import annotations

import threading
import time
from typing import Any, Optional


class TTLCache:
    """A thread-safe dictionary-backed cache where entries expire after *ttl* seconds.

    Example::

        cache = TTLCache(ttl=60)
        cache.set("key", "value")
        cache.get("key")   # "value"
        cache.delete("key")
    """

    def __init__(self, ttl: float = 300.0, max_size: int = 1024) -> None:
        self._ttl = ttl
        self._max_size = max_size
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()

    def _is_expired(self, expiry: float) -> bool:
        return time.monotonic() > expiry

    def get(self, key: str) -> Optional[Any]:
        """Return the cached value for *key*, or None if missing/expired."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expiry = entry
            if self._is_expired(expiry):
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Store *value* under *key*, evicting oldest entries if at capacity."""
        effective_ttl = ttl if ttl is not None else self._ttl
        expiry = time.monotonic() + effective_ttl
        with self._lock:
            if key not in self._store and len(self._store) >= self._max_size:
                oldest_key = next(iter(self._store))
                del self._store[oldest_key]
            self._store[key] = (value, expiry)

    def delete(self, key: str) -> bool:
        """Remove *key* from the cache. Returns True if the key existed."""
        with self._lock:
            return self._store.pop(key, None) is not None

    def clear(self) -> None:
        """Remove all entries from the cache."""
        with self._lock:
            self._store.clear()

    def size(self) -> int:
        """Return the number of non-expired entries currently in the cache."""
        now = time.monotonic()
        with self._lock:
            return sum(1 for _, expiry in self._store.values() if now <= expiry)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None
