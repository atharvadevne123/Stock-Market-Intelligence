"""Tests for cache.ttl_cache.TTLCache."""

from __future__ import annotations

import time

import pytest

from cache.ttl_cache import TTLCache


class TestTTLCacheBasics:
    def setup_method(self):
        self.cache = TTLCache(ttl=60)

    def test_set_and_get(self):
        self.cache.set("key1", "value1")
        assert self.cache.get("key1") == "value1"

    def test_missing_key_returns_none(self):
        assert self.cache.get("nonexistent") is None

    def test_delete_existing_key(self):
        self.cache.set("k", "v")
        assert self.cache.delete("k") is True
        assert self.cache.get("k") is None

    def test_delete_missing_key_returns_false(self):
        assert self.cache.delete("no_such_key") is False

    def test_clear_empties_cache(self):
        for i in range(5):
            self.cache.set(f"key{i}", i)
        self.cache.clear()
        assert self.cache.size() == 0

    def test_contains_operator(self):
        self.cache.set("present", 42)
        assert "present" in self.cache
        assert "absent" not in self.cache


class TestTTLExpiry:
    def test_expired_entry_returns_none(self):
        cache = TTLCache(ttl=0.05)
        cache.set("k", "v")
        time.sleep(0.1)
        assert cache.get("k") is None

    def test_per_entry_ttl_override(self):
        cache = TTLCache(ttl=60)
        cache.set("fast", "gone", ttl=0.05)
        time.sleep(0.1)
        assert cache.get("fast") is None

    def test_non_expired_entry_survives(self):
        cache = TTLCache(ttl=10)
        cache.set("k", "v")
        assert cache.get("k") == "v"


class TestTTLCacheSize:
    def test_size_counts_non_expired(self):
        cache = TTLCache(ttl=60)
        for i in range(3):
            cache.set(f"k{i}", i)
        assert cache.size() == 3

    def test_max_size_evicts_oldest(self):
        cache = TTLCache(ttl=60, max_size=3)
        for i in range(4):
            cache.set(f"k{i}", i)
        assert cache.size() <= 3

    @pytest.mark.parametrize("n", [1, 5, 10])
    def test_size_after_n_sets(self, n):
        cache = TTLCache(ttl=60)
        for i in range(n):
            cache.set(f"key{i}", i)
        assert cache.size() == n
