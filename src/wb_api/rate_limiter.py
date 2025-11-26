"""Rate limiter implementation using token bucket algorithm."""

import asyncio
import threading
import time
from dataclasses import dataclass


@dataclass
class RateLimitState:
    """State of rate limiter."""

    remaining: int
    reset_at: float
    limit: int


class RateLimiter:
    """Token bucket rate limiter for WB API (synchronous)."""

    def __init__(self, requests_per_minute: int, burst: int):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests per minute
            burst: Maximum burst capacity (tokens)
        """
        self.rpm = requests_per_minute
        self.burst = burst
        self.tokens = float(burst)
        self.last_update = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Wait until a request can be made (blocks if needed)."""
        with self._lock:
            self._refill()
            while self.tokens < 1:
                sleep_time = 60.0 / self.rpm
                time.sleep(sleep_time)
                self._refill()
            self.tokens -= 1

    def try_acquire(self) -> bool:
        """
        Try to acquire a token without blocking.

        Returns:
            True if token was acquired, False otherwise
        """
        with self._lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_update
        refill = elapsed * (self.rpm / 60.0)
        self.tokens = min(self.burst, self.tokens + refill)
        self.last_update = now

    def update_from_headers(self, headers: dict[str, str]) -> None:
        """
        Update rate limiter state from response headers.

        Args:
            headers: Response headers from API
        """
        with self._lock:
            # Convert headers to lowercase for case-insensitive access
            headers_lower = {k.lower(): v for k, v in headers.items()}

            if "x-ratelimit-remaining" in headers_lower:
                remaining = int(headers_lower["x-ratelimit-remaining"])
                self.tokens = float(remaining)

            if "x-ratelimit-limit" in headers_lower:
                limit = int(headers_lower["x-ratelimit-limit"])
                self.burst = limit

    def get_state(self) -> RateLimitState:
        """Get current rate limiter state."""
        with self._lock:
            self._refill()
            return RateLimitState(
                remaining=int(self.tokens),
                reset_at=self.last_update + (60.0 / self.rpm),
                limit=self.burst,
            )


class AsyncRateLimiter:
    """Token bucket rate limiter for WB API (asynchronous)."""

    def __init__(self, requests_per_minute: int, burst: int):
        """
        Initialize async rate limiter.

        Args:
            requests_per_minute: Maximum requests per minute
            burst: Maximum burst capacity (tokens)
        """
        self.rpm = requests_per_minute
        self.burst = burst
        self.tokens = float(burst)
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request can be made (blocks if needed)."""
        async with self._lock:
            self._refill()
            while self.tokens < 1:
                sleep_time = 60.0 / self.rpm
                await asyncio.sleep(sleep_time)
                self._refill()
            self.tokens -= 1

    async def try_acquire(self) -> bool:
        """
        Try to acquire a token without blocking.

        Returns:
            True if token was acquired, False otherwise
        """
        async with self._lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_update
        refill = elapsed * (self.rpm / 60.0)
        self.tokens = min(self.burst, self.tokens + refill)
        self.last_update = now

    async def update_from_headers(self, headers: dict[str, str]) -> None:
        """
        Update rate limiter state from response headers.

        Args:
            headers: Response headers from API
        """
        async with self._lock:
            # Convert headers to lowercase for case-insensitive access
            headers_lower = {k.lower(): v for k, v in headers.items()}

            if "x-ratelimit-remaining" in headers_lower:
                remaining = int(headers_lower["x-ratelimit-remaining"])
                self.tokens = float(remaining)

            if "x-ratelimit-limit" in headers_lower:
                limit = int(headers_lower["x-ratelimit-limit"])
                self.burst = limit

    async def get_state(self) -> RateLimitState:
        """Get current rate limiter state."""
        async with self._lock:
            self._refill()
            return RateLimitState(
                remaining=int(self.tokens),
                reset_at=self.last_update + (60.0 / self.rpm),
                limit=self.burst,
            )
