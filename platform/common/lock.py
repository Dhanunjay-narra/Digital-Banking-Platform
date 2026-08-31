"""Concurrency & Distributed Lock simulation for financial operations."""

import threading
from contextlib import contextmanager
from typing import Dict


class LockManager:
    """Thread-safe lock manager for per-account or per-resource isolation."""
    def __init__(self):
        self._locks: Dict[str, threading.Lock] = {}
        self._master_lock = threading.Lock()

    def get_lock(self, resource_id: str) -> threading.Lock:
        with self._master_lock:
            if resource_id not in self._locks:
                self._locks[resource_id] = threading.Lock()
            return self._locks[resource_id]

    @contextmanager
    def acquire(self, resource_id: str, timeout: float = 10.0):
        lock = self.get_lock(resource_id)
        acquired = lock.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError(f"Could not acquire lock for resource {resource_id} within {timeout}s")
        try:
            yield
        finally:
            lock.release()


lock_manager = LockManager()
