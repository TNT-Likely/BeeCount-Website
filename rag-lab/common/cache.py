from __future__ import annotations

import time

try:
    from cachetools import TTLCache as _TTLCache
except Exception:  # noqa: BLE001
    _TTLCache = None


class _SimpleTTLCache:
    def __init__(self, maxsize: int, ttl: int) -> None:
        self._maxsize = maxsize
        self._ttl = ttl
        self._items: dict[str, tuple[float, dict]] = {}

    def get(self, key: str):
        value = self._items.get(key)
        if value is None:
            return None

        expires_at, payload = value
        if expires_at < time.time():
            self._items.pop(key, None)
            return None
        return payload

    def __setitem__(self, key: str, value: dict) -> None:
        now = time.time()
        self._evict(now)
        if len(self._items) >= self._maxsize:
            oldest_key = min(self._items, key=lambda k: self._items[k][0])
            self._items.pop(oldest_key, None)
        self._items[key] = (now + self._ttl, value)

    def clear(self) -> None:
        self._items.clear()

    def _evict(self, now: float) -> None:
        expired = [key for key, (exp_at, _) in self._items.items() if exp_at < now]
        for key in expired:
            self._items.pop(key, None)


class QueryCache:
    def __init__(self, maxsize: int, ttl_seconds: int) -> None:
        if _TTLCache is not None:
            self._cache = _TTLCache(maxsize=maxsize, ttl=ttl_seconds)
            self._simple = False
        else:
            self._cache = _SimpleTTLCache(maxsize=maxsize, ttl=ttl_seconds)
            self._simple = True

    def get(self, key: str) -> dict | None:
        if self._simple:
            return self._cache.get(key)
        return self._cache.get(key)

    def set(self, key: str, value: dict) -> None:
        self._cache[key] = value

    def clear(self) -> None:
        self._cache.clear()
