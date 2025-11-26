"""Tests for RateLimiter."""

import time
import pytest
from wb_api.rate_limiter import RateLimiter, RateLimitState


def test_rate_limiter_initialization():
    """Test rate limiter initialization."""
    limiter = RateLimiter(requests_per_minute=60, burst=10)
    assert limiter.rpm == 60
    assert limiter.burst == 10
    assert limiter.tokens == 10


def test_rate_limiter_acquire():
    """Test acquiring tokens."""
    limiter = RateLimiter(requests_per_minute=60, burst=10)

    # Should be able to acquire immediately
    limiter.acquire()
    assert limiter.tokens == 9


def test_rate_limiter_try_acquire():
    """Test try_acquire method."""
    limiter = RateLimiter(requests_per_minute=60, burst=2)

    assert limiter.try_acquire() is True
    assert limiter.try_acquire() is True
    assert limiter.try_acquire() is False  # No tokens left


def test_rate_limiter_refill():
    """Test token refill."""
    limiter = RateLimiter(requests_per_minute=60, burst=10)

    # Acquire all tokens
    for _ in range(10):
        limiter.acquire()

    # Wait for refill
    time.sleep(1.1)

    # Should have refilled
    assert limiter.try_acquire() is True


def test_rate_limiter_update_from_headers():
    """Test updating from response headers."""
    limiter = RateLimiter(requests_per_minute=60, burst=10)

    headers = {
        "x-ratelimit-remaining": "5",
        "x-ratelimit-limit": "20"
    }

    limiter.update_from_headers(headers)
    assert limiter.tokens == 5
    assert limiter.burst == 20


def test_rate_limiter_get_state():
    """Test getting rate limiter state."""
    limiter = RateLimiter(requests_per_minute=60, burst=10)
    state = limiter.get_state()

    assert isinstance(state, RateLimitState)
    assert state.remaining == 10
    assert state.limit == 10
