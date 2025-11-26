"""Tests for WildberriesClient."""

import pytest
from wb_api import WildberriesClient


def test_client_initialization(test_token):
    """Test client initialization."""
    client = WildberriesClient(token=test_token)
    assert client is not None
    assert client._token == test_token


def test_client_context_manager(test_token):
    """Test client as context manager."""
    with WildberriesClient(token=test_token) as client:
        assert client is not None
    # Client should be closed after context


def test_client_has_api_modules(wb_client):
    """Test that client has all API modules."""
    assert hasattr(wb_client, "content")
    assert hasattr(wb_client, "common")
