"""Pytest fixtures for WB API tests."""

import pytest
from wb_api import WildberriesClient


@pytest.fixture
def test_token():
    """Return a test token."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"


@pytest.fixture
def wb_client(test_token):
    """Return a test WB client."""
    return WildberriesClient(token=test_token, sandbox=True)
